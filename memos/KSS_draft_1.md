# Credit memo: Kohl's Corporation

| Item | Assessment |
|---|---|
| Internal grade | {{grade.grade}} on 1-to-10 (base {{grade.base_grade}} plus {{grade.stress_notches}} stress notches) |
| Recommendation | Decline |
| Agency ratings | {{rating.sp}}; {{rating.moodys}} |
| Key reason | Our unsecured loan ranks behind the secured ABL revolver and secured 2030 notes [DEBT ¶61, 7-LIQ ¶125] |
| Key reason | Stress breaks leverage at {{stress.debt_ebitda}} and DSCR at {{stress.dscr}} |
| Key reason | Pro forma stressed DSCR of {{proforma.stress.dscr}} rests on a lower-bound rate of {{proforma.rate}} |

## 1. Request

The request is a {{facility.type}} of {{facility.amount_usd}}, {{facility.tenor_years}}-year tenor, for {{facility.purpose}}. This is a hypothetical request used to test the borrower's capacity to carry another {{proforma.amount}} of debt. We assume pricing at {{fact.new_debt_rate}}, the coupon on Kohl's most recent senior issue, the {{fact.secured_notes_2030}} of senior secured notes due 2030 [DEBT ¶61]. Our loan would be unsecured. The revolver is a {{fact.revolver_capacity}} senior secured, asset-based facility [7-LIQ ¶125]. The 2030 notes are backed by guarantees secured by distribution centers and e-commerce fulfillment centers [DEBT ¶61]. In a downside we would rank behind both.

## 2. Borrower overview

Kohl's is an omnichannel retailer. It sells moderately priced proprietary and national brand apparel, footwear, accessories, beauty and home products through stores and a website [7 ¶3]. It is a Wisconsin corporation organized in 1988 [1 ¶2]. Total revenue was {{FY2025.income.revenue}} in FY2025, down {{abs:growth.FY2025.revenue}} after a fall of {{abs:growth.FY2024.revenue}} in FY2024. Lower transaction volume drove the drop in net sales [7 ¶52, ¶54]. Sales fell in every line of business except Accessories, which includes Sephora [7 ¶56, ¶65]. Digital sales were approximately flat year over year [7 ¶49]. The business is seasonal, and a major portion of sales and income comes in the second half of the year [1A ¶37]. For FY2026, management guides net and comparable sales to fall or stay flat [7 ¶32].

## 3. Financial analysis

| Metric | FY2023 | FY2024 | FY2025 |
|---|---|---|---|
| Debt / EBITDA | {{FY2023.debt_ebitda}} | {{FY2024.debt_ebitda}} | {{FY2025.debt_ebitda}} |
| Net debt / EBITDA | {{FY2023.net_debt_ebitda}} | {{FY2024.net_debt_ebitda}} | {{FY2025.net_debt_ebitda}} |
| Lease-adj. debt / EBITDAR | {{FY2023.lease_adj_debt_ebitdar}} | {{FY2024.lease_adj_debt_ebitdar}} | {{FY2025.lease_adj_debt_ebitdar}} |
| Interest coverage | {{FY2023.interest_coverage}} | {{FY2024.interest_coverage}} | {{FY2025.interest_coverage}} |
| DSCR | {{FY2023.dscr}} | {{FY2024.dscr}} | {{FY2025.dscr}} |
| Current ratio | {{FY2023.current_ratio}} | {{FY2024.current_ratio}} | {{FY2025.current_ratio}} |
| EBITDA margin | {{FY2023.ebitda_margin}} | {{FY2024.ebitda_margin}} | {{FY2025.ebitda_margin}} |
| Free cash flow | {{FY2023.cashflow.fcf}} | {{FY2024.cashflow.fcf}} | {{FY2025.cashflow.fcf}} |

EBITDA fell {{abs:growth.FY2024.ebitda}} in FY2024, then rose {{growth.FY2025.ebitda}} to {{FY2025.income.ebitda}} in FY2025. One-off items flatter that recovery. Net unusual operating items were a gain of {{abs:FY2025.income.unusual_operating}}, mainly from a credit card interchange fee settlement [7 ¶156]. Excluding unusual items, EBITDA fell {{abs:growth.FY2025.ebitda_ex_unusual}} to {{FY2025.ebitda_ex_unusual}}, compared with {{FY2023.ebitda_ex_unusual}} in FY2023. Adjusted operating income was essentially unchanged from the prior year [7 ¶16]. That means the improvement in leverage to {{FY2025.debt_ebitda}} partly rests on a gain that will not recur.

