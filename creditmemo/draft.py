"""Draft a credit memo with Claude, check it, and render it.

    python -m creditmemo.draft DVA                 # prompt -> claude -p -> check -> render
    python -m creditmemo.draft DVA --prompt-only   # just write memos/DVA_prompt.md

Steps
  1. Build the prompt: the facility, a fact sheet of placeholder names with
     their current values, DaVita-style risk points from config, and the
     extracted 10-K paragraphs with their citation keys.
  2. Run Claude Code non-interactively (claude -p), prompt on stdin.
  3. Run the checker (memo_check.py). If the draft fails, send Claude its own
     draft plus the checker's errors and ask for a corrected draft (twice at most).
  4. On a pass, render memos/<T>_memo.md: placeholders filled from the spread,
     citations turned into "10-K Item 1A ¶12, p. 24" links.

Claude sees the numbers in the fact sheet so it can judge the credit, but it
may only write placeholder names; the checker fails any number it types.
Everything is saved under memos/: the prompt, each raw draft, each check
report and the final memo, so the run can be audited.

The command defaults to `claude -p --output-format text`; override with the
CLAUDE_CMD environment variable (for example to pin a model).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

from . import ROOT, SPREAD_DIR
from .edgar import load_companies
from .memo_check import SECTIONS_DIR, Values, check, render

MEMO_DIR = ROOT / "memos"
DEFAULT_CMD = "claude -p --output-format text"
MAX_REVISIONS = 2

# Paragraphs longer than this are cut in the prompt to save space; the checker
# still verifies quotations against the full paragraph text.
TRIM = {"1": 500, "1A": 500, "7": 400, "7-LIQ": 1500, "7A": 2000, "DEBT": 1200}
FACT_LINES = {
    "income": ["revenue", "operating_costs", "da", "unusual_operating", "operating_income", "interest_expense",
               "other_nonoperating", "pretax_income", "income_tax", "net_income", "ebitda"],
    "balance": ["cash", "current_assets", "total_assets", "debt_current", "ltd", "total_debt",
                "lease_liabilities", "current_liabilities", "total_liabilities", "redeemable_nci", "equity", "nci"],
    "cashflow": ["cfo", "capex", "acquisitions", "debt_issued", "debt_repaid", "dividends", "buybacks", "fcf"],
}


def fact_sheet(spread: dict) -> str:
    v = Values(spread)
    labels = [p["label"] for p in spread["periods"]]
    rows = ["| Placeholder | " + " | ".join(labels) + " |", "|---|" + "---|" * len(labels)]

    def add(name_fn, label):
        vals = []
        for lab in labels:
            ok, txt = v.resolve(name_fn(lab))
            vals.append(txt if ok else "n/a")
        rows.append(f"| `{{{{{name_fn('FYxxxx')}}}}}` {label} | " + " | ".join(vals) + " |")

    for key in spread["ratios"][labels[-1]]:
        add(lambda l, k=key: f"{l}.{k}", "")
    for key in ("ebitda_margin", "ebitdar", "net_debt", "lease_adj_debt"):
        add(lambda l, k=key: f"{l}.{k}", "")
    for st, keys in FACT_LINES.items():
        for key in keys:
            add(lambda l, s=st, k=key: f"{l}.{s}.{k}", "")
    for key in ("cash_taxes", "scheduled_principal", "operating_lease_cost", "operating_lease_liabilities"):
        add(lambda l, k=key: f"{l}.{k}", "(from the notes)")
    for key in ("revenue", "ebitda", "operating_income", "total_debt"):
        add(lambda l, k=key: f"growth.{l}.{k}", "(change on prior year)")

    out = ["Use the placeholder with the real year in place of FYxxxx, e.g. `{{" + labels[-1] + ".debt_ebitda}}`.",
           "", *rows, "", "Stress case and other values:", ""]
    st = spread["stress"]
    names = (["stress." + k for k in st["stressed"]["ratios"]] +
             ["stress.ebitda", "stress.extra_interest", "stress.base_margin", "stress.stressed_margin",
              "stress.revenue_shock", "stress.margin_shock", "stress.rate_shock", "floating_rate_share",
              "facility.type", "facility.amount_usd", "facility.tenor_years", "facility.purpose",
              "grade.grade", "grade.base_grade", "grade.stress_notches", "grade.weighted_score"] +
             ["grade.score." + k for k in spread["grade"]["scores"]])
    for n in names:
        ok, txt = v.resolve(n)
        if ok:
            out.append(f"- `{{{{{n}}}}}` = {txt}")
    br = [st["thresholds"][k]["label"] for k, b in st["stressed"]["breaches"].items() if b]
    out.append(f"- Stress thresholds broken (for your reasoning; describe them in words): "
               f"{', '.join(br) if br else 'none'}")
    return "\n".join(out)


def tenk_text(sections: dict) -> str:
    out = []
    for key, sec in sections["sections"].items():
        out.append(f"\n### [{key}] {sec['title']}" + (f" ({sec['note']})" if sec.get("note") else ""))
        for i, p in enumerate(sec["paragraphs"], 1):
            t = p["text"]
            lim = TRIM.get(key, 500)
            if len(t) > lim:
                t = t[:lim].rsplit(" ", 1)[0] + " […]"
            out.append(f"[{key} ¶{i}] (p. {p.get('page') or '?'}) {t}")
    return "\n".join(out)


INSTRUCTIONS = """You are a senior commercial credit analyst at a bank. Write a credit memo on {name} for the facility below, using ONLY the fact sheet and the 10-K paragraphs provided. Do not use tools, files or outside knowledge.

