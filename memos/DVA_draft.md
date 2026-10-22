# Credit memo: DaVita Inc.

| Summary | |
|---|---|
| Internal grade | {{grade.grade}} on the 1-to-10 scale (base {{grade.base_grade}}, worsened by {{grade.stress_notches}} notch under stress) |
| Recommendation | Approve with conditions |
| Agency ratings | S&P {{rating.sp}}; Moody's {{rating.moodys}} |
| Key reason: cash flow | Operating cash flow of {{FY2025.cashflow.cfo}} and DSCR of {{FY2025.dscr}}, still {{stress.dscr}} under stress |
| Key reason: leverage | Debt to EBITDA of {{FY2025.debt_ebitda}} ({{proforma.debt_ebitda}} with this loan) rises to {{stress.debt_ebitda}} under stress, probably above the credit agreement's {{fact.covenant_max_leverage}} covenant, which uses a different EBITDA definition [DEBT ¶58] |
| Key reason: financial policy | Buybacks of {{abs:FY2025.cashflow.buybacks}} exceeded free cash flow and turned equity negative; the conditions restrict them |

## 1. Request

DaVita Inc. requests a {{facility.type}} of {{facility.amount_usd}} with a {{facility.tenor_years}}-year tenor, for {{facility.purpose}}. The request is hypothetical and tests whether the borrower can carry {{facility.amount_usd}} of extra debt over {{facility.tenor_years}} years. The facility would be unsecured. The senior secured credit facilities are secured by substantially all assets of DaVita and certain domestic subsidiaries, and they rank ahead of all unsecured debt [DEBT ¶58]. Our loan would therefore rank with the senior notes, which are guaranteed by the same domestic subsidiaries that guarantee the secured facilities [DEBT ¶63, ¶64]. A {{facility.tenor_years}}-year loan would mature after the 2030 maturity wall, alongside Term Loan B-2 [DEBT ¶13, ¶47].

## 2. Borrower overview

DaVita is a leading U.S. dialysis provider, and U.S. dialysis is its largest line of business [1 ¶10]. U.S. dialysis produced the large majority of consolidated revenue in 2025 [1 ¶52]. Management estimates it serves more than a third of U.S. dialysis patients [7 ¶59]. Government programs, mainly Medicare and Medicare Advantage, pay for most U.S. dialysis revenue [1 ¶53, ¶57]. Commercial payors pay higher rates and generate nearly all of the company's profits [1 ¶75]. The company also has a growing international business, integrated kidney care, and other ancillary services [1 ¶11, ¶12]. Revenue reached {{FY2025.income.revenue}} in FY2025.

## 3. Financial analysis

| Ratio | FY2023 | FY2024 | FY2025 |
|---|---|---|---|
| Debt / EBITDA | {{FY2023.debt_ebitda}} | {{FY2024.debt_ebitda}} | {{FY2025.debt_ebitda}} |
| Net debt / EBITDA | {{FY2023.net_debt_ebitda}} | {{FY2024.net_debt_ebitda}} | {{FY2025.net_debt_ebitda}} |
| Lease-adj. debt / EBITDAR | {{FY2023.lease_adj_debt_ebitdar}} | {{FY2024.lease_adj_debt_ebitdar}} | {{FY2025.lease_adj_debt_ebitdar}} |
| Interest coverage | {{FY2023.interest_coverage}} | {{FY2024.interest_coverage}} | {{FY2025.interest_coverage}} |
| DSCR | {{FY2023.dscr}} | {{FY2024.dscr}} | {{FY2025.dscr}} |
| Current ratio | {{FY2023.current_ratio}} | {{FY2024.current_ratio}} | {{FY2025.current_ratio}} |
| EBITDA margin | {{FY2023.ebitda_margin}} | {{FY2024.ebitda_margin}} | {{FY2025.ebitda_margin}} |

