# Credit memo: Union Pacific Corporation

| Item | Assessment |
|---|---|
| Internal grade | {{grade.grade}} on 1-to-10 |
| Recommendation | Approve with conditions |
| Agency ratings | {{rating.sp}}; {{rating.moodys}} |
| Key reason | Standalone leverage of {{FY2025.debt_ebitda}} and interest coverage of {{FY2025.interest_coverage}} |
| Key reason | Stressed pro forma DSCR stays at {{proforma.stress.dscr}} and no stress threshold breaks |
| Key reason | About {{fact.merger_cash_consideration}} of Norfolk Southern cash consideration is to be debt-funded [ACQ ¶4] |

## 1. Request

The borrower requests a {{facility.type}} of {{facility.amount_usd}} with a {{facility.tenor_years}}-year tenor, for {{facility.purpose}}. This is a hypothetical request at {{facility.amount_usd}}, used to test the borrower's capacity. We assume pricing at {{proforma.rate}}, the coupon on the company's most recent senior unsecured issue [DEBT ¶32, ¶33]. The Norfolk Southern acquisition is expected to close in 2027 [ACQ ¶8], so most of the {{facility.tenor_years}}-year tenor would run against the combined company.

## 2. Borrower overview

Union Pacific Railroad is the main operating company of the group and a Class I railroad serving the western two-thirds of the United States [1 ¶3, ¶16]. Freight is spread across three groups, Bulk, Industrial and Premium, with no single dominant category [1 ¶18, ¶19, ¶21]. The company reports the Railroad as one segment because the network is integrated [1 ¶14]. FY2025 revenue was {{FY2025.income.revenue}}. BNSF is its main rail competitor and runs parallel routes in many of its main corridors [1A ¶20]. Most employees belong to unions and work under collective bargaining agreements [1A ¶13]. In 2025 the company posted its best-ever personal injury and derailment rates, and service metrics also improved [7 ¶11, ¶12]. In July 2025 it signed a merger agreement to acquire Norfolk Southern [ACQ ¶3]. The combined railroad would be America's first transcontinental railroad [ACQ ¶5].

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

**Earnings.** Revenue grew {{growth.FY2024.revenue}} in FY2024 and {{growth.FY2025.revenue}} in FY2025. EBITDA grew faster, by {{growth.FY2024.ebitda}} and then {{growth.FY2025.ebitda}}, reaching {{FY2025.income.ebitda}}. The EBITDA margin widened from {{FY2023.ebitda_margin}} to {{FY2025.ebitda_margin}}. Management credits core pricing, productivity and volume growth, partly offset by inflation, mix and acquisition costs [7 ¶14]. Our EBITDA excludes other income of {{FY2025.income.other_nonoperating}}, which was lifted by industrial park land sales [7 ¶120].

**Leverage.** Debt/EBITDA improved from {{FY2023.debt_ebitda}} to {{FY2025.debt_ebitda}}. Total debt fell {{abs:growth.FY2024.total_debt}} in FY2024, then rose {{growth.FY2025.total_debt}} in FY2025 to {{FY2025.balance.total_debt}}. Lease-adjusted leverage tracked this at {{FY2025.lease_adj_debt_ebitdar}}. Equity grew to {{FY2025.balance.equity}}.

**Coverage.** Interest expense held at {{FY2025.income.interest_expense}}, giving coverage of {{FY2025.interest_coverage}}. The company had no variable-rate debt at year end [7A ¶4].

**Cash flow.** CFO fell {{abs:growth.FY2025.cfo}} to {{FY2025.cashflow.cfo}}, because of the timing of tax payments and purchased tax credits [7-LIQ ¶29]. Cash taxes fell to {{FY2025.cash_taxes}} from {{FY2023.cash_taxes}}, helped by the permanent return of full bonus depreciation [7-LIQ ¶30]. After capex of {{abs:FY2025.cashflow.capex}}, free cash flow was {{FY2025.cashflow.fcf}}. Dividends of {{abs:FY2025.cashflow.dividends}} and buybacks of {{abs:FY2025.cashflow.buybacks}} together exceeded that free cash flow. Debt issuance of {{FY2025.cashflow.debt_issued}} covered the gap, and debt repaid was {{abs:FY2025.cashflow.debt_repaid}}. Buybacks were paused after the merger was announced, while dividends continue [7 ¶193].

