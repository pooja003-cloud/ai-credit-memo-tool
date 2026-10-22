# AI credit memo tool

Turns a public company's 10-K into a bank-style credit memo. Python builds the spread, the credit ratios, one stress case and a risk grade. Claude drafts an approve-or-decline memo, and a script proves every number in it came from Python.

**Python does every number, Claude only writes, and a script proves it.**

Definitions and rules are in [DECISIONS.md](DECISIONS.md).

## Results

| Company | Grade | Recommendation | Draft attempts | Agrees with grade? | Notable |
|---|---|---|---|---|---|
| [DaVita](memos/DVA_memo.md) | 7 | Approve with conditions | 2 (7 errors, then pass) | Yes | Stressed leverage likely breaches DaVita's own 5.00x covenant [DEBT ¶58] |
| [Union Pacific](memos/UNP_memo.md) | 5 | Approve with conditions | 2 (5 errors, then pass) | Yes; argues the grade understates standalone quality (structural working-capital deficit) | ~$20B debt-funded Norfolk Southern acquisition is the main risk; requires combined projections and a re-grade at closing |
| [Kohl's](memos/KSS_memo.md) | 8 | Decline | 2 (7 errors, then pass) | Yes | FY2025 EBITDA "recovery" rests on a one-off $129M settlement gain; unsecured lender behind secured debt; stressed pro forma DSCR below 1.0x |

**Grade vs agency ratings: 2 matches, 1 one-notch gap, explained.** DaVita and Kohl's match the agencies (Kohl's is one notch better than Moody's alone); Union Pacific is one notch harsher than all three, because its weighted score is exactly 4.50, on the boundary between grades 4 and 5, and rounds up. Details under [Tables](#tables).

Example memo: [DaVita](memos/DVA_memo.md). Recommendation: **Approve with conditions**. Internal grade 7 (S&P BB, Moody's Ba2).

## How it stays honest

Every memo passed the checker on its second attempt; the first attempts' errors went back to Claude (see the Draft attempts column above).

**What the checker proves, and what it doesn't.** It proves every number came from Python and every citation points to a real 10-K paragraph (and quotes match). It does not prove the reasoning is right. A sentence in the stress section had the cap logic backwards (caps protect only when SOFR is *at or above* the strike); it passed every check and was caught in human review. Credit judgment still needs a reviewer.

Human review of the Union Pacific and Kohl's memos (logged in `memos/<T>_result.json`): 22 citations read against the 10-K; one misused citation fixed (Union Pacific [1A ¶11] is about locomotive suppliers, not the railroad's barriers to entry), one sharpened. In two of the six review edits across the project, the reviewer typed a number by hand and the checker rejected it.

### The DaVita memo, step by step

How it was made (`python -m creditmemo.draft DVA`):
- Claude (`claude -p`) got a fact sheet of placeholder names with their values, two analyst points on the interest-rate caps, and 1,052 numbered 10-K paragraphs. It wrote placeholders only.
- **Attempt 1 failed the checker with 7 errors**: six sentences with no placeholder or citation, and one stray number ("Section 8"). The errors went back to Claude; **attempt 2 passed** (94 placeholders, 46 citations, 0 errors). Every prompt, draft and check report is in `memos/`.
- Review after the pass: 21 citations read against the full 10-K paragraphs, and all support their sentence. Two wording edits, both re-checked: the stress notch was described in the wrong direction, and "roughly a third" became "more than a third" (the 10-K says about 36%). The first version of one edit typed "4.0x" by hand, and the checker rejected it. Edits are logged in `memos/DVA_result.json`.
- Recommendation vs grade: consistent. Grade 7 is sub-investment-grade but serviceable; the conditions target what the stress test flags (a leverage covenant set between base and stressed debt / EBITDA, no buybacks from proceeds, matching subsidiary guarantees, hedging past 2028). Claude also spotted that stressed leverage would likely breach DaVita's own 5.00x credit-agreement covenant [DEBT ¶58].
- Second review round (all re-checked, logged in `memos/DVA_result.json`): summary box with grade, recommendation and agency ratings; the covenant step-down to 4.50x after 2028 inside the tenor; NCI puts of $1.4B due in 2026 against $676M of cash, with the undrawn $1.5B revolver as mitigant; EBITDA excluding the FY2024 ownership gain, which turns the FY2025 decline into 2.0% growth; an NCI risk; sign-safe `{{abs:...}}` amounts. 10-K figures that aren't in the spread (covenant levels, puts, revolver, caps) are typed into `config/companies.json` with their 10-K citation, like the floating-rate share, so the no-typed-numbers rule still holds.
- Third review round: a pro forma layer (`creditmemo/proforma.py`) adds the $500M loan: debt / EBITDA 3.72x to 3.90x, just under the 4.00x level above which the credit agreement's restrictions apply; stressed 5.73x. The grade stays on reported figures.
- Known weakness, now addressed: the every-sentence-cited rule pushed Claude to attach decorative citations to opinions. Opinions in the Recommendation section may now carry `[judgment]` instead, and the checker rejects `[judgment]` anywhere else.

### The spread: tie-outs and cross-check

1. **As reported.** `creditmemo/edgar.py` downloads the SEC's rendered statement pages for the latest two 10-Ks. `creditmemo/asreported.py` parses the income statement, balance sheet and cash flow statement exactly as printed: same lines, order and signs, with each line's XBRL tag. The prior 10-K supplies the third balance sheet.
2. **Standard bank spread.** `creditmemo/standard.py` maps every as-reported line into one fixed template (see DECISIONS.md). Each standard line lists the lines it came from; anything unmatched goes to a visible "other" line. Tie-outs check the arithmetic against each statement's own totals (39 checks per company; all pass for DVA, UNP and KSS).
3. **Ratios** run off the standard spread, with lease cost, total lease liabilities, next-year maturities and cash taxes taken from the notes (XBRL company facts).
4. **Cross-check.** The company-facts route (`creditmemo/spread.py`) builds the same items independently. Differences over 1% are printed and explained: DaVita D&A (+1%, the cash flow statement includes amortization the note tag leaves out) and Kohl's debt (+13–21%, the standard spread includes the revolver and sale-leaseback financing obligations).

## Hand check

`handcheck/DVA_handcheck.xlsx` has one tab per statement, laid out exactly as in DaVita's latest 10-K, the latest two years side by side. Type each figure as printed into the yellow cells; differences above 1% turn red, and the Summary tab shows the match rate per tab. A Notes tab covers the note items, and a Ratios tab rebuilds every ratio from your typed figures through the same line mapping as the standard spread.

**Result (DaVita, FY2024–FY2025, 2026-10-21): 228 of 228 lines match the 10-K exactly** (220 statement lines and 8 note items). The first pass had six lines off by exactly 100 ($ thousands); they traced to two hand-typing slips (FY2024 non-controlling interests, FY2025 employee stock proceeds) that the sheet's subtotal formulas carried into four other lines. Both were rechecked against the 10-K and corrected; the tool was right in both cases. Every ratio rebuilt in Excel from the typed figures equals the tool's ratio. Lease-adjusted leverage and DSCR rebuilt from the typed figures also equal the tool's. Full table: [handcheck/DVA_result.md](handcheck/DVA_result.md).

```bash
python -m creditmemo.handcheck make DVA
python -m creditmemo.handcheck compare DVA      # writes handcheck/DVA_result.md
```

## Tables

<!-- tables:start (generated by python -m creditmemo.report) -->
### Credit ratios, latest fiscal year

| Company | Year | Debt / EBITDA | (Debt + leases) / EBITDAR | Net debt / EBITDA | EBITDA / interest | DSCR | Current ratio | Grade |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| DaVita Inc. | FY2025 | 3.72x | 3.72x | 3.48x | 4.76x | 2.91x | 1.29x | 7 |
| Union Pacific Corporation | FY2025 | 2.58x | 2.60x | 2.48x | 9.40x | 2.70x | 0.91x | 5 |
| Kohl's Corporation | FY2025 | 2.94x | 4.16x | 2.43x | 4.60x | 3.13x | 1.46x | 8 |

Note: Kohl's Corporation interest coverage is 4.43x excluding the $11 million debt-repurchase gain booked in interest expense [DEBT ¶63], as used in its memo; the table uses reported interest. The grade is unchanged (8).

### Leverage with and without leases, three years

Lease-adjusted leverage pairs lease liabilities with EBITDAR (EBITDA + operating lease cost), because rent is already deducted inside EBITDA. The gap between the two columns is the lease effect.

| Company | FY2023 without / with leases | FY2024 without / with leases | FY2025 without / with leases |
|---|---:|---:|---:|
| DaVita Inc. | 3.57x / 3.66x | 3.36x / 3.44x | 3.72x / 3.72x |
| Union Pacific Corporation | 2.86x / 2.90x | 2.58x / 2.61x | 2.58x / 2.60x |
| Kohl's Corporation | 3.06x / 4.25x | 3.70x / 4.93x | 2.94x / 4.16x |

Note: DaVita Inc. FY2025 shows almost the same leverage with and without leases (3.724x vs 3.720x). This is not a bug: adding leases moves the ratio only when lease liabilities / lease cost differs from debt / EBITDA, and for DaVita Inc. it is 3.70x against 3.72x, so adding both to the ratio barely changes it.

### Stress test

Revenue -20%, EBITDA margin -300bp, +200bp on the floating-rate share of debt; capex, cash taxes, leases and principal held. Pro forma adds the requested $500M loan at the company's most recent senior unsecured coupon (Kohl's: a secured coupon, so its pro forma interest is a lower bound and its coverage and DSCR are at most the figures shown).

