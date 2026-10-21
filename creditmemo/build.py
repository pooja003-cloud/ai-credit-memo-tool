"""Build the spread for each company: as reported -> standard -> ratios.

    python -m creditmemo.build            # all companies in config
    python -m creditmemo.build DVA

Writes
  outputs/spreads/<TICKER>.json        the final spread: as-reported statements,
                                       standard spread, note items, ratios,
                                       tie-outs and the cross-check
  outputs/xbrl_facts/<TICKER>.json     the company-facts route (cross-check and
  outputs/xbrl_facts/<TICKER>_log.csv  note items), one row per number with its tag
"""

from __future__ import annotations

import argparse
import csv
import json
import sys

from . import ROOT, SPREAD_DIR
from .asreported import build_as_reported
from .edgar import companyfacts_path, load_companies
from .ratios import RATIO_LABELS, compute_period
from .spread import LOG_FIELDS, build_spread, load_override, load_tag_spec, log_rows
from .standard import build_standard

FACTS_DIR = ROOT / "outputs" / "xbrl_facts"

# Items a 10-K gives only in the notes, taken from the company-facts route.
NOTE_ITEMS = ["operating_lease_cost", "operating_lease_liabilities", "scheduled_principal", "cash_taxes"]

# Standard line vs company-facts concept, compared period by period.
CROSS_CHECK = [
    ("income", "revenue", "revenue", 1),
    ("income", "operating_income", "operating_income", 1),
    ("income", "da", "da", 1),
    ("income", "interest_expense", "interest_expense", 1),
    ("cashflow", "cfo", "cfo", 1),
    ("cashflow", "capex", "capex", -1),
    ("balance", "cash", "cash", 1),
    ("balance", "current_assets", "current_assets", 1),
    ("balance", "current_liabilities", "current_liabilities", 1),
    ("balance", "total_debt", None, 1),
]
CROSS_TOL = 0.01


def _line(std, statement, key):
    for ln in std[statement]:
        if ln["key"] == key:
            return dict(zip(std["periods"][statement], ln["values"]))
    return {}


def assemble(ticker: str, company: dict, facility: dict, cf: dict, spec: dict, override: dict,
             years: int = 3) -> dict:
    facts = build_spread(cf, ticker, company, spec, override, years)
    asrep = build_as_reported(ticker, company, years)
    std = build_standard(asrep)
    labels = std["periods"]["income"]

    notes = {c: {lab: facts["lines"][c].get(lab) for lab in labels} for c in NOTE_ITEMS}
    get = lambda st, k: _line(std, st, k)
    inc = {k: get("income", k) for k in ("revenue", "operating_income", "da", "interest_expense")}
    bal = {k: get("balance", k) for k in ("cash", "current_assets", "current_liabilities",
                                          "debt_current", "ltd", "lease_liabilities")}
    cfl = {k: get("cashflow", k) for k in ("cfo", "capex")}

    ratio_inputs, derived, ratios, ratio_notes = {}, {}, {}, {}
    for lab in labels:
        note = lambda c: (notes[c][lab] or {}).get("value")
        lease_liab = note("operating_lease_liabilities")
        if lease_liab is None:
            lease_liab = bal["lease_liabilities"].get(lab)
        capex = cfl["capex"].get(lab)
        v = {
            "revenue": inc["revenue"].get(lab),
            "operating_income": inc["operating_income"].get(lab),
            "da": inc["da"].get(lab),
            "interest_expense": inc["interest_expense"].get(lab),
            "short_term_borrowings": bal["debt_current"].get(lab),
            "commercial_paper": 0.0, "current_ltd": 0.0, "finance_lease_liabilities": 0.0,
            "noncurrent_ltd": bal["ltd"].get(lab),
            "cash": bal["cash"].get(lab),
            "current_assets": bal["current_assets"].get(lab),
            "current_liabilities": bal["current_liabilities"].get(lab),
            "cfo": cfl["cfo"].get(lab),
            "capex": None if capex is None else -capex,
            "operating_lease_liabilities": lease_liab,
            "operating_lease_cost": note("operating_lease_cost"),
            "cash_taxes": note("cash_taxes"),
            "scheduled_principal": note("scheduled_principal"),
        }
        ratio_inputs[lab] = v
        derived[lab], ratios[lab], ratio_notes[lab] = compute_period(v)

    cross = []
    for statement, key, concept, sign in CROSS_CHECK:
        ours = get(statement, key)
        for lab in labels:
            a = ours.get(lab)
            b = facts["derived"][lab]["total_debt"] if concept is None else \
                facts["lines"][concept][lab]["value"]
            if a is None or b is None:
                continue
            a = sign * a
            diff = (a - b) / abs(b) if b else (0.0 if a == 0 else 1.0)
            cross.append({"statement": statement, "line": key, "period": lab,
                          "standard": a, "company_facts": b, "diff": diff,
                          "ok": abs(diff) <= CROSS_TOL})

    warnings = [f"Tie-out failed: {t['statement']} {t['check']} {t['period']}"
                for t in std["ties"] if not t["ok"]]
    warnings += [w for w in facts["warnings"]
                 if any(facts["concept_labels"][c] in w for c in NOTE_ITEMS)]

    return {
        "spread_version": 2,
        "ticker": ticker, "name": company["name"], "cik": company["cik"],
        "role": company.get("role"), "facility": facility,
        "floating_rate_share": company.get("floating_rate_share"),
        "floating_rate_source": company.get("floating_rate_source"),
        "periods": [{"label": lab} for lab in labels],
        "as_reported": asrep,
        "standard": std,
        "notes": notes,
        "ratio_inputs": ratio_inputs,
        "derived": derived,
        "ratios": ratios,
        "ratio_notes": ratio_notes,
        "ties_ok": std["ties_ok"],
        "cross_check": cross,
        "warnings": warnings,
    }, facts


