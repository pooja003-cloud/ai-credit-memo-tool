"""README tables, generated from the spreads (never typed by hand).

    python -m creditmemo.report      # writes outputs/tables.md and refreshes the README block

The README block between <!-- tables:start --> and <!-- tables:end --> is
replaced on every run.
"""

from __future__ import annotations

import json
import re
import sys

from . import ROOT, SPREAD_DIR
from .edgar import load_companies

OUT = ROOT / "outputs" / "tables.md"
README = ROOT / "README.md"


def x(v):
    return "n.m." if v is None else f"{v:.2f}x"


def footnotes(spreads, latest):
    """Where a memo shows a different figure from the table, say why."""
    from .memo_check import make_values
    out = []
    for t, s in spreads.items():
        v = make_values(t, s)
        if "interest_coverage_ex_gain" in v.calcs and "extinguishment_gain" in v.facts:
            _, cov = v.resolve("calc.interest_coverage_ex_gain")
            _, gain = v.resolve("fact.extinguishment_gain")
            out.append(f"Note: {s['name']} interest coverage is {cov} excluding the {gain} debt-repurchase gain "
                       f"booked in interest expense {v.facts['extinguishment_gain']['cite']}, as used in its memo; "
                       f"the table uses reported interest. The grade is unchanged ({s['grade']['grade']}).")
    return out


def lease_coincidences(spreads, tol=0.01):
    """Flag years where leverage with and without leases round to the same figure, and say why."""
    out = []
    for t, s in spreads.items():
        for p in s["periods"]:
            lab = p["label"]
            r, v = s["ratios"][lab], s["ratio_inputs"][lab]
            a, b = r["debt_ebitda"], r["lease_adj_debt_ebitdar"]
            liab, cost = v.get("operating_lease_liabilities"), v.get("operating_lease_cost")
            if None in (a, b, liab, cost) or not cost or abs(a - b) >= tol:
                continue
            out.append(f"Note: {s['name']} {lab} shows almost the same leverage with and without leases "
                       f"({a:.3f}x vs {b:.3f}x). This is not a bug: adding leases moves the ratio only when lease "
                       f"liabilities / lease cost differs from debt / EBITDA, and for {s['name']} it is "
                       f"{liab / cost:.2f}x against {a:.2f}x, so adding both to the ratio barely changes it.")
    return out


def build() -> str:
    cos = load_companies()["companies"]
    spreads = {t: json.loads((SPREAD_DIR / f"{t}.json").read_text()) for t in cos}
    out = []
    latest = {t: s["periods"][-1]["label"] for t, s in spreads.items()}

    out += ["### Credit ratios, latest fiscal year", "",
            "| Company | Year | Debt / EBITDA | (Debt + leases) / EBITDAR | Net debt / EBITDA | EBITDA / interest | DSCR | Current ratio | Grade |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for t, s in spreads.items():
        r = s["ratios"][latest[t]]
        out.append(f"| {s['name']} | {latest[t]} | {x(r['debt_ebitda'])} | {x(r['lease_adj_debt_ebitdar'])} | "
                   f"{x(r['net_debt_ebitda'])} | {x(r['interest_coverage'])} | {x(r['dscr'])} | "
                   f"{x(r['current_ratio'])} | {s['grade']['grade']} |")

    notes = footnotes(spreads, latest)
    if notes:
        out += [""] + notes

    out += ["", "### Leverage with and without leases, three years", "",
            "Lease-adjusted leverage pairs lease liabilities with EBITDAR (EBITDA + operating lease cost), because "
            "rent is already deducted inside EBITDA. The gap between the two columns is the lease effect.", "",
            "| Company | " + " | ".join(f"{p['label']} without / with leases" for p in next(iter(spreads.values()))["periods"]) + " |",
            "|---|" + "---:|" * 3]
    for t, s in spreads.items():
        cells = [f"{x(s['ratios'][p['label']]['debt_ebitda'])} / {x(s['ratios'][p['label']]['lease_adj_debt_ebitdar'])}"
                 for p in s["periods"]]
        out.append(f"| {s['name']} | " + " | ".join(cells) + " |")

    same = lease_coincidences(spreads)
    if same:
        out += [""] + same

    sc = next(iter(spreads.values()))["stress"]["scenario"]
    out += ["", "### Stress test", "",
            f"Revenue -{sc['revenue_shock']:.0%}, EBITDA margin -{sc['margin_shock'] * 1e4:.0f}bp, "
            f"+{sc['rate_shock'] * 1e4:.0f}bp on the floating-rate share of debt; capex, cash taxes, leases and principal held. "
            "Pro forma adds the requested $500M loan at the company's most recent senior unsecured coupon "
            "(Kohl's: a secured coupon, so its pro forma interest is a lower bound and its coverage and DSCR are at most the figures shown).", "",
            "| Company | Floating share | Stressed debt / EBITDA | Stressed EBITDA / interest | Stressed DSCR | "
            "Thresholds broken | Pro forma stressed debt / EBITDA | Pro forma stressed coverage | Pro forma stressed DSCR |",
            "|---|---:|---:|---:|---:|---|---:|---:|---:|"]
    for t, s in spreads.items():
        st = s["stress"]
        r = st["stressed"]["ratios"]
        broken = [st["thresholds"][k]["label"] for k, b in st["stressed"]["breaches"].items() if b]
        pf = (s.get("proforma") or {}).get("stress", {}).get("stressed", {}).get("ratios", {})
        # a lower-bound rate means interest is at least this, so coverage and DSCR are at most this
        lb = " (at most)" if (s.get("proforma") or {}).get("lower_bound") else ""
        out.append(f"| {s['name']} | {st['floating_rate_share']:.1%} | {x(r['debt_ebitda'])} | "
                   f"{x(r['interest_coverage'])} | {x(r['dscr'])} | {'; '.join(broken) or 'none'} | "
                   f"{x(pf.get('debt_ebitda'))} | {x(pf.get('interest_coverage'))}{lb} | {x(pf.get('dscr'))}{lb} |")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    text = build()
    OUT.write_text(text)
    readme = README.read_text()
    block = f"<!-- tables:start (generated by python -m creditmemo.report) -->\n{text}<!-- tables:end -->"
    if "<!-- tables:start" in readme:
        readme = re.sub(r"<!-- tables:start.*?<!-- tables:end -->", lambda m: block, readme, flags=re.S)
    else:
        readme = readme.replace("## Memos: all three companies", "## Ratio and stress tables\n\n" + block +
                                "\n\n## Memos: all three companies", 1)
    README.write_text(readme)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