**Earnings.** Revenue grew {{growth.FY2024.revenue}} and then {{growth.FY2025.revenue}}. EBITDA rose {{growth.FY2024.ebitda}} in FY2024 and then fell {{abs:growth.FY2025.ebitda}} in FY2025, so the margin slipped to {{FY2025.ebitda_margin}}. FY2024 was helped by a non-cash gain on changes in ownership interests of {{abs:FY2024.income.unusual_operating}} [7-LIQ ¶116]. Excluding that gain, FY2024 EBITDA was {{FY2024.ebitda_ex_unusual}}, and FY2025 EBITDA grew {{growth.FY2025.ebitda_ex_unusual}}, so the FY2025 decline disappears on an underlying basis. FY2025 was hurt by charges from the cybersecurity incident [7 ¶111]. U.S. treatment volumes fell in 2025 because of higher mortality and a severe flu season [7 ¶89]. Patient care costs per treatment grew faster than revenue per treatment [7 ¶95, ¶108].

**Leverage and coverage.** Total debt rose {{growth.FY2025.total_debt}} to {{FY2025.balance.total_debt}}, and debt to EBITDA went up to {{FY2025.debt_ebitda}}. Interest expense climbed over two years, from {{FY2023.income.interest_expense}} in FY2023 to {{FY2024.income.interest_expense}} in FY2024 and {{FY2025.income.interest_expense}} in FY2025. Management attributes the rise to new senior notes and the expiry of older, cheaper rate caps [7 ¶183]. As a result, interest coverage fell to {{FY2025.interest_coverage}}. Debt service coverage rose to {{FY2025.dscr}} from {{FY2024.dscr}}, mainly because principal due in the next year fell to {{FY2025.scheduled_principal}} from {{FY2024.scheduled_principal}}.

**Cash flow and capital allocation.** Operating cash flow fell {{abs:growth.FY2025.cfo}} to {{FY2025.cashflow.cfo}}, and free cash flow was {{FY2025.cashflow.fcf}}. The company's own definition of free cash flow also deducts distributions to noncontrolling interests, so it is lower [7-LIQ ¶86]. Buybacks of {{abs:FY2025.cashflow.buybacks}} were larger than free cash flow, and net debt rose to {{FY2025.net_debt}}. Buybacks continued after year-end [7-LIQ ¶78]. Book equity was {{FY2023.balance.equity}} in FY2023 and turned negative at {{FY2025.balance.equity}}.

**Liquidity.** Cash was {{FY2025.balance.cash}} and the current ratio was {{FY2025.current_ratio}}. Redeemable noncontrolling interests of {{FY2025.balance.redeemable_nci}} carry put provisions that partners can exercise, and {{fact.nci_puts_2026}} of that sits in the 2026 column of the contractual obligations table, against year-end cash of {{FY2025.balance.cash}} [7 ¶352, ¶358]. The mitigant is the {{fact.revolver_undrawn}} revolving credit facility, which was fully undrawn at year-end [7-LIQ ¶81].

**Pro forma for this facility.** Pricing the {{proforma.amount}} loan at {{proforma.rate}}, the coupon on DaVita's most recent senior unsecured notes, issued in 2025, adds {{proforma.added_interest}} of annual interest [DEBT ¶63]. That is above the {{fact.avg_debt_rate}} weighted average effective rate on existing debt, because new borrowing costs more than the old average [DEBT ¶114]. On FY2025 figures, total debt would be {{proforma.total_debt}}, debt to EBITDA would rise to {{proforma.debt_ebitda}} from {{FY2025.debt_ebitda}}, and interest coverage would ease to {{proforma.interest_coverage}} from {{FY2025.interest_coverage}}. That leaves little room below {{fact.covenant_restriction_leverage}}, the level above which the credit agreement's restrictions apply, although the agreement measures leverage on its own EBITDA definition [DEBT ¶58]. The pro forma assumes the proceeds are spent rather than held as cash, EBITDA is unchanged and the loan is repaid at maturity; the grade of {{grade.grade}} stays on reported figures.

## 4. Strengths

