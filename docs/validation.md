# Validation: why the numbers can be trusted

Back to the [README](../README.md).

## The memo checker and human review

Every memo passed the checker on its second attempt; the first attempts' errors went back to Claude (see the Draft attempts column in [docs/memos.md](memos.md)).

**What the checker proves, and what it doesn't.** It proves every number came from Python and every citation points to a real 10-K paragraph (and quotes match). It does not prove the reasoning is right. A sentence in the stress section had the cap logic backwards (caps protect only when SOFR is *at or above* the strike); it passed every check and was caught in human review. Credit judgment still needs a reviewer.

Human review of the Union Pacific and Kohl's memos (logged in `memos/<T>_result.json`): 22 citations read against the 10-K; one misused citation fixed (Union Pacific [1A ¶11] is about locomotive suppliers, not the railroad's barriers to entry), one sharpened. In two of the six review edits across the project, the reviewer typed a number by hand and the checker rejected it.

## The spread: tie-outs and cross-check

1. **As reported.** `creditmemo/edgar.py` downloads the SEC's rendered statement pages for the latest two 10-Ks. `creditmemo/asreported.py` parses the income statement, balance sheet and cash flow statement exactly as printed: same lines, order and signs, with each line's XBRL tag. The prior 10-K supplies the third balance sheet.
2. **Standard bank spread.** `creditmemo/standard.py` maps every as-reported line into one fixed template (see DECISIONS.md). Each standard line lists the lines it came from; anything unmatched goes to a visible "other" line. Tie-outs check the arithmetic against each statement's own totals (39 checks per company; all pass for DVA, UNP and KSS).
3. **Ratios** run off the standard spread, with lease cost, total lease liabilities, next-year maturities and cash taxes taken from the notes (XBRL company facts).
4. **Cross-check.** The company-facts route (`creditmemo/spread.py`) builds the same items independently. Differences over 1% are printed and explained: DaVita D&A (+1%, the cash flow statement includes amortization the note tag leaves out) and Kohl's debt (+13–21%, the standard spread includes the revolver and sale-leaseback financing obligations).

## Hand check against the 10-K

`handcheck/DVA_handcheck.xlsx` has one tab per statement, laid out exactly as in DaVita's latest 10-K, the latest two years side by side. Type each figure as printed into the yellow cells; differences above 1% turn red, and the Summary tab shows the match rate per tab. A Notes tab covers the note items, and a Ratios tab rebuilds every ratio from your typed figures through the same line mapping as the standard spread.

**Result (DaVita, FY2024–FY2025, 2026-10-21): 228 of 228 lines match the 10-K exactly** (220 statement lines and 8 note items). The first pass had six lines off by exactly 100 ($ thousands); they traced to two hand-typing slips (FY2024 non-controlling interests, FY2025 employee stock proceeds) that the sheet's subtotal formulas carried into four other lines. Both were rechecked against the 10-K and corrected; the tool was right in both cases. Every ratio rebuilt in Excel from the typed figures equals the tool's ratio. Lease-adjusted leverage and DSCR rebuilt from the typed figures also equal the tool's. Full table: [handcheck/DVA_result.md](../handcheck/DVA_result.md).

```bash
python -m creditmemo.handcheck make DVA
python -m creditmemo.handcheck compare DVA      # writes handcheck/DVA_result.md
```

## Grade vs agency ratings

**Grade vs agency ratings: 2 matches, 1 one-notch gap, explained.** DaVita and Kohl's match the agencies (Kohl's is one notch better than Moody's alone); Union Pacific is one notch harsher than all three, because its weighted score is exactly 4.50, on the boundary between grades 4 and 5, and rounds up.

The 1-to-10 grade was frozen (`config/grade.sha256`) before any rating was looked up. Ratings, sources and dates: `config/agency_ratings.json`; table: [outputs/benchmark.md](../outputs/benchmark.md).

| Company | Internal grade | S&P | Moody's | Fitch | Gap |
|---|---|---|---|---|---|
| Union Pacific | **5** (score 4.50) | A- (4) ⚠ unconfirmed | A3 (4) | A- (4) | +1, tool harsher |
| DaVita | **7** (base 6 + 1 stress notch) | BB (7) | Ba2 (7), last action 2024 | — | 0 |
| Kohl's | **8** (base 6 + 2 stress notches) | B+ stable (8) | B2 positive (9) | BB- (8) | 0 vs S&P and Fitch, -1 vs Moody's |

Why they differ:
- **Union Pacific is one notch harsher.** The weighted score is exactly 4.50, on the 4/5 boundary, and half rounds up (`grade.py` rounds to six decimals first, so floating-point noise can't push an exact 4.50 down; a test pins this). The current ratio (0.91x, score 8) costs it most: railroads run working capital below 1.0x by design. The grade is purely financial, so it gives no credit for scale or for being one of two western US Class I railroads, which the agencies weigh heavily. Not tuned after the fact; that would defeat the freeze.
- **DaVita matches, but only after the stress notch.** On base-case ratios alone it grades 6 (BBB- equivalent), one notch better than the agencies. Stressed leverage (5.47x) adds the notch. The agencies also weigh what the ratios miss: reliance on government reimbursement, and buybacks that have pushed shareholders' equity negative.
- **Kohl's matches S&P and Fitch, but its base-case ratios alone also say 6.** The two stress notches do the work. The real gap is trend: revenue fell from $17.5B to $15.5B in two years, and a one-year ratio snapshot can't see a shrinking business. Moody's B2 is one notch below. Since the 10-K, both agencies' outlooks have improved (Moody's to positive in April 2026, S&P to stable in June 2026); the ratings themselves haven't moved, so the comparison doesn't change.

## Limits

- **Agency benchmark.** What it can and can't show: three companies only show direction, not accuracy. It is partly circular, because the agencies lean on the same leverage and coverage ratios. Each rating records its last agency action and, separately, whether it was confirmed on the agency's own site; only Union Pacific's Fitch rating is confirmed that way so far, and Union Pacific's S&P rating rests on a 2025 news report. The useful finding is the pattern: base-case ratios flatter the two weaker credits, and the stress overlay is what brings them in line.
- **Pro forma rate.** The coupon on each company's most recent senior unsecured issue in its 10-K (DaVita 6.75% [DEBT ¶63], Union Pacific 5.10%, Kohl's 10.00%), not the average cost of existing debt, which understates what new borrowing costs. Kohl's 2025 notes are secured, so its pro forma interest is a lower bound. **Bond coupons are a stand-in for term-loan pricing**, which a 10-K doesn't disclose; a bank term loan would usually price off SOFR plus a margin. Rule and table in DECISIONS.md.
- **Checker scope.** It proves numbers and citations, not reasoning; credit judgment still needs a reviewer (see [The memo checker and human review](#the-memo-checker-and-human-review)).
