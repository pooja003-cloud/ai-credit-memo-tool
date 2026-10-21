"""Layer 1: the three statements exactly as reported in the 10-K.

Parsed from the SEC's rendered statement pages (R files) downloaded by
edgar.py. Each row keeps its label, XBRL tag and the value as printed
(sign included), converted from the page's scale ("$ in Thousands") into
dollars. Member rows (breakdowns by axis, shown below the statement)
are left out.

Periods: the latest 10-K gives three years of income and cash flow and two
balance sheets. The prior 10-K supplies the third balance sheet, matched
to the latest 10-K's rows by XBRL tag.
"""

from __future__ import annotations

import html as _html
import json
import re
from datetime import date
from pathlib import Path
from typing import List, Optional

from .edgar import filings_dir
from .facts import fiscal_label

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
SCALES = {"thousands": 1e3, "millions": 1e6, "billions": 1e9}
KINDS = ("income", "balance", "cashflow")
KIND_NAMES = {"income": "Income statement", "balance": "Balance sheet", "cashflow": "Cash flow statement"}

_TAG_RE = re.compile(r"<[^>]+>")
_DATE_RE = re.compile(r"([A-Z][a-z]{2,3})\.? (\d{1,2}), (\d{4})")


def _text(s: str) -> str:
    return " ".join(_html.unescape(_TAG_RE.sub(" ", s)).split())


def parse_value(cell: str) -> Optional[float]:
    t = _text(cell)
    t = re.sub(r"\[\d+\]", "", t).replace("$", "").replace(",", "").strip()
    if not t or t in {"-", "—", "–"}:
        return None
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()").strip()
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


def parse_date(s: str) -> Optional[date]:
    m = _DATE_RE.search(s)
    if not m:
        return None
    return date(int(m.group(3)), MONTHS[m.group(1)[:3].lower()], int(m.group(2)))


def row_kind(tag: str, label: str = "") -> str:
    """money, per_share or shares; only money rows are scaled to dollars.

    Default is money: a tag like SharesWithheldForTaxes... is a cash amount.
    """
    name = tag.split("_", 1)[-1]
    low = label.lower()
    if re.search(r"Per\w*Share", name) or "per share" in low and "(in" in low:
        return "per_share"
    if name.startswith("WeightedAverageNumber") or "(in shares)" in low or re.search(
            r"Shares(Outstanding|Issued|Authorized|Subscribed)|NumberOfShares|PeriodShares", name):
        return "shares"
    return "money"


def parse_r_page(page: str) -> dict:
    """Parse one rendered statement page into title, columns and rows."""
    table = re.search(r'<table class="report".*?</table>', page, re.S)
    if not table:
        raise ValueError("no report table found")
    t = table.group(0)
    header_rows = re.findall(r"<tr>\s*(<th.*?)</tr>", t, re.S)
    title_cell = re.search(r'<th class="tl"[^>]*>(.*?)</th>', t, re.S)
    title = _text(title_cell.group(1)) if title_cell else ""
    low = title.lower()
    money_scale, share_scale = 1.0, 1.0
    m = re.search(r"\$ in (thousands|millions|billions)", low)
    if m:
        money_scale = SCALES[m.group(1)]
    m = re.search(r"shares in (thousands|millions|billions)", low)
    if m:
        share_scale = SCALES[m.group(1)]

    # Column headers: optional "12 Months Ended" band (with colspan), then dates.
    bands: List[Optional[int]] = []
    dates: List[date] = []
    for hr in header_rows:
        for attrs, inner in re.findall(r"<th([^>]*)>(.*?)</th>", hr, re.S):
            if 'class="tl"' in attrs:
                continue
            txt = _text(inner)
            span = re.search(r'colspan="(\d+)"', attrs)
            n = int(span.group(1)) if span else 1
            mm = re.match(r"(\d+) Months Ended", txt)
            if mm:
                bands += [int(mm.group(1))] * n
                continue
            d = parse_date(txt)
            if d:
                dates.append(d)
    if bands and len(bands) != len(dates):
        bands = [bands[0]] * len(dates)
    columns = [{"end": d.isoformat(), "months": bands[i] if bands else None}
               for i, d in enumerate(dates)]

    rows, in_members = [], False
    for cls, body in re.findall(r'<tr class="(\w+)">(.*?)</tr>', t, re.S):
        if cls == "rh":          # an axis/member header: what follows is a breakdown
            in_members = True
            continue
        if in_members:
            continue
        tag_m = re.search(r"defref_([\w-]+)", body)
        tds = re.findall(r"<td([^>]*)>(.*?)</td>", body, re.S)
        if not tag_m or not tds:
            continue
        tag = tag_m.group(1)
        label = _text(tds[0][1])
        abstract = "<strong>" in tds[0][1] and all(_text(c) == "" for _, c in tds[1:])
        if abstract or tag.endswith("Abstract"):
            rows.append({"label": label, "tag": tag, "abstract": True})
            continue
        kind = row_kind(tag, label)
        scale = money_scale if kind == "money" else share_scale if kind == "shares" else 1.0
        vals = [parse_value(c) for _, c in tds[1:1 + len(columns)]]
        vals = [None if v is None else round(v * scale, 6) for v in vals]
        rows.append({"label": label, "tag": tag, "abstract": False, "kind": kind,
                     "total": cls.endswith("u"), "values": vals})
    return {"title": title, "money_scale": money_scale, "columns": columns, "rows": rows}


