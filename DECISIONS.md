# Decisions

Fixed before coding, 2026-10-21. Change any of them here first, then in the code.

## Scope

| Question | Decision | Why |
|---|---|---|
| Companies | DaVita (DVA), Union Pacific (UNP), Kohl's (KSS) | Investment grade to stressed, fewest XBRL gaps. Code works for any ticker |
| Excluded | REITs, banks, insurers, captive finance arms | They don't fit one spread template |
| Drafting model | Claude via `claude -p` | Follows the placeholder format; outputs committed, so the demo needs no API key |
| Numbers in the memo | Placeholders only, e.g. `{{FY2025.net_debt_ebitda}}`, filled by a script | A wrong number can't reach the memo |
| Floating-rate debt share | Entered by hand per company with a 10-K Item 7A page citation | Not in XBRL; Claude never produces a number |
| Facility | Hypothetical $500M 5-year senior unsecured term loan per company | A memo approves a specific request |
| Recommendation | Claude makes the approve/decline call; it is the one judgment the LLM is allowed. It is then compared with the grade | Tests the model's judgment against a rule-based benchmark |
| Agency ratings | Fetched with source and date, stored unopened until grade thresholds are frozen | Otherwise the grade is fitted to the ratings |
| Demo | Export script writes `demo.json`; a static page reads it | Site is plain HTML/CSS/JS |

## Two layers (decided 2026-10-21)

1. **As reported.** Each company's income statement, balance sheet and cash flow statement exactly as in the 10-K: same line names, order and subtotals, parsed from the SEC's rendered statement pages (R files) for the latest two 10-Ks. Each line keeps its XBRL tag, filing and page.
2. **Standard bank spread.** One fixed template for every company, built only from Layer 1 lines. Each standard line lists the as-reported lines it came from. Anything not mapped goes to a visible "other" line in its section, so the totals tie. Tie-outs check that the standard totals equal the reported totals. Ratios run off this layer.

The company-facts route (`creditmemo/spread.py`) stays as an independent cross-check, plus the source for the note-level items (lease cost, lease liabilities, next-year maturities).

### Standard template

| Income statement | Balance sheet | Cash flow |
|---|---|---|
| Revenue | Cash and equivalents | Cash from operations **(tie)** |
| Operating costs excl. D&A | Receivables | of which D&A |
| D&A (from the cash flow statement) | Inventory | Capex |
| Unusual operating items (impairments, gains) | Other current assets | Acquisitions |
| Operating income **(tie)** | Total current assets **(tie)** | Other investing |
| Interest expense (the face-of-statement line) | PP&E, net | Cash from investing **(tie)** |
| Other non-operating items | Operating lease assets | Debt issued |
| Pre-tax income **(tie)** | Goodwill and intangibles | Debt repaid |
| Income tax | Other non-current assets | Dividends |
| Discontinued operations | Total assets **(tie)** | Share buybacks |
| Non-controlling interests | Short-term debt and current LTD | Other financing (incl. NCI distributions) |
| Net income to the company **(tie)** | Accounts payable | Cash from financing **(tie)** |
| EBITDA = operating income + D&A | Other current liabilities | FCF = CFO − capex |
| | Total current liabilities **(tie)** | |
| | Long-term debt (incl. finance leases if reported inside) | |
| | Operating lease liabilities | |
| | Other non-current liabilities | |
| | Non-controlling / redeemable interests | |
| | Shareholders' equity | |
| | Total liabilities and equity **(tie)** | |

