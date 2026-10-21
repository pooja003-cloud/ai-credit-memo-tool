"""Build spreads and ratios from the cached company facts.

    python -m creditmemo.build            # all companies in config
    python -m creditmemo.build DVA

Writes outputs/spreads/<TICKER>.json (spread, ratios, warnings) and
outputs/spreads/<TICKER>_log.csv (one row per number, with its tag and filing).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys

from . import SPREAD_DIR
from .edgar import companyfacts_path, load_companies
from .ratios import RATIO_LABELS
from .spread import LOG_FIELDS, build_spread, load_override, load_tag_spec, log_rows


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

    for t in [x.upper() for x in args.tickers]:
        co = cfg["companies"][t]
        path = companyfacts_path(co["cik"])
        if not path.exists():
            print(f"{t}: no cached data at {path}. Run: python -m creditmemo.edgar {t}",
                  file=sys.stderr)
            return 1
        with open(path) as fh:
            cf = json.load(fh)
        spread = build_spread(cf, t, co, spec, load_override(t), years)
        spread["facility"] = cfg["defaults"]["facility"]

        with open(SPREAD_DIR / f"{t}.json", "w") as fh:
            json.dump(spread, fh, indent=2)
        with open(SPREAD_DIR / f"{t}_log.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=LOG_FIELDS)
            w.writeheader()
            w.writerows(log_rows(spread))

        labels = [p["label"] for p in spread["periods"]]
        print(f"\n{t}  {spread['name']}  ({', '.join(labels)})")
        for key, name in RATIO_LABELS.items():
            vals = "  ".join(f"{fmt_ratio(spread['ratios'][l][key]):>8}" for l in labels)
            print(f"  {name:32}{vals}")
        for wmsg in spread["warnings"]:
            print(f"  ! {wmsg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