def classify(short_name: str) -> Optional[str]:
    n = short_name.upper()
    if "PARENTHETICAL" in n:
        return None
    if "CASH FLOW" in n:
        return "cashflow"
    if "BALANCE SHEET" in n or "FINANCIAL POSITION" in n or "FINANCIAL CONDITION" in n:
        return "balance"
    if ("INCOME" in n or "OPERATIONS" in n or "EARNINGS" in n) and "COMPREHENSIVE" not in n \
            and "EQUITY" not in n:
        return "income"
    return None


def load_filing(folder: Path) -> dict:
    """Parse the three statements of one cached 10-K."""
    index = json.loads((folder / "index.json").read_text())
    found = {}
    for rep in index["statements"]:
        kind = classify(rep["short_name"])
        if kind and kind not in found:
            parsed = parse_r_page((folder / rep["file"]).read_text(errors="replace"))
            parsed.update({"file": rep["file"], "short_name": rep["short_name"],
                           "url": f"{index['base_url']}/{rep['file']}"})
            found[kind] = parsed
    if "income" not in found:   # combined "operations and comprehensive income" statements
        for rep in index["statements"]:
            n = rep["short_name"].upper()
            if "PARENTHETICAL" not in n and ("INCOME" in n or "OPERATIONS" in n) and "EQUITY" not in n:
                parsed = parse_r_page((folder / rep["file"]).read_text(errors="replace"))
                parsed.update({"file": rep["file"], "short_name": rep["short_name"],
                               "url": f"{index['base_url']}/{rep['file']}"})
                found["income"] = parsed
                break
    missing = [k for k in KINDS if k not in found]
    if missing:
        raise ValueError(f"{folder.name}: statements not found: {missing}")
    return {"accn": index["accessionNumber"], "filed": index["filingDate"],
            "period": index["reportDate"], "statements": found}


def _annual_cols(stmt: dict, kind: str) -> List[int]:
    if kind == "balance":
        return list(range(len(stmt["columns"])))
    return [i for i, c in enumerate(stmt["columns"]) if c["months"] in (None, 12)]


def build_as_reported(ticker: str, company: dict, years: int = 3,
                      folder: Optional[Path] = None) -> dict:
    """Merge the cached 10-Ks into one as-reported set of statements."""
    base = folder or filings_dir(ticker)
    filings = sorted((load_filing(d) for d in base.iterdir() if (d / "index.json").exists()),
                     key=lambda f: f["filed"], reverse=True)
    if not filings:
        raise ValueError(f"{ticker}: no cached filings; run python -m creditmemo.edgar {ticker}")
    convention = company.get("fiscal_label", "end_year")
    latest = filings[0]
    out = {"ticker": ticker, "name": company["name"],
           "filings": [{"accn": f["accn"], "filed": f["filed"], "period": f["period"]} for f in filings],
           "statements": {}}

    for kind in KINDS:
        stmt = latest["statements"][kind]
        cols = _annual_cols(stmt, kind)
        periods = [{"end": stmt["columns"][i]["end"], "accn": latest["accn"], "url": stmt["url"]}
                   for i in cols]
        rows = []
        for r in stmt["rows"]:
            row = {k: r[k] for k in ("label", "tag", "abstract")}
            if not r["abstract"]:
                row.update(kind=r["kind"], total=r["total"],
                           values=[r["values"][i] if i < len(r["values"]) else None for i in cols])
            rows.append(row)

        # Older periods from earlier 10-Ks (the third balance sheet), matched by tag
        # and by the order in which a tag repeats.
        for f in filings[1:]:
            if len(periods) >= years:
                break
            old = f["statements"][kind]
            have = {p["end"] for p in periods}
            for i in _annual_cols(old, kind):
                end = old["columns"][i]["end"]
                if end in have or len(periods) >= years:
                    continue
                periods.append({"end": end, "accn": f["accn"], "url": old["url"]})
                seen, matched = {}, set()
                old_rows = [r for r in old["rows"] if not r["abstract"]]
                for row in rows:
                    if row["abstract"]:
                        continue
                    k = seen.get(row["tag"], 0)
                    seen[row["tag"]] = k + 1
                    cands = [j for j, r in enumerate(old_rows) if r["tag"] == row["tag"]]
                    if k < len(cands):
                        j = cands[k]
                        matched.add(j)
                        row["values"].append(old_rows[j]["values"][i])
                    else:
                        row["values"].append(None)
                for j, r in enumerate(old_rows):   # lines only in the older 10-K
                    if j not in matched and r["values"][i] not in (None, 0):
                        rows.append({"label": r["label"], "tag": r["tag"], "abstract": False,
                                     "kind": r["kind"], "total": r["total"], "only_in_prior": True,
                                     "values": [None] * (len(periods) - 1) + [r["values"][i]]})
                for row in rows:
                    if not row["abstract"]:
                        row["values"] += [None] * (len(periods) - len(row["values"]))

        # oldest first, keep the latest `years`
        order = sorted(range(len(periods)), key=lambda i: periods[i]["end"])[-years:]
        periods = [periods[i] for i in order]
        for row in rows:
            if not row["abstract"]:
                row["values"] = [row["values"][i] for i in order]
        for p in periods:
            p["label"] = fiscal_label(date.fromisoformat(p["end"]), convention)
        for i, row in enumerate(rows):
            row["id"] = i
        out["statements"][kind] = {
            "name": KIND_NAMES[kind], "title": stmt["title"], "short_name": stmt["short_name"],
            "money_scale": stmt["money_scale"], "periods": periods, "rows": rows}
    return out
