"""Download and cache SEC EDGAR JSON.

SEC asks every client to send a User-Agent with a contact email and to
stay under 10 requests a second. We send at most 4 a second and cache
every response, so each file is downloaded once.

    export SEC_USER_AGENT="Your Name your@email.com"
    python -m creditmemo.edgar DVA UNP KSS
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from . import CACHE_DIR, CONFIG_DIR

BASE = "https://data.sec.gov"
MIN_INTERVAL = 0.25  # seconds between requests
_last_request = 0.0


def user_agent() -> str:
    ua = os.environ.get("SEC_USER_AGENT", "").strip()
    if "@" not in ua:
        raise SystemExit(
            'Set SEC_USER_AGENT first, e.g.  export SEC_USER_AGENT="Your Name you@example.com"\n'
            "SEC requires a contact in the User-Agent header.")
    return ua


def companyfacts_path(cik: int, cache_dir: Path = CACHE_DIR) -> Path:
    return cache_dir / "companyfacts" / f"CIK{cik:010d}.json"


def submissions_path(cik: int, cache_dir: Path = CACHE_DIR) -> Path:
    return cache_dir / "submissions" / f"CIK{cik:010d}.json"


def get_json(url: str, path: Path, refresh: bool = False) -> dict:
    """Return cached JSON, downloading it first if needed."""
    if path.exists() and not refresh:
        with open(path) as fh:
            return json.load(fh)
    import requests  # only needed when downloading

    global _last_request
    wait = MIN_INTERVAL - (time.monotonic() - _last_request)
    if wait > 0:
        time.sleep(wait)
    resp = requests.get(url, headers={"User-Agent": user_agent(),
                                      "Accept-Encoding": "gzip, deflate"}, timeout=60)
    _last_request = time.monotonic()
    resp.raise_for_status()
    data = resp.json()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w") as fh:
        json.dump(data, fh)
    tmp.replace(path)
    return data


def companyfacts(cik: int, refresh: bool = False) -> dict:
    return get_json(f"{BASE}/api/xbrl/companyfacts/CIK{cik:010d}.json",
                    companyfacts_path(cik), refresh)


def submissions(cik: int, refresh: bool = False) -> dict:
    return get_json(f"{BASE}/submissions/CIK{cik:010d}.json", submissions_path(cik), refresh)


def load_companies() -> dict:
    with open(CONFIG_DIR / "companies.json") as fh:
        return json.load(fh)


def main(argv=None) -> int:
    cfg = load_companies()
    ap = argparse.ArgumentParser(description="Download SEC company facts and filing lists into data/cache")
    ap.add_argument("tickers", nargs="*", default=list(cfg["companies"]))
    ap.add_argument("--refresh", action="store_true", help="download again even if cached")
    args = ap.parse_args(argv)

    ok = True
    for t in args.tickers:
        co = cfg["companies"].get(t.upper())
        if co is None:
            print(f"{t}: not in config/companies.json", file=sys.stderr)
            ok = False
            continue
        cf = companyfacts(co["cik"], args.refresh)
        sub = submissions(co["cik"], args.refresh)
        n_tags = len(cf.get("facts", {}).get("us-gaap", {}))
        tenks = [f for f in sub.get("filings", {}).get("recent", {}).get("form", []) if f == "10-K"]
        print(f"{t.upper():5} {cf.get('entityName')!r}: {n_tags} us-gaap tags, "
              f"{len(tenks)} 10-Ks in recent filings")
        def squash(s):
            return "".join(ch for ch in s.lower() if ch.isalnum())
        if squash(co["name"].split()[0]) not in squash(cf.get("entityName") or ""):
            print(f"  WARNING: SEC name doesn't match config name {co['name']!r}; check the CIK",
                  file=sys.stderr)
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