Facility requested: {{{{facility.type}}}} of {{{{facility.amount_usd}}}}, {{{{facility.tenor_years}}}}-year tenor, purpose: {{{{facility.purpose}}}}. This is a hypothetical request used to test the borrower's capacity.

RULES (a script checks every one; a draft that breaks any rule is rejected):
1. Never type a number. Every figure, ratio, percentage, amount, multiple and count must be a placeholder from the fact sheet, written exactly like {{{{FY2025.debt_ebitda}}}}. Write "{{{{facility.tenor_years}}}}-year", not "5-year". Words like "one notch" or "two thresholds" are fine. Allowed as typed text: years (2025), FY labels (FY2025), "Item 1A", "Note 12", "10-K", instrument names like "Term Loan A-2", and "1-to-10".
2. Every sentence of six words or more must contain a placeholder or a citation. Cite the 10-K as [1A ¶12] using the section key and paragraph number shown in front of each paragraph, e.g. [7-LIQ ¶3] or [DEBT ¶61]. Several paragraphs: [DEBT ¶95, ¶96].
3. Quotations of five or more words, in double quotes, must be copied word for word from the cited paragraph. Prefer paraphrase with a citation.
4. Do not invent placeholders. If a value is not in the fact sheet, describe it in words with a citation, or leave it out.
5. End with a line in exactly this form: "Recommendation: Approve" or "Recommendation: Decline", optionally followed by " with conditions" and then the conditions.

STRUCTURE (Markdown):
# Credit memo: {name}
## 1. Request
## 2. Borrower overview
## 3. Financial analysis  (include one table of key ratios for the three fiscal years using placeholders; then discuss trends)
## 4. Strengths
## 5. Risks and mitigants
## 6. Stress test  (explain the scenario using the stress placeholders and say which thresholds break)
## 7. Risk grade  (the internal 1-to-10 grade, 1 = best, from {{{{grade.grade}}}} and its parts; stress notches make the grade WORSE, i.e. a higher number)
## 8. Recommendation  (your own judgment on approve or decline; it may differ from what the grade suggests, but explain why)

Paraphrase figures from the 10-K text precisely: if a paragraph says about 36%, don't write 'roughly a third'. Don't attach a citation that doesn't support the sentence; for a pure judgment sentence, tie it to a placeholder instead.

