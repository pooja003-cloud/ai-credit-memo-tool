You are a senior commercial credit analyst at a bank. Write a credit memo on Union Pacific Corporation for the facility below, using ONLY the fact sheet and the 10-K paragraphs provided. Do not use tools, files or outside knowledge.

Facility requested: {{facility.type}} of {{facility.amount_usd}}, {{facility.tenor_years}}-year tenor, purpose: {{facility.purpose}}. This is a hypothetical request used to test the borrower's capacity.

RULES (a script checks every one; a draft that breaks any rule is rejected):
1. Never type a number. Every figure, ratio, percentage, amount, multiple and count must be a placeholder from the fact sheet, written exactly like {{FY2025.debt_ebitda}}. Write "{{facility.tenor_years}}-year", not "5-year". Words like "one notch" or "two thresholds" are fine. Allowed as typed text: years (2025), FY labels (FY2025), "Item 1A", "Note 12", "10-K", instrument names like "Term Loan A-2", and "1-to-10".
2. Every sentence of six words or more must contain a placeholder or a citation. Cite the 10-K as [1A ¶12] using the section key and paragraph number shown in front of each paragraph, e.g. [7-LIQ ¶3] or [DEBT ¶61]. Several paragraphs: [DEBT ¶95, ¶96].
3. Quotations of five or more words, in double quotes, must be copied word for word from the cited paragraph. Prefer paraphrase with a citation.
4. Signs: placeholders print negative values with a minus sign (capex, buybacks, gains, falls). After words like "fell", "declined", "buybacks of" or "capex of", write {{abs:...}} (e.g. "buybacks of {{abs:FY2025.cashflow.buybacks}}", "EBITDA fell {{abs:growth.FY2025.ebitda}}"). The checker rejects a sign that contradicts the word.
5. Do not invent placeholders. If a value is not in the fact sheet, describe it in words with a citation, or leave it out.
6. In section 8 only, an opinion that no number or paragraph supports may end with [judgment] instead of a citation. Do not attach citations that don't support the sentence.
7. End with a line in exactly this form: "Recommendation: Approve" or "Recommendation: Decline", optionally followed by " with conditions" and then the conditions.

STRUCTURE (Markdown):
# Credit memo: Union Pacific Corporation

A summary table right under the title, with rows: Internal grade ({{grade.grade}} on 1-to-10), Recommendation, Agency ratings ({{rating.sp}}; {{rating.moodys}}), and three short "Key reason" rows, each with a placeholder or citation.

## 1. Request
## 2. Borrower overview
## 3. Financial analysis  (include one table of key ratios for the three fiscal years using placeholders; then discuss trends; end with a short pro forma paragraph: the latest year with the requested facility added, using the proforma placeholders)
## 4. Strengths
## 5. Risks and mitigants
## 6. Stress test  (explain the scenario using the stress placeholders and say which thresholds break; add the pro forma stressed ratios. Interest rate caps pay only when SOFR is at or above the strike, so capped debt still bears rate rises up to the strike: treat the stress extra interest as a lower bound)
## 7. Risk grade  (the internal 1-to-10 grade, 1 = best, from {{grade.grade}} and its parts; stress notches make the grade WORSE, i.e. a higher number)
## 8. Recommendation  (your own judgment on approve or decline; it may differ from what the grade suggests, but explain why)

Paraphrase figures from the 10-K text precisely: if a paragraph says about 36%, don't write 'roughly a third'. Don't attach a citation that doesn't support the sentence; for a pure judgment sentence, tie it to a placeholder instead.

Keep it to about 900-1,300 words. Be specific and balanced. A credit committee reads this.

## FACT SHEET (values are shown only so you can reason; write the placeholder, never the value)
Use the placeholder with the real year in place of FYxxxx, e.g. `{{FY2025.debt_ebitda}}`.

| Placeholder | FY2023 | FY2024 | FY2025 |
|---|---|---|---|
| `{{FYxxxx.debt_ebitda}}`  | 2.86x | 2.58x | 2.58x |
| `{{FYxxxx.net_debt_ebitda}}`  | 2.77x | 2.49x | 2.48x |
| `{{FYxxxx.lease_adj_debt_ebitdar}}`  | 2.90x | 2.61x | 2.60x |
| `{{FYxxxx.lease_adj_net_debt_ebitdar}}`  | 2.81x | 2.53x | 2.50x |
| `{{FYxxxx.interest_coverage}}`  | 8.51x | 9.54x | 9.40x |
| `{{FYxxxx.dscr}}`  | 2.28x | 2.72x | 2.70x |
| `{{FYxxxx.current_ratio}}`  | 0.81x | 0.77x | 0.91x |
| `{{FYxxxx.ebitda_margin}}`  | 47.3% | 49.9% | 50.2% |
| `{{FYxxxx.ebitdar}}`  | $11.8 billion | $12.5 billion | $12.6 billion |
| `{{FYxxxx.net_debt}}`  | $31.5 billion | $30.2 billion | $30.5 billion |
| `{{FYxxxx.lease_adj_debt}}`  | $34.2 billion | $32.5 billion | $32.8 billion |
| `{{FYxxxx.ebitda_ex_unusual}}`  | $11.4 billion | $12.1 billion | $12.3 billion |
| `{{FYxxxx.income.revenue}}`  | $24.1 billion | $24.2 billion | $24.5 billion |
| `{{FYxxxx.income.operating_costs}}`  | $12.7 billion | $12.1 billion | $12.2 billion |
| `{{FYxxxx.income.da}}`  | $2.3 billion | $2.4 billion | $2.5 billion |
| `{{FYxxxx.income.unusual_operating}}`  | $0 | $0 | $0 |
| `{{FYxxxx.income.operating_income}}`  | $9.1 billion | $9.7 billion | $9.8 billion |
| `{{FYxxxx.income.interest_expense}}`  | $1.3 billion | $1.3 billion | $1.3 billion |
| `{{FYxxxx.income.other_nonoperating}}`  | $491 million | $350 million | $629 million |
| `{{FYxxxx.income.pretax_income}}`  | $8.2 billion | $8.8 billion | $9.2 billion |
| `{{FYxxxx.income.income_tax}}`  | $1.9 billion | $2.0 billion | $2.0 billion |
| `{{FYxxxx.income.net_income}}`  | $6.4 billion | $6.7 billion | $7.1 billion |
| `{{FYxxxx.income.ebitda}}`  | $11.4 billion | $12.1 billion | $12.3 billion |
| `{{FYxxxx.balance.cash}}`  | $1.1 billion | $1.0 billion | $1.3 billion |
| `{{FYxxxx.balance.current_assets}}`  | $4.1 billion | $4.0 billion | $4.6 billion |
| `{{FYxxxx.balance.total_assets}}`  | $67.1 billion | $67.7 billion | $69.7 billion |
| `{{FYxxxx.balance.debt_current}}`  | $1.4 billion | $1.4 billion | $1.5 billion |
| `{{FYxxxx.balance.ltd}}`  | $31.2 billion | $29.8 billion | $30.3 billion |
| `{{FYxxxx.balance.total_debt}}`  | $32.6 billion | $31.2 billion | $31.8 billion |
| `{{FYxxxx.balance.lease_liabilities}}`  | $1.2 billion | $925 million | $738 million |
| `{{FYxxxx.balance.current_liabilities}}`  | $5.1 billion | $5.3 billion | $5.0 billion |
| `{{FYxxxx.balance.total_liabilities}}`  | $52.3 billion | $50.8 billion | $51.2 billion |
| `{{FYxxxx.balance.redeemable_nci}}`  | $0 | $0 | $0 |
| `{{FYxxxx.balance.equity}}`  | $14.8 billion | $16.9 billion | $18.5 billion |
| `{{FYxxxx.balance.nci}}`  | $0 | $0 | $0 |
| `{{FYxxxx.cashflow.cfo}}`  | $8.4 billion | $9.3 billion | $9.3 billion |
| `{{FYxxxx.cashflow.capex}}`  | -$3.6 billion | -$3.5 billion | -$3.8 billion |
| `{{FYxxxx.cashflow.acquisitions}}`  | $0 | $0 | $0 |
| `{{FYxxxx.cashflow.debt_issued}}`  | $1.6 billion | $800 million | $2.0 billion |
| `{{FYxxxx.cashflow.debt_repaid}}`  | -$2.2 billion | -$2.2 billion | -$1.4 billion |
| `{{FYxxxx.cashflow.dividends}}`  | -$3.2 billion | -$3.2 billion | -$3.2 billion |
| `{{FYxxxx.cashflow.buybacks}}`  | -$705 million | -$1.5 billion | -$2.7 billion |
| `{{FYxxxx.cashflow.fcf}}`  | $4.8 billion | $5.9 billion | $5.5 billion |
| `{{FYxxxx.cash_taxes}}` (from the notes) | $1.5 billion | $1.3 billion | $877 million |
| `{{FYxxxx.scheduled_principal}}` (from the notes) | $1.4 billion | $1.4 billion | $1.5 billion |
| `{{FYxxxx.operating_lease_cost}}` (from the notes) | $369 million | $340 million | $305 million |
| `{{FYxxxx.operating_lease_liabilities}}` (from the notes) | $1.6 billion | $1.3 billion | $1.0 billion |
| `{{growth.FYxxxx.revenue}}` (change on prior year) | n/a | 0.5% | 1.1% |
| `{{growth.FYxxxx.ebitda}}` (change on prior year) | n/a | 6.2% | 1.7% |
| `{{growth.FYxxxx.ebitda_ex_unusual}}` (change on prior year) | n/a | 6.2% | 1.7% |
| `{{growth.FYxxxx.operating_income}}` (change on prior year) | n/a | 6.9% | 1.4% |
| `{{growth.FYxxxx.cfo}}` (change on prior year) | n/a | 11.5% | -0.6% |
| `{{growth.FYxxxx.total_debt}}` (change on prior year) | n/a | -4.3% | 2.0% |

Stress case and other values:

