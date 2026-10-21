"""Compare the frozen internal grade with agency ratings.

    python -m creditmemo.benchmark        # writes outputs/benchmark.md

The grade thresholds were frozen (config/grade.sha256) before the ratings in
config/agency_ratings.json were looked up, so this is a test, not a fit.
"""

from __future__ import annotations

import json
import sys

from . import CONFIG_DIR, ROOT, SPREAD_DIR
from .grade import agency_equivalent, load_config

OUT = ROOT / "outputs" / "benchmark.md"
AGENCIES = [("sp", "S&P"), ("moodys", "Moody's"), ("fitch", "Fitch")]


def compare() -> list:
    cfg = load_config()
    ratings = json.loads((CONFIG_DIR / "agency_ratings.json").read_text())["companies"]
    rows = []
    for t, r in ratings.items():
        spread = json.loads((SPREAD_DIR / f"{t}.json").read_text())
        g = spread["grade"]
        eq = {k: agency_equivalent(r[k]["rating"], cfg) for k, _ in AGENCIES if r.get(k)}
        rows.append({"ticker": t, "name": spread["name"], "grade": g["grade"], "base": g["base_grade"],
                     "weighted": g["weighted_score"], "notches": g["stress_notches"],
                     "ratings": {k: r[k] for k, _ in AGENCIES if r.get(k)}, "equivalent": eq,
                     "gap_sp": None if "sp" not in eq else g["grade"] - eq["sp"],
                     "gap_moodys": None if "moodys" not in eq else g["grade"] - eq["moodys"]})
    return rows


def main(argv=None) -> int:
    rows = compare()
    lines = ["# Internal grade vs agency ratings", "",
             "Grade scale 1 (best) to 10. Agency equivalents use the map frozen with the grade. "
             "Gap = internal grade minus agency equivalent: positive means the tool is harsher.", "",
             "| Company | Internal grade | S&P | Moody's | Fitch | Gap vs S&P | Gap vs Moody's |",
             "|---|---|---|---|---|---|---|"]
    for x in rows:
        def cell(k):
            r = x["ratings"].get(k)
            if not r:
                return "—"
            stale = " ⚠ stale" if r.get("stale") else ""
            out = f" {r['outlook']}" if r.get("outlook") else ""
            return f"{r['rating']}{out} (= {x['equivalent'][k]}, {r['as_of']}){stale}"
        gap = lambda v: "—" if v is None else f"{v:+d}"
        lines.append(f"| {x['name']} | **{x['grade']}** (base {x['base']}, score {x['weighted']:.2f}, "
                     f"stress +{x['notches']}) | {cell('sp')} | {cell('moodys')} | {cell('fitch')} | "
                     f"{gap(x['gap_sp'])} | {gap(x['gap_moodys'])} |")
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