Cash flow from operations rose {{growth.FY2025.cfo}} to {{FY2025.cashflow.cfo}}, helped by the settlement cash and lower inventory [7-LIQ ¶49]. After capex of {{abs:FY2025.cashflow.capex}}, free cash flow was {{FY2025.cashflow.fcf}}. Dividends were cut to {{abs:FY2025.cashflow.dividends}} from {{abs:FY2024.cashflow.dividends}}. Kohl's repaid {{abs:FY2025.cashflow.debt_repaid}} and raised {{FY2025.cashflow.debt_issued}}, so total debt declined {{abs:growth.FY2025.total_debt}} to {{FY2025.balance.total_debt}} [7-LIQ ¶73, ¶74, ¶75]. Cash rose to {{FY2025.balance.cash}}, and the current ratio improved to {{FY2025.current_ratio}} [7-LIQ ¶123].

Leases matter here. Lease liabilities of {{FY2025.balance.lease_liabilities}} bring lease-adjusted debt to {{FY2025.lease_adj_debt}} and lease-adjusted leverage to {{FY2025.lease_adj_debt_ebitdar}}. Interest expense eased to {{FY2025.income.interest_expense}}, but that figure includes a gain on extinguishment from open-market note repurchases [DEBT ¶63]. In FY2024, scheduled principal of {{FY2024.scheduled_principal}} pushed DSCR down to {{FY2024.dscr}}, which shows how thin the cushion can get in a weak year.

**Pro forma.** Adding {{proforma.amount}} at {{proforma.rate}} adds {{proforma.added_interest}} of interest and brings total debt to {{proforma.total_debt}}. On a pro forma basis, debt/EBITDA would be {{proforma.debt_ebitda}}, net debt/EBITDA {{proforma.net_debt_ebitda}}, lease-adjusted leverage {{proforma.lease_adj_debt_ebitdar}}, interest coverage {{proforma.interest_coverage}}, DSCR {{proforma.dscr}} and the current ratio {{proforma.current_ratio}}. The rate comes from a secured issue, so for an unsecured loan this pro forma interest is a lower bound [DEBT ¶61].

## 4. Strengths

- **Liquidity:** Cash was {{FY2025.balance.cash}}, mostly short-term investments [7-LIQ ¶5]. The {{fact.revolver_capacity}} revolver was undrawn, with {{fact.letters_of_credit}} of letters of credit reducing availability [DEBT ¶65].
- **Near-term maturities:** No senior notes were due within a year at year-end [DEBT ¶51]. Current debt was {{FY2025.balance.debt_current}}.
- **Cash generation:** FY2025 DSCR was {{FY2025.dscr}} and free cash flow was {{FY2025.cashflow.fcf}}.
- **Conservative capital allocation:** Buybacks were {{FY2025.cashflow.buybacks}}. Management expects to resume them only after overall leverage improves [7-LIQ ¶78].
- **Merchandising:** Gross margin improved on tighter inventory management, merchandise mix and lower shrink [7 ¶96].
- **Rating momentum:** Since the 10-K date, Moody's has moved to {{rating.moodys}} and S&P to {{rating.sp}}.

## 5. Risks and mitigants

