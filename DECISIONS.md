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
- Thresholds flagged: leverage above 4.0x, interest coverage below 2.0x

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