| Company | Floating share | Stressed debt / EBITDA | Stressed EBITDA / interest | Stressed DSCR | Thresholds broken | Pro forma stressed debt / EBITDA | Pro forma stressed coverage | Pro forma stressed DSCR |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| DaVita Inc. | 3.6% | 5.47x | 3.20x | 1.62x | Debt / EBITDA above 4.0x | 5.73x | 3.02x | 1.54x |
| Union Pacific Corporation | 0.0% | 3.44x | 7.07x | 1.62x | none | 3.49x | 6.94x | 1.61x |
| Kohl's Corporation | 0.0% | 5.66x | 2.38x | 0.92x | Debt / EBITDA above 4.0x; DSCR below 1.0x | 6.39x | 2.03x (at most) | 0.78x (at most) |
<!-- tables:end -->

### Grade vs agency ratings

The 1-to-10 grade was frozen (`config/grade.sha256`) before any rating was looked up. Ratings, sources and dates: `config/agency_ratings.json`; table: [outputs/benchmark.md](outputs/benchmark.md).

| Company | Internal grade | S&P | Moody's | Fitch | Gap |
|---|---|---|---|---|---|
| Union Pacific | **5** (score 4.50) | A- (4) ⚠ unconfirmed | A3 (4) | A- (4) | +1, tool harsher |
| DaVita | **7** (base 6 + 1 stress notch) | BB (7) | Ba2 (7), last action 2024 | — | 0 |
| Kohl's | **8** (base 6 + 2 stress notches) | B+ stable (8) | B2 positive (9) | BB- (8) | 0 vs S&P and Fitch, -1 vs Moody's |