- **Market position and predictable revenue.** DaVita has scale and a leading market share [7 ¶59]. Medicare provides a relatively predictable, recurring revenue stream [1 ¶65]. CMS finalized a reimbursement increase for 2026 [7 ¶64].
- **Solid, though declining, cash generation.** Operating cash flow was {{FY2025.cashflow.cfo}}, down {{abs:growth.FY2025.cfo}} on FY2024, capex was {{abs:FY2025.cashflow.capex}}, and DSCR was {{FY2025.dscr}}.
- **Limited unhedged floating-rate exposure.** Only {{fact.unhedged_floating_debt}}, or {{floating_rate_share}} of debt, is floating and not covered by interest rate caps [DEBT ¶61].
- **Light near-term maturities.** Scheduled maturities are small each year until 2030 [DEBT ¶43, ¶44, ¶45, ¶46].
- **Stated leverage target.** Management says leverage stayed within its target range throughout 2025 [7 ¶32].

## 5. Risks and mitigants

- **Commercial payor concentration.** Profits depend on commercial patients, and those rates face downward pressure [1A ¶58, ¶65]. *Mitigant:* no single commercial payor accounts for more than a small share of revenue [1 ¶76].
- **Debt-funded shareholder returns.** The company may take on more debt to fund repurchases [1A ¶164]. Equity is now {{FY2025.balance.equity}}. *Mitigant:* the covenant package proposed in the Recommendation section.
- **Earnings shared with partners.** Net income attributable to noncontrolling interests was {{FY2025.income.nci}} in FY2025, earnings that belong to joint-venture partners and reach DaVita's creditors only after distributions to those partners. Our DSCR of {{FY2025.dscr}} does not deduct those distributions, so it overstates the cash available to service DaVita's own debt.
- **Structural ranking.** Secured lenders have a claim on substantially all assets ahead of us [DEBT ¶58]. *Mitigant:* we would require the same subsidiary guarantees as the senior notes [DEBT ¶63].
- **Rate caps only pay above their strikes.** The caps pay only when SOFR is at or above the strike [DEBT ¶61, ¶96]. The weighted average SOFR strike rises from {{fact.cap_strike_2026}} in 2026 to {{fact.cap_strike_2029}} in 2029, and some caps step up their strikes at end-2026 and end-2027 [DEBT ¶96, ¶97, ¶98, ¶99, ¶100]. Below the strike, the company bears rate movements on the hedged debt as well as on the {{floating_rate_share}} that is unhedged.
- **Cap coverage falls in 2029.** Cap notional drops from {{fact.cap_coverage_2025_2028}} in each year from 2025 to 2028 to {{fact.cap_coverage_2029}} in 2029, inside our {{facility.tenor_years}}-year tenor [DEBT ¶95]. In the same window the credit agreement's maximum leverage covenant steps down from {{fact.covenant_max_leverage}} to {{fact.covenant_max_leverage_after_2028}} after 2028, so covenant headroom tightens just as hedging thins [DEBT ¶58]. Management says the caps shield exposure through 2029 [7 ¶32]. However, coverage in that year is much thinner, and nothing is hedged after it. *Mitigant:* management's sensitivity shows only a modest net income effect from a parallel rate rise [7A ¶5].
- **Refinancing concentration.** Most debt matures in 2030 and beyond [DEBT ¶47, ¶48]. Term Loan A-2 comes due early if the 2030 notes are still outstanding [DEBT ¶34].
- **Volume, regulatory and cyber risk.** New drugs that slow kidney disease could reduce demand for dialysis [1A ¶161]. Extensive regulation brings legal exposure [1A ¶49, ¶55]. The 2025 cyber incident disrupted operations [7 ¶111].

## 6. Stress test

The scenario applies a revenue shock of {{stress.revenue_shock}} and a margin shock of {{stress.margin_shock}}. Under these shocks, the margin falls from {{stress.base_margin}} to {{stress.stressed_margin}} and EBITDA drops to {{stress.ebitda}}. It also adds a rate shock of {{stress.rate_shock}}, applied only to the unhedged share of debt ({{floating_rate_share}}), which adds {{stress.extra_interest}} of interest. The capped term loans get no extra cost in this scenario, which is too generous: a cap pays only when SOFR is at or above its strike, so capped debt still bears any rise in SOFR up to the strike [DEBT ¶61, ¶96]. The extra interest of {{stress.extra_interest}} is therefore a lower bound.

