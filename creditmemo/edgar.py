"""Download and cache SEC EDGAR data.

For each company:
  * company facts (all XBRL values) and the filing list (JSON)
  * for the latest two 10-Ks: FilingSummary.xml and the rendered statement
    pages (R files) that the as-reported layer is parsed from
  * the latest 10-K's main document, for the memo's text sections

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
import xml.etree.ElementTree as ET
from pathlib import Path

from . import CACHE_DIR, CONFIG_DIR

BASE = "https://data.sec.gov"
ARCHIVES = "https://www.sec.gov/Archives/edgar/data"
N_TENKS = 2  # latest 10-K has 2 balance sheets; the prior one supplies the third
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


def _download(url: str) -> bytes:
    import requests  # only needed when downloading

    global _last_request
    wait = MIN_INTERVAL - (time.monotonic() - _last_request)
    if wait > 0:
        time.sleep(wait)
    resp = requests.get(url, headers={"User-Agent": user_agent(),
                                      "Accept-Encoding": "gzip, deflate"}, timeout=60)
    _last_request = time.monotonic()
    resp.raise_for_status()
    return resp.content


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def get_bytes(url: str, path: Path, refresh: bool = False) -> bytes:
    """Return a cached file, downloading it first if needed."""
    if path.exists() and not refresh:
        return path.read_bytes()
    data = _download(url)
    _write(path, data)
    return data


def get_json(url: str, path: Path, refresh: bool = False) -> dict:
    """Return cached JSON, downloading it first if needed."""
    return json.loads(get_bytes(url, path, refresh))


def companyfacts(cik: int, refresh: bool = False) -> dict:
    return get_json(f"{BASE}/api/xbrl/companyfacts/CIK{cik:010d}.json",
                    companyfacts_path(cik), refresh)


def submissions(cik: int, refresh: bool = False) -> dict:
    return get_json(f"{BASE}/submissions/CIK{cik:010d}.json", submissions_path(cik), refresh)


def filings_dir(ticker: str, cache_dir: Path = CACHE_DIR) -> Path:
    return cache_dir / "filings" / ticker


def latest_10ks(sub: dict, n: int = N_TENKS) -> list:
    """The latest n original 10-K filings (newest first) from the filing list."""
    recent = sub.get("filings", {}).get("recent", {})
    keys = ["accessionNumber", "form", "filingDate", "reportDate", "primaryDocument"]
    rows = [dict(zip(keys, vals)) for vals in zip(*(recent.get(k, []) for k in keys))]
    tenks = [r for r in rows if r["form"] == "10-K"]
    tenks.sort(key=lambda r: r["filingDate"], reverse=True)
    return tenks[:n]


def statement_reports(filing_summary_xml: bytes) -> list:
    """Reports in the 'Statements' menu of a FilingSummary.xml.

    Returns dicts with position, short_name, long_name and file (R page name).
    """
    root = ET.fromstring(filing_summary_xml)
    out = []
    for rep_el in root.iter("Report"):
        cat = (rep_el.findtext("MenuCategory") or "").strip()
        fname = (rep_el.findtext("HtmlFileName") or rep_el.findtext("XmlFileName") or "").strip()
        if cat != "Statements" or not fname:
            continue
        out.append({
            "position": int(rep_el.findtext("Position") or 0),
            "short_name": (rep_el.findtext("ShortName") or "").strip(),
            "long_name": (rep_el.findtext("LongName") or "").strip(),
            "file": fname,
        })
    return sorted(out, key=lambda r: r["position"])


def fetch_filings(ticker: str, cik: int, sub: dict, refresh: bool = False) -> list:
    """Download FilingSummary.xml + statement R pages for the latest 10-Ks,
    and the latest 10-K's main document. Writes an index.json per filing."""
    done = []
    for i, f in enumerate(latest_10ks(sub)):
        accn = f["accessionNumber"]
        base = f"{ARCHIVES}/{cik}/{accn.replace('-', '')}"
        folder = filings_dir(ticker) / accn
        summary = get_bytes(f"{base}/FilingSummary.xml", folder / "FilingSummary.xml", refresh)
        reports = statement_reports(summary)
        for r in reports:
            get_bytes(f"{base}/{r['file']}", folder / r["file"], refresh)
        if i == 0 and f.get("primaryDocument"):
            get_bytes(f"{base}/{f['primaryDocument']}", folder / f["primaryDocument"], refresh)
        index = dict(f, ticker=ticker, cik=cik, base_url=base, statements=reports,
                     main_document=f["primaryDocument"] if i == 0 else None)
        _write(folder / "index.json", json.dumps(index, indent=2).encode())
        done.append(index)
    return done


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
        filings = fetch_filings(t.upper(), co["cik"], sub, args.refresh)
        print(f"{t.upper():5} {cf.get('entityName')!r}: {n_tags} us-gaap tags")
        for f in filings:
            print(f"      10-K {f['accessionNumber']} filed {f['filingDate']} "
                  f"(period {f['reportDate']}): {len(f['statements'])} statement pages")
            if len(f["statements"]) < 3:
                print("      WARNING: fewer than 3 statement pages found", file=sys.stderr)
                ok = False
        def squash(s):
            return "".join(ch for ch in s.lower() if ch.isalnum())
        if squash(co["name"].split()[0]) not in squash(cf.get("entityName") or ""):
            print(f"  WARNING: SEC name doesn't match config name {co['name']!r}; check the CIK",
                  file=sys.stderr)
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