Why they differ:
- **Union Pacific is one notch harsher.** The weighted score is exactly 4.50, on the 4/5 boundary, and half rounds up (`grade.py` rounds to six decimals first, so floating-point noise can't push an exact 4.50 down; a test pins this). The current ratio (0.91x, score 8) costs it most: railroads run working capital below 1.0x by design. The grade is purely financial, so it gives no credit for scale or for being one of two western US Class I railroads, which the agencies weigh heavily. Not tuned after the fact; that would defeat the freeze.
- **DaVita matches, but only after the stress notch.** On base-case ratios alone it grades 6 (BBB- equivalent), one notch better than the agencies. Stressed leverage (5.47x) adds the notch. The agencies also weigh what the ratios miss: reliance on government reimbursement, and buybacks that have pushed shareholders' equity negative.
- **Kohl's matches S&P and Fitch, but its base-case ratios alone also say 6.** The two stress notches do the work. The real gap is trend: revenue fell from $17.5B to $15.5B in two years, and a one-year ratio snapshot can't see a shrinking business. Moody's B2 is one notch below. Since the 10-K, both agencies' outlooks have improved (Moody's to positive in April 2026, S&P to stable in June 2026); the ratings themselves haven't moved, so the comparison doesn't change.

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

## Limits

- **Agency benchmark.** What it can and can't show: three companies only show direction, not accuracy. It is partly circular, because the agencies lean on the same leverage and coverage ratios. Each rating records its last agency action and, separately, whether it was confirmed on the agency's own site; only Union Pacific's Fitch rating is confirmed that way so far, and Union Pacific's S&P rating rests on a 2025 news report. The useful finding is the pattern: base-case ratios flatter the two weaker credits, and the stress overlay is what brings them in line.
- **Pro forma rate.** The coupon on each company's most recent senior unsecured issue in its 10-K (DaVita 6.75% [DEBT ¶63], Union Pacific 5.10%, Kohl's 10.00%), not the average cost of existing debt, which understates what new borrowing costs. Kohl's 2025 notes are secured, so its pro forma interest is a lower bound. **Bond coupons are a stand-in for term-loan pricing**, which a 10-K doesn't disclose; a bank term loan would usually price off SOFR plus a margin. Rule and table in DECISIONS.md.
- **Checker scope.** It proves numbers and citations, not reasoning; credit judgment still needs a reviewer (see [How it stays honest](#how-it-stays-honest)).
