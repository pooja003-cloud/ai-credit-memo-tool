# AI credit memo tool

Turns a public company's 10-K into a bank-style credit memo. Python builds the spread, the credit ratios, one stress case and a risk grade. Claude drafts an approve-or-decline memo, and a script proves every number in it came from Python.

**Python does every number, Claude only writes, and a script proves it.**

Status: step 1 of 5 (spread and ratios). Definitions and rules are in [DECISIONS.md](DECISIONS.md).

## Run it

```bash
pip install -r requirements.txt

# 1. Download SEC data once (cached in data/cache/)
export SEC_USER_AGENT="Your Name you@example.com"
python -m creditmemo.edgar DVA UNP KSS

# 2. Build spreads and ratios
python -m creditmemo.build

# 3. Tests
pytest
```

`build` writes, per company:

- `outputs/spreads/<TICKER>.json`: as-reported statements, standard spread, note items, ratios (with the reason for every n.m.), tie-outs and the cross-check
- `outputs/xbrl_facts/<TICKER>_log.csv`: the company-facts route, one row per number with its XBRL tag, filing and a link

## How the spread is built

1. **As reported.** `creditmemo/edgar.py` downloads the SEC's rendered statement pages for the latest two 10-Ks. `creditmemo/asreported.py` parses the income statement, balance sheet and cash flow statement exactly as printed: same lines, order and signs, with each line's XBRL tag. The prior 10-K supplies the third balance sheet.
2. **Standard bank spread.** `creditmemo/standard.py` maps every as-reported line into one fixed template (see DECISIONS.md). Each standard line lists the lines it came from; anything unmatched goes to a visible "other" line. Tie-outs check the arithmetic against each statement's own totals (39 checks per company; all pass for DVA, UNP and KSS).
3. **Ratios** run off the standard spread, with lease cost, total lease liabilities, next-year maturities and cash taxes taken from the notes (XBRL company facts).
4. **Cross-check.** The company-facts route (`creditmemo/spread.py`) builds the same items independently. Differences over 1% are printed and explained: DaVita D&A (+1%, the cash flow statement includes amortization the note tag leaves out) and Kohl's debt (+13–21%, the standard spread includes the revolver and sale-leaseback financing obligations).

## Hand check

`handcheck/DVA_handcheck.xlsx` has one tab per statement, laid out exactly as in DaVita's latest 10-K, the latest two years side by side. Type each figure as printed into the yellow cells; differences above 1% turn red, and the Summary tab shows the match rate per tab. A Notes tab covers the note items, and a Ratios tab rebuilds every ratio from your typed figures through the same line mapping as the standard spread.

**Result (DaVita, FY2024–FY2025, 2026-10-21): 220 of 220 statement lines match the 10-K exactly.** The first pass had six lines off by exactly 100 ($ thousands); they traced to two hand-typing slips (FY2024 non-controlling interests, FY2025 employee stock proceeds) that the sheet's subtotal formulas carried into four other lines. Both were rechecked against the 10-K and corrected; the tool was right in both cases. Every ratio rebuilt in Excel from the typed figures equals the tool's ratio. Notes tab still to do. Full table: [handcheck/DVA_result.md](handcheck/DVA_result.md).

```bash
python -m creditmemo.handcheck make DVA
python -m creditmemo.handcheck compare DVA      # writes handcheck/DVA_result.md
```

## Layout

```
config/companies.json     tickers, CIKs, fiscal-year convention, facility, floating-rate share
config/tags.json          tag priority list per spread concept
config/overrides/         per-company tag overrides and hand-entered values (with sources)
creditmemo/edgar.py       download + cache
creditmemo/facts.py       one value per period (latest 10-K wins)
creditmemo/asreported.py  layer 1: statements as printed, from the SEC statement pages
creditmemo/standard.py    layer 2: standard bank spread, tie-outs
creditmemo/spread.py      company-facts route: note items and cross-check
creditmemo/ratios.py      ratio definitions (pure functions)
creditmemo/build.py       CLI: builds outputs/spreads/<T>.json and outputs/xbrl_facts/
creditmemo/handcheck.py   hand-check workbook and match-rate report
tests/                    worked examples and edge cases
```

## Results

To come: example memo, DaVita hand-check, ratio table, stress table, grade vs agency rating.