- **Subordination:** We would rank behind the secured asset-based revolver and the secured 2030 notes [DEBT ¶61, 7-LIQ ¶125]. The {{fact.revolver_capacity}} revolver could be drawn ahead of us in a downturn. Only partial mitigant: the 2030 notes are just {{fact.secured_notes_2030}}.
- **Revenue decline:** Revenue fell {{abs:growth.FY2025.revenue}} as competition and price comparison intensified [1A ¶32, ¶33]. Mitigant: lower SG&A spending partly offset the decline [7 ¶101].
- **Earnings quality:** The settlement gain will not recur [7 ¶156]. EBITDA excluding unusual items was {{FY2025.ebitda_ex_unusual}}.
- **Rating-linked costs:** Downgrades have already raised the coupon on the {{fact.stepup_notes}} of 2031 notes by {{fact.stepup_total}} in total [7-LIQ ¶70]. Further S&P downgrades would raise borrowing costs again [1A ¶75]. Mitigant: the outlooks are now {{rating.sp}} and {{rating.moodys}}.
- **Covenants:** The revolver has a springing fixed charge coverage covenant [7-LIQ ¶125]. A revolver default could trigger cross-default on other debt [1A ¶76]. Mitigant: Kohl's was in compliance with all covenants at year-end [7-LIQ ¶125].
- **Tariffs:** Most goods are made outside the United States, mainly in Asia [1A ¶10].
- **Credit card income:** Program profitability depends on the health of moderate-income customers and on regulation [1A ¶47, ¶48].

## 6. Stress test

The scenario applies a revenue shock of {{stress.revenue_shock}} and cuts the EBITDA margin by {{stress.margin_shock}}, from {{stress.base_margin}} to {{stress.stressed_margin}}. It also adds {{stress.rate_shock}} to floating rates. Stressed EBITDA is {{stress.ebitda}}. With a floating-rate share of {{floating_rate_share}}, the rate shock adds {{stress.extra_interest}}, because long-term debt is fixed and the revolver was undrawn [7A ¶2, ¶3]. Treat that figure as a lower bound: any revolver draw in a downturn would bear SOFR-based interest [7A ¶3].

Stressed debt/EBITDA is {{stress.debt_ebitda}} and net debt/EBITDA {{stress.net_debt_ebitda}}. Lease-adjusted leverage is {{stress.lease_adj_debt_ebitdar}}, or {{stress.lease_adj_net_debt_ebitdar}} net of cash. Interest coverage is {{stress.interest_coverage}}, DSCR {{stress.dscr}} and the current ratio {{stress.current_ratio}}.

Two thresholds break:
- **Leverage:** debt/EBITDA of {{stress.debt_ebitda}} is above our leverage limit.
- **DSCR:** {{stress.dscr}} means cash flow no longer covers debt service.

With the facility added, stressed debt/EBITDA is {{proforma.stress.debt_ebitda}}, interest coverage {{proforma.stress.interest_coverage}} and DSCR {{proforma.stress.dscr}}. Extra floating interest stays at {{proforma.stress.extra_interest}}. Pro forma stressed coverage of {{proforma.stress.interest_coverage}} is just above our coverage threshold. A realistic unsecured rate, above the secured {{fact.new_debt_rate}}, would likely push it below.

## 7. Risk grade

The weighted score of {{grade.weighted_score}} maps to a base grade of {{grade.base_grade}}. The component scores are:

- Lease-adjusted leverage: {{grade.score.lease_adj_debt_ebitdar}} (weakest)
- Interest coverage: {{grade.score.interest_coverage}}
- Current ratio: {{grade.score.current_ratio}}
- DSCR: {{grade.score.dscr}} (strongest)

The stress test adds {{grade.stress_notches}} notches, which worsens the final grade to {{grade.grade}} on the 1-to-10 scale. That is consistent with agency ratings of {{rating.sp}}, {{rating.moodys}} and {{rating.fitch}}.

## 8. Recommendation

I recommend declining the facility as structured, which matches the grade of {{grade.grade}}. Base-case metrics are acceptable, with debt/EBITDA of {{FY2025.debt_ebitda}} and DSCR of {{FY2025.dscr}]. However, they depend on a non-recurring settlement gain [7 ¶156], while underlying EBITDA keeps falling, down {{abs:growth.FY2025.ebitda_ex_unusual}}.

An unsecured lender is structurally behind a large secured revolver and secured notes [DEBT ¶61, 7-LIQ ¶125]. That is the wrong place to be for a retailer whose sales are shrinking. Under stress, pro forma DSCR is {{proforma.stress.dscr}}, and coverage of {{proforma.stress.interest_coverage}} is likely overstated because the assumed rate is a secured coupon [DEBT ¶61].

The improved outlooks, {{rating.moodys}} and {{rating.sp}}, are encouraging but not yet backed by earnings growth. I would revisit a smaller, secured or ABL-participation structure once EBITDA excluding unusual items stabilises [judgment].

Recommendation: Decline
