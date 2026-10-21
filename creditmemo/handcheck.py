"""Hand-check workbook: compare the tool's spread with figures typed from the 10-K.

    python -m creditmemo.handcheck make DVA --unit 1000      # writes handcheck/DVA_handcheck.xlsx
    python -m creditmemo.handcheck compare DVA               # reads it back, writes handcheck/DVA_result.md

`--unit` is the unit the 10-K reports in (DaVita: dollars in thousands -> 1000;
Union Pacific and Kohl's: millions -> 1000000). You type numbers exactly as the
10-K prints them; the sheet converts the tool's values to the same unit.

Tabs:
  Summary            unit, target, instructions, match rate per tab and overall
  Income statement   one tab per statement, lines in statement order,
  Cash flow          years side by side: tool | 10-K (type here) | diff | OK
  Balance sheet
  Notes              lines that come from the notes (leases, debt maturities)
  Ratios             every ratio rebuilt in Excel from your typed figures,
                     next to the tool's ratio, so the Python ratio code is
                     checked separately from the XBRL mapping
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import ROOT, SPREAD_DIR

HANDCHECK_DIR = ROOT / "handcheck"

# Tab -> lines in the order they appear on the statement, with where to look.
SECTIONS = [
    ("Income statement", [
        ("revenue", "Total revenues"),
        ("operating_income", "Operating income"),
        ("interest_expense", "Interest / debt expense"),
        ("pretax_income", "Income before income taxes"),
        ("net_income", "Net income attributable to the company"),
    ]),
    ("Cash flow", [
        ("cfo", "Net cash provided by operating activities"),
        ("da", "Depreciation and amortization (operating section)"),
        ("capex", "Additions of property and equipment (investing section)"),
        ("cash_taxes", "Income taxes paid (supplemental disclosure or tax note)"),
    ]),
    ("Balance sheet", [
        ("cash", "Cash and cash equivalents"),
        ("current_assets", "Total current assets"),
        ("total_assets", "Total assets"),
        ("short_term_borrowings", "Short-term borrowings (type 0 if no such line)"),
        ("commercial_paper", "Commercial paper (type 0 if none)"),
        ("current_ltd", "Current portion of long-term debt"),
        ("current_liabilities", "Total current liabilities"),
        ("noncurrent_ltd", "Long-term debt, less current portion"),
        ("equity", "Total shareholders' equity (company share)"),
    ]),
    ("Notes", [
        ("operating_lease_cost", "Leases note: operating lease cost"),
        ("operating_lease_liabilities", "Leases note: total operating lease liabilities"),
        ("finance_lease_liabilities", "Leases note: total finance lease liabilities"),
        ("scheduled_principal", "Debt note: maturities table, first year"),
    ]),
]

FIRST_ROW = 6          # first data row on a statement tab
COLS_PER_YEAR = 4      # tool | 10-K | diff | OK
YEAR_START_COL = 3     # column C


def _path(ticker: str) -> Path:
    return HANDCHECK_DIR / f"{ticker}_handcheck.xlsx"


def _col(n: int) -> str:
    from openpyxl.utils import get_column_letter
    return get_column_letter(n)


def make(ticker: str, unit: int, periods=None) -> Path:
    from openpyxl import Workbook
    from openpyxl.comments import Comment
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.worksheet.datavalidation import DataValidation

    spread = json.loads((SPREAD_DIR / f"{ticker}.json").read_text())
    labels = periods or [p["label"] for p in spread["periods"]][-2:]
    covered = {c for _, lines in SECTIONS for c, _ in lines}
    missing = set(spread["lines"]) - covered
    if missing:
        raise ValueError(f"spread lines not placed on any tab: {sorted(missing)}")

    F = "Arial"
    base = Font(name=F, size=10)
    bold = Font(name=F, size=10, bold=True)
    title = Font(name=F, size=14, bold=True)
    blue = Font(name=F, size=10, color="0000FF")
    green = Font(name=F, size=10, color="008000")
    grey = Font(name=F, size=9, color="666666")
    link = Font(name=F, size=10, color="0563C1", underline="single")
    head_fill = PatternFill("solid", fgColor="DDE3EA")
    year_fill = PatternFill("solid", fgColor="EEF1F5")
    yellow = PatternFill("solid", fgColor="FFFF00")
    red_fill = PatternFill("solid", fgColor="F8CBAD")
    thin = Side(style="thin", color="B7B7B7")
    wrap = Alignment(wrap_text=True, vertical="top")
    center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    num = '#,##0;(#,##0);"-"'
    pct = '0.00%;(0.00%);0.00%'
    mult = '0.00"x";(0.00"x");"-"'

    wb = Workbook()

    # ---------------- Summary ----------------
    sm = wb.active
    sm.title = "Summary"
    sm["A1"] = f"{spread['name']} ({ticker}): hand check of the tool's spread"
    sm["A1"].font = title
    sm["A3"], sm["B3"] = "Unit you type in ($ per unit)", unit
    sm["B3"].font, sm["B3"].fill, sm["B3"].number_format = blue, yellow, "#,##0"
    sm["C3"] = "1,000 if the 10-K says 'in thousands'; 1,000,000 if 'in millions'"
    sm["A4"], sm["B4"] = "Match target", 0.01
    sm["B4"].font, sm["B4"].number_format = blue, "0.0%"
    sm["A5"] = "Years"
    sm["B5"] = ", ".join(labels)
    sm["A7"] = "How to use"
    sm["B7"] = ("Work through the tabs with the 10-K open at that statement. Type each figure exactly "
                "as printed into the yellow cells, and the page or note into 'Page / note'. Leave a "
                "cell blank until you've checked it. Differences above the target turn red.")
    ex_lab = labels[-1]
    ex_val = spread["lines"]["revenue"][ex_lab]["value"] / unit
    sm["A8"] = "Example"
    sm["B8"] = (f"Income statement tab, Revenue, {ex_lab}: if the 10-K prints total revenues as "
                f"{ex_val:,.0f}, type {ex_val:.0f} in the yellow cell and something like "
                "'Consolidated Statements of Income, p. 72' under 'Page / note'.")
    for c in ("A3", "A4", "A5", "A7", "A8"):
        sm[c].font = bold
        sm[c].alignment = Alignment(vertical="top")
    for c in ("B3", "B4", "B5"):
        sm[c].alignment = Alignment(horizontal="left", vertical="top")
    for c in ("C3", "B7", "B8"):
        sm[c].font = base
        sm[c].alignment = wrap
    sm["B5"].font = base
    sm.merge_cells("C3:F3")
    sm.merge_cells("B7:F7")
    sm.merge_cells("B8:F8")
    sm.row_dimensions[7].height = 45
    sm.row_dimensions[8].height = 45
    sm.column_dimensions["A"].width = 28
    for c in "BCDEF":
        sm.column_dimensions[c].width = 16
    sm.column_dimensions["C"].width = 30

    for i, h in enumerate(["Tab", "Lines checked", "Within target", "Match rate"], 1):
        c = sm.cell(row=10, column=i, value=h)
        c.font, c.fill = bold, head_fill
    summary_rows = []

    # ---------------- Statement tabs ----------------
    where_cell = {}   # (concept, label) -> "'Tab'!$X$n" of the typed 10-K value
    for tab_i, (tab, lines) in enumerate(SECTIONS):
        ws = wb.create_sheet(tab)
        ws["A1"] = f"{tab}: {spread['name']}"
        ws["A1"].font = title
        ws["A2"] = "Yellow = type the 10-K figure as printed. Blue = the tool's value. Red = outside the target."
        ws["A2"].font = grey

        # header rows 4 (year band) and 5 (column names)
        ws.cell(row=5, column=1, value="Line")
        ws.cell(row=5, column=2, value="Where to look")
        for yi, lab in enumerate(labels):
            c0 = YEAR_START_COL + yi * COLS_PER_YEAR
            ws.merge_cells(start_row=4, start_column=c0, end_row=4, end_column=c0 + COLS_PER_YEAR - 1)
            band = ws.cell(row=4, column=c0, value=lab)
            band.font, band.fill, band.alignment = bold, year_fill, center
            for k, h in enumerate(["Tool", "10-K", "Diff", "OK"]):
                ws.cell(row=5, column=c0 + k, value=h)
        tail = YEAR_START_COL + len(labels) * COLS_PER_YEAR
        extra = ["Page / note", "XBRL tag / source", "Filing", "Tool note", "concept"]
        for k, h in enumerate(extra):
            ws.cell(row=5, column=tail + k, value=h)
        for cell in ws[5]:
            if cell.value is not None:
                cell.font, cell.fill, cell.alignment = bold, head_fill, center
                cell.border = Border(bottom=thin)
        ws.freeze_panes = ws.cell(row=FIRST_ROW, column=YEAR_START_COL)

        r = FIRST_ROW
        for concept, hint in lines:
            by_p = spread["lines"][concept]
            ws.cell(row=r, column=1, value=spread["concept_labels"][concept]).font = bold
            ws.cell(row=r, column=2, value=hint).font = base
            notes, srcs = [], []
            for yi, lab in enumerate(labels):
                rec = by_p[lab]
                c0 = YEAR_START_COL + yi * COLS_PER_YEAR
                T, K, D, O = (_col(c0 + k) for k in range(4))
                raw = rec.get("reported_value", rec["value"])
                t = ws.cell(row=r, column=c0,
                            value=None if raw is None else f"={raw}/Summary!$B$3")
                t.font, t.number_format = blue, num
                t.comment = Comment(f"outputs/spreads/{ticker}.json, {lab}: "
                                    f"{raw if raw is not None else 'missing'} dollars "
                                    f"({rec['source']})", "creditmemo")
                k = ws.cell(row=r, column=c0 + 1)
                k.fill, k.font, k.number_format = yellow, blue, num
                d = ws.cell(row=r, column=c0 + 2,
                            value=f'=IF(OR({K}{r}="",{T}{r}=""),"",'
                                  f'IF({K}{r}=0,IF({T}{r}=0,0,1),({T}{r}-{K}{r})/ABS({K}{r})))')
                d.font, d.number_format = base, pct
                o = ws.cell(row=r, column=c0 + 3,
                            value=f'=IF({D}{r}="","",IF(ABS({D}{r})<=Summary!$B$4,1,0))')
                o.font, o.number_format, o.alignment = base, '"✓";;"✗"', center
                ws.conditional_formatting.add(
                    f"{D}{r}:{O}{r}",
                    FormulaRule(formula=[f'AND(${D}{r}<>"",ABS(${D}{r})>Summary!$B$4)'], fill=red_fill))
                where_cell[(concept, lab)] = f"'{tab}'!${K}${r}"

                src = rec.get("tag") or rec["source"]
                if rec["source"] == "manual":
                    src = f"manual: {rec.get('manual_source')}"
                elif rec["source"] == "assumed_zero":
                    src = "not tagged (counted as 0)"
                elif rec["source"] == "missing":
                    src = "missing"
                srcs.append(src)
                note = rec.get("note") or ""
                if rec["source"] == "included_in_debt":
                    note = "Already inside long-term debt; the tool does not add it again."
                if rec.get("proxy"):
                    note = "PROXY. " + note
                if note:
                    notes.append(note)

            uniq = list(dict.fromkeys(srcs))
            src_text = uniq[0] if len(uniq) == 1 else "; ".join(f"{l}: {s}" for l, s in zip(labels, srcs))
            pg = ws.cell(row=r, column=tail)
            pg.fill, pg.font = yellow, blue
            ws.cell(row=r, column=tail + 1, value=src_text).font = base
            latest = by_p[labels[-1]]
            if latest.get("filing_url"):
                lc = ws.cell(row=r, column=tail + 2, value=f"{latest.get('form')} filed {latest.get('filed')}")
                lc.hyperlink, lc.font = latest["filing_url"], link
            ws.cell(row=r, column=tail + 3, value=" ".join(dict.fromkeys(notes))).font = base
            ws.cell(row=r, column=tail + 4, value=concept).font = grey  # read by compare()
            for cc in range(1, tail + 4):
                ws.cell(row=r, column=cc).border = Border(bottom=Side(style="hair", color="D9D9D9"))
            r += 1
        last = r - 1

        widths = {1: 30, 2: 40}
        for yi in range(len(labels)):
            c0 = YEAR_START_COL + yi * COLS_PER_YEAR
            widths.update({c0: 13, c0 + 1: 13, c0 + 2: 9, c0 + 3: 5})
        widths.update({tail: 26, tail + 1: 42, tail + 2: 20, tail + 3: 50, tail + 4: 22})
        for cnum, w in widths.items():
            ws.column_dimensions[_col(cnum)].width = w
        ws.column_dimensions[_col(tail + 4)].hidden = True

        dv = DataValidation(type="decimal", allow_blank=True)
        dv.error, dv.errorTitle = "Type a number, as printed in the 10-K", "Number expected"
        ws.add_data_validation(dv)
        for yi in range(len(labels)):
            K = _col(YEAR_START_COL + yi * COLS_PER_YEAR + 1)
            dv.add(f"{K}{FIRST_ROW}:{K}{last}")

        # summary row for this tab
        k_cols = [_col(YEAR_START_COL + yi * COLS_PER_YEAR + 1) for yi in range(len(labels))]
        o_cols = [_col(YEAR_START_COL + yi * COLS_PER_YEAR + 3) for yi in range(len(labels))]
        sr = 11 + tab_i
        sm.cell(row=sr, column=1, value=tab).font = base
        sm.cell(row=sr, column=2, value="=" + "+".join(
            f"COUNT('{tab}'!{k}{FIRST_ROW}:{k}{last})" for k in k_cols)).font = green
        sm.cell(row=sr, column=3, value="=" + "+".join(
            f"SUM('{tab}'!{o}{FIRST_ROW}:{o}{last})" for o in o_cols)).font = green
        sm.cell(row=sr, column=4, value=f'=IF(B{sr}=0,"",C{sr}/B{sr})').number_format = "0.0%"
        summary_rows.append(sr)

    tr = summary_rows[-1] + 1
    sm.cell(row=tr, column=1, value="All tabs").font = bold
    sm.cell(row=tr, column=2, value=f"=SUM(B{summary_rows[0]}:B{summary_rows[-1]})").font = bold
    sm.cell(row=tr, column=3, value=f"=SUM(C{summary_rows[0]}:C{summary_rows[-1]})").font = bold
    c = sm.cell(row=tr, column=4, value=f'=IF(B{tr}=0,"",C{tr}/B{tr})')
    c.font, c.number_format = bold, "0.0%"
    for rr in range(11, tr + 1):
        sm.cell(row=rr, column=4).font = bold if rr == tr else base
        sm.cell(row=rr, column=1).border = sm.cell(row=rr, column=4).border = Border(bottom=thin)

    # ---------------- Ratios ----------------
    rs = wb.create_sheet("Ratios")
    rs["A1"] = "Ratios rebuilt in Excel from your 10-K figures, next to the tool's ratios"
    rs["A1"].font = title
    rs["A2"] = ("A year fills in once all its inputs are typed on the statement tabs. Definitions "
                "follow DECISIONS.md. Green = linked from the statement tabs.")
    rs["A2"].font = grey
    fl_in = 0 if any(spread["lines"]["finance_lease_liabilities"][l]["source"] == "included_in_debt"
                     for l in labels) else 1
    rs["A3"], rs["B3"] = "Add finance leases to debt? (1 = yes, 0 = already inside LTD)", fl_in
    rs["A3"].font, rs["B3"].font, rs["B3"].fill = bold, blue, yellow

    def H(concept, lab):
        return where_cell[(concept, lab)]

    for yi, lab in enumerate(labels):
        c0 = 2 + yi * 3
        rs.merge_cells(start_row=4, start_column=c0, end_row=4, end_column=c0 + 2)
        band = rs.cell(row=4, column=c0, value=lab)
        band.font, band.fill, band.alignment = bold, year_fill, center
        for k, h in enumerate(["From 10-K", "Tool", "Diff"]):
            cell = rs.cell(row=5, column=c0 + k, value=h)
            cell.font, cell.fill, cell.alignment = bold, head_fill, center
    rs.cell(row=5, column=1, value="Item").font = bold
    rs.cell(row=5, column=1).fill = head_fill
    rs.column_dimensions["A"].width = 32
    for i in range(2, 2 + 3 * len(labels)):
        rs.column_dimensions[_col(i)].width = 13
    rs.freeze_panes = "B6"

    rows = {}
    state = {"r": 6}

    def cell_for(key, lab):
        return f"{_col(2 + 3 * labels.index(lab))}{rows[key]}"

    def put(label, key, kind, formula_fn, tool_fn):
        r = state["r"]
        rs.cell(row=r, column=1, value=label).font = bold if kind == "ratio" else base
        for yi, lab in enumerate(labels):
            c0 = 2 + yi * 3
            fx = rs.cell(row=r, column=c0, value=formula_fn(lab))
            fx.font, fx.number_format = green, mult if kind == "ratio" else num
            t = rs.cell(row=r, column=c0 + 1, value=tool_fn(lab))
            t.font, t.number_format = blue, mult if kind == "ratio" else num
            a, b = fx.coordinate, t.coordinate
            d = rs.cell(row=r, column=c0 + 2,
                        value=f'=IF(OR({a}="",{b}="",{a}="n.m."),"",IF({a}=0,"",({b}-{a})/ABS({a})))')
            d.font, d.number_format = base, pct
        rows[key] = r
        state["r"] += 1

    def need(cells, expr):
        return f'=IF(OR({",".join(f"{c}=" + chr(34) * 2 for c in cells)}),"",{expr})'

    def tool_amt(k):
        return lambda l: (None if spread["derived"][l][k] is None
                          else f"={spread['derived'][l][k]}/Summary!$B$3")

    def tool_ratio(k):
        return lambda l: spread["ratios"][l][k]

    debt_parts = ["short_term_borrowings", "commercial_paper", "current_ltd", "noncurrent_ltd"]
    put("EBITDA", "ebitda", "amt",
        lambda l: need([H("operating_income", l), H("da", l)],
                       f"{H('operating_income', l)}+{H('da', l)}"),
        tool_amt("ebitda"))
    put("EBITDAR", "ebitdar", "amt",
        lambda l: need([cell_for("ebitda", l), H("operating_lease_cost", l)],
                       f"{cell_for('ebitda', l)}+{H('operating_lease_cost', l)}"),
        tool_amt("ebitdar"))
    put("Total debt", "total_debt", "amt",
        lambda l: need([H(c, l) for c in debt_parts + ["finance_lease_liabilities"]],
                       "+".join(H(c, l) for c in debt_parts)
                       + f"+$B$3*{H('finance_lease_liabilities', l)}"),
        tool_amt("total_debt"))
    put("Net debt", "net_debt", "amt",
        lambda l: need([cell_for("total_debt", l), H("cash", l)],
                       f"{cell_for('total_debt', l)}-{H('cash', l)}"),
        tool_amt("net_debt"))
    state["r"] += 1

    def ratio(num_cells, numer, denom):
        return lambda l: need(num_cells(l), f'IF({denom(l)}<=0,"n.m.",({numer(l)})/({denom(l)}))')

    E = lambda l: cell_for("ebitda", l)
    ER = lambda l: cell_for("ebitdar", l)
    TD = lambda l: cell_for("total_debt", l)
    ND = lambda l: cell_for("net_debt", l)
    put("Debt / EBITDA", "debt_ebitda", "ratio",
        ratio(lambda l: [TD(l), E(l)], TD, E), tool_ratio("debt_ebitda"))
    put("Net debt / EBITDA", "net_debt_ebitda", "ratio",
        ratio(lambda l: [ND(l), E(l)], ND, E), tool_ratio("net_debt_ebitda"))
    put("(Debt + leases) / EBITDAR", "lease_adj_debt_ebitdar", "ratio",
        ratio(lambda l: [TD(l), ER(l), H("operating_lease_liabilities", l)],
              lambda l: f"{TD(l)}+{H('operating_lease_liabilities', l)}", ER),
        tool_ratio("lease_adj_debt_ebitdar"))
    put("EBITDA / interest", "interest_coverage", "ratio",
        ratio(lambda l: [E(l), H("interest_expense", l)], E, lambda l: H("interest_expense", l)),
        tool_ratio("interest_coverage"))
    put("DSCR", "dscr", "ratio",
        ratio(lambda l: [E(l), H("capex", l), H("cash_taxes", l), H("interest_expense", l),
                         H("scheduled_principal", l)],
              lambda l: f"{E(l)}-{H('capex', l)}-{H('cash_taxes', l)}",
              lambda l: f"{H('interest_expense', l)}+{H('scheduled_principal', l)}"),
        tool_ratio("dscr"))
    put("Current ratio", "current_ratio", "ratio",
        ratio(lambda l: [H("current_assets", l), H("current_liabilities", l)],
              lambda l: H("current_assets", l), lambda l: H("current_liabilities", l)),
        tool_ratio("current_ratio"))

    for sheet in wb.worksheets:   # print each tab on one page width, landscape
        sheet.page_setup.orientation = "landscape"
        sheet.sheet_properties.pageSetUpPr.fitToPage = True
        sheet.page_setup.fitToWidth = 1
        sheet.page_setup.fitToHeight = 0

    HANDCHECK_DIR.mkdir(parents=True, exist_ok=True)
    out = _path(ticker)
    wb.save(out)
    return out


def compare(ticker: str, target: float = 0.01) -> str:
    """Read typed 10-K values back and write a markdown result for the README.

    Recomputes the differences in Python from the raw typed values, so it
    doesn't depend on Excel having recalculated the workbook.
    """
    from openpyxl import load_workbook

    wb = load_workbook(_path(ticker), data_only=False)
    spread = json.loads((SPREAD_DIR / f"{ticker}.json").read_text())
    unit = wb["Summary"]["B3"].value
    rows = []
    for tab, _ in SECTIONS:
        ws = wb[tab]
        labels = []
        c = YEAR_START_COL
        while ws.cell(row=4, column=c).value:
            labels.append(ws.cell(row=4, column=c).value)
            c += COLS_PER_YEAR
        tail = YEAR_START_COL + len(labels) * COLS_PER_YEAR
        for r in range(FIRST_ROW, ws.max_row + 1):
            concept = ws.cell(row=r, column=tail + 4).value
            if not concept:
                continue
            page = ws.cell(row=r, column=tail).value
            for yi, lab in enumerate(labels):
                tenk = ws.cell(row=r, column=YEAR_START_COL + yi * COLS_PER_YEAR + 1).value
                if tenk is None or tenk == "":
                    continue
                rec = spread["lines"][concept][lab]
                raw = rec.get("reported_value", rec["value"])
                tool = None if raw is None else raw / unit
                tenk = float(tenk)
                if tool is None:
                    diff = None
                elif tenk == 0:
                    diff = 0.0 if tool == 0 else 1.0
                else:
                    diff = (tool - tenk) / abs(tenk)
                ok = diff is not None and abs(diff) <= target
                rows.append((tab, spread["concept_labels"][concept], lab, tool, tenk, diff, ok, page))

    n, hit = len(rows), sum(1 for x in rows if x[6])
    unit_name = {1000: "$ thousands", 1_000_000: "$ millions"}.get(unit, f"units of ${unit:,}")
    out = [f"## {ticker} hand check", "",
           f"**{hit} of {n} lines within {target:.0%} of the 10-K "
           f"({(hit / n if n else 0):.0%} match rate).** Values in {unit_name}.", ""]
    for tab, _ in SECTIONS:
        sub = [x for x in rows if x[0] == tab]
        if not sub:
            continue
        out += [f"### {tab}", "", "| Line | Year | Tool | 10-K | Diff | Page / note |",
                "|---|---|---:|---:|---:|---|"]
        for _, line, year, t, k, d, ok, page in sub:
            ts = "missing" if t is None else f"{t:,.0f}"
            ds = "n/a" if d is None else f"{d:+.2%}"
            out.append(f"| {line} | {year} | {ts} | {k:,.0f} | {ds}{'' if ok else ' ⚠'} | {page or ''} |")
        out.append("")
    if hit < n:
        out += ["Lines marked ⚠ are outside the target and need an explanation."]
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
    print(make(t, args.unit, args.periods) if args.cmd == "make" else compare(t))
    return 0


if __name__ == "__main__":
    sys.exit(main())
