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

`build` writes two files per company to `outputs/spreads/`:

- `<TICKER>.json`: the spread, derived figures (EBITDA, debt), ratios, the reason for every n.m. ratio, and warnings
- `<TICKER>_log.csv`: one row per number with its XBRL tag, unit, filing accession number, filing date, period and a link to the filing

## Hand check

`handcheck/DVA_handcheck.xlsx` lists every spread line for the latest two years with the tool's value, its XBRL tag and a link to the filing. Type each figure from the 10-K into the yellow column; the sheet shows the difference against the 1% target, and a second sheet rebuilds the ratios in Excel from your figures so the Python ratio code is checked independently.

```bash
python -m creditmemo.handcheck make DVA --unit 1000     # DaVita reports in $ thousands
python -m creditmemo.handcheck compare DVA              # writes handcheck/DVA_result.md
```

## Layout

```
config/companies.json     tickers, CIKs, fiscal-year convention, facility, floating-rate share
config/tags.json          tag priority list per spread concept
config/overrides/         per-company tag overrides and hand-entered values (with sources)
creditmemo/edgar.py       download + cache
creditmemo/facts.py       one value per period (latest 10-K wins)
creditmemo/spread.py      tag mapping, fallbacks, proxy flags
creditmemo/ratios.py      ratio definitions (pure functions)
creditmemo/build.py       CLI: spreads, logs, console ratio table
creditmemo/handcheck.py   hand-check workbook and match-rate report
tests/                    worked examples and edge cases
```

## Results

To come: example memo, DaVita hand-check, ratio table, stress table, grade vs agency rating.