**Liquidity.** The current ratio is {{FY2025.current_ratio}}, a working capital deficit that management attributes to upcoming debt maturities [7-LIQ ¶3]. Liquidity consists of cash of {{FY2025.balance.cash}}, an undrawn revolver of {{fact.revolver_undrawn}}, and {{fact.receivables_facility_undrawn}} undrawn on the Receivables Facility [7-LIQ ¶5]. Scheduled principal is {{FY2025.scheduled_principal}}. Under the revolver covenant, debt as defined was {{fact.covenant_debt_outstanding}} against {{fact.covenant_debt_capacity}} allowed [DEBT ¶27].

**Pro forma.** Adding {{proforma.amount}} at {{proforma.rate}} costs {{proforma.added_interest}} of interest a year and lifts total debt to {{proforma.total_debt}}. Pro forma debt/EBITDA becomes {{proforma.debt_ebitda}} and lease-adjusted leverage {{proforma.lease_adj_debt_ebitdar}}. Interest coverage would be {{proforma.interest_coverage}}, DSCR {{proforma.dscr}} and the current ratio {{proforma.current_ratio}}. These pro forma figures cover Union Pacific standalone, because the Norfolk Southern deal has not yet closed [ACQ ¶8].

## 4. Strengths

- **Franchise and margins:** the EBITDA margin of {{FY2025.ebitda_margin}} reflects a hard-to-replicate network with high entry barriers [1 ¶16] [1A ¶11].
- **Debt capacity:** debt as defined is {{fact.covenant_debt_outstanding}} against a covenant ceiling of {{fact.covenant_debt_capacity}} [DEBT ¶27], and the revolver has no rating triggers apart from pricing [DEBT ¶27].
- **Rate risk:** {{floating_rate_share}} of debt is floating [7A ¶4].
- **Maturity profile:** annual maturities through 2030 are small compared with CFO of {{FY2025.cashflow.cfo}} [DEBT ¶17, ¶18, ¶19, ¶20, ¶21].
- **Ratings:** the company is rated {{rating.sp}} by S&P, {{rating.moodys}} by Moody's and {{rating.fitch}} by Fitch.
- **Fuel pass-through:** fuel surcharges recover a significant share of fuel costs [1A ¶26].

## 5. Risks and mitigants

- **Norfolk Southern acquisition (main risk).** About {{fact.merger_cash_consideration}} of cash consideration is to be funded with new debt and operating cash [ACQ ¶4]. Closing needs STB approval and is expected in 2027 [ACQ ¶7, ¶8]. The combined company will carry more debt, and servicing it will take more cash than either company needs today [1A ¶65]. The merger financing is expected to include a leverage covenant [1A ¶66, ¶67]. *Mitigants:* buybacks are paused [7 ¶193], and covenant headroom of {{fact.covenant_debt_capacity}} against {{fact.covenant_debt_outstanding}} is large [DEBT ¶27]. Beyond the {{fact.merger_cash_consideration}} funding need, we cannot size combined leverage, because no Norfolk Southern figures are available.
- **Deal failure.** If the deal fails, the company could owe a termination fee of {{fact.merger_termination_fee}} [ACQ ¶17]. *Mitigant:* the fee equals less than one year of free cash flow of {{FY2025.cashflow.fcf}}.
- **Integration and regulation.** Neither company has completed a deal of this size [1A ¶50]. The STB may impose conditions that reduce the benefits [1A ¶41, ¶42]. *Mitigant:* the standalone business is performing well on safety and service [7 ¶11, ¶12].
- **Refinancing.** The revolver expires in 2027 [DEBT ¶26], around the expected closing [ACQ ¶8]. If bond ratings fell below investment grade, access to the Receivables Facility could be reduced [7-LIQ ¶5].
- **Operations and macro.** The main exposures are hazardous materials [1A ¶6], labor disputes [1A ¶13], weather [1A ¶9] and trade disruption [1A ¶10]. Management expects macro uncertainty in 2026, with industrial production forecast flat [7 ¶26]. *Mitigant:* the 2026 capital plan is lower than FY2025 capex of {{abs:FY2025.cashflow.capex}} [7-LIQ ¶58].