Stressed results:

- Debt to EBITDA: {{stress.debt_ebitda}}
- Net debt to EBITDA: {{stress.net_debt_ebitda}}
- Lease-adjusted leverage: {{stress.lease_adj_debt_ebitdar}}
- Interest coverage: {{stress.interest_coverage}}
- DSCR: {{stress.dscr}}
- Current ratio: {{stress.current_ratio}}

**Pro forma stress.** With the new loan added, stressed debt to EBITDA would reach {{proforma.stress.debt_ebitda}}, stressed interest coverage {{proforma.stress.interest_coverage}} and stressed DSCR {{proforma.stress.dscr}}. Leverage breaks the threshold by a wider margin than the reported {{stress.debt_ebitda}}, while coverage and DSCR stay above their thresholds.

One threshold breaks: debt to EBITDA rises to {{stress.debt_ebitda}}, above our leverage limit. Stressed leverage of {{stress.debt_ebitda}} would probably also exceed the credit agreement's {{fact.covenant_max_leverage}} maximum leverage covenant, though that agreement defines EBITDA differently [DEBT ¶58]. Coverage and DSCR stay adequate. Under stress the real risk is leverage, while interest coverage of {{stress.interest_coverage}} still supports cash debt service.

## 7. Risk grade

The internal grade is {{grade.grade}} on the 1-to-10 scale. It starts from a base grade of {{grade.base_grade}}, which comes from a weighted score of {{grade.weighted_score}}. The stress result then makes it worse by {{grade.stress_notches}} notch, because stressed debt to EBITDA of {{stress.debt_ebitda}} breaks the leverage threshold.

Component scores:

- Lease-adjusted leverage: {{grade.score.lease_adj_debt_ebitdar}}
- Interest coverage: {{grade.score.interest_coverage}}
- DSCR: {{grade.score.dscr}}
- Current ratio: {{grade.score.current_ratio}}

Leverage, scored {{grade.score.lease_adj_debt_ebitdar}}, is the weakest part of the grade, and DSCR, scored {{grade.score.dscr}}, is the strongest.

## 8. Recommendation

I recommend approval, with conditions. The grade of {{grade.grade}} reflects real leverage risk, but the cash-flow base is durable. The company generated {{FY2025.cashflow.cfo}} of operating cash flow, and DSCR stays at {{stress.dscr}} even under stress.

The main concern is financial policy, not capacity: buybacks of {{abs:FY2025.cashflow.buybacks}} have pushed equity to {{FY2025.balance.equity}}. Our unsecured loan also ranks behind the secured lenders [DEBT ¶58]. Rate risk is small today but rises late in our tenor as cap coverage thins [DEBT ¶95, ¶96]. The conditions below address each of these points [judgment].

Recommendation: Approve with conditions:
- (a) Proceeds may not fund share repurchases, and the use of the {{facility.amount_usd}} must be reported.
- (b) The loan must carry the same subsidiary guarantees as the senior notes [DEBT ¶63].
- (c) A maximum debt to EBITDA covenant must be tested quarterly, set with headroom above pro forma leverage of {{proforma.debt_ebitda}} and below stressed leverage of {{stress.debt_ebitda}}, and no looser than the credit agreement's own covenant, which steps down to {{fact.covenant_max_leverage_after_2028}} after 2028 [DEBT ¶58]. Because the credit agreement calculates leverage on its own definition of EBITDA, our covenant should be defined on reported debt to EBITDA as measured in this memo, not by reference to theirs [DEBT ¶58].
- (d) Restricted payments must be limited whenever leverage exceeds {{fact.covenant_restriction_leverage}}, the level above which the credit agreement's own restrictions apply [DEBT ¶58].
- (e) DaVita must hedge floating-rate exposure through the full {{facility.tenor_years}}-year tenor, including 2029 and later [DEBT ¶95].