def fmt_ratio(x):
    return "n.m." if x is None else f"{x:.2f}x"


def main(argv=None) -> int:
    cfg = load_companies()
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*", default=list(cfg["companies"]))
    args = ap.parse_args(argv)

    spec = load_tag_spec()
    years = cfg["defaults"].get("years", 3)
    SPREAD_DIR.mkdir(parents=True, exist_ok=True)
    FACTS_DIR.mkdir(parents=True, exist_ok=True)

    for t in [x.upper() for x in args.tickers]:
        co = cfg["companies"][t]
        path = companyfacts_path(co["cik"])
        if not path.exists():
            print(f"{t}: no cached data. Run: python -m creditmemo.edgar {t}", file=sys.stderr)
            return 1
        cf = json.loads(path.read_text())
        spread, facts = assemble(t, co, cfg["defaults"]["facility"], cf, spec, load_override(t), years)

        (SPREAD_DIR / f"{t}.json").write_text(json.dumps(spread, indent=2))
        (FACTS_DIR / f"{t}.json").write_text(json.dumps(facts, indent=2))
        with open(FACTS_DIR / f"{t}_log.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=LOG_FIELDS)
            w.writeheader()
            w.writerows(log_rows(facts))

        labels = [p["label"] for p in spread["periods"]]
        n_ties = len(spread["standard"]["ties"])
        n_bad = sum(not x["ok"] for x in spread["standard"]["ties"])
        print(f"\n{t}  {spread['name']}  ({', '.join(labels)})  "
              f"tie-outs: {n_ties - n_bad}/{n_ties} pass")
        for key, name in RATIO_LABELS.items():
            vals = "  ".join(f"{fmt_ratio(spread['ratios'][l][key]):>8}" for l in labels)
            print(f"  {name:32}{vals}")
        for x in spread["cross_check"]:
            if not x["ok"]:
                print(f"  ~ cross-check {x['period']} {x['line']}: standard {x['standard']/1e6:,.1f}m "
                      f"vs company facts {x['company_facts']/1e6:,.1f}m ({x['diff']:+.1%})")
        for wmsg in spread["warnings"]:
            print(f"  ! {wmsg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