Mapping rules that matter:
- D&A comes from the cash flow statement, so EBITDA catches D&A that the income statement folds into other costs.
- Debt includes every debt-like line on the balance sheet: revolver borrowings, current and long-term debt, finance leases and financing obligations from failed sale-leasebacks (Kohl's).
- Interest is the face-of-statement line. Non-operating lines are printed income-positive by some filers (DaVita, Union Pacific) and expense-positive by others (Kohl's); the sign is taken from the statement's own arithmetic, not guessed.
- Total operating lease liabilities come from the notes (company facts), because some balance sheets fold the current part into other liabilities (Union Pacific).

EBITDA is reported EBITDA: no add-backs. Unusual items are shown on their own line so a reader can see them, but they are not removed.

## Definitions

- **EBITDA** = operating income + D&A
- **Total debt** = short-term borrowings + commercial paper + current portion of LTD + LTD (noncurrent) + finance lease liabilities. If the debt tag already includes finance leases (`LongTermDebtAndCapitalLeaseObligations`, used by DaVita and Union Pacific), the separate finance lease line is not added again. This is detected from the tag name; `finance_leases_in_debt` in a company override overrules it.
- **Net debt** = total debt − cash and equivalents
- **Leverage** = debt / EBITDA and net debt / EBITDA
- **Lease-adjusted leverage** = (debt + operating lease liabilities) / EBITDAR, where EBITDAR = EBITDA + operating lease cost. Under ASC 842, rent is already deducted inside EBITDA, so adding lease debt without adding back rent overstates leverage.
- **Interest coverage** = EBITDA / interest expense. Interest expense is the line on the face of the income statement (DaVita's "Debt expense", which includes finance lease interest and financing costs), not the narrower debt-note figure
- **DSCR** = (EBITDA − capex − cash taxes) / (interest + scheduled principal). Scheduled principal = principal due in the next 12 months at year end (forward-looking), or the current portion of LTD if that isn't tagged.
- **Liquidity** = current ratio and cash on hand
- **Not meaningful (n.m.)**: leverage when EBITDA ≤ 0; any ratio whose denominator is ≤ 0. Negative coverage is kept, since it is a real, failing result.

## Stress case

- Stressed revenue = base revenue × 0.8
- Stressed EBITDA = stressed revenue × (base EBITDA margin − 3 percentage points)
- Extra interest = 2% × floating-rate share × total debt
- Capex, cash taxes, lease cost and scheduled principal held at base (conservative)
- Thresholds flagged: debt / EBITDA above 4.0x, interest coverage below 2.0x, DSCR below 1.0x (cash flow doesn't cover interest plus scheduled principal)
- Why the stress uses leverage without leases while the grade uses leverage with leases: the stress mimics a bank covenant (funded debt / EBITDA); the grade mimics agency practice (lease-adjusted). FY2025 stressed results are the same either way: DaVita 5.47x / 4.99x (breaks), Union Pacific 3.44x / 3.43x (holds), Kohl's 5.66x / 6.92x (breaks)

## Data rules

- Each fiscal-year value comes from the latest 10-K (or 10-K/A) that reports it. Flows must cover 340–380 days. Restated figures win.
- 3 years of income and cash flow. Balance sheets come from the same rule, so the third year's balance sheet comes from the prior 10-K when it is in the cache.
- Tag priority lists in `config/tags.json`; per-company overrides in `config/overrides/`.
- **Proxies are flagged, not just logged.** A proxy measures something slightly different: cash interest paid for interest expense, current tax expense for cash taxes, lease payments for lease cost, cash including restricted cash. They show as PROXY in the spread warnings and get a footnote in the demo.
- Hand-entered values must cite a source, or the build fails.
- Fiscal years come from all revenue tags combined. Companies switch tags (Union Pacific moved from `Revenues` to the ASC 606 tag after 2020).
- When two tags report the same period, the one from the newest 10-K wins; ties go to tag priority. Proxy tags are tried only when no real tag, component sum or fallback exists.
- Cash taxes: when no total is tagged, federal + state + foreign taxes paid are summed (new ASU 2023-09 disclosure; Union Pacific FY2025). Absolute values are used, because filers flip the sign of taxes paid between filings.
- A missing current portion of LTD counts as 0, and that zero carries into scheduled principal, flagged (Kohl's FY2023).
- Fiscal year labels follow the company. Kohl's year ending 31 Jan 2026 is FY2025.
- EDGAR: User-Agent with a contact (from `SEC_USER_AGENT`), at most 4 requests a second, every response cached.

## Floating-rate share (2026-10-21)

From each latest 10-K; quotes and pages are also in `config/companies.json`.

| Company | Share | Status | Source | Basis |
|---|---|---|---|---|
| DaVita | 3.6% | Confirmed | Note 12: debt table p. F-26, unhedged balance p. F-28, cap table p. F-29; Item 7A p. 69 | Term Loans A-2 and B-2 ($3.87B, SOFR + margin). Caps cover $3.5B in each year 2025–2028 and $1.0B in 2029, leaving $369M of $10.16B debt principal unhedged (3.6%). Item 7A agrees: +100bp cuts net income by about $5.3M after caps |
| Union Pacific | 0% | Draft | Item 7 Other Matters (Item 7A refers there), p. 39 | "At both December 31, 2025, and 2024, we did not have variable-rate debt." |
| Kohl's | 0% | Draft | Item 7A, p. 37 | All long-term debt fixed; revolver SOFR-based but undrawn at year end. Rating-linked coupon step-ups on $425M notes are a repricing risk for the memo, not floating exposure |

Correction: the first draft used 38.1% for DaVita, saying most caps "expire 2025–2027". That misread the cap table: total notional coverage is $3.5B through 2028 (p. F-29), and MD&A says the caps shield exposure "through 2029". The unhedged share is the accurate input. What it leaves out goes in the memo as risks:
- the caps only pay above their strikes: weighted average SOFR strike 4.32% (2026), 4.46% (2027), 4.43% (2028), 4.50% (2029), with 25bp step-ups at end-2026 and end-2027;
- cover falls to $1.0B in 2029, inside the requested 5-year loan.

## Pro forma (2026-10-21)

The latest fiscal year as if the requested facility were already drawn (`creditmemo/proforma.py`):
- debt + facility amount; interest + amount x rate, where the rate is a cited 10-K fact (DaVita: 5.51% weighted average effective rate on all debt, Debt note p. F-30);
- EBITDA, cash, capex, cash taxes, leases and next-year principal unchanged (proceeds spent, bullet repayment);
- the stress case is rerun on pro forma inputs with the company's floating share applied to pro forma debt.
Shown next to reported figures in the memo; not graded. The grade stays on reported figures.

## Memo rules

- Numbers only as placeholders, filled by `creditmemo/memo_check.py` from the spread (`{{FY2025.debt_ebitda}}`, `{{stress.dscr}}`, `{{growth.FY2025.revenue}}`, ...).
- Every sentence carries a placeholder or a citation to the extracted 10-K text: `[1A ¶12]` = Item 1A, paragraph 12 in `outputs/sections/<TICKER>.json`. Rendered as "10-K Item 1A ¶12, p. 24" with a link to the filing.
- Quotations of five words or more must appear verbatim in the cited paragraph.
- The draft fails on any hand-typed number (years, FY labels, Item/Note numbers, 10-K and instrument names like Term Loan A-2 are allowed), unknown placeholder, bad citation, uncited sentence, misquote, or a missing "Recommendation: Approve/Decline" line.
- The recommendation is the one judgment Claude makes; it is compared with the grade afterwards.

## Risk grade (FROZEN 2026-10-21, signed off before any agency rating was looked up)

1 = best, 10 = worst. Latest fiscal year, base case. Rules in `config/grade.json`, code in `creditmemo/grade.py`.

| Score | (Debt + leases) / EBITDAR | EBITDA / interest | DSCR | Current ratio |
|---|---|---|---|---|
| 1 | ≤ 1.0x | ≥ 15x | ≥ 4.0x | ≥ 2.5x |
| 2 | ≤ 1.5x | ≥ 12x | ≥ 3.25x | ≥ 2.0x |
| 3 | ≤ 2.0x | ≥ 9x | ≥ 2.75x | ≥ 1.75x |
| 4 | ≤ 2.5x | ≥ 7x | ≥ 2.25x | ≥ 1.5x |
| 5 | ≤ 3.0x | ≥ 5.5x | ≥ 1.75x | ≥ 1.25x |
| 6 | ≤ 3.5x | ≥ 4.5x | ≥ 1.5x | ≥ 1.1x |
| 7 | ≤ 4.0x | ≥ 3.5x | ≥ 1.25x | ≥ 1.0x |
| 8 | ≤ 5.0x | ≥ 2.5x | ≥ 1.1x | ≥ 0.8x |
| 9 | ≤ 6.0x | ≥ 1.5x | ≥ 1.0x | ≥ 0.6x |
| 10 | > 6.0x or n.m. | < 1.5x | < 1.0x or n.m. | < 0.6x |
| **Weight** | **40%** | **30%** | **20%** | **10%** |

- Base grade = weighted average of the four scores, rounded half up. No interest at all scores 1 on coverage.
- Stress overlay: one notch worse per stress threshold broken (leverage > 4.0x, coverage < 2.0x, DSCR < 1.0x), at most two.
- Why these choices: leverage is lease-adjusted so retailers and railroads compare fairly; leverage and coverage carry 70% because they drive agency ratings; DSCR adds the maturity wall; the current ratio gets little weight because some strong credits (railroads) run below 1.0x by design. Scale, business mix and management are left out on purpose: the grade is purely financial, and that is a known reason it will differ from agency ratings.
- Agency comparison map (used only after grading): 1 = AAA to AA, 2 = AA-/A+, 3 = A, 4 = A-/BBB+, 5 = BBB, 6 = BBB-, 7 = BB+/BB, 8 = BB-/B+, 9 = B/B-, 10 = CCC and below. Grade 6 and better is investment grade.
- Frozen: `config/grade.sha256` pins the file, and a test fails if it changes.
- Known limit: I (Claude) have rough memories of these companies' ratings, so the bands were set from generic conventions without running them on the three companies. The grades are computed only after sign-off.