- `{{stress.debt_ebitda}}` = 3.44x
- `{{stress.net_debt_ebitda}}` = 3.30x
- `{{stress.lease_adj_debt_ebitdar}}` = 3.43x
- `{{stress.lease_adj_net_debt_ebitdar}}` = 3.30x
- `{{stress.interest_coverage}}` = 7.07x
- `{{stress.dscr}}` = 1.62x
- `{{stress.current_ratio}}` = 0.91x
- `{{stress.ebitda}}` = $9.3 billion
- `{{stress.extra_interest}}` = $0
- `{{stress.base_margin}}` = 50.2%
- `{{stress.stressed_margin}}` = 47.2%
- `{{stress.revenue_shock}}` = 20.0%
- `{{stress.margin_shock}}` = 300bp
- `{{stress.rate_shock}}` = 200bp
- `{{floating_rate_share}}` = 0.0%
- `{{facility.type}}` = Senior unsecured term loan
- `{{facility.amount_usd}}` = $500 million
- `{{facility.tenor_years}}` = 5
- `{{facility.purpose}}` = General corporate purposes
- `{{grade.grade}}` = 5
- `{{grade.base_grade}}` = 5
- `{{grade.stress_notches}}` = 0
- `{{grade.weighted_score}}` = 4.50
- `{{grade.score.lease_adj_debt_ebitdar}}` = 5
- `{{grade.score.interest_coverage}}` = 3
- `{{grade.score.dscr}}` = 4
- `{{grade.score.current_ratio}}` = 8
- `{{proforma.amount}}` = $500 million
- `{{proforma.rate}}` = 5.10%
- `{{proforma.added_interest}}` = $26 million
- `{{proforma.total_debt}}` = $32.3 billion
- `{{proforma.debt_ebitda}}` = 2.62x
- `{{proforma.net_debt_ebitda}}` = 2.52x
- `{{proforma.lease_adj_debt_ebitdar}}` = 2.64x
- `{{proforma.lease_adj_net_debt_ebitdar}}` = 2.54x
- `{{proforma.interest_coverage}}` = 9.23x
- `{{proforma.dscr}}` = 2.68x
- `{{proforma.current_ratio}}` = 0.91x
- `{{proforma.stress.debt_ebitda}}` = 3.49x
- `{{proforma.stress.interest_coverage}}` = 6.94x
- `{{proforma.stress.dscr}}` = 1.61x
- `{{proforma.stress.extra_interest}}` = $0
- `{{fact.covenant_debt_capacity}}` = $47.7 billion: Debt allowed under the revolver's adjusted debt-to-EBITDA covenant at December 31, 2025 (facility definition) [DEBT ¶27]
- `{{fact.covenant_debt_outstanding}}` = $33.5 billion: Debt as defined in the facility at December 31, 2025 [DEBT ¶27]
- `{{fact.merger_cash_consideration}}` = $20.0 billion: Approximate cash consideration for Norfolk Southern, to be funded by new debt and cash from operations [ACQ ¶4]
- `{{fact.merger_termination_fee}}` = $2.5 billion: Termination fee either party may have to pay [ACQ ¶17]
- `{{fact.new_debt_rate}}` = 5.10%: Coupon on Union Pacific's most recent senior unsecured issue: 5.100% notes due 2035, issued February 13, 2025 (same day as 5.600% notes due 2054; 2035 is closer to the 5-year tenor) [DEBT ¶32, ¶33]
- `{{fact.receivables_facility_undrawn}}` = $600 million: Undrawn Receivables Facility capacity; access may shrink if bond ratings fall below investment grade [7-LIQ ¶5]
- `{{fact.revolver_undrawn}}` = $2.0 billion: Undrawn revolving credit facility (expires 2027; supports commercial paper) [DEBT ¶26]
- `{{rating.sp}}` = A- (S&P, no dated action found)
- `{{rating.moodys}}` = A3 stable (Moody's, last action 2025-07-29)
- `{{rating.fitch}}` = A- (Fitch, last action 2026-07-15)
- Pro forma rate source: Coupon on Union Pacific's most recent senior unsecured issue: 5.100% notes due 2035, issued February 13, 2025 (same day as 5.600% notes due 2054; 2035 is closer to the 5-year tenor) [DEBT ¶32, ¶33]
- Stress thresholds broken (for your reasoning; describe them in words): none

## ANALYST POINTS TO COVER (each must appear in the memo, with its citation)
- The pending Norfolk Southern acquisition dominates the credit: about $20 billion of cash consideration is to be funded through new debt and operating cash [ACQ ¶4], closing expected in 2027 after STB approval [ACQ ¶7, ¶8]. FY2025 figures show Union Pacific standalone; the requested 5-year loan would run mostly against the combined, more indebted company [1A ¶65]. Do not compute a merger pro forma (no Norfolk Southern figures are in the fact sheet); treat it as the main qualitative risk.
- Share repurchases were paused after the merger announcement [7 ¶193]; dividends continue.
- Revolver covenant headroom at year end: debt as defined of $33.5B against $47.7B allowed [DEBT ¶27]; use the fact placeholders.

## 10-K PARAGRAPHS (Union Pacific Corporation 10-K filed 2026-02-06)

### [1] Item 1. Business
[1 ¶1] (p. 6) Item 1. Business
[1 ¶2] (p. 6) GENERAL
[1 ¶3] (p. 6) Union Pacific Railroad Company is the principal operating company of Union Pacific Corporation. One of America's most recognized companies, Union Pacific Railroad Company connects 23 states in the western two-thirds of the country by rail, providing a critical link in the global supply chain. The Railroad’s diversified business mix includes Bulk, Industrial, and Premium. Union Pacific serves many of the fastest-growing U.S. population centers, operates from all major West Coast and Gulf Coast […]
[1 ¶4] (p. 6) Union Pacific Corporation was incorporated in Utah in 1969 and maintains its principal executive offices at 1400 Douglas Street, Omaha, NE 68179. The telephone number at that address is (402) 544-5000. The common stock of Union Pacific Corporation is listed on the New York Stock Exchange (NYSE) under the symbol “UNP”.
[1 ¶5] (p. 6) For purposes of this report, unless the context otherwise requires, all references herein to "Union Pacific", “UPC”, “Corporation”, “Company”, “we”, “us”, and “our” shall mean Union Pacific Corporation and its subsidiaries, including Union Pacific Railroad Company, which we separately refer to as “UPRR” or the “Railroad”.
[1 ¶6] (p. 6) STRATEGY
[1 ¶7] (p. 6) Safety, Service, and Operational Excellence supports the Company's long-term initiative to Grow its freight volumes. Together as a team, the Company will focus on achieving the best safety record in the industry, being known for superior service, grounded in operational excellence, which, in turn, drives growth.
[1 ¶8] (p. 6) Safety is paramount and, as our first area of focus, sets the foundation for achieving the Company's objectives. The mindset and culture are built around a personal commitment by all employees to prioritize safety so everyone goes home safely.
[1 ¶9] (p. 6) Service is all about delivering what we sold our customers. We work with our customers to understand the service they need to win in their markets and then drive how we win together. We commit to these service levels and do it with excellence.
[1 ¶10] (p. 6) Operational Excellence is about operating efficiently and productively. We will drive value with our available resources but also maintain a buffer so our service is resilient, managing the inevitable ups and downs that come with weather, fluctuating volumes, and securing growth.
[1 ¶11] (p. 6) Growth is the outcome of executing our strategy to be the industry leader in both safety and service resulting in improved margins and greater cash generation, creating long term enterprise value. The expected outcome of successfully executing our strategy will be an industry leading operating ratio and return on invested capital.
[1 ¶12] (p. 6) As we work to transform our railroad, our core values continue to guide us. Our passion for performance will help us win; our high ethical standards ensure we win in a way that supports all of our stakeholders; and our teamwork ensures we win together.
[1 ¶13] (p. 6) OPERATIONS
[1 ¶14] (p. 6) The Railroad, along with its subsidiaries and rail affiliates, is our one reportable operating segment. Although we provide and analyze revenues by commodity group, we treat the financial results of the Railroad as one segment due to the integrated nature of our rail network. Additional information regarding our business and operations, including revenues, financial information and data, and other information regarding environmental matters, is presented in Risk Factors, Item 1A; Legal […]
[1 ¶15] (p. 6) 5
[1 ¶16] (p. 6) Operations – UPRR is a Class I railroad operating in the U.S. We have 32,889 route miles, connecting Pacific Coast and Gulf Coast ports with the Midwest and Eastern U.S. gateways and providing several corridors to key Mexican and Canadian gateways. We serve the western two-thirds of the country and maintain coordinated schedules with other rail carriers to move freight to and from the Atlantic Coast, the Pacific Coast, the Southeast, the Southwest, Canada, and Mexico. Export and import traffic […]
[1 ¶17] (p. 6) 2025 Freight Revenues
[1 ¶18] (p. 6) Bulk – The Company's Bulk shipments consist of grain and grain products, fertilizer, food and refrigerated, and coal and renewables. In 2025, this group generated 33% of our freight revenues. We access most major grain markets, connecting the Midwest and Western U.S. producing areas to export terminals in the Pacific Northwest and Gulf Coast ports as well as Mexico. We also serve significant domestic markets, including grain processors, animal feeders, ethanol, and renewable biofuel producers […]
[1 ¶19] (p. 6) Industrial – Our extensive network facilitates the movement of numerous commodities between thousands of origin and destination points throughout North America. The Industrial group consists of several categories, including construction, industrial chemicals, plastics, forest products, specialized products (primarily waste, salt, and roofing), metals and ores, petroleum, liquid petroleum gases (LPG), soda ash, and sand. Transportation of these products accounted for 37% of our freight revenues […]
[1 ¶20] (p. 6) The industrial chemicals market consists of a vast number of chemical compounds that support the manufacturing of more complex chemicals. Plastics shipments support automotive, housing, and the durable and disposable consumer goods markets. Forest product shipments include lumber and paper commodities. Lumber shipments originate primarily in the Pacific Northwest or Western Canada and move throughout the U.S. for use in new home construction and repairs and remodeling. Paper shipments primarily […]
[1 ¶21] (p. 6) Premium – In 2025, Premium shipments generated 30% of Union Pacific’s total freight revenues. Premium includes finished automobiles, automotive parts, and merchandise in intermodal containers, both domestic and international. International business consists of import and export traffic moving in 20 or 40-foot shipping containers, that mainly pass through West Coast ports, destined for one of the Company's many inland intermodal terminals. Domestic business includes container and trailer traffic […]
[1 ¶22] (p. 6) We are the largest automotive carrier west of the Mississippi River and operate or access more than 40 vehicle distribution centers. The Railroad’s extensive franchise accesses six vehicle assembly plants and connects to West Coast ports, all six major Mexico gateways, and the Port of Houston to accommodate both import and export shipments. In addition to transporting finished vehicles, the Company provides expedited handling of automotive parts in both boxcars and intermodal containers […]
[1 ¶23] (p. 7) Seasonality – Some of the commodities we carry have peak shipping seasons, reflecting either or both the nature of the commodity (such as certain agricultural and food products that have specific growing and harvesting seasons) and the demand cycle for the commodity (such as intermodal traffic that generally peaks during the third quarter to meet back-to-school and holiday-related demand for consumer goods during the fourth quarter). The peak shipping seasons for these commodities can vary […]
[1 ¶24] (p. 7) Proud & engaged workforce – Our employees are central to our strategy of Safety, Service, and Operational Excellence leading to Growth, and investing in our workforce is key to our success.
[1 ¶25] (p. 7) Our people: Our award-winning, multigenerational workforce includes talented people from all walks of life, in many stages of life. Made up of management and craft professionals, we are focused on attracting, retaining, and developing talent across our entire system. We employed an average of 29,287 employees during 2025.
[1 ¶26] (p. 7) Union Pacific works with 13 major rail unions, representing approximately 83% of our workforce. Pursuant to the Railway Labor Act (RLA), a federal statute enacted in 1926, our collective bargaining agreements are subject to modification every five years. Existing agreements remain in effect until new agreements are ratified or until the RLA procedures are exhausted. The RLA is designed to bring the railroads and unions to agreement without disruptions to rail transportation. We have concluded […]
[1 ¶27] (p. 7) Our culture: At Union Pacific, The How Matters – high ethical standards guide the decisions we make and action we take to protect our employees, communities, and customers. Our passion for performance drives our safety, customer experience, and financial results while we work as a team to create opportunity for all.
[1 ¶28] (p. 7) Safety is central to everything we do at Union Pacific. Together, we are committed to cultivating a safety-focused culture, so our employees return home safely every day. To achieve this, our employees identify risks, initiate action to mitigate those risks, and have the courage to care to keep each other safe.
[1 ¶29] (p. 7) Our success is measured by our personal injury rate (the number of reportable injuries for every 200,000 employee-hours worked) and our derailment incident rate (the number of reportable derailment incidents per million train miles). Reportable personal injuries are defined as on duty incidents or occupational illnesses that result in employees losing time away from work, modifying or restricting their normal duties, or receiving any medical treatment above and beyond first aid. Reportable […]
[1 ¶30] (p. 7) Our 2025 personal injury rate of 0.68 improved 24%, and our derailment incident rate of 1.75 improved 19% versus 2024. (See further discussion in Management’s Discussion and Analysis of Financial Condition and Results of Operations, Item 7, of this report.) Union Pacific is committed to creating an environment where people can be their best, personally and professionally. We believe that a supportive culture increases employee engagement, improves morale, and allows qualified employees to […]
[1 ¶31] (p. 7) The employee journey: From recruitment to retirement and milestones in between, we are relentlessly focused on supporting and engaging employees throughout their Union Pacific journey. We view it as imperative to invest in our employees with meaningful benefit offerings, developmental experiences, and career opportunities.
[1 ¶32] (p. 7) The process begins with recruitment, where we strive to attract the most talented employees to join our team. Then, we focus on training and development, which includes courses and programs designed to help our employees grow into new roles and/or learn a new skill in their current role so that we can retain our workforce over time.
[1 ¶33] (p. 7) Providing competitive compensation and meaningful benefits is key to attracting and retaining talented employees. Union Pacific is committed to continuously reviewing its compensation programs and comprehensive benefits programs to promote programs that are fair and competitive. Both are key to enhancing the value of working for Union Pacific and demonstrating the Company’s commitment to the health and wealth of employees during their career. Benefits vary based on the applicable collective […]
[1 ¶34] (p. 8) Our Board of Directors evaluates our non-union compensation plans and reviews recommendations from the Compensation and Talent Committee, while collective bargaining agreements govern compensation for our union employees. The median annual compensation for all employees employed as of December 31, 2025, was $107,889 (excluding the CEO).
[1 ¶35] (p. 8) Talent is critical - our ability to recruit and retain employees is directly tied to our railroad’s success, as proven by our 2025 retention rate of 89%, our robust benefit offerings, and work environment that creates meaningful family-supporting careers. We are focused on effectively managing workforce levels to the demands of the business and improving quality of life for our employees.
[1 ¶36] (p. 8) Railroad security – Our security efforts consist of a wide variety of measures, including employee training, engagement with our customers, training of emergency responders, and partnerships with numerous federal, state, and local government agencies. While federal law requires us to protect the confidentiality of our security plans designed to safeguard against terrorism and other security incidents, the following provides a general overview of our security initiatives.
[1 ¶37] (p. 8) UPRR security measures – We maintain a comprehensive security plan designed to both deter and respond to any potential or actual threats as they arise. The plan includes four levels of alert status, each with its own set of countermeasures. We employ our own police force, consisting of commissioned and highly-trained officers. The police are certified state law enforcement officers with investigative and arrest powers. The Union Pacific Police Department has achieved accreditation under the […]
[1 ¶38] (p. 8) We operate an emergency response management center 24 hours a day. The center receives reports of emergencies, dangerous or potentially dangerous conditions, and other safety and security issues from our employees, the public, law enforcement, and other government officials. In cooperation with government officials, we monitor both threats and public events, and, as necessary, we may alter rail traffic flow at times of concern to minimize risk to communities and our operations. We comply with […]
[1 ¶39] (p. 8) We established a number of our own innovative safety and security-oriented initiatives ranging from various investments in technology to The Officer on Train program, which provides local law enforcement officers with the opportunity to ride with train crews to enhance their understanding of railroad operations and risks. Our staff of information security professionals continually assess cybersecurity risks and implement mitigation programs that evolve with the changing technology threat […]
[1 ¶40] (p. 8) Cooperation with federal, state, and local government agencies – We work closely on physical and cybersecurity initiatives with government agencies, including the U.S. Department of Transportation (DOT); the Federal Bureau of Investigation (FBI); the Department of Homeland Security (DHS), along with its Cybersecurity and Infrastructure Security Agency (CISA), and the TSA; as well as local police departments, fire departments, and other first responders.
[1 ¶41] (p. 8) In compliance with TSA regulations established in 2022, we designated a Cybersecurity Coordinator to oversee our cybersecurity initiatives and report required incidents to the CISA. We communicated our Cybersecurity Incident Response Plan and conducted a Cybersecurity Vulnerability Assessment to identify potential risks. Our Cybersecurity Implementation Plan outlines the specific actions taken to meet the TSA prevention, detection, and response requirements. Additionally, an ongoing assessment […]
[1 ¶42] (p. 8) In conjunction with the Association of American Railroads (AAR), we sponsor Ask Rail, a mobile application that provides first responders with secure links to electronic information, including commodity and emergency response information required by emergency personnel to respond to accidents and other situations. We also participate in the National Joint Terrorism Task Force, a multi-agency effort established by the U.S. Department of Justice and the FBI to combat and prevent terrorism.
[1 ¶43] (p. 8) We work with the Coast Guard, U.S. Customs and Border Protection (CBP), and the Military Transport Management Command, which monitor shipments entering the UPRR rail network at U.S. border crossings and ports. We were the first railroad in the U.S. to be named a partner in CBP’s Customs-Trade Partnership Against Terrorism, a partnership designed to develop, enhance, and maintain effective security processes throughout the global supply chain.
[1 ¶44] (p. 9) Cooperation with customers and trade associations – Through TransCAER (Transportation Community Awareness and Emergency Response), we work with the AAR, the American Chemistry Council, the American Petroleum Institute, and other chemical trade groups to provide communities with preparedness tools, including the training of emergency responders. In cooperation with the FRA and other interested groups, we are also working to develop additional improvements to tank car design that will further […]
[1 ¶45] (p. 9) Sustainable future – Union Pacific believes it is important that we act as environmental stewards, reducing greenhouse gas (GHG) emissions and supporting the transition to a more sustainable future. While we work to further reduce our environmental footprint, it is important to note that railroads are already one of the most fuel-efficient means of transportation. Freight rail leads other forms of surface transportation when it comes to minimizing GHG emissions, and we expect rail will continue […]
[1 ¶46] (p. 9) Competition – see “We Face Competition from Other Railroads and Other Transportation Providers” in the Risk Factors in Item 1A of this report.
[1 ¶47] (p. 9) Key suppliers – see “We Are Dependent on Certain Key Suppliers of Locomotives and Rail” in the Risk Factors in Item 1A of this report.
[1 ¶48] (p. 9) Available information – Our Internet website is www.up.com. We make available free of charge on our website (under the “Investors” caption link) our Annual Reports on Form 10-K; our Quarterly Reports on Form 10-Q; our current reports on Form 8-K; our proxy statements; Forms 3, 4, and 5, filed on behalf of our directors and certain executive officers; and amendments to such reports filed or furnished pursuant to the Securities Exchange Act of 1934, as amended (the Exchange Act). We provide these […]
[1 ¶49] (p. 9) References to our website address, in this report, including references in Management’s Discussion and Analysis of Financial Condition and Results of Operations, Item 7, are provided as a convenience and do not constitute, and should not be deemed, an incorporation by reference of the information contained on, or available through, the website. Therefore, such information should not be considered part of this report.
[1 ¶50] (p. 9) GOVERNMENTAL AND ENVIRONMENTAL REGULATION
[1 ¶51] (p. 9) Governmental regulation – Our operations are subject to a variety of federal, state, and local regulations, generally applicable to all businesses. (See also the discussion of certain regulatory proceedings in Legal Proceedings, Item 3.) The operations of the Railroad are subject to the regulations of the FRA and other federal and state agencies as well as the regulatory jurisdiction of the Surface Transportation Board (STB). The STB has jurisdiction over rates charged on certain regulated rail […]
[1 ¶52] (p. 9) The DOT, the Occupational Safety and Health Administration, the Pipeline and Hazardous Materials Safety Administration, and the DHS, along with other federal agencies, have jurisdiction over certain aspects of safety, movement of hazardous materials and hazardous waste, emissions requirements, and equipment standards. Additionally, various state and local agencies have jurisdiction over disposal of hazardous waste and seek to regulate movement of hazardous materials in ways not preempted by […]
[1 ¶53] (p. 10) Environmental regulation – We are subject to extensive federal and state environmental statutes and regulations pertaining to public health and the environment. The statutes and regulations are administered and monitored by the Environmental Protection Agency (EPA) and by various state environmental agencies, such as the California Air Resources Board (CARB) and the Texas Commission on Environmental Quality (TCEQ), among others. The primary laws affecting our operations are the Resource […]
[1 ¶54] (p. 10) Information concerning environmental claims and contingencies and estimated remediation costs is set forth in Management’s Discussion and Analysis of Financial Condition and Results of Operations - Critical Accounting Estimates - Environmental, Item 7, and Note 17 to the Financial Statements and Supplementary Data, Item 8.

### [1A] Item 1A. Risk Factors
[1A ¶1] (p. 10) Item 1A. Risk Factors
[1A ¶2] (p. 10) The following discussion addresses significant factors, events, and uncertainties that make an investment in our securities risky and provides important information for the understanding of our “forward-looking statements,” which are discussed immediately preceding Item 7A of this Form 10-K and elsewhere. The risk factors set forth in this Item 1A should be read in conjunction with the rest of the information included in this report, including Management’s Discussion and Analysis of Financial […]
[1A ¶3] (p. 10) We urge you to consider carefully the factors described below and the risks that they present for our operations as well as the risks addressed in other reports and materials that we file with the SEC and the other information included or incorporated by reference in this Form 10-K. When the factors, events, and contingencies described below or elsewhere in this Form 10-K materialize, our business, reputation, financial condition, results of operations, cash flows, or prospects can be […]
[1A ¶4] (p. 10) Strategic and operational risks
[1A ¶5] (p. 10) We must manage fluctuating demand for our services and network capacity – Significant reductions in demand for rail services with respect to one or more commodities or changes in consumer preferences that affect the businesses of our customers can lead to increased costs associated with resizing our operations, including higher unit operating costs and costs for the storage of locomotives, rail cars, and other equipment; workforce adjustments; and other related activities, which could have a […]
[1A ¶6] (p. 10) We transport hazardous materials – We transport certain hazardous materials and other materials, including crude oil, ethanol, and toxic inhalation hazard (TIH) materials, such as chlorine, that pose certain risks in the event of a release or combustion. Additionally, U.S. laws impose common carrier obligations on railroads that require us to transport certain hazardous materials regardless of risk or potential exposure to loss. An accident or other incident on our network, at our facilities, […]
[1A ¶7] (p. 11) The ability to update or maintain technology could adversely affect our operations – We rely on information technology in all aspects of our business, including technology systems operated by us (whether created by us or purchased), under control of third parties, and open-source software. If we do not have sufficient capital or do not deploy sufficient capital in a timely manner to acquire, develop, or implement new technology or maintain or upgrade current systems, such as Positive Train […]
[1A ¶8] (p. 11) We are subject to cybersecurity risks – We rely on information technology in all aspects of our business, including technology systems operated by us (whether created by us or purchased), under control of third parties, and open-source software. We have experienced and will likely continue to experience varying degrees of cyber incidents in the normal course of business. There can be no assurance that the resources we devote to protect our technology systems and proprietary data or the systems […]
[1A ¶9] (p. 11) Severe weather and natural events could result in significant business interruptions and expenditures – As a railroad with a vast network, we are exposed to severe weather conditions and other natural phenomena, including earthquakes, hurricanes, fires, floods, mudslides or landslides, extreme temperatures, avalanches, and significant precipitation, and climate change may cause or contribute to the severity or frequency of such weather conditions. Line outages and other interruptions caused by […]
[1A ¶10] (p. 11) A significant portion of our revenues involves transportation of commodities to and from international markets – Although revenues from our operations are attributable to transportation services provided in the U.S., a significant portion of our revenues involves the transportation of commodities to and from international markets, including Mexico, Canada, and Southeast Asia, by various carriers and, at times, various modes of transportation. Significant and sustained interruptions of trade […]
[1A ¶11] (p. 12) We are dependent on certain key suppliers of locomotives and rail – Due to the capital-intensive nature and sophistication of locomotive equipment, parts, and maintenance, potential new suppliers face high barriers to entry. Therefore, if any of our two domestic suppliers of locomotives discontinues manufacturing locomotives, supplying parts, or providing maintenance for any reason, including bankruptcy or insolvency or the inability to manufacture locomotives that meet efficiency or regulatory […]
[1A ¶12] (p. 12) Workforce risks
[1A ¶13] (p. 12) Strikes or work stoppages could adversely affect our operations – The U.S. Class I railroads are party to collective bargaining agreements with various labor unions. The majority of our employees belong to labor unions and are subject to these agreements. Disputes over the terms of these or future agreements or the terms of such agreements, or our potential inability to negotiate acceptable contracts with these unions or the renegotiation of them or their term can lead to, among other things, […]
[1A ¶14] (p. 12) The availability of qualified personnel could adversely affect our operations – Changes in demographics, training requirements, and pandemic illnesses or restrictions could negatively affect the availability of qualified personnel for us, our customers, and throughout the supply chain. Our ability to quickly react to other factors that affect our ability to attract and retain employees may be restricted due to limited flexibility to make unilateral changes to collective bargaining agreements, […]
[1A ¶15] (p. 12) Legal and regulatory risks
[1A ¶16] (p. 12) We are subject to significant governmental regulation – We are subject to governmental regulation by a significant number of federal, state, and local authorities covering a variety of health, safety, labor, employment, environmental, economic (as discussed below), tax, social, and other matters. Many laws and regulations require us to obtain and maintain various licenses, permits, and other authorizations, and we cannot guarantee that we will continue to be able to do so. Our failure to comply […]
[1A ¶17] (p. 13) We may be subject to various claims and lawsuits that could result in significant expenditures – As a railroad with operations in densely populated urban areas and a vast rail network, we are exposed to the potential for various claims and litigation related to labor and employment, personal injury, property damage, environmental liability, and other matters. Any material changes to litigation trends or a catastrophic rail accident or series of accidents involving any or all of property damage, […]
[1A ¶18] (p. 13) We are subject to significant environmental laws and regulations – Due to the nature of the railroad business, our operations are subject to extensive federal, state, and local environmental laws and regulations concerning, among other things, emissions to the air; discharges to waters; handling, storage, transportation, and disposal of waste and other materials; and hazardous material or petroleum releases. We generate and transport hazardous and non-hazardous waste in our operations. […]
[1A ¶19] (p. 13) Macroeconomic and industry risks
[1A ¶20] (p. 13) We face competition from other railroads and other transportation providers – We face competition from other railroads, motor carriers, ships, barges, and pipelines. Our main railroad competitor is Burlington Northern Santa Fe LLC. Its primary subsidiary, BNSF Railway Company (BNSF), operates parallel routes in many of our main traffic corridors. In addition, we operate in corridors served by other railroads and motor carriers. Motor carrier competition exists in all three of our commodity […]
[1A ¶21] (p. 14) We may be affected by climate change and market or regulatory responses to climate change – Climate change, including the impact of global warming and transition risks involving policy, legal risks, and market risks, could have a material adverse effect on our results of operations, financial condition, and liquidity on both a long-term and near-term basis. Restrictions, caps, taxes, or other controls on emissions of greenhouse gases (GHGs), including diesel exhaust, could significantly […]
[1A ¶22] (p. 14) Compliance with laws or regulations related to climate change, along with defending and resolving legal claims and other litigation, could have a material adverse effect on our results of operations, financial condition, and liquidity. Climate change may cause severe weather conditions and other natural phenomena, including earthquakes, hurricanes, fires, floods, mudslides or landslides, extreme temperatures, avalanches, and significant precipitation. Severe weather conditions and other natural […]
[1A ¶23] (p. 14) Our efforts to achieve emission reduction targets or aspirations could significantly increase our operational costs and capital expenditures. In addition, stakeholder expectations regarding some of these matters may be evolving and there may be differing views among stakeholders, which could harm our reputation or increase our costs. Our ability to meet such targets or aspirations can depend on significant technological advancements, including, for example, suitable alternative fuels and […]
[1A ¶24] (p. 14) Our business, financial condition, and results of operations have been adversely affected, and in the future, could be materially adversely affected by pandemics or other public health crises – Pandemics, epidemics, and other outbreaks of disease can have significant and widespread impacts. As we saw during the peaks of the COVID pandemic, outbreaks of disease can cause a global slowdown of economic activity (including the decrease in demand for a broad variety of goods), disruptions in global […]
[1A ¶25] (p. 15) Financial risks
[1A ¶26] (p. 15) We are affected by fluctuating fuel prices – Fuel costs constitute a significant portion of our transportation expenses. Diesel fuel prices can be subject to dramatic fluctuations, and significant price increases could have a material adverse effect on our operating results. Although we currently are able to recover a significant amount of our fuel expenses from our customers through revenues from fuel surcharges, we cannot be certain that we will always be able to mitigate rising or elevated […]
[1A ¶27] (p. 15) We rely on capital markets – Due to the significant capital expenditures required to operate and maintain a safe and efficient railroad, we rely on the capital markets to provide some of our capital requirements. We utilize long-term debt instruments, bank financing, and commercial paper, and we pledge certain amount of our receivables as collateral for credit. Significant instability or disruptions of the capital markets, including, among other things, elevated interest rates in the credit […]
[1A ¶28] (p. 15) Pending acquisition risks
[1A ¶29] (p. 15) The mergers are subject to conditions, some or all of which may not be satisfied or completed on a timely basis, if at all. Failure to complete the mergers could have material adverse effects on our business — On July 28, 2025, the Company, Norfolk Southern, Ruby Merger Sub 1 Corporation, and Ruby Merger Sub 2 LLC, entered into an agreement and plan of merger (the merger agreement). The completion of the mergers (as defined in the merger agreement) is subject to a number of conditions, […]
[1A ¶30] (p. 15) If the mergers are not completed, our ongoing business may be materially adversely affected and, without realizing any of the benefits of having completed the mergers, we will be subject to a number of risks, including the following:
[1A ¶31] (p. 15) •the market price of our common stock could decline;
[1A ¶32] (p. 15) •we could owe substantial termination fees to Norfolk Southern under certain circumstances;
[1A ¶33] (p. 15) •time, resources, and costs committed by our management team to matters relating to the mergers could otherwise have been devoted to pursuing other beneficial opportunities;
[1A ¶34] (p. 15) •we may experience negative reactions from the financial markets or from customers, suppliers, employees, labor unions, or other business partners; and •we will be required to pay our respective costs relating to the mergers, such as legal, accounting, and printing fees, whether or not the mergers are completed.
[1A ¶35] (p. 15) In addition, if the mergers are not completed, we could be subject to litigation related to any failure to complete the mergers or related to any enforcement proceeding commenced against us to perform our obligations under the merger agreement, and whether or not any such litigation has any merit, the cost of defending such litigation may be significant. The materialization of any of these risks could adversely impact our ongoing business.
[1A ¶36] (p. 16) Similarly, delays in the completion of the mergers could, among other things, result in additional transaction costs, loss of revenues, or other negative effects associated with uncertainty about completion of the mergers.
[1A ¶37] (p. 16) The merger agreement contains provisions that limit our ability to pursue alternatives to the mergers, and, in specified circumstances, could require us to pay substantial termination fees to Norfolk Southern — The merger agreement contains certain provisions that restrict our ability to initiate, solicit, knowingly encourage, or, subject to certain exceptions, engage in discussions or negotiations with respect to, or approve or recommend, any alternative proposal.
[1A ¶38] (p. 16) In some circumstances, upon termination of the merger agreement in connection with an alternative proposal, we may be required to pay a termination fee of $2.5 billion to Norfolk Southern.
[1A ¶39] (p. 16) These provisions could discourage a potential acquiror of us or alternative merger partner that might have an interest in acquiring all or a significant portion of the Company or pursuing an alternative acquisition transaction with us from considering or proposing such a transaction, even if it were prepared to pay consideration with a higher per-share value than the per-share value proposed to be realized in the mergers. In particular, a termination fee, if applicable, could result in a […]
[1A ¶40] (p. 16) If the merger agreement is terminated in accordance with its terms, and we or Norfolk Southern seek another business combination, we may not be able to negotiate a transaction with another party on terms comparable to, or better than, the terms of the merger agreement.
[1A ¶41] (p. 16) The mergers are subject to the receipt of the requisite regulatory approvals, which requisite regulatory approvals may never be obtained, therefore preventing completion of the mergers. In addition, in granting such approvals, regulatory authorities may impose conditions that could have a significant adverse effect on the Company, Norfolk Southern, or the combined company and the expected benefits of the mergers therefore preventing completion of the mergers — Before the mergers may be […]
[1A ¶42] (p. 17) In addition, under existing law, our railroad competitors and customers, Norfolk Southern’s railroad competitors and customers, and other interested parties may intervene to oppose the STB application or seek protective conditions in the event approval by the STB is granted, which might affect the decision of the STB, delay the approval process, or reduce the anticipated benefits of the mergers. Furthermore, if the STB does not provide final approval or imposes conditions on its approval in a […]
[1A ¶43] (p. 17) The Company and Norfolk Southern are each subject to business uncertainties and contractual restrictions while the mergers are pending, which could adversely affect both our business and operations and the combined company’s business and operations — In connection with the pendency of the mergers, some customers, suppliers, and other persons with whom the Company or Norfolk Southern has a business relationship have or may delay or defer certain business decisions or terminate, change, or […]
[1A ¶44] (p. 17) Under the terms of the merger agreement, each of the Company and Norfolk Southern is subject to certain restrictions on the conduct of its business prior to completing the first merger (as defined in the merger agreement), which may adversely affect its ability to execute certain of its business strategies, including, in the case of Norfolk Southern, the ability in certain cases to enter into or amend contracts, acquire or dispose of assets, incur indebtedness, incur capital expenditures, […]
[1A ¶45] (p. 17) Each of the risks described above may be exacerbated by delays or other adverse developments with respect to the completion of the mergers.
[1A ¶46] (p. 17) Uncertainties associated with the mergers may cause a loss of management personnel and other key employees, and the Company and Norfolk Southern may have difficulty attracting and motivating management personnel and other key employees, and combining cultures between the two companies could be challenging, which could adversely affect the future business and operations of the combined company — The Company and Norfolk Southern are dependent on the experience and industry knowledge of their […]
[1A ¶47] (p. 17) We may and have been a target of securities class action and derivative lawsuits that could result in substantial costs and may delay or prevent the mergers from being completed, whether or not such lawsuits have any merit — Securities class action lawsuits and derivative lawsuits are often brought against public companies that have entered into merger agreements. Even if the lawsuits are without merit, defending against or otherwise resolving these claims can result in substantial costs and […]
[1A ¶48] (p. 17) Completion of the mergers may trigger change in control or other provisions in certain agreements to which Norfolk Southern or its subsidiaries are a party, which may have an adverse impact on the combined company’s business and results of operations — The completion of the mergers may trigger change in control and other provisions in certain agreements to which Norfolk Southern or its subsidiaries are a party. If the Company and Norfolk Southern are unable to negotiate waivers of those […]
[1A ¶49] (p. 18) The combined company may be unable to successfully integrate the businesses of the Company and Norfolk Southern and realize the anticipated benefits of the mergers — The success of the mergers will depend, in part, on the combined company’s ability to successfully combine the businesses of the Company and Norfolk Southern, which currently operate as independent public companies, and realize the anticipated benefits, including synergies, cost savings, innovation, and operational efficiencies, […]
[1A ¶50] (p. 18) The mergers involve the integration of Norfolk Southern’s business with our existing business, which is a complex, costly, and time-consuming process. Neither the Company nor Norfolk Southern have previously completed a transaction comparable in size or scope to the mergers. The integration of the two (2) companies may result in material challenges, including, without limitation:
[1A ¶51] (p. 18) •the diversion of management’s attention from ongoing business concerns and performance shortfalls at one or both of the companies as a result of the devotion of management’s attention to the mergers;
[1A ¶52] (p. 18) •managing a larger combined company;
[1A ¶53] (p. 18) •creating, implementing, and executing a unified business strategy, and operational, financial, and managerial control with respect to the combined entity;
[1A ¶54] (p. 18) •the inherent risk and complexity of integrating railroad operations, including operating, information technology, safety, and managerial systems and processes, particularly on a large scale, in the context of ongoing business operations and customer commitments;
[1A ¶55] (p. 18) •maintaining employee morale and attracting, motivating, and retaining management personnel and other key employees;
[1A ¶56] (p. 18) •the possibility of faulty assumptions underlying expectations regarding the integration process;
[1A ¶57] (p. 18) •retaining existing business and operational relationships and attracting new business and operational relationships;
[1A ¶58] (p. 18) •consolidating corporate and administrative infrastructures and eliminating duplicative operations and inconsistencies in standards, controls, procedures, and policies;
[1A ¶59] (p. 18) •coordinating geographically separate organizations;
[1A ¶60] (p. 18) •unanticipated changes in federal or state laws or regulations or international trade agreements, including additional regulatory scrutiny or additional regulatory requirements as a result of the transaction or the size, scope, and complexity of the combined company’s business operations; and •unforeseen expenses or delays associated with the mergers.
[1A ¶61] (p. 18) Many of these factors will be outside of the combined company’s control and any one of them could result in delays, increased costs, decreases in the amount of expected revenues, and diversion of management’s time and energy, which could materially affect the combined company’s financial position, results of operations, and cash flows.
[1A ¶62] (p. 18) The Company and Norfolk Southern have operated, and until completion of the mergers will continue to operate, independently. The Company and Norfolk Southern are currently permitted to conduct only limited planning for the integration of the two (2) companies following the mergers and have not yet determined the exact nature of how the businesses and operations of the two (2) companies will be combined after the mergers. The actual integration may result in additional and unforeseen expenses, […]
[1A ¶63] (p. 18) The future results of the combined company may be adversely impacted if the combined company does not effectively manage its expanded operations following the completion of the mergers — Following the completion of the mergers, the size of the combined company’s business will be significantly larger than the current size of our business. The combined company’s ability to successfully manage this expanded business will depend, in part, upon management’s ability to design and implement […]
[1A ¶64] (p. 19) The combined company is expected to incur substantial expenses related to the completion of the mergers and the integration of the Company and Norfolk Southern — The combined company is expected to incur substantial expenses in connection with the completion of the mergers and the integration of the Company and Norfolk Southern. There are a large number of processes, policies, procedures, operations, technologies, and systems that must be integrated, including purchasing, accounting and […]
[1A ¶65] (p. 19) The combined company’s indebtedness may limit its flexibility and increase its borrowing costs — The combined company’s consolidated indebtedness may have the effect of, among other things, increasing borrowing costs. In addition, the amount of cash required to service the indebtedness levels will be greater than the amount of cash flows required to service the indebtedness of the Company or Norfolk Southern individually prior to completion of the mergers. The level of indebtedness could also […]
[1A ¶66] (p. 19) The financing arrangements that the combined company will enter into in connection with the mergers may, under certain circumstances, contain restrictions and limitations that could significantly impact the combined company’s ability to operate its business — We expect to incur significant new indebtedness in connection with the mergers. We also expect that the agreements governing the indebtedness that the combined company will incur in connection with the mergers will contain covenants that, […]
[1A ¶67] (p. 19) In addition, the combined company will likely be required to comply with a leverage covenant as set forth in these agreements.
[1A ¶68] (p. 19) The combined company’s ability to comply with the leverage covenant in future periods will depend on its ongoing financial and operating performance, which in turn will be subject to economic conditions and to financial, market, and competitive factors, many of which are beyond the combined company’s control. The ability to comply with this covenant in future periods will also depend on the combined company’s ability to successfully implement its overall business strategy and realize the […]
[1A ¶69] (p. 19) Various risks, uncertainties, and events beyond the combined company’s control could affect its ability to comply with the covenants contained in its financing agreements. Failure to comply with any of the covenants in its existing or future financing agreements could result in a default under those agreements and under other agreements containing cross-default provisions. A default would permit lenders to accelerate the maturity of the debt under these agreements and to foreclose upon any […]
[1A ¶70] (p. 19) General risk factors
[1A ¶71] (p. 19) We are affected by general economic conditions – Prolonged, severe adverse domestic and global macroeconomic conditions or disruptions of financial and credit markets, including, for example, the cycles of recessionary fears, inflationary pressures, changes in interest rates, and/or related monetary policy actions by governments in response to inflation, may affect the producers and consumers of the commodities we carry and may have a material adverse effect on our access to liquidity, results […]
[1A ¶72] (p. 20) We may be affected by acts of terrorism, war, or risk of war – Our rail lines, facilities, and equipment, including rail cars carrying hazardous materials, could be direct targets or indirect casualties of terrorist attacks. Terrorist attacks, or other similar events, any government response thereto, and war or risk of war may adversely affect our results of operations, financial condition, and liquidity. In addition, insurance premiums for some or all of our current coverages could increase […]

### [7] Item 7. Management's Discussion and Analysis
[7 ¶1] (p. 28) Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations
[7 ¶2] (p. 28) The following discussion should be read in conjunction with the Consolidated Financial Statements and applicable notes to the Financial Statements and Supplementary Data, Item 8, and other information in this report, including Risk Factors set forth in Item 1A and Critical Accounting Estimates and Cautionary Information at the end of this Item 7. The following section generally discusses 2025 and […]
[7 ¶3] (p. 28) The Railroad, along with its subsidiaries and rail affiliates, is our one reportable operating segment. Although we provide and analyze revenues by commodity group, we treat the financial results of the Railroad as one segment due to the integrated nature of our rail network.
[7 ¶4] (p. 28) EXECUTIVE SUMMARY
[7 ¶5] (p. 28) 2025 Results
[7 ¶6] (p. 28) •Safety – Building on the foundation and commitment to our safety culture, 2025 furthered our progress towards world-class safety. With a focus on four central pillars – Injury Prevention, Leverage Technology, Situational Awareness Testing, and Peer-to-Peer Engagement, we are cultivating a safety-focused mindset so all of our employees return home safely each day.
[7 ¶7] (p. 28) Injury Prevention efforts focus on specific, critical tasks where any form of non-compliance can result in a serious injury. Training is vital to teach our employees how to safely execute those critical tasks in order to reduce the risk of injury or derailment.
[7 ¶8] (p. 28) By Leveraging Technology, we seek to eliminate or automate activities with the most risk. Over 7,000 wayside detectors monitor freight cars and locomotives in real time, generating 72 million data points daily to proactively identify and mitigate risks. We are building safer trains with our proprietary Physics Train Builder technology, which allows us to evaluate train and route characteristics […]
[7 ¶9] (p. 28) Situational Awareness Testing (a program we call COMMIT) is our program that observes, tests, and coaches our employees to promote understanding and compliance with our work rules. COMMIT goes beyond traditional classroom learning, with an emphasis on in-the-field training with employees actively running the railroad.
[7 ¶10] (p. 29) Peer-to-Peer Engagement drives employee ownership through engagement with our safety programs. Our culture embodies a personal commitment to do our jobs with a passion for safety so everyone goes home safe. Employees are encouraged to speak up if they see unsafe behaviors.
[7 ¶11] (p. 29) The focus on these four pillars continues to drive improvement, resulting in our best-ever personal injury and derailment incident rate annual safety results. Compared to 2024, our personal injury rate (the number of reportable injuries for every 200,000 employee-hours worked) of 0.68 decreased 24% and our derailment incident rate (the number of reportable derailment incidents per million train […]
[7 ¶12] (p. 29) •Service – Bolstered by sequentially improving freight car velocity and terminal dwell, our network remained fluid throughout 2025 as we achieved best-ever results for many of our operating metrics. For the year ended December 31, 2025, freight car velocity increased to 225 daily miles per car, an improvement of 8%, while terminal dwell declined 8% during the same period compared to 2024. Both […]
[7 ¶13] (p. 29) •Operational Excellence – We effectively adapted to shifts in business traffic mix throughout 2025 as we handled elevated international intermodal shipments in the first half of the year coupled with strong bulk shipments throughout the year. As customer demand changed, we efficiently modified our resources to match demand while improving our service performance.
[7 ¶14] (p. 29) •Financial results – Core pricing gains, strong productivity, and 1% volume growth positively impacted our financial results and offset the impact of inflation, negative business mix, and acquisition-related costs. Operating income of $9.8 billion increased 1% from 2024, and our operating ratio improved 10 basis points to 59.8% in 2025. Net income of $7.1 billion translated into earnings of […]
[7 ¶15] (p. 29) We generated $9.3 billion of cash provided by operating activities, yielded free cash flow of $2.3 billion after reductions of $3.8 billion for cash used in investing activities and $3.2 billion in dividends paid. Cash provided by operating activities was positively impacted by $0.3 billion due to the enactment of H.R.1 and the reinstatement of 100% bonus depreciation.
[7 ¶16] (p. 29) Free cash flow is defined as cash provided by operating activities less cash used in investing activities and dividends paid. Free cash flow is not considered a financial measure under GAAP by SEC Regulation G and Item 10 of SEC Regulation S-K and may not be defined and calculated by other companies in the same manner. We believe free cash flow is important to management and investors in […]
[7 ¶17] (p. 29) Millions | 2025 | 2024 | 2023
[7 ¶18] (p. 29) Cash provided by operating activities | $ | 9,290 | $ | 9,346 | $ | 8,379
[7 ¶19] (p. 29) Cash used in investing activities | (3,762) | (3,325) | (3,667)
[7 ¶20] (p. 29) Dividends paid | (3,236) | (3,213) | (3,173)
[7 ¶21] (p. 29) Free cash flow | $ | 2,292 | $ | 2,808 | $ | 1,539
[7 ¶22] (p. 29) 2026 Outlook
[7 ¶23] (p. 29) •Safety – We are committed to our goal of world-class safety and are continuously identifying areas in which we can enhance safety. In 2026, our focus remains on our four pillars of safety. Critical safety tasks will be reinforced. Training to engage both new and experienced employees is fundamental to our success. We will continue using a comprehensive safety management approach utilizing […]
[7 ¶24] (p. 29) •Service – We are committed to delivering the service we sold to our customers. As we meet with customers to agree on their specific needs and outcomes, we will continue to measure ourselves against the best service we provided them over the last three years and use that as a guide for meeting their expectations. We will engage with customers by being the first to act on new opportunities, […]
[7 ¶25] (p. 30) •Operational Excellence – To provide our customers with the service we sold, we must run a fluid network. Network fluidity enables us to effectively utilize all our resources and provides the capacity to respond in an ever-changing environment. Terminal dwell and freight car velocity are key indicators of that fluidity. We will continue to transform our railroad using technology and automation to […]
[7 ¶26] (p. 30) •Business volumes – We expect macroeconomic uncertainties to persist in 2026, and those uncertainties could have a material impact on our 2026 financial and operating results. 2026 industrial production is forecasted to be essentially flat with 2025, coupled with reduced expectations for housing starts and light vehicle sales. Lower international intermodal business, largely due to the resumption […]
[7 ¶27] (p. 30) RESULTS OF OPERATIONS
[7 ¶28] (p. 30) Operating revenues
[7 ¶29] (p. 30) Millions | 2025 | 2024 | 2023 | % Change 2025 v 2024 | % Change 2024 v 2023
[7 ¶30] (p. 30) Freight revenues | $ | 23,220 | $ | 22,811 | $ | 22,571 | 2 | % | 1 | %
[7 ¶31] (p. 30) Other subsidiary revenues | 718 | 788 | 872 | (9) | (10)
[7 ¶32] (p. 30) Accessorial revenues | 475 | 554 | 584 | (14) | (5)
[7 ¶33] (p. 30) Other | 97 | 97 | 92 | - | 5
[7 ¶34] (p. 30) Total | $ | 24,510 | $ | 24,250 | $ | 24,119 | 1 | % | 1 | %
[7 ¶35] (p. 30) We generate freight revenues by transporting products from our three commodity groups. Freight revenues vary with volumes (carloads) and average revenue per car (ARC). Changes in price, traffic mix, and fuel surcharges drive ARC. Customer incentives, which are primarily provided for shipping to/from specific locations or based on cumulative volumes, are recorded as a reduction to operating […]
[7 ¶36] (p. 30) Other subsidiary revenues (primarily logistics and commuter rail operations) are generally recognized over time as shipments move from origin to destination. The allocation of revenues between reporting periods is based on the relative transit time in each reporting period with expenses recognized as incurred. Accessorial revenues are recognized at a point in time as performance obligations are […]
[7 ¶37] (p. 30) Freight revenues of $23.2 billion increased 2% from 2024 driven by core pricing gains and a 1% increase in volumes, partially offset by traffic mix (for example, a relative increase in coal and rock shipments, which have a lower ARC, combined with a decline in lumber shipments, which have a higher ARC) and lower fuel surcharge revenues. Volume increases were primarily driven by coal, grain and […]
[7 ¶38] (p. 30) Our fuel surcharge programs generated freight revenues of $2.3 billion and $2.6 billion in 2025 and 2024, respectively. Fuel surcharge revenues in 2025 decreased $218 million due to lower fuel prices and the lag impact of fluctuating fuel prices (it can generally take up to two months for changing fuel prices to affect fuel surcharge recoveries), partially offset by higher volumes.
[7 ¶39] (p. 30) In 2025, other subsidiary revenues decreased compared to 2024 due to the transfer of our commuter operations to Metra. Accessorial revenues decreased in 2025 compared to 2024 as a result of lower intermodal container revenues due to an intermodal equipment sale and a one-time contract settlement, both of which occurred in 2024, partially offset by higher intermodal accessorial revenues.
[7 ¶40] (p. 31) The following tables summarize the year-over-year changes in freight revenues, revenue carloads, and ARC by commodity type:
[7 ¶41] (p. 31) Freight revenues
[7 ¶42] (p. 31) Millions
[7 ¶43] (p. 31) 2025 | 2024 | 2023 | % Change 2025 v 2024 | % Change 2024 v 2023
[7 ¶44] (p. 31) Grain & grain products | $ | 3,926 | $ | 3,828 | $ | 3,644 | 3 | % | 5 | %
[7 ¶45] (p. 31) Fertilizer | 856 | 811 | 757 | 6 | 7
[7 ¶46] (p. 31) Food & refrigerated | 1,018 | 1,085 | 1,041 | (6) | 4
[7 ¶47] (p. 31) Coal & renewables | 1,786 | 1,483 | 1,916 | 20 | (23)
[7 ¶48] (p. 31) Bulk | 7,586 | 7,207 | 7,358 | 5 | (2)
[7 ¶49] (p. 31) Industrial chemicals & plastics | 2,512 | 2,345 | 2,176 | 7 | 8
[7 ¶50] (p. 31) Metals & minerals | 2,193 | 2,081 | 2,194 | 5 | (5)
[7 ¶51] (p. 31) Forest products | 1,290 | 1,326 | 1,347 | (3) | (2)
[7 ¶52] (p. 31) Energy & specialized markets | 2,609 | 2,688 | 2,521 | (3) | 7
[7 ¶53] (p. 31) Industrial | 8,604 | 8,440 | 8,238 | 2 | 2
[7 ¶54] (p. 31) Automotive | 2,398 | 2,452 | 2,421 | (2) | 1
[7 ¶55] (p. 31) Intermodal | 4,632 | 4,712 | 4,554 | (2) | 3
[7 ¶56] (p. 31) Premium | 7,030 | 7,164 | 6,975 | (2) | 3
[7 ¶57] (p. 31) Total | $ | 23,220 | $ | 22,811 | $ | 22,571 | 2 | % | 1 | %
[7 ¶58] (p. 31) Revenue carloads
[7 ¶59] (p. 31) Thousands
[7 ¶60] (p. 31) 2025 | 2024 | 2023 | % Change 2025 v 2024 | % Change 2024 v 2023
[7 ¶61] (p. 31) Grain & grain products | 880 | 850 | 798 | 4 | % | 7 | %
[7 ¶62] (p. 31) Fertilizer | 216 | 213 | 191 | 1 | 12
[7 ¶63] (p. 31) Food & refrigerated | 163 | 177 | 175 | (8) | 1
[7 ¶64] (p. 31) Coal & renewables | 797 | 702 | 867 | 14 | (19)
[7 ¶65] (p. 31) Bulk | 2,056 | 1,942 | 2,031 | 6 | (4)
[7 ¶66] (p. 31) Industrial chemicals & plastics | 704 | 672 | 645 | 5 | 4
[7 ¶67] (p. 31) Metals & minerals | 747 | 719 | 793 | 4 | (9)
[7 ¶68] (p. 31) Forest products | 203 | 213 | 213 | (5) | -
[7 ¶69] (p. 31) Energy & specialized markets | 587 | 607 | 582 | (3) | 4
[7 ¶70] (p. 31) Industrial | 2,241 | 2,211 | 2,233 | 1 | (1)
[7 ¶71] (p. 31) Automotive | 793 | 824 | 820 | (4) | -
[7 ¶72] (p. 31) Intermodal [a] | 3,357 | 3,357 | 3,028 | - | 11
[7 ¶73] (p. 31) Premium | 4,150 | 4,181 | 3,848 | (1) | 9
[7 ¶74] (p. 31) Total | 8,447 | 8,334 | 8,112 | 1 | % | 3 | %
[7 ¶75] (p. 31) Average revenue per car | 2025 | 2024 | 2023 | % Change 2025 v 2024 | % Change 2024 v 2023
[7 ¶76] (p. 31) Grain & grain products | $ | 4,461 | $ | 4,505 | $ | 4,567 | (1) | % | (1) | %
[7 ¶77] (p. 31) Fertilizer | 3,970 | 3,809 | 3,962 | 4 | (4)
[7 ¶78] (p. 31) Food & refrigerated | 6,233 | 6,104 | 5,929 | 2 | 3
[7 ¶79] (p. 31) Coal & renewables | 2,241 | 2,113 | 2,211 | 6 | (4)
[7 ¶80] (p. 31) Bulk | 3,690 | 3,710 | 3,623 | (1) | 2
[7 ¶81] (p. 31) Industrial chemicals & plastics | 3,568 | 3,493 | 3,374 | 2 | 4
[7 ¶82] (p. 31) Metals & minerals | 2,935 | 2,893 | 2,765 | 1 | 5
[7 ¶83] (p. 31) Forest products | 6,369 | 6,229 | 6,310 | 2 | (1)
[7 ¶84] (p. 31) Energy & specialized markets | 4,446 | 4,426 | 4,335 | - | 2
[7 ¶85] (p. 31) Industrial | 3,840 | 3,818 | 3,689 | 1 | 3
[7 ¶86] (p. 31) Automotive | 3,024 | 2,976 | 2,955 | 2 | 1
[7 ¶87] (p. 31) Intermodal [a] | 1,380 | 1,404 | 1,504 | (2) | (7)
[7 ¶88] (p. 31) Premium | 1,694 | 1,714 | 1,813 | (1) | (5)
[7 ¶89] (p. 31) Average | $ | 2,749 | $ | 2,737 | $ | 2,782 | - | % | (2) | %
[7 ¶90] (p. 31) [a]For intermodal shipments, each container or trailer equals one carload.
[7 ¶91] (p. 32) Bulk – Bulk includes shipments of grain and grain products, fertilizer, food and refrigerated, and coal and renewables. Freight revenues from bulk shipments increased in 2025 compared to 2024 due to 6% higher volumes and core pricing gains, partially offset by negative mix, from increased coal shipments, and lower fuel surcharge revenues. Bulk volume growth compared to 2024 was driven by […]
[7 ¶92] (p. 32) Industrial – Industrial includes shipments of industrial chemicals and plastics, metals and minerals, forest products, and energy and specialized markets. Freight revenues from industrial shipments increased in 2025 versus 2024 due to core pricing gains and higher volumes, partially offset by a negative mix of traffic, from increased rock and lower lumber shipments, and lower fuel surcharge […]
[7 ¶93] (p. 32) Premium – Premium includes shipments of finished automobiles, automotive parts, and merchandise in intermodal containers, both domestic and international. Freight revenues from premium shipments decreased in 2025 driven by lower fuel surcharge revenues, negative business mix from reduced automotive shipments, and lower volumes, partially offset by core pricing gains. The heavy demand from […]
[7 ¶94] (p. 32) 2025 Bulk Carloads
[7 ¶95] (p. 32) 2025 Industrial Carloads
[7 ¶96] (p. 32) 2025 Premium Carloads
[7 ¶97] (p. 32) Mexico business – Freight revenues from each of our commodity groups includes revenues from shipments to and from Mexico, which equated to $2.9 billion in 2025, down 1% compared to 2024, driven by a 2% reduction in ARC partially offset by 2% higher volumes. Compared to 2024, intermodal and grain and grain products volumes increased and were partially offset by lower auto parts and finished […]
[7 ¶98] (p. 32) Operating expenses
[7 ¶99] (p. 32) Millions | 2025 | 2024 | 2023 | % Change 2025 v 2024 | % Change 2024 v 2023
[7 ¶100] (p. 32) Compensation and benefits | $ | 4,897 | $ | 4,899 | $ | 4,818 | - | % | 2 | %
[7 ¶101] (p. 32) Purchased services and materials | 2,626 | 2,520 | 2,616 | 4 | (4)
[7 ¶102] (p. 32) Depreciation | 2,465 | 2,398 | 2,318 | 3 | 3
[7 ¶103] (p. 32) Fuel | 2,390 | 2,474 | 2,891 | (3) | (14)
[7 ¶104] (p. 32) Equipment and other rents | 912 | 920 | 947 | (1) | (3)
[7 ¶105] (p. 32) Other | 1,374 | 1,326 | 1,447 | 4 | (8)
[7 ¶106] (p. 32) Total | $ | 14,664 | $ | 14,537 | $ | 15,037 | 1 | % | (3) | %
[7 ¶107] (p. 33) Operating expenses increased $127 million, or 1%, in 2025 compared to 2024 driven by inflation, volume-related costs, acquisition-related expenses, and higher depreciation, partially offset by productivity and lower fuel prices. In addition, the year-over-year comparison was negatively impacted by a gain on the sale of intermodal equipment in 2024 and higher crew staffing agreement ratification […]
[7 ¶108] (p. 33) 2025 Operating Expenses
[7 ¶109] (p. 33) Compensation and benefits – Compensation and benefits include wages, payroll taxes, health and welfare costs, pension costs, and incentive costs. In 2025, expenses were essentially flat compared to 2024 due to wage inflation, increased volumes, higher incentive compensation, and increased crew needs associated with labor agreements, partially offset by 3% lower employee levels. Active train, […]
[7 ¶110] (p. 33) Purchased services and materials – Expense for purchased services and materials includes the costs of services purchased from outside contractors and other service providers (including equipment maintenance and contract expenses incurred by our subsidiaries for external transportation services); materials used to maintain the Railroad’s lines, structures, and equipment; costs of operating […]
[7 ¶111] (p. 33) Fuel – Fuel includes locomotive fuel and gasoline for highway and non-highway vehicles and heavy equipment. Fuel expense decreased compared to 2024 due to a 6% decrease in locomotive diesel fuel prices, declining from an average of $2.64 per gallon (including taxes and transportation costs) in 2024 to $2.49 per gallon in 2025, resulting in a $138 million decrease in expense (excluding any impact […]
[7 ¶112] (p. 33) Depreciation – The majority of depreciation relates to road property, including rail, ties, ballast, and other track material. Depreciation expense was up 3% in 2025 compared to 2024 due to a higher depreciable asset base.
[7 ¶113] (p. 33) Equipment and other rents – Equipment and other rents expense primarily includes rental expense that the Railroad pays for freight cars owned by other railroads or private companies; freight car, intermodal, and locomotive leases; and office and other rent expenses, offset by equity income from certain equity method investments. Equipment and other rents expense decreased 1% compared to 2024 due […]
[7 ¶114] (p. 33) Other – Other expenses include property taxes; freight, equipment, and property damage; utilities; insurance; personal injury; environmental; employee travel; telephone and cellular; computer software; bad debt; and other general expenses. Other expenses increased 4% in 2025 compared to 2024 driven by the negative comparison from a 2024 gain on the sale of intermodal equipment, in addition to, […]
[7 ¶115] (p. 34) Non-operating items
[7 ¶116] (p. 34) Millions | 2025 | 2024 | 2023 | % Change 2025 v 2024 | % Change 2024 v 2023
[7 ¶117] (p. 34) Other income, net | $ | 629 | $ | 350 | $ | 491 | 80 | % | (29) | %
[7 ¶118] (p. 34) Interest expense | (1,309) | (1,269) | (1,340) | 3 | (5)
[7 ¶119] (p. 34) Income tax expense | $ | (2,028) | $ | (2,047) | $ | (1,854) | (1) | % | 10 | %
[7 ¶120] (p. 34) Other income, net – Other income increased $279 million in 2025 compared to 2024 driven by $295 million in higher real estate income, including $250 million in industrial park land sales. The higher real estate income was partially offset by interest received in 2024 from the IRS on refund claims. See Note 6 to the Financial Statements and Supplementary Data, Item 8, for additional detail.
[7 ¶121] (p. 34) Interest expense – Interest expense increased 3% in 2025 compared to 2024 due to an increased weighted-average debt level of $32.1 billion in 2025 from $31.6 billion in 2024. In addition, the effective interest rate of 4.1% in 2025 increased from 4.0% in 2024.
[7 ¶122] (p. 34) Income tax expense – Income tax expense decreased in 2025 compared to 2024. While pre-tax income was higher in 2025, the increase was more than offset by a $115 million reduction in deferred tax expense resulting from newly enacted Kansas legislation, along with the favorable impact of purchased tax credits during the year. In 2024, the states of Louisiana and Arkansas enacted legislation to […]
[7 ¶123] (p. 34) OTHER OPERATING/PERFORMANCE AND FINANCIAL STATISTICS
[7 ¶124] (p. 34) We report a number of key performance measures weekly to the STB. We provide these on our website at https://investor.unionpacific.com/key-performance-metrics.
[7 ¶125] (p. 34) Operating/performance statistics
[7 ¶126] (p. 34) Management continuously monitors these key operating metrics to evaluate our operational efficiency in striving to deliver the service product we sold to our customers.
[7 ¶127] (p. 34) Railroad performance measures are included in the table below:
[7 ¶128] (p. 34) 2025 | 2024 | 2023 | % Change 2025 v 2024 | % Change 2024 v 2023
[7 ¶129] (p. 34) Gross ton-miles (GTMs) (billions) | 873.6 | 847.4 | 837.5 | 3 | % | 1 | %
[7 ¶130] (p. 34) Revenue ton-miles (billions) | 426.9 | 409.7 | 413.3 | 4 | (1)
[7 ¶131] (p. 34) Freight car velocity (daily miles per car) | 225 | 208 | 204 | 8 | 2
[7 ¶132] (p. 34) Average train speed (miles per hour) [a] | 24.3 | 23.6 | 24.2 | 3 | (2)
[7 ¶133] (p. 34) Average terminal dwell time (hours) [a] | 20.9 | 22.6 | 23.4 | (8) | (3)
[7 ¶134] (p. 34) Locomotive productivity (GTMs per horsepower day) | 139 | 135 | 129 | 3 | 5
[7 ¶135] (p. 34) Train length (feet) | 9,678 | 9,469 | 9,356 | 2 | 1
[7 ¶136] (p. 34) Intermodal service performance index (%) | 99 | 90 | 88 | 9 | pts | 2 | pts
[7 ¶137] (p. 34) Manifest service performance index (%) | 100 | 89 | 85 | 11 | pts | 4 | pts
[7 ¶138] (p. 34) Workforce productivity (car miles per employee) | 1,132 | 1,062 | 1,000 | 7 | 6
[7 ¶139] (p. 34) Total employees (average) | 29,287 | 30,336 | 31,490 | (3) | (4)
[7 ¶140] (p. 34) Operating ratio (%) | 59.8 | 59.9 | 62.3 | (0.1) | pts | (2.4) | pts
[7 ¶141] (p. 34) [a]As reported to the STB.
[7 ¶142] (p. 34) Gross and revenue ton-miles – Gross ton-miles are calculated by multiplying the weight of loaded and empty freight cars by the number of miles hauled. Revenue ton-miles are calculated by multiplying the weight of freight by the number of tariff miles. In 2025, gross ton-miles increased 3% and revenue ton-miles increased 4% on 1% higher carloadings year-over-year. Changes in commodity mix drove […]
[7 ¶143] (p. 35) Freight car velocity – Freight car velocity measures the average daily miles per car on our network. The two key drivers of this metric are the speed of the train between terminals (average train speed) and the time a rail car spends at the terminals (average terminal dwell time). Compared to 2024, freight car velocity increased 8% driven by record terminal dwell, which also improved 8%, and 3% […]
[7 ¶144] (p. 35) Locomotive productivity – Locomotive productivity is gross ton-miles per average daily locomotive horsepower. Locomotive productivity improved 3% in 2025 compared to 2024 driven by improved network fluidity and asset utilization.
[7 ¶145] (p. 35) Train length – Train length is the average maximum train length on a route measured in feet. Our train length increased 2% compared to 2024 due to train length improvement initiatives and increases in coal train length, coinciding with increased shipments.
[7 ¶146] (p. 35) Service performance index (SPI) – SPI is a ratio of the service customers are currently receiving relative to the best monthly performance over the last three years. Measuring our performance relative to a historical benchmark demonstrates our focus on continuously improving service for our customers, and we believe it is a better indicator of service performance than the previously disclosed […]
[7 ¶147] (p. 35) Workforce productivity – Workforce productivity is average daily car miles per employee. Workforce productivity improved 7% in 2025 as average daily car miles increased 3% while employees decreased 3% compared to 2024. We adequately aligned our active TE&Y workforce to support carload demand while maintaining an adequate training pipeline to provide a capacity buffer to enable responsiveness in […]
[7 ¶148] (p. 35) Operating ratio – Operating ratio is our operating expenses reflected as a percentage of operating revenues. Our operating ratio of 59.8% improved 0.1 points compared to 2024 driven by core pricing gains and productivity initiatives, partially offset by the impact of negative business mix, inflation, and acquisition-related expenses. In addition, operating ratio year-over-year comparison was […]
[7 ¶149] (p. 35) Return on average common shareholders’ equity
[7 ¶150] (p. 35) Millions, except percentages | 2025 | 2024 | 2023
[7 ¶151] (p. 35) Net income | $ | 7,138 | $ | 6,747 | $ | 6,379
[7 ¶152] (p. 35) Average equity | $ | 17,679 | $ | 15,839 | $ | 13,476
[7 ¶153] (p. 35) Return on average common shareholders' equity | 40.4 | % | 42.6 | % | 47.3 | %
[7 ¶154] (p. 35) Return on invested capital as adjusted (ROIC)
[7 ¶155] (p. 35) Millions, except percentages | 2025 | 2024 | 2023
[7 ¶156] (p. 35) Net income | $ | 7,138 | $ | 6,747 | $ | 6,379
[7 ¶157] (p. 35) Interest expense | 1,309 | 1,269 | 1,340
[7 ¶158] (p. 35) Interest on average operating lease liabilities | 46 | 55 | 58
[7 ¶159] (p. 35) Taxes on interest | (299) | (308) | (315)
[7 ¶160] (p. 35) Net operating profit after taxes as adjusted | $ | 8,194 | $ | 7,763 | $ | 7,462
[7 ¶161] (p. 35) Average equity | $ | 17,679 | $ | 15,839 | $ | 13,476
[7 ¶162] (p. 35) Average debt | 31,503 | 31,886 | 32,953
[7 ¶163] (p. 35) Average operating lease liabilities | 1,140 | 1,436 | 1,616
[7 ¶164] (p. 35) Average invested capital as adjusted | $ | 50,322 | $ | 49,161 | $ | 48,045
[7 ¶165] (p. 35) Return on invested capital as adjusted | 16.3 | % | 15.8 | % | 15.5 | %
[7 ¶166] (p. 35) ROIC is considered a non-GAAP financial measure by SEC Regulation G and Item 10 of SEC Regulation S-K and may not be defined and calculated by other companies in the same manner. We believe this measure is important to management and investors in evaluating the efficiency and effectiveness of our long-term capital investments. In addition, we currently use ROIC as a performance criterion in […]
[7 ¶167] (p. 36) Debt / net income
[7 ¶168] (p. 36) Millions, except ratios | 2025 | 2024 | 2023
[7 ¶169] (p. 36) Debt | $ | 31,814 | $ | 31,192 | $ | 32,579
[7 ¶170] (p. 36) Net income | $ | 7,138 | $ | 6,747 | $ | 6,379
[7 ¶171] (p. 36) Debt / net income | 4.5 | 4.6 | 5.1
[7 ¶172] (p. 36) Adjusted debt / adjusted EBITDA
[7 ¶173] (p. 36) Millions, except ratios | 2025 | 2024 | 2023
[7 ¶174] (p. 36) Net income | $ | 7,138 | $ | 6,747 | $ | 6,379
[7 ¶175] (p. 36) Add:
[7 ¶176] (p. 36) Income tax expense | 2,028 | 2,047 | 1,854
[7 ¶177] (p. 36) Depreciation | 2,465 | 2,398 | 2,318
[7 ¶178] (p. 36) Interest expense | 1,309 | 1,269 | 1,340
[7 ¶179] (p. 36) EBITDA | $ | 12,940 | $ | 12,461 | $ | 11,891
[7 ¶180] (p. 36) Adjustments:
[7 ¶181] (p. 36) Other income, net | (629) | (350) | (491)
[7 ¶182] (p. 36) Interest on operating lease liabilities [1] | 40 | 48 | 58
[7 ¶183] (p. 36) Adjusted EBITDA (a) | $ | 12,351 | $ | 12,159 | $ | 11,458
[7 ¶184] (p. 36) Debt | $ | 31,814 | $ | 31,192 | $ | 32,579
[7 ¶185] (p. 36) Operating lease liabilities | 1,008 | 1,271 | 1,600
[7 ¶186] (p. 36) Adjusted debt (b) | $ | 32,822 | $ | 32,463 | $ | 34,179
[7 ¶187] (p. 36) Adjusted debt / adjusted EBITDA (b/a) | 2.7 | 2.7 | 3.0
[7 ¶188] (p. 36) [1]Represents the hypothetical interest expense we would incur (using the incremental borrowing rate) if the property under our operating leases were owned or accounted for as finance leases.
[7 ¶189] (p. 36) Adjusted debt (total debt plus operating lease liabilities plus after-tax unfunded pension and OPEB (other post-retirement benefit obligations) to adjusted EBITDA (earnings before interest, taxes, depreciation, amortization, and adjustments for other income and interest on present value of operating leases) is considered a non-GAAP financial measure by SEC Regulation G and Item 10 of SEC […]
[7 ¶190] (p. 36) LIQUIDITY AND CAPITAL RESOURCES
[7 ¶191] (p. 36) We are continually evaluating our financial condition and liquidity. We analyze a wide range of economic scenarios and the impact on our ability to generate cash. These analyses inform our liquidity plans and activities outlined below and indicate we have sufficient borrowing capacity to sustain an extended period of lower volumes.
[7 ¶192] (p. 36) At both December 31, 2025 and 2024, we had a working capital deficit due to upcoming debt maturities. It is not unusual for us to have a working capital deficit, and we believe it is not an indication of a lack of liquidity. We generate strong cash from operations and also maintain adequate resources, including our credit facility and, when necessary, access the capital markets to meet […]
[7 ¶193] (p. 36) During 2025, we generated $9.3 billion of cash provided by operating activities, paid down $1.4 billion of long-term debt, paid $3.2 billion in dividends, and repurchased shares totaling $2.7 billion. We also announced the pending acquisition of Norfolk Southern described in Note 20 to the Financial Statements and Supplementary Data, Item 8, and paused our share repurchase program. We have been, […]
[7 ¶194] (p. 37) Our principal sources of liquidity include cash and cash equivalents, our Receivables Facility, our revolving credit facility, as well as, the availability of commercial paper and other sources of financing through the capital markets. On December 31, 2025, we had $1.3 billion of cash and cash equivalents, $250 million of short-term investments, $2.0 billion of committed credit available under […]
[7 ¶195] (p. 37) As described in the notes to the Consolidated Financial Statements and as referenced in the table below, we have contractual obligations that may affect our financial condition. Based on our assessment of the underlying provisions and circumstances of our contractual obligations, other than the risks that we and other similarly situated companies face with respect to the condition of the capital […]
[7 ¶196] (p. 37) The following table identifies material contractual obligations as of December 31, 2025:
[7 ¶197] (p. 37) Payments due by December 31, Millions
[7 ¶198] (p. 37) Total | 2026 | 2027 | 2028 | 2029 | 2030 | After
[7 ¶199] (p. 37) 2030
[7 ¶200] (p. 37) Debt [a] | $ | 59,424 | $ | 2,724 | $ | 2,455 | $ | 2,402 | $ | 2,360 | $ | 1,816 | $ | 47,667
[7 ¶201] (p. 37) Purchase obligations [b] | 2,537 | 817 | 579 | 434 | 389 | 302 | 16
[7 ¶202] (p. 37) Operating leases [c] | 1,125 | 276 | 238 | 191 | 123 | 121 | 176
[7 ¶203] (p. 37) Other post-retirement benefits [d] | 355 | 36 | 36 | 36 | 36 | 36 | 175
[7 ¶204] (p. 37) Finance lease obligations [e] | 114 | 42 | 37 | 14 | 21 | - | -
[7 ¶205] (p. 37) Total contractual obligations | $ | 63,555 | $ | 3,895 | $ | 3,345 | $ | 3,077 | $ | 2,929 | $ | 2,275 | $ | 48,034
[7 ¶206] (p. 37) [a]Excludes finance lease obligations of $105 million as well as unamortized discount and deferred issuance costs of ($1,678) million. Includes an interest component of $26,037 million.
[7 ¶207] (p. 37) [b]Purchase obligations include locomotive maintenance contracts; purchase commitments for ties, ballast, and rail; and agreements to purchase other goods and services.
[7 ¶208] (p. 37) [c]Includes leases for locomotives, freight cars, other equipment, and real estate. Includes an interest component of $117 million.
[7 ¶209] (p. 37) [d]Includes estimated other post-retirement medical payments and payments made under the unfunded pension plan for the next ten years.
[7 ¶210] (p. 37) [e]Represents total obligations, including an interest component of $9 million.
[7 ¶211] (p. 37) Cash flows
[7 ¶212] (p. 37) Millions | 2025 | 2024 | 2023
[7 ¶213] (p. 37) Cash provided by operating activities | $ | 9,290 | $ | 9,346 | $ | 8,379
[7 ¶214] (p. 37) Cash used in investing activities | (3,762) | (3,325) | (3,667)
[7 ¶215] (p. 37) Cash used in financing activities | (5,276) | (6,067) | (4,625)
[7 ¶216] (p. 37) Net change in cash, cash equivalents, and restricted cash | $ | 252 | $ | (46) | $ | 87
[7 ¶217] (p. 37) Operating activities
[7 ¶218] (p. 37) Cash provided by operating activities decreased in 2025 compared to 2024 due to timing of payments to taxing authorities and purchased tax credits.
[7 ¶219] (p. 38) On July 4, 2025, H.R.1 was enacted that makes key elements of the 2017 Tax Cuts and Jobs Act permanent, including provisions for 100% bonus depreciation on qualified property and fully expensing internally developed software, which has and will continue to favorably impact our cash provided by operating activities.
[7 ¶220] (p. 38) Cash flow conversion is defined as cash provided by operating activities less cash used in capital investments as a ratio of net income. Cash flow conversion rate is not considered a financial measure under GAAP by SEC Regulation G and Item 10 of SEC Regulation S-K and may not be defined and calculated by other companies in the same manner. We believe cash flow conversion rate is important to […]
[7 ¶221] (p. 38) Millions, except percentages | 2025 | 2024 | 2023
[7 ¶222] (p. 38) Cash provided by operating activities | $ | 9,290 | $ | 9,346 | $ | 8,379
[7 ¶223] (p. 38) Cash used in capital investments | (3,791) | (3,452) | (3,606)
[7 ¶224] (p. 38) Total (a) | 5,499 | 5,894 | 4,773
[7 ¶225] (p. 38) Net income (b) | $ | 7,138 | $ | 6,747 | $ | 6,379
[7 ¶226] (p. 38) Cash flow conversion rate (a/b) | 77 | % | 87 | % | 75 | %
[7 ¶227] (p. 38) Investing activities
[7 ¶228] (p. 38) Cash used in investing activities in 2025 increased compared to 2024 primarily driven by higher capital investments and the purchase of short term investments, partially offset by higher proceeds from real estate sales.
[7 ¶229] (p. 38) The following table details cash capital investments for the years ended December 31:
[7 ¶230] (p. 38) Millions | 2025 | 2024 | 2023
[7 ¶231] (p. 38) Ties | $ | 523 | $ | 503 | $ | 565
[7 ¶232] (p. 38) Rail and other track material | 562 | 493 | 454
[7 ¶233] (p. 38) Ballast | 197 | 197 | 194
[7 ¶234] (p. 38) Other [a] | 705 | 740 | 691
[7 ¶235] (p. 38) Total road infrastructure replacements | 1,987 | 1,933 | 1,904
[7 ¶236] (p. 38) Line expansion and other capacity projects | 258 | 183 | 239
[7 ¶237] (p. 38) Commercial facilities | 359 | 317 | 425
[7 ¶238] (p. 38) Total capacity and commercial facilities | 617 | 500 | 664
[7 ¶239] (p. 38) Locomotives and freight cars [b] | 810 | 788 | 728
[7 ¶240] (p. 38) Technology and other | 377 | 231 | 310
[7 ¶241] (p. 38) Total cash capital investments [c] | $ | 3,791 | $ | 3,452 | $ | 3,606
[7 ¶242] (p. 38) [a]Other includes bridges and tunnels, signals, other road assets, and road work equipment.
[7 ¶243] (p. 38) [b]Locomotives and freight cars include lease buyouts of $311 million, $143 million, and $57 million in 2025, 2024, and 2023, respectively.
[7 ¶244] (p. 38) [c]Weather-related damages for 2025, 2024, and 2023 are immaterial.
[7 ¶245] (p. 38) See Note 20 to the Financial Statements and Supplementary Data, Item 8, for information regarding the pending acquisition of Norfolk Southern.
[7 ¶246] (p. 38) Capital plan
[7 ¶247] (p. 38) In 2026, we expect our capital plan to be approximately $3.3 billion. We plan to continue to make investments to support our growth strategy, improve the safety, resiliency, and operational efficiency of the network, harden our infrastructure, and replace older assets, including modernization of our locomotive fleet and acquiring freight cars to support replacement and growth opportunities. In […]
[7 ¶248] (p. 39) Financing activities
[7 ¶249] (p. 39) Cash used in financing activities decreased in 2025 compared to 2024 driven by an increase of debt issued and a decrease in debt repaid, partially offset by an increase in share repurchases.
[7 ¶250] (p. 39) See Note 14 to the Financial Statements and Supplementary Data, Item 8, for a description of all our outstanding financing arrangements and significant new borrowings, Note 18 to the Financial Statements and Supplementary Data, Item 8, for a description of our share repurchase programs, and Note 20 to the Financial Statements and Supplementary Data, Item 8, for the pending acquisition of Norfolk […]
[7 ¶251] (p. 39) OTHER MATTERS
[7 ¶252] (p. 39) Inflation – For capital-intensive companies, inflation significantly increases asset replacement costs for long-lived assets. As a result, assuming that we replace all operating assets at current price levels, depreciation charges (on an inflation-adjusted basis) would be substantially greater than historically reported amounts.
[7 ¶253] (p. 39) Sensitivity analyses – The sensitivity analyses that follow illustrate the economic effect that hypothetical changes in interest and tax rates could have on our results of operations and financial condition. These hypothetical changes do not consider other factors that could impact actual results.
[7 ¶254] (p. 39) Interest rates – At both December 31, 2025, and 2024, we did not have variable-rate debt.
[7 ¶255] (p. 39) Market risk for fixed-rate debt is estimated as the potential increase in fair value resulting from a hypothetical 1% decrease in interest rates as of December 31, 2025, and 2024, and totals an increase of approximately $3.2 billion and $3.0 billion to the fair value of our debt at December 31, 2025, and 2024, respectively. We estimated the fair values of our fixed-rate debt by considering the […]
[7 ¶256] (p. 39) Tax rates – Our deferred tax assets and liabilities are measured based on current tax law. Future tax legislation, such as a change in the federal corporate tax rate, could have a material impact on our financial condition, results of operations, or liquidity. For example, as of December 31, 2025, a future, permanent 1% increase in our federal income tax rate would increase our deferred tax […]
[7 ¶257] (p. 39) Accounting pronouncements – See Note 3 to the Financial Statements and Supplementary Data, Item 8.
[7 ¶258] (p. 39) Asserted and unasserted claims – See Note 17 to the Financial Statements and Supplementary Data, Item 8.
[7 ¶259] (p. 39) Indemnities – See Note 17 to the Financial Statements and Supplementary Data, Item 8.
[7 ¶260] (p. 39) Pending Acquisition – See Note 20 to the Financial Statements and Supplementary Data, Item 8, and the Agreement and Plan of Merger dated as of July 28, 2025, by and among the Company, Ruby Merger Sub 1 Corporation, Ruby Merger Sub 2 LLC, and Norfolk Southern, which is incorporated herein by reference to Exhibit 2.1 to the Corporation’s Current Report on Form 8-K dated July 29, 2025.
[7 ¶261] (p. 39) Climate change – Climate change could have an adverse impact on our operations and financial performance (see Risk Factors under Item 1A of this report). We utilize climate scenario analyses to better understand climate-related risks and opportunities the Company may face in the future under a range of potential scenarios. We continue to refine our approach to understand climate-related risks and […]
[7 ¶262] (p. 39) We continue to take steps and explore opportunities to reduce our operational impact on the environment, including improving our operational fluidity to increase fuel efficiency, modernizing locomotives for improved reliability and fuel consumption, using renewable fuels, and exploring and testing low- and zero-emissions propulsion technologies. These initiatives are aligned with our strategy of […]
[7 ¶263] (p. 40) Personal injury – See Note 17 to the Financial Statements and Supplementary Data, Item 8, and "We may be subject to various claims and lawsuits that could result in significant expenditures" in the Risk Factors, Item 1A.
[7 ¶264] (p. 40) Our personal injury liability is subject to uncertainty due to unasserted claims, timing and outcome of claims, and evolving trends in litigation. There were no material changes to the assumptions used in the latest actuarial analysis.
[7 ¶265] (p. 40) Our personal injury liability balance and claims activity was as follows:
[7 ¶266] (p. 40) 2025 | 2024 | 2023
[7 ¶267] (p. 40) Ending liability balance at December 31 (millions) | $ | 413 | $ | 379 | $ | 383
[7 ¶268] (p. 40) Open claims, beginning balance | 1,567 | 1,871 | 2,036
[7 ¶269] (p. 40) New claims | 2,602 | 2,842 | 3,008
[7 ¶270] (p. 40) Settled or dismissed claims | (2,829) | (3,146) | (3,173)
[7 ¶271] (p. 40) Open claims, ending balance at December 31 | 1,340 | 1,567 | 1,871
[7 ¶272] (p. 40) Environmental costs – See Note 17 to the Financial Statements and Supplementary Data, Item 8; "We are subject to significant environmental laws and regulations" in the Risk Factors, Item 1A; and Environmental Matters in the Legal Proceedings, Item 3.
[7 ¶273] (p. 40) Our environmental liability is subject to several factors such as type of remediation, nature and volume of contaminate, number and financial viability of other potentially responsible parties, as well as uncertainty due to unknown alleged contamination, evolving trends in remediation techniques and final remedies, and changes in laws and regulations.
[7 ¶274] (p. 40) Our environmental liability balance and site activity was as follows:
[7 ¶275] (p. 40) 2025 | 2024 | 2023
[7 ¶276] (p. 40) Ending liability balance at December 31 (millions) | $ | 259 | $ | 268 | $ | 245
[7 ¶277] (p. 40) Open sites, beginning balance | 352 | 333 | 353
[7 ¶278] (p. 40) New sites | 73 | 84 | 74
[7 ¶279] (p. 40) Closed sites | (82) | (65) | (94)
[7 ¶280] (p. 40) Open sites, ending balance at December 31 | 343 | 352 | 333
[7 ¶281] (p. 40) Property and depreciation – See Note 11 to the Financial Statements and Supplementary Data, Item 8.
[7 ¶282] (p. 40) Assets purchased or constructed throughout the year are capitalized if they meet applicable minimum units of property.
[7 ¶283] (p. 40) Estimated service lives of depreciable railroad property may vary over time due to changes in physical use, technology, asset strategies, and other factors that will have an impact on the retirement profiles of our assets. We are not aware of any specific factors that are reasonably likely to significantly change the estimated service lives of our assets. Actual use and retirement of our assets […]
[7 ¶284] (p. 40) Changes in estimated useful lives of our assets due to the results of our depreciation studies could significantly impact future periods’ depreciation expense and have a material impact on our Consolidated Financial Statements. If the estimated useful lives of all depreciable assets were increased by one year, annual depreciation expense would decrease by approximately $81 million. If the […]
[7 ¶285] (p. 41) Pension plans – See Note 5 to the Financial Statements and Supplementary Data, Item 8.
[7 ¶286] (p. 41) The critical assumptions used to measure pension obligations and expenses are the discount rates and expected rate of return on pension assets.
[7 ¶287] (p. 41) We evaluate our critical assumptions at least annually, and selected assumptions are based on the following factors:
[7 ¶288] (p. 41) •We measure the service cost and interest cost components of our net periodic pension benefit/cost by using individual spot rates matched with separate cash flows for each future year. Discount rates are based on a Mercer yield curve of high-quality corporate bonds (rated AA by a recognized rating agency).
[7 ¶289] (p. 41) •Expected return on plan assets is based on our asset allocation mix and our historical return, taking into consideration current and expected market conditions.
[7 ¶290] (p. 41) The following tables present the key assumptions used to measure net periodic pension benefit/cost for 2026 and the estimated impact on 2026 net periodic pension benefit/cost relative to a change in those assumptions:
[7 ¶291] (p. 41) Assumptions
[7 ¶292] (p. 41) Discount rate for interest on benefit obligations | 4.94 | %
[7 ¶293] (p. 41) Discount rate for service cost | 5.88 | %
[7 ¶294] (p. 41) Discount rate for interest on service cost | 5.64 | %
[7 ¶295] (p. 41) Expected return on plan assets | 5.25 | %
[7 ¶296] (p. 41) Sensitivities
[7 ¶297] (p. 41) Millions
[7 ¶298] (p. 41) Increase in
[7 ¶299] (p. 41) pension cost
[7 ¶300] (p. 41) 0.25% decrease in discount rates | $ | -
[7 ¶301] (p. 41) 0.25% decrease in expected return on plan assets | $ | 12
[7 ¶302] (p. 41) The following table presents the net periodic pension benefit/cost for the years ended December 31:
[7 ¶303] (p. 41) Millions | Est.
[7 ¶304] (p. 41) 2026 | 2025 | 2024 | 2023
[7 ¶305] (p. 41) Net periodic pension (benefit)/cost | $ | (23) | $ | (14) | $ | (3) | $ | -
[7 ¶306] (p. 42) CAUTIONARY INFORMATION
[7 ¶307] (p. 42) Certain statements in this report, and statements in other reports or information filed or to be filed with the SEC (as well as information included in oral statements or other written statements made or to be made by us), are, or will be, forward-looking statements as defined by the Securities Act of 1933 and the Securities Exchange Act of 1934. These forward-looking statements and information […]
[7 ¶308] (p. 42) Forward-looking statements should not be read as a guarantee of future performance, results, or outcomes, and will not necessarily be accurate indications of the times that, or by which, such performance, results or outcomes will be achieved, if ever. Forward-looking statements and information are subject to risks and uncertainties that could cause actual performance or results to differ […]
[7 ¶309] (p. 42) The Risk Factors in Item 1A of this report could affect our future results and could cause those results or other outcomes to differ materially from those expressed or implied in any forward-looking statements or information. To the extent circumstances require or we deem it otherwise necessary, we will update or amend these risk factors in a Form 10-Q, Form 8-K, or subsequent Form 10-K. All […]
[7 ¶310] (p. 42) Forward-looking statements speak only as of the date the statement was made. We assume no obligation to update forward-looking information to reflect actual results, changes in assumptions, or changes in other factors affecting forward-looking information. If we do update one or more forward-looking statements, no inference should be drawn that we will make additional updates with respect thereto […]

### [7-LIQ] Item 7. Liquidity and Capital Resources
[7-LIQ ¶1] (p. 36) LIQUIDITY AND CAPITAL RESOURCES
[7-LIQ ¶2] (p. 36) We are continually evaluating our financial condition and liquidity. We analyze a wide range of economic scenarios and the impact on our ability to generate cash. These analyses inform our liquidity plans and activities outlined below and indicate we have sufficient borrowing capacity to sustain an extended period of lower volumes.
[7-LIQ ¶3] (p. 36) At both December 31, 2025 and 2024, we had a working capital deficit due to upcoming debt maturities. It is not unusual for us to have a working capital deficit, and we believe it is not an indication of a lack of liquidity. We generate strong cash from operations and also maintain adequate resources, including our credit facility and, when necessary, access the capital markets to meet foreseeable cash requirements.
[7-LIQ ¶4] (p. 36) During 2025, we generated $9.3 billion of cash provided by operating activities, paid down $1.4 billion of long-term debt, paid $3.2 billion in dividends, and repurchased shares totaling $2.7 billion. We also announced the pending acquisition of Norfolk Southern described in Note 20 to the Financial Statements and Supplementary Data, Item 8, and paused our share repurchase program. We have been, and we expect to continue to be, in compliance with our debt covenants.
[7-LIQ ¶5] (p. 37) Our principal sources of liquidity include cash and cash equivalents, our Receivables Facility, our revolving credit facility, as well as, the availability of commercial paper and other sources of financing through the capital markets. On December 31, 2025, we had $1.3 billion of cash and cash equivalents, $250 million of short-term investments, $2.0 billion of committed credit available under our revolving credit facility, and up to $600 million undrawn on the Receivables Facility. As of December 31, 2025, none of the revolving credit facility was drawn, and we did not draw on our revolving credit facility at any time during 2025. Our access to the Receivables Facility may be reduced or restricted if our bond ratings fall to certain levels below investment grade. If our bond rating were to deteriorate, it could have an adverse impact on our liquidity. Access to commercial paper, as well as, other capital market financing is dependent on market conditions. Deterioration of our operating results or financial condition due to internal or external factors could negatively impact our ability to access capital markets as a source of liquidity. Access to liquidity through the capital markets is also dependent on our financial stability. We expect that we will continue to have access to liquidity through any or all of the following sources or activities: (a) increasing the utilization of our Receivables Facility, (b) issuing commercial paper, (c) entering into bank loans, outside […]
[7-LIQ ¶6] (p. 37) As described in the notes to the Consolidated Financial Statements and as referenced in the table below, we have contractual obligations that may affect our financial condition. Based on our assessment of the underlying provisions and circumstances of our contractual obligations, other than the risks that we and other similarly situated companies face with respect to the condition of the capital markets (as described in Item 1A of Part II of this report), as of the date of this filing, there is no known trend, demand, commitment, event, or uncertainty that is reasonably likely to occur that would have a material adverse effect on our consolidated results of operations, financial condition, or liquidity. In addition, our commercial obligations, financings, and commitments are customary transactions that are like those of other comparable corporations, particularly within the transportation industry.
[7-LIQ ¶7] (p. 37) The following table identifies material contractual obligations as of December 31, 2025:
[7-LIQ ¶8] (p. 37) Payments due by December 31, Millions
[7-LIQ ¶9] (p. 37) Total | 2026 | 2027 | 2028 | 2029 | 2030 | After
[7-LIQ ¶10] (p. 37) 2030
[7-LIQ ¶11] (p. 37) Debt [a] | $ | 59,424 | $ | 2,724 | $ | 2,455 | $ | 2,402 | $ | 2,360 | $ | 1,816 | $ | 47,667
[7-LIQ ¶12] (p. 37) Purchase obligations [b] | 2,537 | 817 | 579 | 434 | 389 | 302 | 16
[7-LIQ ¶13] (p. 37) Operating leases [c] | 1,125 | 276 | 238 | 191 | 123 | 121 | 176
[7-LIQ ¶14] (p. 37) Other post-retirement benefits [d] | 355 | 36 | 36 | 36 | 36 | 36 | 175
[7-LIQ ¶15] (p. 37) Finance lease obligations [e] | 114 | 42 | 37 | 14 | 21 | - | -
[7-LIQ ¶16] (p. 37) Total contractual obligations | $ | 63,555 | $ | 3,895 | $ | 3,345 | $ | 3,077 | $ | 2,929 | $ | 2,275 | $ | 48,034
[7-LIQ ¶17] (p. 37) [a]Excludes finance lease obligations of $105 million as well as unamortized discount and deferred issuance costs of ($1,678) million. Includes an interest component of $26,037 million.
[7-LIQ ¶18] (p. 37) [b]Purchase obligations include locomotive maintenance contracts; purchase commitments for ties, ballast, and rail; and agreements to purchase other goods and services.
[7-LIQ ¶19] (p. 37) [c]Includes leases for locomotives, freight cars, other equipment, and real estate. Includes an interest component of $117 million.
[7-LIQ ¶20] (p. 37) [d]Includes estimated other post-retirement medical payments and payments made under the unfunded pension plan for the next ten years.
[7-LIQ ¶21] (p. 37) [e]Represents total obligations, including an interest component of $9 million.
[7-LIQ ¶22] (p. 37) Cash flows
[7-LIQ ¶23] (p. 37) Millions | 2025 | 2024 | 2023
[7-LIQ ¶24] (p. 37) Cash provided by operating activities | $ | 9,290 | $ | 9,346 | $ | 8,379
[7-LIQ ¶25] (p. 37) Cash used in investing activities | (3,762) | (3,325) | (3,667)
[7-LIQ ¶26] (p. 37) Cash used in financing activities | (5,276) | (6,067) | (4,625)
[7-LIQ ¶27] (p. 37) Net change in cash, cash equivalents, and restricted cash | $ | 252 | $ | (46) | $ | 87
[7-LIQ ¶28] (p. 37) Operating activities
[7-LIQ ¶29] (p. 37) Cash provided by operating activities decreased in 2025 compared to 2024 due to timing of payments to taxing authorities and purchased tax credits.
[7-LIQ ¶30] (p. 38) On July 4, 2025, H.R.1 was enacted that makes key elements of the 2017 Tax Cuts and Jobs Act permanent, including provisions for 100% bonus depreciation on qualified property and fully expensing internally developed software, which has and will continue to favorably impact our cash provided by operating activities.
[7-LIQ ¶31] (p. 38) Cash flow conversion is defined as cash provided by operating activities less cash used in capital investments as a ratio of net income. Cash flow conversion rate is not considered a financial measure under GAAP by SEC Regulation G and Item 10 of SEC Regulation S-K and may not be defined and calculated by other companies in the same manner. We believe cash flow conversion rate is important to management and investors in evaluating our financial performance and measures our ability to generate cash without additional external financing. Cash flow conversion rate should be considered in addition to, rather than as a substitute for, cash provided by operating activities. The following table reconciles cash provided by operating activities (GAAP measure) to cash flow conversion rate (non-GAAP measure):
[7-LIQ ¶32] (p. 38) Millions, except percentages | 2025 | 2024 | 2023
[7-LIQ ¶33] (p. 38) Cash provided by operating activities | $ | 9,290 | $ | 9,346 | $ | 8,379
[7-LIQ ¶34] (p. 38) Cash used in capital investments | (3,791) | (3,452) | (3,606)
[7-LIQ ¶35] (p. 38) Total (a) | 5,499 | 5,894 | 4,773
[7-LIQ ¶36] (p. 38) Net income (b) | $ | 7,138 | $ | 6,747 | $ | 6,379
[7-LIQ ¶37] (p. 38) Cash flow conversion rate (a/b) | 77 | % | 87 | % | 75 | %
[7-LIQ ¶38] (p. 38) Investing activities
[7-LIQ ¶39] (p. 38) Cash used in investing activities in 2025 increased compared to 2024 primarily driven by higher capital investments and the purchase of short term investments, partially offset by higher proceeds from real estate sales.
[7-LIQ ¶40] (p. 38) The following table details cash capital investments for the years ended December 31:
[7-LIQ ¶41] (p. 38) Millions | 2025 | 2024 | 2023
[7-LIQ ¶42] (p. 38) Ties | $ | 523 | $ | 503 | $ | 565
[7-LIQ ¶43] (p. 38) Rail and other track material | 562 | 493 | 454
[7-LIQ ¶44] (p. 38) Ballast | 197 | 197 | 194
[7-LIQ ¶45] (p. 38) Other [a] | 705 | 740 | 691
[7-LIQ ¶46] (p. 38) Total road infrastructure replacements | 1,987 | 1,933 | 1,904
[7-LIQ ¶47] (p. 38) Line expansion and other capacity projects | 258 | 183 | 239
[7-LIQ ¶48] (p. 38) Commercial facilities | 359 | 317 | 425
[7-LIQ ¶49] (p. 38) Total capacity and commercial facilities | 617 | 500 | 664
[7-LIQ ¶50] (p. 38) Locomotives and freight cars [b] | 810 | 788 | 728
[7-LIQ ¶51] (p. 38) Technology and other | 377 | 231 | 310
[7-LIQ ¶52] (p. 38) Total cash capital investments [c] | $ | 3,791 | $ | 3,452 | $ | 3,606
[7-LIQ ¶53] (p. 38) [a]Other includes bridges and tunnels, signals, other road assets, and road work equipment.
[7-LIQ ¶54] (p. 38) [b]Locomotives and freight cars include lease buyouts of $311 million, $143 million, and $57 million in 2025, 2024, and 2023, respectively.
[7-LIQ ¶55] (p. 38) [c]Weather-related damages for 2025, 2024, and 2023 are immaterial.
[7-LIQ ¶56] (p. 38) See Note 20 to the Financial Statements and Supplementary Data, Item 8, for information regarding the pending acquisition of Norfolk Southern.
[7-LIQ ¶57] (p. 38) Capital plan
[7-LIQ ¶58] (p. 38) In 2026, we expect our capital plan to be approximately $3.3 billion. We plan to continue to make investments to support our growth strategy, improve the safety, resiliency, and operational efficiency of the network, harden our infrastructure, and replace older assets, including modernization of our locomotive fleet and acquiring freight cars to support replacement and growth opportunities. In addition, the plan includes investments in growth-related projects to drive more carloads to the network and enhance productivity. This includes terminal investments supporting our manifest network and intermodal ramps to efficiently handle new and existing customers, along with siding investments (extensions and new), and second mainline track projects. The capital plan may be revised if business conditions warrant or if laws or regulations affect our ability to generate sufficient returns on these investments.
[7-LIQ ¶59] (p. 39) Financing activities
[7-LIQ ¶60] (p. 39) Cash used in financing activities decreased in 2025 compared to 2024 driven by an increase of debt issued and a decrease in debt repaid, partially offset by an increase in share repurchases.
[7-LIQ ¶61] (p. 39) See Note 14 to the Financial Statements and Supplementary Data, Item 8, for a description of all our outstanding financing arrangements and significant new borrowings, Note 18 to the Financial Statements and Supplementary Data, Item 8, for a description of our share repurchase programs, and Note 20 to the Financial Statements and Supplementary Data, Item 8, for the pending acquisition of Norfolk Southern.

### [7A] Item 7A. Market Risk (in Item 7, Other Matters) (Item 7A refers to 'Other Matters' in Item 7; that part is used here)
[7A ¶1] (p. 39) OTHER MATTERS
[7A ¶2] (p. 39) Inflation – For capital-intensive companies, inflation significantly increases asset replacement costs for long-lived assets. As a result, assuming that we replace all operating assets at current price levels, depreciation charges (on an inflation-adjusted basis) would be substantially greater than historically reported amounts.
[7A ¶3] (p. 39) Sensitivity analyses – The sensitivity analyses that follow illustrate the economic effect that hypothetical changes in interest and tax rates could have on our results of operations and financial condition. These hypothetical changes do not consider other factors that could impact actual results.
[7A ¶4] (p. 39) Interest rates – At both December 31, 2025, and 2024, we did not have variable-rate debt.
[7A ¶5] (p. 39) Market risk for fixed-rate debt is estimated as the potential increase in fair value resulting from a hypothetical 1% decrease in interest rates as of December 31, 2025, and 2024, and totals an increase of approximately $3.2 billion and $3.0 billion to the fair value of our debt at December 31, 2025, and 2024, respectively. We estimated the fair values of our fixed-rate debt by considering the impact of the hypothetical interest rates on quoted market prices and current borrowing rates.
[7A ¶6] (p. 39) Tax rates – Our deferred tax assets and liabilities are measured based on current tax law. Future tax legislation, such as a change in the federal corporate tax rate, could have a material impact on our financial condition, results of operations, or liquidity. For example, as of December 31, 2025, a future, permanent 1% increase in our federal income tax rate would increase our deferred tax liability by approximately $550 million. Similarly, a future, permanent 1% decrease in our federal income tax rate would decrease our deferred tax liability by approximately $550 million. As of December 31, 2024, a permanent 1% increase or decrease in our federal income tax rate would have correspondingly increased or decreased our deferred tax liability by approximately $525 million, respectively.
[7A ¶7] (p. 39) Accounting pronouncements – See Note 3 to the Financial Statements and Supplementary Data, Item 8.
[7A ¶8] (p. 39) Asserted and unasserted claims – See Note 17 to the Financial Statements and Supplementary Data, Item 8.
[7A ¶9] (p. 39) Indemnities – See Note 17 to the Financial Statements and Supplementary Data, Item 8.
[7A ¶10] (p. 39) Pending Acquisition – See Note 20 to the Financial Statements and Supplementary Data, Item 8, and the Agreement and Plan of Merger dated as of July 28, 2025, by and among the Company, Ruby Merger Sub 1 Corporation, Ruby Merger Sub 2 LLC, and Norfolk Southern, which is incorporated herein by reference to Exhibit 2.1 to the Corporation’s Current Report on Form 8-K dated July 29, 2025.
[7A ¶11] (p. 39) Climate change – Climate change could have an adverse impact on our operations and financial performance (see Risk Factors under Item 1A of this report). We utilize climate scenario analyses to better understand climate-related risks and opportunities the Company may face in the future under a range of potential scenarios. We continue to refine our approach to understand climate-related risks and are taking an iterative approach in our business planning processes as risk factors, solutions, and technology develop. However, we are unable to predict the likelihood, manner, severity, or ultimate financial impact of actual future incidents as climate scenario analysis considers a range of potential outcomes.
[7A ¶12] (p. 39) We continue to take steps and explore opportunities to reduce our operational impact on the environment, including improving our operational fluidity to increase fuel efficiency, modernizing locomotives for improved reliability and fuel consumption, using renewable fuels, and exploring and testing low- and zero-emissions propulsion technologies. These initiatives are aligned with our strategy of Safety, Service, and Operational Excellence leading to Growth. (See further discussion in "Sustainable Future" in the Operations section in Item 1 of this report.)

### [ACQ] Note 20. Pending Acquisition (Norfolk Southern)
[ACQ ¶1] (p. 74) 20. Pending Acquisition
[ACQ ¶2] (p. 74) Norfolk Southern Corporation (Norfolk Southern), a Virginia corporation, is one of the nation’s premier transportation companies, moving goods and materials that help drive the U.S. economy. Norfolk Southern connects customers to markets and communities to economic opportunity with safe, reliable, and cost-effective shipping solutions. Its Norfolk Southern Railway Company subsidiary operates in 22 states and the District of Columbia. Norfolk Southern is a major transporter of industrial […]
[ACQ ¶3] (p. 74) On July 28, 2025, Union Pacific, Norfolk Southern, Ruby Merger Sub 1 Corporation, and Ruby Merger Sub 2 LLC, entered into an agreement and plan of merger (the merger agreement). The merger agreement provides, among other things, for the acquisition of Norfolk Southern by Union Pacific, subject to the satisfaction or waiver of the conditions specified therein, through two mergers: (i) first, Ruby Merger Sub 1 Corporation will merge with and into Norfolk Southern with Norfolk Southern surviving […]
[ACQ ¶4] (p. 74) At the effective time of the first merger (first effective time), each share of Norfolk Southern common stock issued and outstanding immediately prior to the first effective time, except for shares held by Union Pacific or Norfolk Southern, or their direct or indirect subsidiaries (other than, with respect to shares held by Union Pacific, Norfolk Southern, Ruby Merger Sub 1 Corporation, or Ruby Merger Sub 2 LLC, shares held on behalf of third parties), will be converted automatically into the […]
[ACQ ¶5] (p. 75) The combination of Norfolk Southern and Union Pacific would create America’s first transcontinental railroad that spans over 50,000 miles across 43 states with access to 10 international interchanges and approximately 100 ports.
[ACQ ¶6] (p. 75) Union Pacific filed a registration statement on Form S-4 (File No. 333-290282), which the SEC declared effective on September 30, 2025. Union Pacific and Norfolk Southern each also filed definitive proxy statements on October 1, 2025. Both Union Pacific's and Norfolk Southern's special meetings of shareholders was held on November 14, 2025. Union Pacific shareholders approved the share issuance proposal, and Norfolk Southern shareholders approved the merger agreement proposal (each as described […]
[ACQ ¶7] (p. 75) Completion of the mergers is conditioned on the receipt of Surface Transportation Board (STB) approval and a number of other conditions before the mergers can be consummated, as described in the merger agreement. On December 19, 2025, Union Pacific and Norfolk Southern (applicants) submitted a joint application to the STB seeking approval of the mergers. On December 19, 2025, the STB issued a decision inviting public comment on the application's completeness. Comments were due December 29, […]
[ACQ ¶8] (p. 75) Norfolk Southern's management and Board of Directors will continue to manage Norfolk Southern until the first effective time, pursuing its independent business plans and growth strategies. Subject to completion of the mergers, the acquisition is expected to be accounted for as a business combination using the acquisition method of accounting and currently expected to be completed in 2027.
[ACQ ¶9] (p. 75) Union Pacific incurred the following acquisition-related expense associated with the merger agreement for the year ended December 31:
[ACQ ¶10] (p. 75) Millions | 2025
[ACQ ¶11] (p. 75) Acquisition-related expense
[ACQ ¶12] (p. 75) Purchased services and materials | $ | 68
[ACQ ¶13] (p. 75) Other | 4
[ACQ ¶14] (p. 75) Total acquisition-related expense [a] | $ | 72
[ACQ ¶15] (p. 75) [a]Certain acquisition-related costs are non-deductible for income tax purposes.
[ACQ ¶16] (p. 75) At December 31, 2025, deferred share issuance costs of $13 million was recorded and will be recognized in paid-in-surplus upon completion of the mergers.
[ACQ ¶17] (p. 75) Both Union Pacific and Norfolk Southern may be required to pay the other a termination fee of $2.5 billion if the merger agreement is terminated under certain circumstances described in the merger agreement.

### [DEBT] Debt note (financial statements)
[DEBT ¶1] (p. 69) 14. Debt
[DEBT ¶2] (p. 69) Total debt as of December 31, 2025 and 2024, is summarized below:
[DEBT ¶3] (p. 69) Millions | 2025 | 2024
[DEBT ¶4] (p. 69) Notes and debentures, 2.3% to 7.2% due through February 14, 2072
[DEBT ¶5] (p. 69) $ | 32,694 | $ | 32,044
[DEBT ¶6] (p. 69) Equipment obligations, 2.6% to 6.2% due through January 2, 2031 [a]
[DEBT ¶7] (p. 69) 693 | 732
[DEBT ¶8] (p. 69) Finance leases, 3.1% to 6.8% due through August 21, 2029
[DEBT ¶9] (p. 69) 105 | 109
[DEBT ¶10] (p. 69) Unamortized discount and deferred issuance costs | (1,678) | (1,693)
[DEBT ¶11] (p. 69) Total debt | 31,814 | 31,192
[DEBT ¶12] (p. 69) Less: current portion | (1,520) | (1,425)
[DEBT ¶13] (p. 69) Total long-term debt | $ | 30,294 | $ | 29,767
[DEBT ¶14] (p. 69) [a]Equipment obligations are secured by an interest in certain railroad equipment with a carrying value of approximately $0.8 billion at both December 31, 2025 and 2024.
[DEBT ¶15] (p. 69) Debt maturities – The following table presents aggregate debt maturities as of December 31, 2025, excluding market value adjustments:
[DEBT ¶16] (p. 69) Millions
[DEBT ¶17] (p. 69) 2026 | $ | 1,521
[DEBT ¶18] (p. 69) 2027 | 1,291
[DEBT ¶19] (p. 69) 2028 | 1,239
[DEBT ¶20] (p. 69) 2029 | 1,276
[DEBT ¶21] (p. 69) 2030 | 753
[DEBT ¶22] (p. 69) Thereafter | 27,412
[DEBT ¶23] (p. 69) Total principal | 33,492
[DEBT ¶24] (p. 69) Unamortized discount and deferred issuance costs | (1,678)
[DEBT ¶25] (p. 69) Total debt | $ | 31,814
[DEBT ¶26] (p. 69) Credit facilities – At December 31, 2025, we had $2.0 billion of credit available under our revolving credit facility (the Facility), which is designated for general corporate purposes and supports the issuance of commercial paper. During 2025, we issued $0 and repaid $0 through the Facility. As of both December 31, 2025 and 2024, we had $0 outstanding with the Facility. Commitment fees and interest rates payable under the Facility are similar to fees and rates available to comparably rated, investment-grade borrowers. The Facility allows for borrowings at floating rates based on Term Secured Overnight Financing Rate (SOFR), plus a spread, depending upon credit ratings for our senior unsecured debt. The Facility, set to expire May 20, 2027, requires UPC to maintain an adjusted debt-to-EBITDA (earnings before interest, taxes, depreciation, and amortization) coverage ratio.
[DEBT ¶27] (p. 70) The definition of debt used for purposes of calculating the adjusted debt-to-EBITDA coverage ratio includes, among other things, certain credit arrangements, finance leases, guarantees, unfunded and vested pension benefits under Title IV of Employee Retirement Income Security Act of 1974 (ERISA), and unamortized debt discount and deferred debt issuance costs. At December 31, 2025, the Company was in compliance with the adjusted debt-to-EBITDA coverage ratio, which allows us to carry up to $47.7 billion of debt (as defined in the Facility), and we had $33.5 billion of debt (as defined in the Facility) outstanding at that date. The Facility does not include any other financial restrictions, credit rating triggers (other than rating-dependent pricing), or any other provision that could require us to post collateral. The Facility also includes a $150 million cross-default provision and a change-of-control provision.
[DEBT ¶28] (p. 70) During 2025, we issued $0 and repaid $0 of commercial paper. As of both December 31, 2025 and 2024, we had $0 of commercial paper outstanding. Our revolving credit facility supports our outstanding commercial paper balances, and, unless we change the terms of our commercial paper program, our aggregate issuance of commercial paper will not exceed the amount of borrowings available under the Facility.
[DEBT ¶29] (p. 70) Shelf registration statement and significant new borrowings – We filed an automatic shelf registration statement with the SEC that became effective on February 13, 2024. On July 28, 2025, the Board of Directors authorized the issuance of up to $20.0 billion of debt securities, replacing the prior authorization from 2024, which had $7.0 billion of authority remaining. Under our shelf registration, we may issue, from time to time, any combination of debt securities, preferred stock, common stock, or warrants for debt securities or preferred stock in one or more offerings.
[DEBT ¶30] (p. 70) During the year ended December 31, 2025, we issued the following unsecured, fixed-rate debt securities under our shelf registration:
[DEBT ¶31] (p. 70) Date | Description of securities
[DEBT ¶32] (p. 70) February 13, 2025
[DEBT ¶33] (p. 70) $1.00 billion of 5.100% Notes due February 20, 2035
[DEBT ¶34] (p. 70) $1.00 billion of 5.600% Notes due December 1, 2054
[DEBT ¶35] (p. 70) We used the net proceeds from the offerings for general corporate purposes, including the repurchase of common stock pursuant to our share repurchase programs. These debt securities include change-of-control provisions. At December 31, 2025, we had remaining authority from the Board of Directors to issue up to $20.0 billion of debt securities under our shelf registration.
[DEBT ¶36] (p. 70) Receivables securitization facility – As of both December 31, 2025 and 2024, we recorded $0 of borrowings under our Receivables Facility as secured debt. (See further discussion in the "Receivables Securitization Facility" section of Note 10.)