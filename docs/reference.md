# Reference: running it and code layout

Back to the [README](../README.md).

## Run it

```bash
pip install -r requirements.txt

# 1. Download SEC data once (cached in data/cache/)
export SEC_USER_AGENT="Your Name you@example.com"
python -m creditmemo.edgar DVA UNP KSS

# 2. Build spreads and ratios
python -m creditmemo.build

# 3. Draft, check and render a memo (needs Claude Code: claude -p)
python -m creditmemo.draft DVA

# 4. Refresh the README tables and the benchmark
python -m creditmemo.report
python -m creditmemo.benchmark

# 5. Tests
pytest
```

`build` writes, per company:

- `outputs/spreads/<TICKER>.json`: as-reported statements, standard spread, note items, ratios (with the reason for every n.m.), tie-outs and the cross-check
- `outputs/xbrl_facts/<TICKER>_log.csv`: the company-facts route, one row per number with its XBRL tag, filing and a link

Drafting needs Claude Code (`claude -p`) on your machine. The committed memos in `memos/` don't: they are already rendered, and `python -m creditmemo.memo_check memos/DVA_draft.md` re-checks and re-renders one without calling Claude.

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
creditmemo/sections.py    10-K text sections as numbered paragraphs for citations
creditmemo/stress.py      stress case and threshold flags
creditmemo/proforma.py    pro forma for the requested facility
creditmemo/grade.py       1-to-10 grade (rules frozen in config/grade.json)
creditmemo/benchmark.py   grade vs agency ratings
creditmemo/draft.py       prompt, claude -p, check-and-revise loop
creditmemo/memo_check.py  placeholder renderer and memo checker
creditmemo/report.py      README tables
memos/                    prompts, drafts, check reports and rendered memos
tests/                    worked examples and edge cases
```
