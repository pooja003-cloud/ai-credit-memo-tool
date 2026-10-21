"""Hand-check workbook: compare the tool's spread with figures typed from the 10-K.

    python -m creditmemo.handcheck make DVA --unit 1000      # writes handcheck/DVA_handcheck.xlsx
    python -m creditmemo.handcheck compare DVA               # reads it back, writes handcheck/DVA_result.md

`--unit` is the unit the 10-K reports in (DaVita: dollars in thousands -> 1000;
Union Pacific and Kohl's: millions -> 1000000). You type numbers exactly as the
10-K prints them; the sheet converts the tool's values to the same unit.

Two sheets:
  Hand check  one row per spread line and year. Type the 10-K figure into the
              yellow column; the sheet shows the difference and whether it is
              within the 1% target.
  Ratios      the same ratio formulas rebuilt in Excel from your typed figures,
              next to the tool's ratios. This checks the Python ratio code
              independently of the XBRL mapping.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import ROOT, SPREAD_DIR

HANDCHECK_DIR = ROOT / "handcheck"

WHERE = {
    "revenue": "Income statement",
    "operating_income": "Income statement",
    "da": "Cash flow statement (operating section) or income statement",
    "interest_expense": "Income statement",
    "pretax_income": "Income statement",
    "net_income": "Income statement",
    "cfo": "Cash flow statement",
    "capex": "Cash flow statement (investing section)",
    "cash_taxes": "Cash flow supplemental disclosure or income tax note",
    "operating_lease_cost": "Leases note",
    "cash": "Balance sheet",
    "current_assets": "Balance sheet",
    "current_liabilities": "Balance sheet",
    "total_assets": "Balance sheet",
    "equity": "Balance sheet",
    "short_term_borrowings": "Balance sheet (enter 0 if no such line)",
    "commercial_paper": "Balance sheet or debt note (enter 0 if none)",
    "current_ltd": "Balance sheet",
    "noncurrent_ltd": "Balance sheet",
    "finance_lease_liabilities": "Leases note",
    "operating_lease_liabilities": "Leases note or balance sheet (current + noncurrent)",
    "scheduled_principal": "Debt note: maturities table, next year",
}

RATIOS = [
    ("debt_ebitda", "Debt / EBITDA"),
    ("net_debt_ebitda", "Net debt / EBITDA"),
    ("lease_adj_debt_ebitdar", "(Debt + leases) / EBITDAR"),
    ("interest_coverage", "EBITDA / interest"),
    ("dscr", "DSCR"),
    ("current_ratio", "Current ratio"),
]


def _path(ticker: str) -> Path:
    return HANDCHECK_DIR / f"{ticker}_handcheck.xlsx"


def make(ticker: str, unit: int, periods=None) -> Path:
    from openpyxl import Workbook
    from openpyxl.comments import Comment
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.worksheet.datavalidation import DataValidation

    spread = json.loads((SPREAD_DIR / f"{ticker}.json").read_text())
    labels = periods or [p["label"] for p in spread["periods"]][-2:]

    F = "Arial"
    base = Font(name=F, size=10)
    bold = Font(name=F, size=10, bold=True)
    title = Font(name=F, size=14, bold=True)
    blue = Font(name=F, size=10, color="0000FF")
    green = Font(name=F, size=10, color="008000")
    link = Font(name=F, size=10, color="0563C1", underline="single")
    head_fill = PatternFill("solid", fgColor="DDE3EA")
    yellow = PatternFill("solid", fgColor="FFFF00")
    thin = Side(style="thin", color="B7B7B7")
    box = Border(bottom=thin)
    wrap = Alignment(wrap_text=True, vertical="top")
    num = '#,##0;(#,##0);"-"'
    pct = '0.00%;(0.00%);0.00%'
    mult = '0.00"x";(0.00"x");"-"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Hand check"

    ws["A1"] = f"{spread['name']} ({ticker}): hand check of the tool's spread"
    ws["A1"].font = title
    ws["A3"], ws["B3"] = "Unit you type in ($ per unit)", unit
    ws["B3"].font, ws["B3"].fill = blue, yellow
    ws["B3"].number_format = "#,##0"
    ws["C3"] = "1,000 if the 10-K says 'in thousands'; 1,000,000 if 'in millions'"
    ws["A4"], ws["B4"] = "Match target", 0.01
    ws["B4"].font, ws["B4"].number_format = blue, "0.0%"
    ws["A5"] = "How to use"
    ws["B5"] = ("Type each figure exactly as the 10-K prints it into the yellow '10-K value' column, "
                "and the page or note into 'Where you found it'. Leave a cell blank if you haven't "
                "checked it yet. Everything else is calculated.")
    ws["A6"] = "Example"
    ex_lab = labels[-1]
    ex_val = spread["lines"]["revenue"][ex_lab]["value"] / unit
    ws["B6"] = (f"Revenue {ex_lab}: if the income statement prints total revenues as {ex_val:,.0f}, "
                f"type {ex_val:.0f} in the yellow cell and something like "
                "'Consolidated Statements of Income, p. 72' next to it.")
    for c in ("A3", "A4", "A5", "A6"):
        ws[c].font = bold
    for c in ("C3", "B5", "B6"):
        ws[c].font = base
        ws[c].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("B5:L5")
    ws.merge_cells("B6:L6")
    ws.row_dimensions[5].height = 30
    ws.row_dimensions[6].height = 30

    ws["A8"], ws["B8"] = "Lines checked", '=COUNT(F12:F200)'
    ws["A9"], ws["B9"] = "Within target", '=COUNTIF(H12:H200,"Yes")'
    ws["C8"], ws["D8"] = "Match rate", '=IF(B8=0,"",B9/B8)'
    for c in ("A8", "A9", "C8"):
        ws[c].font = bold
    for c in ("B8", "B9", "D8"):
        ws[c].font = Font(name=F, size=11, bold=True)
    ws["D8"].number_format = "0.0%"

    headers = ["Line", "Concept", "Year", "Tool value ($)", "Tool value (10-K units)",
               "10-K value (type here)", "Difference %", "Within target?", "Where you found it",
               "Where to look", "XBRL tag / source", "Filing", "Tool note"]
    hr = 11
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=hr, column=i, value=h)
        c.font, c.fill, c.alignment, c.border = bold, head_fill, wrap, box
    ws.freeze_panes = "A12"

    row_of = {}
    r = hr + 1
    for concept, by_period in spread["lines"].items():
        for lab in labels:
            rec = by_period[lab]
            raw = rec.get("reported_value", rec["value"])
            note = rec.get("note") or ""
            if rec["source"] == "included_in_debt":
                note = "Reported separately but already inside long-term debt; the tool does not add it again."
            if rec.get("proxy"):
                note = "PROXY. " + note
            src = rec.get("tag") or rec["source"]
            if rec["source"] == "manual":
                src = f"manual: {rec.get('manual_source')}"
            elif rec["source"] == "assumed_zero":
                src = "not tagged (counted as 0)"
            vals = [spread["concept_labels"][concept], concept, lab, raw]
            for i, v in enumerate(vals, 1):
                ws.cell(row=r, column=i, value=v).font = base
            ws.cell(row=r, column=4).font = blue
            ws.cell(row=r, column=4).number_format = num
            ws.cell(row=r, column=4).comment = Comment(
                f"From outputs/spreads/{ticker}.json ({rec['source']})", "creditmemo")
            e = ws.cell(row=r, column=5, value=f'=IF(D{r}="","",D{r}/$B$3)')
            e.font, e.number_format = base, num
            f = ws.cell(row=r, column=6)
            f.fill, f.font, f.number_format = yellow, blue, num
            g = ws.cell(row=r, column=7,
                        value=f'=IF(OR(F{r}="",E{r}=""),"",IF(F{r}=0,IF(E{r}=0,0,1),(E{r}-F{r})/ABS(F{r})))')
            g.font, g.number_format = base, pct
            h = ws.cell(row=r, column=8, value=f'=IF(G{r}="","",IF(ABS(G{r})<=$B$4,"Yes","No"))')
            h.font = base
            ws.cell(row=r, column=9).fill = yellow
            ws.cell(row=r, column=9).font = blue
            ws.cell(row=r, column=10, value=WHERE.get(concept, "")).font = base
            ws.cell(row=r, column=11, value=src).font = base
            if rec.get("filing_url"):
                lc = ws.cell(row=r, column=12, value=f"{rec.get('form')} filed {rec.get('filed')}")
                lc.hyperlink, lc.font = rec["filing_url"], link
            ws.cell(row=r, column=13, value=note).font = base
            row_of[(concept, lab)] = r
            r += 1
    last = r - 1
    ws["B8"] = f"=COUNT(F12:F{last})"
    ws["B9"] = f'=COUNTIF(H12:H{last},"Yes")'

    widths = [30, 24, 8, 16, 14, 14, 11, 10, 26, 34, 44, 20, 50]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[ws.cell(row=hr, column=i).column_letter].width = w

    dv = DataValidation(type="decimal", allow_blank=True)
    dv.error, dv.errorTitle = "Type a number, as printed in the 10-K", "Number expected"
    ws.add_data_validation(dv)
    dv.add(f"F12:F{last}")

    # ---- Ratios sheet: rebuild ratios from the typed figures ----
    rs = wb.create_sheet("Ratios")
    rs["A1"] = "Ratios rebuilt in Excel from your 10-K figures, next to the tool's ratios"
    rs["A1"].font = title
    rs["A2"] = ("Fills in once every input for a year is typed on 'Hand check'. Definitions follow "
                "DECISIONS.md. Green cells link to 'Hand check'.")
    rs["A2"].font = base
    fl_in = 0 if any(spread["lines"]["finance_lease_liabilities"][l]["source"] == "included_in_debt"
                     for l in labels) else 1
    rs["A3"], rs["B3"] = "Add finance leases to debt? (1 = yes, 0 = already inside LTD)", fl_in
    rs["A3"].font, rs["B3"].font, rs["B3"].fill = bold, blue, yellow

    def H(concept, lab):
        return f"'Hand check'!$F${row_of[(concept, lab)]}"

    hdr = ["Item"]
    for lab in labels:
        hdr += [f"{lab} from 10-K", f"{lab} tool", f"{lab} diff"]
    for i, h in enumerate(hdr, 1):
        c = rs.cell(row=5, column=i, value=h)
        c.font, c.fill, c.alignment = bold, head_fill, wrap
    rs.column_dimensions["A"].width = 34
    for i in range(2, len(hdr) + 1):
        rs.column_dimensions[rs.cell(row=5, column=i).column_letter].width = 13

    def blank_guard(concepts, lab, expr):
        cond = ",".join(f'{H(c, lab)}=""' for c in concepts)
        return f'=IF(OR({cond}),"",{expr})'

    items = []  # (label, key, kind, builder(lab)->formula, tool getter)
    debt_parts = ["short_term_borrowings", "commercial_paper", "current_ltd", "noncurrent_ltd"]

    def f_ebitda(l):
        return blank_guard(["operating_income", "da"], l,
                           f"{H('operating_income', l)}+{H('da', l)}")

    def f_debt(l):
        parts = "+".join(H(c, l) for c in debt_parts)
        return blank_guard(debt_parts + ["finance_lease_liabilities"], l,
                           f"{parts}+$B$3*{H('finance_lease_liabilities', l)}")

    rows = {}
    rr = 6

    def put(label, key, kind, formula_fn, tool_fn):
        nonlocal rr
        rs.cell(row=rr, column=1, value=label).font = bold if kind == "ratio" else base
        col = 2
        for lab in labels:
            fx = formula_fn(lab)
            c = rs.cell(row=rr, column=col, value=fx)
            c.font = green
            c.number_format = mult if kind == "ratio" else num
            tv = tool_fn(lab)
            t = rs.cell(row=rr, column=col + 1, value=tv)
            t.font = blue
            t.number_format = mult if kind == "ratio" else num
            a = c.coordinate
            b = t.coordinate
            d = rs.cell(row=rr, column=col + 2,
                        value=f'=IF(OR({a}="",{b}=""),"",IF({a}=0,"",({b}-{a})/ABS({a})))')
            d.font, d.number_format = base, pct
            col += 3
        rows[key] = rr
        rr += 1

    unit_div = f"'Hand check'!$B$3"

    def tool_derived(k):
        return lambda l: (None if spread["derived"][l][k] is None
                          else f"={spread['derived'][l][k]}/{unit_div}")

    def tool_ratio(k):
        return lambda l: spread["ratios"][l][k]

    put("EBITDA", "ebitda", "amt", f_ebitda, tool_derived("ebitda"))
    put("EBITDAR", "ebitdar", "amt",
        lambda l: (f'=IF(OR({_c(rs, rows["ebitda"], labels, l)}="",{H("operating_lease_cost", l)}=""),"",'
                   f'{_c(rs, rows["ebitda"], labels, l)}+{H("operating_lease_cost", l)})'),
        tool_derived("ebitdar"))
    put("Total debt", "total_debt", "amt", f_debt, tool_derived("total_debt"))
    put("Net debt", "net_debt", "amt",
        lambda l: (f'=IF(OR({_c(rs, rows["total_debt"], labels, l)}="",{H("cash", l)}=""),"",'
                   f'{_c(rs, rows["total_debt"], labels, l)}-{H("cash", l)})'),
        tool_derived("net_debt"))
    rr += 1

    def ratio(numer, denom, positive_only=True):
        def fn(l):
            n, d = numer(l), denom(l)
            test = f"{d}<=0"
            return f'=IF(OR({n}="",{d}=""),"",IF({test},"n.m.",{n}/{d}))'
        return fn

    E = lambda l: _c(rs, rows["ebitda"], labels, l)
    ER = lambda l: _c(rs, rows["ebitdar"], labels, l)
    TD = lambda l: _c(rs, rows["total_debt"], labels, l)
    ND = lambda l: _c(rs, rows["net_debt"], labels, l)

    put("Debt / EBITDA", "debt_ebitda", "ratio", ratio(TD, E), tool_ratio("debt_ebitda"))
    put("Net debt / EBITDA", "net_debt_ebitda", "ratio", ratio(ND, E), tool_ratio("net_debt_ebitda"))
    put("(Debt + leases) / EBITDAR", "lease_adj_debt_ebitdar", "ratio",
        lambda l: (f'=IF(OR({TD(l)}="",{ER(l)}="",{H("operating_lease_liabilities", l)}=""),"",'
                   f'IF({ER(l)}<=0,"n.m.",({TD(l)}+{H("operating_lease_liabilities", l)})/{ER(l)}))'),
        tool_ratio("lease_adj_debt_ebitdar"))
    put("EBITDA / interest", "interest_coverage", "ratio",
        lambda l: (f'=IF(OR({E(l)}="",{H("interest_expense", l)}=""),"",'
                   f'IF({H("interest_expense", l)}<=0,"n.m.",{E(l)}/{H("interest_expense", l)}))'),
        tool_ratio("interest_coverage"))
    put("DSCR", "dscr", "ratio",
        lambda l: (f'=IF(OR({E(l)}="",{H("capex", l)}="",{H("cash_taxes", l)}="",'
                   f'{H("interest_expense", l)}="",{H("scheduled_principal", l)}=""),"",'
                   f'IF({H("interest_expense", l)}+{H("scheduled_principal", l)}<=0,"n.m.",'
                   f'({E(l)}-{H("capex", l)}-{H("cash_taxes", l)})/'
                   f'({H("interest_expense", l)}+{H("scheduled_principal", l)})))'),
        tool_ratio("dscr"))
    put("Current ratio", "current_ratio", "ratio",
        lambda l: (f'=IF(OR({H("current_assets", l)}="",{H("current_liabilities", l)}=""),"",'
                   f'IF({H("current_liabilities", l)}<=0,"n.m.",'
                   f'{H("current_assets", l)}/{H("current_liabilities", l)}))'),
        tool_ratio("current_ratio"))
    rs.freeze_panes = "B6"

    HANDCHECK_DIR.mkdir(parents=True, exist_ok=True)
    out = _path(ticker)
    wb.save(out)
    return out


def _c(ws, row, labels, lab):
    """Cell holding the 10-K-based value for `lab` in a Ratios-sheet row."""
    from openpyxl.utils import get_column_letter
    col = 2 + 3 * labels.index(lab)
    return f"{get_column_letter(col)}{row}"


def compare(ticker: str, target: float = 0.01) -> str:
    """Read typed 10-K values back and write a markdown result for the README."""
    from openpyxl import load_workbook

    wb = load_workbook(_path(ticker), data_only=True)
    ws = wb["Hand check"]
    unit = ws["B3"].value
    rows, misses = [], []
    for r in range(12, ws.max_row + 1):
        line, concept, year, tool, tenk = (ws.cell(row=r, column=c).value for c in (1, 2, 3, 4, 6))
        if concept is None or tenk is None or tenk == "":
            continue
        tool_u = tool / unit
        diff = 0.0 if tenk == 0 and tool_u == 0 else (
            1.0 if tenk == 0 else (tool_u - tenk) / abs(tenk))
        ok = abs(diff) <= target
        rows.append((line, year, tool_u, float(tenk), diff, ok, ws.cell(row=r, column=9).value))
        if not ok:
            misses.append(rows[-1])

    n, hit = len(rows), sum(1 for x in rows if x[5])
    unit_name = {1000: "$ thousands", 1_000_000: "$ millions"}.get(unit, f"units of ${unit:,}")
    out = [f"## {ticker} hand check", "",
           f"{hit} of {n} lines within {target:.0%} of the 10-K "
           f"({(hit / n if n else 0):.0%} match rate). Values in {unit_name}.", ""]
    out += ["| Line | Year | Tool | 10-K | Diff | Where |", "|---|---|---:|---:|---:|---|"]
    for line, year, t, k, d, ok, where in rows:
        flag = "" if ok else " ⚠"
        out.append(f"| {line} | {year} | {t:,.0f} | {k:,.0f} | {d:+.2%}{flag} | {where or ''} |")
    if misses:
        out += ["", "Lines outside the target need an explanation before the tool is trusted."]
    text = "\n".join(out) + "\n"
    (HANDCHECK_DIR / f"{ticker}_result.md").write_text(text)
    return text


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("make")
    m.add_argument("ticker")
    m.add_argument("--unit", type=int, required=True,
                   help="10-K reporting unit in dollars: 1000 (thousands) or 1000000 (millions)")
    m.add_argument("--periods", nargs="*", help="default: latest two fiscal years")
    c = sub.add_parser("compare")
    c.add_argument("ticker")
    args = ap.parse_args(argv)
    t = args.ticker.upper()
    if args.cmd == "make":
        print(make(t, args.unit, args.periods))
    else:
        print(compare(t))
    return 0


if __name__ == "__main__":
    sys.exit(main())