## 6. Stress test

The scenario applies a revenue decline of {{stress.revenue_shock}}, a margin cut of {{stress.margin_shock}} (from {{stress.base_margin}} to {{stress.stressed_margin}}), and a rate shock of {{stress.rate_shock}}. Stressed EBITDA is {{stress.ebitda}}. Debt/EBITDA rises to {{stress.debt_ebitda}} and lease-adjusted leverage to {{stress.lease_adj_debt_ebitdar}}. Interest coverage falls to {{stress.interest_coverage}}, DSCR to {{stress.dscr}}, and the current ratio stays at {{stress.current_ratio}}. No grading threshold breaks, so stress adds {{grade.stress_notches}} notches. Extra interest from the rate shock is {{stress.extra_interest}}, because {{floating_rate_share}} of existing debt is floating [7A ¶4]. We treat that {{stress.extra_interest}} as a lower bound, since the term loan or the merger debt may carry floating rates. With the facility added, stressed leverage is {{proforma.stress.debt_ebitda}}, coverage {{proforma.stress.interest_coverage}} and DSCR {{proforma.stress.dscr}}. The facility's stressed extra interest is shown as {{proforma.stress.extra_interest}}, which also understates cost if the loan floats.

## 7. Risk grade

The weighted score of {{grade.weighted_score}} gives a base grade of {{grade.base_grade}} on the 1-to-10 scale. The component scores are:
- lease-adjusted leverage: {{grade.score.lease_adj_debt_ebitdar}}
- interest coverage: {{grade.score.interest_coverage}}
- DSCR: {{grade.score.dscr}}
- current ratio: {{grade.score.current_ratio}}

The current ratio score of {{grade.score.current_ratio}} pulls the grade down, although the deficit is structural and backed by committed lines [7-LIQ ¶3, ¶5]. Stress adds {{grade.stress_notches}} notches, so the final grade is {{grade.grade}}. The grade is standalone and does not reflect the higher post-merger indebtedness [1A ¶65].

## 8. Recommendation

I recommend approval. The {{facility.amount_usd}} exposure is small against covenant headroom of {{fact.covenant_debt_capacity}} versus {{fact.covenant_debt_outstanding}} outstanding [DEBT ¶27]. Even stressed and pro forma, DSCR holds at {{proforma.stress.dscr}} and coverage at {{proforma.stress.interest_coverage}}. A grade of {{grade.grade}} understates standalone quality, because the current ratio score of {{grade.score.current_ratio}} reflects a structural working capital deficit rather than weak liquidity [7-LIQ ¶3]. The real uncertainty is the post-merger balance sheet, which we cannot measure today [ACQ ¶4]. Structure should therefore protect us if combined leverage overshoots [judgment]. Approval should not be repeated without combined-company projections [judgment].

Recommendation: Approve with conditions:
- (a) the loan ranks pari passu with senior unsecured debt priced at least at {{proforma.rate}};
- (b) the loan carries an adjusted debt-to-EBITDA covenant and cross-default no looser than the revolver's [DEBT ¶26, ¶27];
- (c) a ratings-based pricing grid applies, plus a prepayment right if ratings fall below investment grade [7-LIQ ¶5];
- (d) the borrower delivers the merger financing plan and combined projections, and we re-grade at closing [ACQ ¶4, ¶8];
- (e) any floating-rate exposure on this loan is hedged, given the {{stress.rate_shock}} stress [7A ¶4].
