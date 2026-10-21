"""Fill a memo draft's placeholders from the spread and check the draft.

    python -m creditmemo.memo_check memos/DVA_draft.md          # check + render
    python -m creditmemo.memo_check memos/DVA_draft.md --check  # check only

Claude writes numbers only as placeholders and cites the 10-K text by
section and paragraph. This script is what proves "every number came from
Python":

Placeholders
  {{FY2025.debt_ebitda}}            ratio                    -> 3.72x
  {{FY2025.ebitda}}                 derived amount           -> $2.8 billion
  {{FY2025.ebitda_margin}}          derived percentage       -> 20.2%
  {{FY2025.revenue}}                standard spread line     -> $13.6 billion
  {{FY2025.balance.cash}}           line from one statement (when a key is in several)
  {{growth.FY2025.revenue}}         change on the prior year -> 6.5%
  {{stress.debt_ebitda}}            stressed ratio; also stress.ebitda, stress.extra_interest,
                                    stress.base_margin, stress.stressed_margin
  {{facility.amount_usd}}, {{facility.tenor_years}}, {{floating_rate_share}}
  {{abs:FY2025.cashflow.buybacks}}  any placeholder without its minus sign (for 'fell', 'buybacks of')
  {{fact.covenant_max_leverage}}    a 10-K figure entered by hand in config/companies.json with its citation
  {{rating.sp}}                     agency rating from config/agency_ratings.json, with its last action date
  {{proforma.debt_ebitda}}          latest year with the requested facility added; also
                                    proforma.stress.<ratio>, proforma.rate, proforma.added_interest
  {{grade.grade}}, {{grade.base_grade}}, {{grade.stress_notches}}, {{grade.weighted_score}},
  {{grade.score.dscr}} (a metric's 1-10 score)

Citations
  [1A ¶12]  section key and paragraph number from outputs/sections/<TICKER>.json
            (sections: 1, 1A, 7, 7-LIQ, 7A, DEBT)

The draft fails if it has
  * a placeholder the spread can't fill
  * a number typed by hand (allowed: years, FY labels, Item/Note numbers, 10-K/10-Q,
    and the 1-to-10 scale)
  * a sentence with neither a placeholder nor a citation (headings, table rows
    of placeholders and the recommendation line excepted); in the Recommendation
    section an opinion may carry [judgment] instead
  * a sign mismatch: a negative value after 'fell'/'declined'/'buybacks of'
    (use {{abs:...}}), or 'rose'/'grew' with a negative change
  * a citation to a section or paragraph that doesn't exist
  * a quotation (5+ words in double quotes) that isn't in the cited paragraph
  * no recommendation line: "Recommendation: Approve" or "Recommendation: Decline"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from . import ROOT, SPREAD_DIR

SECTIONS_DIR = ROOT / "outputs" / "sections"
SECTION_TITLES = {"1": "Item 1", "1A": "Item 1A", "7": "Item 7", "7-LIQ": "Item 7, Liquidity",
                  "7A": "Item 7A", "DEBT": "Debt note"}

PH_RE = re.compile(r"\{\{\s*((?:abs:)?[A-Za-z0-9_.\-]+)\s*\}\}")
JUDG_RE = re.compile(r"\[judgment\]", re.I)
# a change word followed by a placeholder: the sign must agree with the word
DOWN_RE = re.compile(r"\b(fell|declined|decreased|dropped|shrank|buybacks of|repurchases of|capex of|capital expenditures of)\s+(?:by\s+)?\{\{\s*((?:abs:)?[A-Za-z0-9_.\-]+)\s*\}\}", re.I)
UP_RE = re.compile(r"\b(rose|increased|grew|climbed)\s+(?:by\s+)?\{\{\s*((?:abs:)?growth\.[A-Za-z0-9_.\-]+)\s*\}\}", re.I)
AGENCY_NAMES = {"sp": "S&P", "moodys": "Moody's", "fitch": "Fitch"}
CITE_RE = re.compile(r"\[(1A|1|7-LIQ|7A|7|DEBT)\s*¶\s*(\d+)(?:\s*[,;]\s*¶?\s*(\d+))*\]")
CITE_ANY_RE = re.compile(r"\[[^\]]*¶[^\]]*\]")
REC_RE = re.compile(r"^\**\s*Recommendation\s*:?\**\s*:?\s*\**\s*(Approve|Decline)\b", re.I | re.M)
ALLOWED_NUMBER_RES = [
    r"\bFY\d{4}\b", r"\b(19|20)\d{2}\b", r"\b10-[KQ]\b", r"\bItem\s+\d{1,2}[A-C]?\b",
    r"\bNote\s+\d{1,2}\b", r"\b1-to-10\b", r"\bQ[1-4]\b", r"\bpart\s+[IV]+\b",
    r"\b[A-Z]{1,3}-\d{1,2}\b",  # instrument names such as Term Loan A-2
]
PCT_KEYS = {"ebitda_margin", "base_margin", "stressed_margin", "floating_rate_share", "revenue_shock",
            "margin_shock", "rate_shock"}
RATIO_KEYS = {"debt_ebitda", "net_debt_ebitda", "lease_adj_debt_ebitdar", "lease_adj_net_debt_ebitdar",
              "interest_coverage", "dscr", "current_ratio"}


# ------------------------------------------------------------------ values

def fmt_money(v: float) -> str:
    sign = "-" if v < 0 else ""
    a = abs(v)
    if a >= 1e9:
        return f"{sign}${a / 1e9:,.1f} billion"
    if a >= 1e6:
        return f"{sign}${a / 1e6:,.0f} million"
    return f"{sign}${a:,.0f}"


def fmt(key: str, v, kind: Optional[str] = None) -> str:
    if v is None:
        return "n.m."
    if isinstance(v, str):
        return v
    kind = kind or ("ratio" if key in RATIO_KEYS else "pct" if key in PCT_KEYS else "money")
    if kind == "ratio":
        return f"{v:.2f}x"
    if kind == "pct":
        return f"{v * 100:.1f}%"
    if kind == "int":
        return f"{v:,.0f}"
    return fmt_money(v)


class Values:
    """Resolves placeholder names against one spread."""

    def __init__(self, spread: dict, grade: Optional[dict] = None, facts: Optional[dict] = None,
                 ratings: Optional[dict] = None):
        self.s = spread
        self.grade = grade or spread.get("grade")
        self.labels = [p["label"] for p in spread["periods"]]
        self.facts = facts or {}        # hand-entered 10-K figures with citations (config/companies.json)
        self.ratings = ratings or {}    # agency ratings (config/agency_ratings.json)

    def _line(self, statement: str, key: str, label: str):
        std = self.s["standard"]
        per = std["periods"][statement]
        for ln in std[statement]:
            if ln["key"] == key and label in per:
                return True, ln["values"][per.index(label)]
        return False, None

    def _period_value(self, label: str, key: str) -> Tuple[bool, object, Optional[str]]:
        if label not in self.labels:
            return False, None, None
        parts = key.split(".")
        if len(parts) == 2 and parts[0] in ("income", "balance", "cashflow"):
            found, v = self._line(parts[0], parts[1], label)
            return found, v, None
        if key in self.s["ratios"][label]:
            return True, self.s["ratios"][label][key], None
        if key in self.s["derived"][label]:
            return True, self.s["derived"][label][key], None
        for st in ("income", "balance", "cashflow"):
            found, v = self._line(st, key, label)
            if found:
                return True, v, None
        if key in self.s["ratio_inputs"][label]:
            return True, self.s["ratio_inputs"][label][key], None
        return False, None, None

    def raw(self, name: str):
        """The underlying number for sign checks (None if not numeric)."""
        parts = name.split(".")
        if parts[0] in self.labels and len(parts) >= 2:
            found, v, _ = self._period_value(parts[0], ".".join(parts[1:]))
            return v if found else None
        if parts[0] == "growth" and len(parts) == 3 and parts[1] in self.labels:
            i = self.labels.index(parts[1])
            if i == 0:
                return None
            _, cur, _ = self._period_value(parts[1], parts[2])
            _, prev, _ = self._period_value(self.labels[i - 1], parts[2])
            return None if not prev or cur is None else (cur - prev) / abs(prev)
        return None

    def resolve(self, name: str) -> Tuple[bool, str]:
        if name.startswith("abs:"):
            ok, txt = self.resolve(name[4:])
            return ok, txt.lstrip("-") if ok else ""
        parts = name.split(".")
        head = parts[0]
        if head in self.labels and len(parts) >= 2:
            found, v, kind = self._period_value(head, ".".join(parts[1:]))
            return found, fmt(parts[-1], v, kind) if found else ""
        if head == "growth" and len(parts) == 3 and parts[1] in self.labels:
            i = self.labels.index(parts[1])
            if i == 0:
                return False, ""
            f1, cur, _ = self._period_value(parts[1], parts[2])
            f0, prev, _ = self._period_value(self.labels[i - 1], parts[2])
            if not (f1 and f0):
                return False, ""
            g = None if not prev or cur is None else (cur - prev) / abs(prev)
            return True, fmt("", g, "pct")
        if head == "stress" and len(parts) == 2:
            st = self.s["stress"]
            k = parts[1]
            if k in st["stressed"]["ratios"]:
                return True, fmt(k, st["stressed"]["ratios"][k])
            if k in st["stressed"]["derived"]:
                return True, fmt(k, st["stressed"]["derived"][k])
            if k in ("extra_interest",):
                return True, fmt(k, st[k], "money")
            if k in ("base_margin", "stressed_margin", "floating_rate_share"):
                return True, fmt(k, st[k], "pct")
            if k in ("margin_shock", "rate_shock"):      # shifts in rates and margins read as basis points
                return True, f"{st['scenario'][k] * 1e4:.0f}bp"
            if k in st["scenario"]:
                return True, fmt(k, st["scenario"][k], "pct")
            return False, ""
        if head == "facility" and len(parts) == 2 and parts[1] in (self.s.get("facility") or {}):
            v = self.s["facility"][parts[1]]
            kind = "money" if parts[1].endswith("_usd") else "int" if isinstance(v, (int, float)) else None
            return True, fmt(parts[1], v, kind)
        if name == "floating_rate_share":
            return True, fmt(name, self.s.get("floating_rate_share"), "pct")
        if head == "grade" and self.grade is not None and len(parts) == 2 and parts[1] in self.grade:
            v = self.grade[parts[1]]
            if isinstance(v, (dict, list)):
                return False, ""
            return True, f"{v:.2f}" if isinstance(v, float) else str(v)
        if head == "proforma" and self.s.get("proforma"):
            pf = self.s["proforma"]
            if len(parts) == 2 and parts[1] in ("amount", "added_interest"):
                return True, fmt(parts[1], pf[parts[1]], "money")
            if len(parts) == 2 and parts[1] == "rate":
                return True, f"{pf['rate'] * 100:.2f}%"
            if len(parts) == 2 and parts[1] in pf["ratios"]:
                return True, fmt(parts[1], pf["ratios"][parts[1]])
            if len(parts) == 2 and parts[1] in pf["derived"]:
                return True, fmt(parts[1], pf["derived"][parts[1]])
            if len(parts) == 3 and parts[1] == "stress":
                st = pf["stress"]["stressed"]
                if parts[2] in st["ratios"]:
                    return True, fmt(parts[2], st["ratios"][parts[2]])
                if parts[2] in st["derived"]:
                    return True, fmt(parts[2], st["derived"][parts[2]])
                if parts[2] == "extra_interest":
                    return True, fmt("", pf["stress"]["extra_interest"], "money")
            return False, ""
        if head == "fact" and len(parts) == 2 and parts[1] in self.facts:
            f = self.facts[parts[1]]
            return True, fmt(parts[1], f["value"], f.get("kind", "money"))
        if head == "rating" and len(parts) == 2 and self.ratings.get(parts[1]):
            r = self.ratings[parts[1]]
            outlook = f" {r['outlook'].split(' (')[0].lower()}" if r.get("outlook") else ""
            when = f"last action {r['last_action']}" if r.get("last_action") else "no dated action found"
            if r.get("last_action") and r.get("last_action_confirmed") is False:
                when += ", date unconfirmed"
            return True, f"{r['rating']}{outlook} ({AGENCY_NAMES.get(parts[1], parts[1])}, {when})"
        if head == "grade" and self.grade is not None and len(parts) == 3 and parts[1] == "score" \
                and parts[2] in self.grade.get("scores", {}):
            return True, str(self.grade["scores"][parts[2]]["score"])
        return False, ""


# --------------------------------------------------------------- checking

def _sentences(text: str) -> List[Tuple[int, str, str]]:
    """(line number, sentence, section heading) for prose lines; headings,
    table rules and blank lines are skipped. Quote-block lines are checked
    like any other line. Abbreviations like 'U.S.' and decimals are protected
    before splitting."""
    out = []
    section = ""
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("#"):
            section = s.lstrip("#").strip()
            continue
        s = re.sub(r"^(>\s*)+", "", s)
        if not s or re.fullmatch(r"[|:\-\s]+", s):
            continue
        s = re.sub(r"^([-*+]|\d+\.)\s+", "", s)
        protected = re.sub(r"\b(U\.S|e\.g|i\.e|vs|Inc|Co|Corp|No|approx)\.", lambda m: m.group(0).replace(".", "§"), s)
        protected = re.sub(r"\{\{[^}]*\}\}", lambda m: m.group(0).replace(".", "§"), protected)
        protected = re.sub(r"\[[^\]]*\]", lambda m: m.group(0).replace(".", "§"), protected)
        for part in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“(\[])", protected):
            part = part.replace("§", ".").strip()
            if part:
                out.append((n, part, section))
    return out


def _strip_allowed(s: str) -> str:
    s = PH_RE.sub(" ", s)
    s = CITE_ANY_RE.sub(" ", s)
    s = JUDG_RE.sub(" ", s)
    for r in ALLOWED_NUMBER_RES:
        s = re.sub(r, " ", s, flags=re.I)
    return s


def check(draft: str, values: Values, sections: dict) -> dict:
    errors, warnings = [], []
    secs = sections["sections"]

    for m in PH_RE.finditer(draft):
        ok, _ = values.resolve(m.group(1))
        if not ok:
            line = draft.count("\n", 0, m.start()) + 1
            errors.append({"line": line, "type": "unknown_placeholder", "text": m.group(0)})

    cites = []
    for m in CITE_ANY_RE.finditer(draft):
        line = draft.count("\n", 0, m.start()) + 1
        cm = CITE_RE.fullmatch(m.group(0))
        if not cm:
            errors.append({"line": line, "type": "bad_citation", "text": m.group(0)})
            continue
        key = cm.group(1)
        nums = [int(x) for x in re.findall(r"\d+", m.group(0)[len(key) + 1:])]
        if key not in secs:
            errors.append({"line": line, "type": "bad_citation", "text": m.group(0),
                           "detail": f"section {key} not extracted"})
            continue
        for k in nums:
            if not 1 <= k <= len(secs[key]["paragraphs"]):
                errors.append({"line": line, "type": "bad_citation", "text": m.group(0),
                               "detail": f"{key} has {len(secs[key]['paragraphs'])} paragraphs"})
        cites.append((line, key, nums))

    rec = REC_RE.search(draft)
    if not rec:
        errors.append({"line": None, "type": "no_recommendation",
                       "text": "Missing 'Recommendation: Approve' or 'Recommendation: Decline'"})

    n_sent = 0
    for name, f in values.facts.items():
        cm = CITE_RE.fullmatch(f.get("cite", "") or "")
        if not cm or cm.group(1) not in secs:
            errors.append({"line": None, "type": "fact_without_source", "text": name,
                           "detail": "every fact in config needs a valid 10-K citation in 'cite'"})
    for m in DOWN_RE.finditer(draft):
        v = values.raw(m.group(2).replace("abs:", ""))
        bad = v is not None and ((m.group(2).startswith("abs:") and v > 0) or
                                 (not m.group(2).startswith("abs:") and v < 0))
        if bad:
            errors.append({"line": draft.count("\n", 0, m.start()) + 1, "type": "sign_mismatch",
                           "text": m.group(0), "detail": "after a word like 'fell', use {{abs:...}} on a value that "
                           "is actually negative; a plain placeholder here would print a minus sign"})
    for m in UP_RE.finditer(draft):
        v = values.raw(m.group(2).replace("abs:", ""))
        if v is not None and v < 0:
            errors.append({"line": draft.count("\n", 0, m.start()) + 1, "type": "sign_mismatch",
                           "text": m.group(0), "detail": "says it rose but the change is negative"})

    for line, sent, section in _sentences(draft):
        is_table = sent.startswith("|")
        bare = _strip_allowed(sent)
        stray = re.findall(r"(?<![A-Za-z])[$€£]?\d[\d,]*(\.\d+)?\s*(%|x\b|bp\b|billion|million)?", bare)
        if stray:
            nums = re.findall(r"[$]?\d[\d,.]*\s*(?:%|x|bp|billion|million)?", bare)
            errors.append({"line": line, "type": "typed_number", "text": sent[:160],
                           "detail": ", ".join(n.strip() for n in nums[:5])})
        if is_table or REC_RE.match(sent) or len(sent.split()) < 6:
            continue
        n_sent += 1
        if JUDG_RE.search(sent) and not re.search(r"recommendation", section, re.I):
            errors.append({"line": line, "type": "judgment_outside_recommendation", "text": sent[:160]})
        elif not PH_RE.search(sent) and not CITE_RE.search(sent) and not JUDG_RE.search(sent):
            errors.append({"line": line, "type": "uncited_claim", "text": sent[:160]})
        for q in re.findall(r"[\"“]([^\"”]+)[\"”]", sent):
            if len(q.split()) < 5:
                continue
            refs = [(k, n) for m in CITE_RE.finditer(sent)
                    for k in [m.group(1)] for n in map(int, re.findall(r"\d+", m.group(0)[len(k) + 1:]))]
            pool = " ".join(secs[k]["paragraphs"][n - 1]["text"] for k, n in refs
                            if k in secs and 1 <= n <= len(secs[k]["paragraphs"]))
            norm = lambda x: re.sub(r"\s+", " ", x.replace("’", "'").replace("“", '"').replace("”", '"')).strip()
            if not refs or norm(q) not in norm(pool):
                errors.append({"line": line, "type": "quote_not_found", "text": q[:120],
                               "detail": "quotation not found in the cited paragraph(s)"})

    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "recommendation": rec.group(1).capitalize() if rec else None,
            "stats": {"placeholders": len(PH_RE.findall(draft)), "citations": len(cites),
                      "sentences_checked": n_sent}}


def render(draft: str, values: Values, sections: dict) -> str:
    def ph(m):
        ok, txt = values.resolve(m.group(1))
        return txt if ok else m.group(0)

    secs = sections["sections"]
    url = sections.get("url", "")

    def cite(m):
        key = m.group(1)
        nums = [int(x) for x in re.findall(r"\d+", m.group(0)[len(key) + 1:])]
        pages = sorted({secs[key]["paragraphs"][n - 1].get("page") for n in nums
                        if key in secs and 1 <= n <= len(secs[key]["paragraphs"])} - {None})
        pg = f", p. {', '.join(pages)}" if pages else ""
        label = f"10-K {SECTION_TITLES.get(key, key)} ¶{', ¶'.join(map(str, nums))}{pg}"
        return f"[{label}]({url})" if url else f"[{label}]"

    out = CITE_RE.sub(cite, PH_RE.sub(ph, draft))
    return JUDG_RE.sub("*(analyst judgment)*", out)


def load(ticker: str):
    spread = json.loads((SPREAD_DIR / f"{ticker}.json").read_text())
    sections = json.loads((SECTIONS_DIR / f"{ticker}.json").read_text())
    return spread, sections


def make_values(ticker: str, spread: dict) -> Values:
    """Values with the company's cited 10-K facts and its agency ratings."""
    from . import CONFIG_DIR
    co = json.loads((CONFIG_DIR / "companies.json").read_text())["companies"].get(ticker, {})
    rpath = CONFIG_DIR / "agency_ratings.json"
    ratings = json.loads(rpath.read_text())["companies"].get(ticker, {}) if rpath.exists() else {}
    return Values(spread, facts=co.get("facts"), ratings={k: v for k, v in ratings.items()
                                                         if k in AGENCY_NAMES})


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("draft", type=Path)
    ap.add_argument("--ticker", help="default: the file name's first part, e.g. DVA_draft.md")
    ap.add_argument("--check", action="store_true", help="check only, don't render")
    args = ap.parse_args(argv)
    ticker = (args.ticker or args.draft.name.split("_")[0]).upper()
    spread, sections = load(ticker)
    draft = args.draft.read_text()
    values = make_values(ticker, spread)
    report = check(draft, values, sections)
    report_path = args.draft.with_name(args.draft.stem.replace("_draft", "") + "_check.json")
    report_path.write_text(json.dumps(report, indent=2))
    for e in report["errors"]:
        print(f"  line {e['line']}: {e['type']}: {e['text']}" + (f" ({e['detail']})" if e.get("detail") else ""))
    print(f"{ticker}: {'PASS' if report['ok'] else 'FAIL'} - {len(report['errors'])} errors, "
          f"{report['stats']['placeholders']} placeholders, {report['stats']['citations']} citations, "
          f"recommendation: {report['recommendation']}")
    if report["ok"] and not args.check:
        out = args.draft.with_name(args.draft.stem.replace("_draft", "") + "_memo.md")
        out.write_text(render(draft, values, sections))
        print(f"  rendered -> {out}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