Keep it to about 900-1,300 words. Be specific and balanced. A credit committee reads this.
"""


def build_prompt(ticker: str) -> str:
    cfg = load_companies()
    co = cfg["companies"][ticker]
    spread = json.loads((SPREAD_DIR / f"{ticker}.json").read_text())
    sections = json.loads((SECTIONS_DIR / f"{ticker}.json").read_text())
    points = co.get("memo_points") or []
    parts = [INSTRUCTIONS.format(name=spread["name"]),
             "## FACT SHEET (values are shown only so you can reason; write the placeholder, never the value)",
             fact_sheet(spread)]
    if co.get("floating_rate_basis"):
        parts += ["", "Floating-rate basis (analyst note): " + co["floating_rate_basis"]]
    if points:
        parts += ["", "## ANALYST POINTS TO COVER (each must appear in the memo, with its citation)",
                  *[f"- {p}" for p in points]]
    parts += ["", f"## 10-K PARAGRAPHS ({spread['name']} 10-K filed {sections['filed']})", tenk_text(sections)]
    return "\n".join(parts)


def run_claude(prompt: str) -> str:
    cmd = shlex.split(os.environ.get("CLAUDE_CMD", DEFAULT_CMD))
    res = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=900)
    if res.returncode != 0:
        raise SystemExit(f"claude failed ({res.returncode}): {res.stderr[:2000]}")
    text = res.stdout.strip()
    m = re.search(r"```(?:markdown|md)?\s*\n(.*)\n```", text, re.S)   # unwrap a fenced reply
    if m and m.group(1).lstrip().startswith("#"):
        text = m.group(1)
    i = text.find("# Credit memo")
    return (text[i:] if i > 0 else text).strip() + "\n"


def revision_prompt(prompt: str, draft: str, report: dict) -> str:
    errs = "\n".join(f"- line {e['line']}: {e['type']}: {e['text']}" + (f" ({e['detail']})" if e.get("detail") else "")
                     for e in report["errors"])
    return (prompt + "\n\n## YOUR PREVIOUS DRAFT\n\n" + draft +
            "\n\n## CHECKER ERRORS - fix every one and return the full corrected memo, nothing else\n\n" + errs)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--prompt-only", action="store_true")
    args = ap.parse_args(argv)
    t = args.ticker.upper()
    MEMO_DIR.mkdir(exist_ok=True)
    prompt = build_prompt(t)
    (MEMO_DIR / f"{t}_prompt.md").write_text(prompt)
    print(f"prompt: memos/{t}_prompt.md ({len(prompt):,} characters)")
    if args.prompt_only:
        return 0

    spread = json.loads((SPREAD_DIR / f"{t}.json").read_text())
    sections = json.loads((SECTIONS_DIR / f"{t}.json").read_text())
    values = Values(spread)
    current = prompt
    for attempt in range(MAX_REVISIONS + 1):
        print(f"attempt {attempt + 1}: running claude ...", flush=True)
        draft = run_claude(current)
        (MEMO_DIR / f"{t}_draft_{attempt + 1}.md").write_text(draft)
        report = check(draft, values, sections)
        (MEMO_DIR / f"{t}_check_{attempt + 1}.json").write_text(json.dumps(report, indent=2))
        print(f"  {'PASS' if report['ok'] else 'FAIL'}: {len(report['errors'])} errors, "
              f"{report['stats']['placeholders']} placeholders, {report['stats']['citations']} citations, "
              f"recommendation {report['recommendation']}")
        for e in report["errors"][:15]:
            print(f"    line {e['line']}: {e['type']}: {e['text'][:100]}")
        if report["ok"]:
            (MEMO_DIR / f"{t}_draft.md").write_text(draft)
            memo = render(draft, values, sections)
            header = (f"<!-- Rendered from memos/{t}_draft.md by creditmemo/memo_check.py. Every number comes "
                      f"from outputs/spreads/{t}.json; Claude wrote placeholders only. "
                      f"Check: {report['stats']['placeholders']} placeholders, {report['stats']['citations']} "
                      f"citations, 0 errors, attempt {attempt + 1}. -->\n\n")
            (MEMO_DIR / f"{t}_memo.md").write_text(header + memo)
            summary = {"ticker": t, "attempts": attempt + 1, "recommendation": report["recommendation"],
                       "grade": spread["grade"]["grade"], "stats": report["stats"]}
            (MEMO_DIR / f"{t}_result.json").write_text(json.dumps(summary, indent=2))
            print(f"memo: memos/{t}_memo.md  (recommendation {report['recommendation']}, "
                  f"grade {spread['grade']['grade']})")
            return 0
        current = revision_prompt(prompt, draft, report)
    print(f"Still failing after {MAX_REVISIONS + 1} attempts; see memos/{t}_check_*.json", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
