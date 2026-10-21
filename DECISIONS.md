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

## Definitions

- **EBITDA** = operating income + D&A
- **Total debt** = short-term borrowings + commercial paper + current portion of LTD + LTD (noncurrent) + finance lease liabilities. If a company's debt tags already include finance leases, `finance_leases_in_debt: true` in its override stops double counting.
- **Net debt** = total debt − cash and equivalents
- **Leverage** = debt / EBITDA and net debt / EBITDA
- **Lease-adjusted leverage** = (debt + operating lease liabilities) / EBITDAR, where EBITDAR = EBITDA + operating lease cost. Under ASC 842, rent is already deducted inside EBITDA, so adding lease debt without adding back rent overstates leverage.
- **Interest coverage** = EBITDA / interest expense
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
- Fiscal year labels follow the company. Kohl's year ending 31 Jan 2026 is FY2025.
- EDGAR: User-Agent with a contact (from `SEC_USER_AGENT`), at most 4 requests a second, every response cached.
