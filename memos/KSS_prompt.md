You are a senior commercial credit analyst at a bank. Write a credit memo on Kohl's Corporation for the facility below, using ONLY the fact sheet and the 10-K paragraphs provided. Do not use tools, files or outside knowledge.

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
# Credit memo: Kohl's Corporation

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
| `{{FYxxxx.debt_ebitda}}`  | 3.06x | 3.70x | 2.94x |
| `{{FYxxxx.net_debt_ebitda}}`  | 2.94x | 3.59x | 2.43x |
| `{{FYxxxx.lease_adj_debt_ebitdar}}`  | 4.25x | 4.93x | 4.16x |
| `{{FYxxxx.lease_adj_net_debt_ebitdar}}`  | 4.14x | 4.84x | 3.73x |
| `{{FYxxxx.interest_coverage}}`  | 4.26x | 3.69x | 4.60x |
| `{{FYxxxx.dscr}}`  | 2.38x | 0.94x | 3.13x |
| `{{FYxxxx.current_ratio}}`  | 1.31x | 1.08x | 1.46x |
| `{{FYxxxx.ebitda_margin}}`  | 8.4% | 7.2% | 8.5% |
| `{{FYxxxx.ebitdar}}`  | $1.7 billion | $1.5 billion | $1.6 billion |
| `{{FYxxxx.net_debt}}`  | $4.3 billion | $4.2 billion | $3.2 billion |
| `{{FYxxxx.lease_adj_debt}}`  | $7.4 billion | $7.2 billion | $6.6 billion |
| `{{FYxxxx.ebitda_ex_unusual}}`  | $1.5 billion | $1.3 billion | $1.2 billion |
| `{{FYxxxx.income.revenue}}`  | $17.5 billion | $16.2 billion | $15.5 billion |
| `{{FYxxxx.income.operating_costs}}`  | $16.0 billion | $15.0 billion | $14.3 billion |
| `{{FYxxxx.income.da}}`  | $749 million | $743 million | $700 million |
| `{{FYxxxx.income.unusual_operating}}`  | $0 | $76 million | -$114 million |
| `{{FYxxxx.income.operating_income}}`  | $717 million | $433 million | $624 million |
| `{{FYxxxx.income.interest_expense}}`  | $344 million | $319 million | $288 million |
| `{{FYxxxx.income.other_nonoperating}}`  | $0 | $0 | $0 |
| `{{FYxxxx.income.pretax_income}}`  | $373 million | $114 million | $336 million |
| `{{FYxxxx.income.income_tax}}`  | $56 million | $5 million | $64 million |
| `{{FYxxxx.income.net_income}}`  | $317 million | $109 million | $272 million |
| `{{FYxxxx.income.ebitda}}`  | $1.5 billion | $1.2 billion | $1.3 billion |
| `{{FYxxxx.balance.cash}}`  | $183 million | $134 million | $674 million |
| `{{FYxxxx.balance.current_assets}}`  | $3.4 billion | $3.4 billion | $3.7 billion |
| `{{FYxxxx.balance.total_assets}}`  | $14.0 billion | $13.6 billion | $13.4 billion |
| `{{FYxxxx.balance.debt_current}}`  | $175 million | $724 million | $85 million |
| `{{FYxxxx.balance.ltd}}`  | $4.3 billion | $3.6 billion | $3.8 billion |
| `{{FYxxxx.balance.total_debt}}`  | $4.5 billion | $4.4 billion | $3.9 billion |
| `{{FYxxxx.balance.lease_liabilities}}`  | $2.9 billion | $2.8 billion | $2.7 billion |
| `{{FYxxxx.balance.current_liabilities}}`  | $2.6 billion | $3.1 billion | $2.5 billion |
| `{{FYxxxx.balance.total_liabilities}}`  | $10.1 billion | $9.8 billion | $9.3 billion |
| `{{FYxxxx.balance.redeemable_nci}}`  | $0 | $0 | $0 |
| `{{FYxxxx.balance.equity}}`  | $3.9 billion | $3.8 billion | $4.0 billion |
| `{{FYxxxx.balance.nci}}`  | $0 | $0 | $0 |
| `{{FYxxxx.cashflow.cfo}}`  | $1.2 billion | $648 million | $1.4 billion |
| `{{FYxxxx.cashflow.capex}}`  | -$577 million | -$466 million | -$372 million |
| `{{FYxxxx.cashflow.acquisitions}}`  | $0 | $0 | $0 |
| `{{FYxxxx.cashflow.debt_issued}}`  | $7 million | $198 million | $357 million |
| `{{FYxxxx.cashflow.debt_repaid}}`  | -$275 million | -$113 million | -$730 million |
| `{{FYxxxx.cashflow.dividends}}`  | -$220 million | -$222 million | -$56 million |
| `{{FYxxxx.cashflow.buybacks}}`  | $0 | $0 | $0 |
| `{{FYxxxx.cashflow.fcf}}`  | $591 million | $182 million | $1.0 billion |
| `{{FYxxxx.cash_taxes}}` (from the notes) | $69 million | $78 million | $51 million |
| `{{FYxxxx.scheduled_principal}}` (from the notes) | $0 | $353 million | $0 |
| `{{FYxxxx.operating_lease_cost}}` (from the notes) | $271 million | $276 million | $271 million |
| `{{FYxxxx.operating_lease_liabilities}}` (from the notes) | $2.9 billion | $2.8 billion | $2.7 billion |
| `{{growth.FYxxxx.revenue}}` (change on prior year) | n/a | -7.2% | -4.3% |
| `{{growth.FYxxxx.ebitda}}` (change on prior year) | n/a | -19.8% | 12.6% |
| `{{growth.FYxxxx.ebitda_ex_unusual}}` (change on prior year) | n/a | -14.6% | -3.4% |
| `{{growth.FYxxxx.operating_income}}` (change on prior year) | n/a | -39.6% | 44.1% |
| `{{growth.FYxxxx.cfo}}` (change on prior year) | n/a | -44.5% | 113.0% |
| `{{growth.FYxxxx.total_debt}}` (change on prior year) | n/a | -3.1% | -10.7% |

Stress case and other values:

- `{{stress.debt_ebitda}}` = 5.66x
- `{{stress.net_debt_ebitda}}` = 4.68x
- `{{stress.lease_adj_debt_ebitdar}}` = 6.92x
- `{{stress.lease_adj_net_debt_ebitdar}}` = 6.22x
- `{{stress.interest_coverage}}` = 2.38x
- `{{stress.dscr}}` = 0.92x
- `{{stress.current_ratio}}` = 1.46x
- `{{stress.ebitda}}` = $687 million
- `{{stress.extra_interest}}` = $0
- `{{stress.base_margin}}` = 8.5%
- `{{stress.stressed_margin}}` = 5.5%
- `{{stress.revenue_shock}}` = 20.0%
- `{{stress.margin_shock}}` = 300bp
- `{{stress.rate_shock}}` = 200bp
- `{{floating_rate_share}}` = 0.0%
- `{{facility.type}}` = Senior unsecured term loan
- `{{facility.amount_usd}}` = $500 million
- `{{facility.tenor_years}}` = 5
- `{{facility.purpose}}` = General corporate purposes
- `{{grade.grade}}` = 8
- `{{grade.base_grade}}` = 6
- `{{grade.stress_notches}}` = 2
- `{{grade.weighted_score}}` = 6.10
- `{{grade.score.lease_adj_debt_ebitdar}}` = 8
- `{{grade.score.interest_coverage}}` = 6
- `{{grade.score.dscr}}` = 3
- `{{grade.score.current_ratio}}` = 5
- `{{proforma.amount}}` = $500 million
- `{{proforma.rate}}` = 10.00%
- `{{proforma.added_interest}}` = $50 million
- `{{proforma.total_debt}}` = $4.4 billion
- `{{proforma.debt_ebitda}}` = 3.31x
- `{{proforma.net_debt_ebitda}}` = 2.80x
- `{{proforma.lease_adj_debt_ebitdar}}` = 4.47x
- `{{proforma.lease_adj_net_debt_ebitdar}}` = 4.05x
- `{{proforma.interest_coverage}}` = 3.92x
- `{{proforma.dscr}}` = 2.67x
- `{{proforma.current_ratio}}` = 1.46x
- `{{proforma.stress.debt_ebitda}}` = 6.39x
- `{{proforma.stress.interest_coverage}}` = 2.03x
- `{{proforma.stress.dscr}}` = 0.78x
- `{{proforma.stress.extra_interest}}` = $0
- `{{fact.letters_of_credit}}` = $44 million: Letters of credit outstanding under the revolver, reducing availability [DEBT ¶65]
- `{{fact.new_debt_rate}}` = 10.00%: Coupon on Kohl's most recent senior issue: 10.000% senior secured notes due 2030, issued in the second quarter of 2025. Secured, so the pro forma interest on an unsecured loan is a lower bound [DEBT ¶61]
- `{{fact.revolver_capacity}}` = $1.5 billion: Senior secured asset-based revolving credit facility; $0 drawn at January 31, 2026 ($290M a year earlier) [DEBT ¶65]
- `{{fact.secured_notes_2030}}` = $360 million: 10.000% senior secured notes due 2030, guaranteed by subsidiaries and secured by distribution and e-commerce fulfillment centers [DEBT ¶61]
- `{{fact.stepup_notes}}` = $425 million: 2031 notes with rating-linked coupon step-ups (already triggered) [7A ¶2]
- `{{fact.stepup_total}}` = 175bp: Total coupon increase on the 2031 notes since issuance from downgrades [7-LIQ ¶70]
- `{{rating.sp}}` = B+ stable (S&P, last action 2026-06-17)
- `{{rating.moodys}}` = B2 positive (Moody's, last action 2026-04-14)
- `{{rating.fitch}}` = BB- negative (Fitch, last action 2025-04-07)
- Pro forma rate source: Coupon on Kohl's most recent senior issue: 10.000% senior secured notes due 2030, issued in the second quarter of 2025. Secured, so the pro forma interest on an unsecured loan is a lower bound [DEBT ¶61]
- The pro forma rate comes from a SECURED issue, so an unsecured loan would cost more: say in the memo that the pro forma interest is a lower bound.
- Stress thresholds broken (for your reasoning; describe them in words): Debt / EBITDA above 4.0x, DSCR below 1.0x

Floating-rate basis (analyst note): All long-term debt is fixed rate. The $1.5B revolver is SOFR-based but undrawn at January 31, 2026 ($290M drawn a year earlier). $425M of 2021 notes carry rating-linked coupon step-ups, already triggered; that is a fixed-rate repricing, not floating exposure.

## ANALYST POINTS TO COVER (each must appear in the memo, with its citation)
- Our loan would be unsecured, while the revolver is secured and asset-based and the 2030 notes are secured by distribution and fulfillment centers [DEBT ¶61, 7-LIQ ¶125]: we would rank behind both in a downside.
- The pro forma rate comes from secured notes, so the pro forma interest is a lower bound; with stressed coverage close to the threshold, say plainly that a realistic unsecured rate would likely push it below.
- Downgrades have already raised the coupon on the 2031 notes by 175bp in total [7-LIQ ¶70]; use the fact placeholders.
- Rating outlooks improved after the 10-K date (Moody's to positive, S&P to stable): use {{rating.moodys}} and {{rating.sp}}.
- The revolver has a springing fixed charge coverage covenant [7-LIQ ¶125].

## 10-K PARAGRAPHS (Kohl's Corporation 10-K filed 2026-03-19)

### [1] Item 1. Business
[1 ¶1] (p. 4) Item 1. Business
[1 ¶2] (p. 4) Kohl’s Corporation (the “Company," “Kohl’s,” "we," "our," or "us") was organized in 1988 and is a Wisconsin corporation. As of January 31, 2026, we operated 1,153 Kohl's stores and a website (www.Kohls.com). Our Kohl's stores and website sell moderately-priced proprietary and national brand apparel, footwear, accessories, beauty, and home products. Our Kohl's stores generally carry a consistent merchandise assortment with some differences attributable to local preferences and store size. Our […]
[1 ¶3] (p. 4) Our merchandise mix includes both national brands and proprietary brands that are available only at Kohl's. Our proprietary portfolio includes well-known established brands such as Apt. 9, Croft & Barrow, FLX, Jumping Beans, SO, Sonoma Goods for Life, and Tek Gear, and exclusive brands that are developed and marketed through agreements with nationally-recognized brands such as LC Lauren Conrad, Nine West, and Simply Vera Vera Wang. Compared to national brands, proprietary brands generally have […]
[1 ¶4] (p. 4) The following graphs summarize our net sales penetration by line of business and brand type over the last three years:
[1 ¶5] (p. 4) Our fiscal year ends on the Saturday closest to January 31st each year. Unless otherwise stated, references to years in this report relate to fiscal years rather than to calendar years. The following fiscal periods are presented in this report:
[1 ¶6] (p. 4) Fiscal Year
[1 ¶7] (p. 4) Ended
[1 ¶8] (p. 4) Number of Weeks
[1 ¶9] (p. 4) 2025
[1 ¶10] (p. 4) January 31, 2026
[1 ¶11] (p. 4) 52
[1 ¶12] (p. 4) 2024
[1 ¶13] (p. 4) February 1, 2025
[1 ¶14] (p. 4) 52
[1 ¶15] (p. 4) 2023
[1 ¶16] (p. 4) February 3, 2024
[1 ¶17] (p. 4) 53
[1 ¶18] (p. 4) For discussion of our financial results, see Item 7, "Management's Discussion and Analysis of Financial Condition and Results of Operations." 3 Distribution We receive substantially all of our merchandise at our nine retail distribution centers and four e-commerce fulfillment centers. A small amount of our merchandise is delivered directly to the stores by vendors or their distributors. The retail distribution centers, which are strategically located throughout the United States, ship […]
[1 ¶19] (p. 4) See Item 2, “Properties,” for additional information about our distribution and e-commerce fulfillment centers.
[1 ¶20] (p. 4) Human Capital
[1 ¶21] (p. 4) At Kohl’s, we strive to foster a workplace where respect, empathy, and inclusion thrive. We believe our associates are our most valuable asset and a differentiator for our business. Our teams of associates take care of each other, our customers, and the communities we serve. We support our associates by fostering a safe and healthy work environment, offering competitive total compensation and benefits, including many health and wellness offerings, providing ongoing training and development […]
[1 ¶22] (p. 4) Employee Count
[1 ¶23] (p. 4) During 2025, we employed an average of approximately 84,000 associates, which included approximately 29,000 full-time and 55,000 part-time associates. The number of associates varies during the year, peaking during the back-to-school and holiday seasons. None of our associates are represented by a collective bargaining unit. We believe we maintain positive relationships with our associates.
[1 ¶24] (p. 4) Health, Safety, and Wellness
[1 ¶25] (p. 4) We lead initiatives that ensure the way we communicate, work, and develop our product enables our customers and associates to shop, work, and engage in a safe environment. We have a team dedicated to defining plans and preparing for business crisis events, including natural disasters and other unplanned disruptions. To keep a healthy workforce, we maintain an advocacy program that provides associates with 24/7 access to medical professionals following a work accident. We continue to pursue […]
[1 ¶26] (p. 4) Inclusion and Belonging
[1 ¶27] (p. 4) At Kohl's, one of our priorities as a company is to reflect our values of being a welcoming, respectful, and inclusive company for all of our associates and all of the customers we serve. We believe that an inclusive and productive workforce that serves a broad base of customers will help drive our business forward. We are committed to our inclusion and belonging strategy, which focuses on Our People, Our Customers, and Our Community.
[1 ¶28] (p. 4) We strive to be purposeful in attracting, growing, and engaging a workforce comprised of different backgrounds, perspectives, and lived experiences, which helps us serve a broad base of customers. We are committed to cultivating a strong sense of connection and engagement within our eight Business Resource Groups (BRGs), which encompass more than 8,500 unique members and are a key component in recognizing and fostering our culture of inclusion and belonging. Our BRGs are inherently inclusive […]
[1 ¶29] (p. 5) We believe our leaders are responsible for strengthening, modeling, and supporting our company Values and Behaviors by promoting a culture where all associates feel seen, heard, and valued. We provide tools and resources for our leaders to help drive a welcoming, respectful and inclusive culture while also engaging associates on how this creates a competitive advantage for Kohl's.
[1 ¶30] (p. 5) Compensation and Benefits
[1 ¶31] (p. 5) We are committed to providing competitive and fair compensation and benefits programs to our associates and offer a range of benefits that are meaningful to our associates' everyday lives, with a commitment to supporting all aspects of associates' well-being. All eligible associates receive an immediately vested 100% match (up to 5% of pay) in Kohl’s 401(k) Savings Plan after one year of employment. Full-time associates are offered medical, dental, vision, prescription drug, disability and life […]
[1 ¶32] (p. 5) Kohl's fosters all associates' total wellness, which includes a number of benefits that focus on mental well-being, health, and personal growth, including the Employee Assistance Program, counseling sessions, proactive coaching, mental well-being activities, webinars, support groups, and leader resources. Kohl’s offers an education benefit which provides options for associates pursuing high school completion and undergraduate degrees.
[1 ¶33] (p. 5) Training and Development
[1 ¶34] (p. 5) Behind our success are great teams of talented individuals who embody our values. We are committed to attracting, growing, and engaging talent, while giving associates equitable opportunities for career growth. Our talent management team brings together performance management, talent assessment, succession planning, and career planning. This team provides tools, resources, and best practices to ensure we have the right talent in the right roles at the right time. We invest in leadership […]
[1 ¶35] (p. 5) From initial onboarding to high potential leadership development, we believe in training and career growth for our associates. We encourage our associates to keep their skills fresh through different mediums ranging from live workshops to on-demand skills training available through our online library of courses. We also offer training to teams that provide skills and mindsets to help them perform at their highest level. Additionally, our development teams throughout the company provide […]
[1 ¶36] (p. 5) We are committed to the highest integrity standards and maintain a Code of Ethics to guide ethical decision-making for associates. As a company of integrity, we expect our associates to be honest and accountable. Our ethics training, which we require all associates to take annually, is refreshed yearly to ensure topics covered are relevant and impactful. The training helps connect ethics to an associate's day-to-day job responsibilities and promotes honesty, integrity, and fairness.
[1 ¶37] (p. 5) Competition
[1 ¶38] (p. 5) The retail industry is highly competitive. Management considers product and value to be the most significant competitive factors in the industry. Merchandise mix, brands, service, loyalty programs, credit availability, and customer experience are also key competitive factors. Our primary competitors are online retailers, off-price retailers, warehouse clubs, mass merchandisers, specialty stores, traditional department stores, and other forms of retail commerce. Our specific competitors vary […]
[1 ¶39] (p. 6) Merchandise Vendors
[1 ¶40] (p. 6) We purchase merchandise from numerous domestic and foreign suppliers. All suppliers must meet certain requirements to do business with us. Our Terms of Engagement are part of our purchase order terms and conditions and include provisions regarding laws and regulations, employment practices, ethical standards, environmental requirements, communication, monitoring and compliance, record keeping, subcontracting, and corrective action. We expect that all suppliers will comply with our purchase […]
[1 ¶41] (p. 6) No vendor individually accounted for more than 10% of our net purchases in 2025. We have no significant long-term purchase commitments with any of our suppliers and believe that we are not dependent on any one supplier or one geographical location. We believe we have good working relationships with our suppliers.
[1 ¶42] (p. 6) Seasonality
[1 ¶43] (p. 6) Our business, like that of other retailers, is subject to seasonal influences. Sales and income are typically higher during the back-to-school and holiday seasons. Because of the seasonality of our business, results for any quarter are not necessarily indicative of the results that may be achieved for a full fiscal year.
[1 ¶44] (p. 6) Trademarks and Service Marks
[1 ¶45] (p. 6) KOHL'S® is a registered trademark owned by one of our wholly-owned subsidiaries. This subsidiary has over 200 additional registered trademarks, most of which are used in connection with our private brand products.
[1 ¶46] (p. 6) We consider the KOHL'S® mark, all other trademarks, and the accompanying goodwill to be valuable to our business.
[1 ¶47] (p. 6) Available Information
[1 ¶48] (p. 6) Our corporate website is https://corporate.kohls.com. Through the “Investors” portion of this website, we make available, free of charge, our proxy statements, Annual Reports on Form 10-K, Quarterly Reports on Form 10-Q, Current Reports on Form 8-K, Securities and Exchange Commission (“SEC”) Forms 3, 4, and 5, and any amendments to those reports filed or furnished pursuant to Sections 13(a) and 15(d) of the Securities Exchange Act of 1934, as amended, as soon as reasonably practicable after […]
[1 ¶49] (p. 6) The following have also been posted on our website, under the caption “Investors” and sub-captions "Corporate Governance" or “ESG”:
[1 ¶50] (p. 6) •
[1 ¶51] (p. 6) Committee charters of our Board of Directors’ Audit Committee, Compensation Committee, Finance Committee, and Nominating and ESG Committee • Corporate Governance Guidelines • Code of Ethics • Environmental, Social, and Governance Reports (under “ESG” sub-caption) The information contained on our website is not part of this Annual Report on Form 10-K. Paper copies of any of the materials listed above will be provided without charge to any shareholder submitting a written request to our Investor […]

### [1A] Item 1A. Risk Factors
[1A ¶1] (p. 7) Item 1A. Risk Factors
[1A ¶2] (p. 7) This Form 10-K contains “forward-looking statements” within the meaning of the Private Securities Litigation Reform Act of 1995. Words such as "believes," "anticipates," "plans," "may," "intends," "will," "should," "expects," and similar expressions are intended to identify forward-looking statements. Forward-looking statements include certain statements under Management's Discussion and Analysis and Financial and Capital Allocation Outlook and may include comments about our future sales or […]
[1A ¶3] (p. 7) Our sales, revenues, gross margin, expenses, and operating results could be negatively impacted by a number of factors including, but not limited to, those described below. Many of these risk factors are outside of our control. If we are not successful in managing these risks, they could have a negative impact on our sales, revenues, gross margin, expenses, and/or operating results.
[1A ¶4] (p. 7) Macroeconomic, Regulatory, Legal, and External Risks
[1A ¶5] (p. 7) Our business is highly sensitive to general economic conditions, consumer spending levels, and/or other external conditions, which could decline.
[1A ¶6] (p. 7) Our business is sensitive to the growth of the U.S. economy and the strength of the U.S. consumer. Consumer spending habits, including demand for the merchandise we sell, are affected by various factors beyond our control, including prevailing economic conditions, inflation and measures taken to control it, consumer responses to recessionary concerns, levels of employment, salaries and wage rates, prevailing interest rates, housing costs, energy and fuel costs, income tax rates and policies, […]
[1A ¶7] (p. 7) Geopolitical instability, hostilities, and public health events could adversely affect consumer behavior and our operations.
[1A ¶8] (p. 7) Consumer confidence and purchasing power are influenced by the domestic and international political environment. The outbreak or escalation of war, or the occurrence of terrorist acts or other hostilities in or affecting the United States or our global supply chain partners, could lead to decreased consumer spending or widespread operational disruptions. Future pandemics or other public health crises could have a material adverse impact on our business, financial condition, and results of […]
[1A ¶9] (p. 8) Changes in global trade policies and the imposition of tariffs could increase our costs and disrupt our supply chain.
[1A ¶10] (p. 8) The majority of goods we source are manufactured outside of the United States, primarily in Asia. Consequently, our business is subject to risks associated with foreign trade, including changes in trade policy. Recent or potential impositions of new or increased tariffs on imported products, or the removal of de minimis thresholds for direct-to-consumer imports, could increase our merchandise costs and have a material adverse effect on our business, results of operations, and liquidity. On […]
[1A ¶11] (p. 8) We are subject to income and other taxes in the United States and various local jurisdictions, and changes in tax laws or the interpretation of existing laws could increase our tax liabilities and impact our financial results.
[1A ¶12] (p. 8) We are subject to income and other taxes in the United States and various local jurisdictions. Our effective tax rate and profitability could be adversely affected by several factors, including changes in tax laws; the interpretation of existing laws; or the results of audits or reviews by taxing authorities. We are subject to regular reviews and ongoing audits by federal, state, and local tax authorities. While we believe our tax positions and estimates are reasonable, the ultimate resolution […]
[1A ¶13] (p. 8) Evolving regulations related to ESG, climate change, and sustainability could increase our costs and impose operational restrictions.
[1A ¶14] (p. 8) Increased governmental focus on climate change and other ESG matters has led to complex and conflicting regulatory requirements, such as increasing state-level regulations related to the use of per- and polyfluoroalkyl substances in merchandise, extended producer responsibility legislation related to packaging and waste, and climate risk and greenhouse gas reporting mandates (such as those in California, which is currently partially enjoined, and the SEC climate-related disclosure rule, which […]
[1A ¶15] (p. 9) Regulatory and legal matters could adversely affect our business operations and change financial performance.
[1A ¶16] (p. 9) Various aspects of our operations are subject to federal, state, or local laws, rules, and regulations, including consumer regulations, any of which may change from time to time. The costs and other effects of new or changed legal requirements cannot be determined with certainty. For example, new legislation or regulations may result in increased costs directly for our compliance or indirectly to the extent such requirements increase prices of goods and services, reduce the availability of raw […]
[1A ¶17] (p. 9) We continually monitor the state and federal legal and regulatory environments for developments that may impact us. Failure to detect changes and comply with such laws and regulations may result in an erosion of our reputation, disruption of business, and/or loss of associate morale. Additionally, we are involved in various legal matters and regulatory proceedings that arise out of the conduct of our business. Litigation or regulatory developments could adversely affect our business operations […]
[1A ¶18] (p. 9) Weather conditions, natural disasters, and the potential impacts of climate change could adversely affect consumer shopping patterns and disrupt our operations.
[1A ¶19] (p. 9) As our business includes apparel, footwear, accessories, beauty, and home products, our business is subject to risks associated with weather conditions and natural disasters, which can occur with little warning. Severe weather—including unusually heavy snow, ice, or rainstorms, and natural disasters such as earthquakes, wildfires, floods, or hurricanes—has previously resulted, and could in the future result, in physical damage to or the closure of our stores, distribution centers, or other […]
[1A ¶20] (p. 9) Furthermore, unseasonable weather conditions, including unusually warm weather in the fall or winter months or abnormally wet or cold weather in the spring or summer months, whether due to climate change or otherwise, could have a material adverse effect on our business, financial condition, and operating results, as such conditions may reduce demand for seasonal merchandise and create inventory imbalances. This inconsistency between consumer spending and our typical inventory purchasing cycle […]
[1A ¶21] (p. 9) Climate change also presents widespread transition risks and long-term physical risks that are difficult to predict, including increased energy costs, greenhouse gas regulation, and threats to the habitability of specific geographic regions where we operate. Climate change may impact the frequency and/or intensity of major disruption events, as well as contribute to various changes in the physical environment. Although we maintain crisis management and disaster response plans and may take […]
[1A ¶22] (p. 9) Strategic, Competitive, and Operational Risks
[1A ¶23] (p. 9) We may be unable to successfully execute our omnichannel strategy.
[1A ¶24] (p. 9) Customer expectations regarding how they purchase and receive products are continuously evolving, with increasing use of technology and mobile devices to rapidly compare products, check prices, make purchases, and seek alternate delivery options. To stay competitive, we must continually anticipate and adapt to these changes in consumer behavior. The success of our omnichannel strategy depends on the seamless integration of our physical and digital channels to deliver a frictionless shopping […]
[1A ¶25] (p. 10) Our ability to compete with other retailers and to meet our customers' expectations may suffer if we are unable to provide relevant customer-facing technology and a compelling omnichannel value proposition. As consumer behavior shifts toward a value-seeking mindset, our ability to differentiate our value proposition through personalization and loyalty remains critical. Our efforts to refine our omnichannel value strategy may negatively impact the loyalty of certain customers and our efforts to […]
[1A ¶26] (p. 10) Furthermore, our ability to compete may also suffer if Kohl’s, our suppliers, or our third-party shipping and delivery vendors are unable to effectively and efficiently fulfill and deliver orders, especially during the holiday season when sales volumes are especially high. Any disruptions in these areas could adversely affect our results of operations.
[1A ¶27] (p. 10) We may be unable to offer merchandise that resonates with existing customers and attracts new customers while successfully managing our inventory levels.
[1A ¶28] (p. 10) Our business is dependent on our ability to anticipate fluctuations in consumer demand for a wide variety of merchandise. Failure to accurately predict constantly changing consumer tastes, preferences, spending patterns, and other lifestyle decisions, or to successfully execute our inventory allocation strategy, could result in inventory distortions that are often characterized by simultaneous lack of available stock in high-demand categories and excess inventory in others, which could create […]
[1A ¶29] (p. 10) Negative publicity surrounding us, our activities, or the products we offer, including consumer perception of our response to political and social issues, and campaigns by political activists promoting certain causes, could adversely impact our brand image and may decrease demand for our products, thereby adversely affecting our business, results of operations, cash flows or financial condition.
[1A ¶30] (p. 10) As with most retailers, we also experience inventory shrinkage due to theft or damage, and we have observed an increase in external theft incidents and organized retail crime. Higher rates of inventory shrinkage or increased security or other costs to combat inventory shrinkage could adversely affect our results of operations and financial condition. Our efforts to contain or reduce inventory shrinkage may not be successful, and certain theft-deterrence measures could negatively impact the […]
[1A ¶31] (p. 10) Our competitors could make changes to their pricing and other practices.
[1A ¶32] (p. 10) The retail industry is highly competitive. We compete for customers, associates, locations, merchandise, services, and other important aspects of our business with many other local, regional, and national retailers. Those competitors include online retailers, off-price retailers, warehouse clubs, mass merchandisers, specialty stores, traditional department stores, and other forms of retail commerce.
[1A ¶33] (p. 10) We consider product and value to be the most significant competitive factors in our industry. The continuing migration and evolution of retailing to digital channels has increased our challenges in differentiating ourselves from other retailers especially as it relates to national brands. In particular, consumers can quickly and conveniently comparison shop with digital tools, which can lead to decisions based solely on price. Unanticipated changes in the pricing and other practices of our […]
[1A ¶34] (p. 11) Our marketing and loyalty programs may be ineffective at building personalized connections with customers.
[1A ¶35] (p. 11) We believe that differentiating Kohl's in the marketplace is critical to our success. We design our marketing and loyalty programs to increase brand awareness, build personalized connections with new and existing customers, and drive traffic and conversion. We believe these programs will strengthen customer loyalty, increase the number and frequency of customers that shop our stores and website, and increase our sales. If our marketing and loyalty programs are not successful or efficient, we […]
[1A ¶36] (p. 11) Our business is seasonal in nature, which could negatively affect our sales, revenues, operating results, and cash requirements.
[1A ¶37] (p. 11) Our business is subject to seasonal influences, with a major portion of sales and income historically realized during the second half of the fiscal year, which includes the back-to-school and holiday seasons.
[1A ¶38] (p. 11) If we do not adequately stock or restock popular products, particularly during the back-to-school and holiday seasons, we may fail to meet customer demand, which could affect our revenue and our future growth. If we overstock products, we may be required to take significant inventory markdowns or write-offs, which could reduce profitability. Underestimating customer demand, or failing to timely receive merchandise to meet demand, can lead to inventory shortages and missed sales opportunities, […]
[1A ¶39] (p. 11) We have and may continue to experience an increase in costs associated with shipping digital orders due to promotional shipping offers, split shipments, freight surcharges due to peak capacity constraints, and additional long-zone shipments necessary to ensure timely delivery for the holiday season. If too many customers access our website within a short period of time, particularly during peak selling periods, we may experience system interruptions that make our website unavailable or prevent […]
[1A ¶40] (p. 11) This seasonality causes our operating results and cash needs to vary considerably from quarter to quarter. Additionally, any decrease in sales or profitability during the second half of the fiscal year could have a disproportionately adverse effect on our results of operations.
[1A ¶41] (p. 11) The reputation and brand image of Kohl’s and the brands and products we sell could be damaged.
[1A ¶42] (p. 11) The Kohl's brand and many of our private brands are powerful sales and marketing tools that depend on positive consumer and stakeholder perceptions. We devote significant resources to develop, promote, and protect private brands that generate national recognition. In some cases, the private brands or the marketing of such brands are tied to or affiliated with well-known individuals. We also associate the Kohl’s brand with third-party national brands that we sell in our store and through our […]
[1A ¶43] (p. 12) Our ESG profile is a component of our strategy, and we have and may at times continue to engage in voluntary initiatives (such as voluntary disclosures, certifications, or goals, among others) to improve the ESG profile of our company and/or products. However, these disclosures reflect goals and assumptions that are inherently uncertain and which may not be realized. These initiatives may be costly, fail to achieve intended results, or lead to litigation or regulatory or stakeholder scrutiny. […]
[1A ¶44] (p. 12) Furthermore, the use of online media by us, our influencer network, and our consumers and other stakeholders has increased the risk that our reputation and brand could be damaged, as the dissemination of information via online and social media is immediate and damage could arise quickly without affording us an opportunity for redress or correction. This risk is exacerbated by the rise of generative artificial intelligence and deepfake technologies, which can be used to create fictitious media […]
[1A ¶45] (p. 12) We are subject to payment-related risks, including in our credit card operations, that could adversely affect our sales, revenues, and/or profitability, increase our operating costs, expose us to fraud or theft, and subject us to potential liability.
[1A ¶46] (p. 12) We accept payments using a variety of methods, including our private label and co-branded Kohl’s credit card, credit and debit cards, gift cards, mobile payments, cash, and checks. Acceptance of these payment options subjects us to rules, regulations, contractual obligations and compliance requirements, including payment network rules and operating guidelines and rules governing electronic funds transfers. These requirements may change over time or be reinterpreted, making compliance more […]
[1A ¶47] (p. 12) Our credit card operations facilitate merchandise sales and generate additional revenue from fees related to extending credit. The profitability of our credit card program is sensitive to the economic health of our core moderate-income customer. The private label and co-branded Kohl's credit card accounts are owned by an unrelated third-party, but we share in the net risk-adjusted revenue of the portfolio, which is defined as the sum of finance charges, late fees, and other revenue less […]
[1A ¶48] (p. 13) The regulatory framework governing our private label and co-branded Kohl’s credit card program remains subject to regulatory scrutiny, and our results are sensitive to legislative or executive actions that impact credit card services. Although the Consumer Financial Protection Bureau’s (CFPB) rule limiting credit card late fees was vacated, new or re-proposed rules, including potential federal limits on credit card interest rates, could adversely affect our program’s profitability. Furthermore, […]
[1A ¶49] (p. 13) The payment and payment process methods that we accept subject us to potential fraud and theft by threat actors, including increased credit fraud risks associated with self check out, self pick up, and digital payment methods which could negatively impact our revenue and profitability. If we fail to comply with applicable rules or requirements for the payment methods we accept, or if payment-related data is compromised due to a breach or misuse of data, we may be liable for costs incurred by […]
[1A ¶50] (p. 13) Changes in credit card use and applications, payment patterns, credit fraud, and default rates may also result from a variety of economic, legal, social, and other factors that we cannot control or predict with certainty. Changes that adversely impact our ability to extend credit and collect payments could negatively affect our results.
[1A ¶51] (p. 13) We may be unable to attract, develop, and retain quality associates while controlling costs, which could adversely affect our operating results.
[1A ¶52] (p. 13) Our performance is dependent on attracting and retaining a large number of quality associates, including our senior management team and other key associates, and successfully executing organizational changes, such as leadership transitions. Leadership transitions can be disruptive and may result in the loss of key personnel, changes in business direction, or difficulties in maintaining operational focus and consistency. While we have succession plans for our senior management team, they may not […]
[1A ¶53] (p. 13) Many associates are in entry-level or part-time positions with historically high rates of turnover. Many of our strategic initiatives require that we hire and/or develop associates with appropriate experience. Our staffing needs are especially high during the holiday season. Competition for these associates is intense. We cannot be sure that we will be able to attract and retain a sufficient number of qualified personnel in future periods.
[1A ¶54] (p. 13) Our ability to meet our labor needs while controlling costs is subject to external factors such as government benefits, unemployment levels and labor participation rates, prevailing wage rates, minimum wage legislation, actions by our competitors in compensation levels, perceptions of our employee experience, potential labor organizing efforts, and changing demographics. Competitive and regulatory pressures have already significantly increased our labor costs. Further changes that adversely […]
[1A ¶55] (p. 14) Information Systems, Cybersecurity, Data Management, and Privacy Risks
[1A ¶56] (p. 14) We may be unable to adequately maintain and/or update our information systems.
[1A ¶57] (p. 14) The efficient operation of our business is dependent on our information systems. In particular, we rely on our information systems to effectively manage sales, distribution, and merchandise planning and allocation functions. We also generate sales through the operations of our Kohls.com website and the Kohl’s app. We frequently make investments that will help maintain and update our existing information systems. We also depend on third parties as it relates to our information systems. Although […]
[1A ¶58] (p. 14) Our efforts to protect the privacy and security of sensitive or confidential customer, associate, or company information could be unsuccessful, which could severely damage our reputation, expose us to risks of litigation and liability, disrupt our operations, and harm our business.
[1A ¶59] (p. 14) As part of our normal course of business, we collect, retain, process, and transmit sensitive and confidential customer, associate, and company information. We also engage third-party vendors that provide technology, systems, and services to facilitate our collection, retention, processing, and transmission of this information. We face risk that our facilities and systems and those of our third-party vendors are vulnerable to cybersecurity threats, security breaches, system failures, acts of […]
[1A ¶60] (p. 15) Our information technology projects may not yield their intended results, and our use of artificial intelligence and machine learning technology presents evolving operational and legal risks.
[1A ¶61] (p. 15) We regularly have internal information technology projects in process. Although the technology is intended to increase productivity and operating efficiencies, these projects may not yield their intended results or may deliver an adverse user or customer experience. We may incur significant costs in connection with the implementation, ongoing use, or discontinuation of technology projects, or fail to successfully implement these technology initiatives, or achieve the anticipated efficiencies […]
[1A ¶62] (p. 15) We continue to incorporate artificial intelligence, including generative AI and machine learning technology, into our business operations and customer experiences. Challenges with properly managing the use of AI and machine learning technology could result in reputational harm, competitive disadvantage, and legal liability. The legal, regulatory, and ethical landscape around the use of AI is rapidly evolving, and our ability to timely adopt and adapt to this emerging technology in an effective […]
[1A ¶63] (p. 15) Supply Chain, Third Party, and Product-Related Risks
[1A ¶64] (p. 15) We may be unable to source merchandise in a timely and cost-effective manner.
[1A ¶65] (p. 15) Our ability to find qualified vendors and access to brands or products in a timely and efficient manner is a significant challenge. Our merchandise is sourced from a wide variety of domestic and international vendors. Substantially all goods sourced outside the U.S. are shipped by ocean to ports in the United States, making us vulnerable to port strikes, port congestion and delays, transport capacity constraints, and rising freight costs. Political or financial instability, trade restrictions, […]
[1A ¶66] (p. 15) Increases in the price of merchandise, raw materials, fuel, and labor, or their reduced availability, increase our cost of merchandise sold. The price and availability of raw materials may fluctuate substantially, depending on a variety of factors, including demand, weather, supply conditions, transportation costs, energy prices, work stoppages, government regulation and policy, economic climates, market speculation, and other unpredictable factors. An inability to mitigate these cost […]
[1A ¶67] (p. 16) If any of our significant vendors were to become subject to bankruptcy, receivership, or similar proceedings, we may be unable to arrange for alternate or replacement contracts, transactions, or business relationships on terms as favorable as current terms, which could adversely affect our sales and operating results.
[1A ¶68] (p. 16) Our vendors may not adhere to our Terms of Engagement or to applicable laws.
[1A ¶69] (p. 16) A substantial portion of our merchandise is received from vendors and factories outside of the United States. We require all of our suppliers to comply with all applicable local and national laws and regulations and our Terms of Engagement for Kohl's Business Partners. These Terms of Engagement include provisions regarding laws and regulations, employment practices, ethical standards, environmental and legal requirements, communication, monitoring/compliance, record keeping, subcontracting, and […]
[1A ¶70] (p. 16) There may be concerns about the safety of products that we sell.
[1A ¶71] (p. 16) If our merchandise offerings do not meet applicable safety standards or our customers' expectations regarding safety, we could experience lost sales, experience increased costs, and/or be exposed to legal and reputational risk. Events that give rise to actual, potential, or perceived product safety concerns could expose us to government enforcement action and/or private litigation. Reputational damage caused by real or perceived product safety concerns could have a negative impact on our sales […]
[1A ¶72] (p. 16) Capital Risks
[1A ¶73] (p. 16) We may be unable to raise additional capital or maintain credit on favorable terms, which could constrain our operational flexibility and increase our cost of doing business.
[1A ¶74] (p. 16) We have historically relied on the public debt markets and lines of credit with financial institutions to raise capital and to partially fund our operations, growth, seasonal working capital needs, and strategic initiatives. In January 2023, we upsized and replaced our unsecured credit facility with a $1.5 billion senior secured, asset based revolving credit facility. Changes in the credit and capital markets, including market disruptions, limited liquidity, and interest rate fluctuations may […]
[1A ¶75] (p. 16) During 2024, S&P downgraded our senior unsecured credit rating from BB to BB- and Moody's downgraded our rating from Ba3 to B1. These downgrades have caused our cost of borrowing to increase. During 2025, Moody's further downgraded our senior unsecured credit rating from B1 to B3; however, further downgrades by Moody's do not trigger incremental interest rate increases on our existing debt. Further downgrades by S&P would cause our cost of borrowing to further increase. Declines in our credit […]
[1A ¶76] (p. 17) Our existing debt agreements, particularly our revolving credit facility, contain restrictive covenants. Any failure to comply with these covenants could result in an event of default, allowing lenders to terminate their commitments thereunder and declare the outstanding loans thereunder to be immediately due and payable. A default under our revolving credit facility could trigger a cross-default, acceleration, or other consequences under other indebtedness or financial instruments to which we […]
[1A ¶77] (p. 17) Our capital allocation strategy may be inefficient, may not yield the anticipated returns, or may not effectively support our long-term growth.
[1A ¶78] (p. 17) Our goal is to invest capital in a manner that maximizes long-term returns and shareholder value. This includes prioritizing spending on inventory, capital projects and expenses; managing debt levels; and periodically returning value to our shareholders through dividends and, longer term, share repurchases. To a large degree, capital efficiency reflects how well we manage our other key risks. The actions taken to address other specific risks may affect how well we manage the more general risk […]

### [7] Item 7. Management's Discussion and Analysis
[7 ¶1] (p. 25) Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations
[7 ¶2] (p. 25) Executive Summary
[7 ¶3] (p. 25) Kohl's is a leading omnichannel retailer operating 1,153 stores and a website (www.Kohls.com) as of January 31, 2026. Our Kohl's stores and website sell moderately-priced proprietary and national brand apparel, footwear, accessories, beauty, and home products. Our Kohl's stores generally carry a consistent merchandise assortment with some differences attributable to local preferences and store […]
[7 ¶4] (p. 25) Key financial results for 2025 as compared to 2024 include:
[7 ¶5] (p. 25) •
[7 ¶6] (p. 25) Net sales decreased 4.0%, to $14.8 billion, with comparable sales down 3.1%.
[7 ¶7] (p. 25) •
[7 ¶8] (p. 25) Gross margin as a percent of net sales was 37.5%, an increase of 34 basis points.
[7 ¶9] (p. 25) •
[7 ¶10] (p. 25) Selling, general & administration ("SG&A") expenses decreased 4.1% year-over-year, to $5.1 billion. As a percentage of total revenue, SG&A expenses were 32.8%, an increase of 5 basis points year-over-year.
[7 ¶11] (p. 25) •
[7 ¶12] (p. 25) Gain on legal settlement was $129 million from a credit card interchange fee lawsuit settlement.
[7 ¶13] (p. 25) •
[7 ¶14] (p. 25) Operating income was $624 million compared to $433 million in the prior year. As a percentage of total revenue, operating income was 4.0%, an increase of 135 basis points year-over-year.
[7 ¶15] (p. 25) •
[7 ¶16] (p. 25) On an adjusted non-GAAP basis, our adjusted operating income was $510 million compared to $509 million in the prior year.(a) As a percentage of total revenue, adjusted operating income was 3.3% compared to 3.1% in the prior year.(a) • Net income was $272 million, or $2.38 per diluted share. This compares to net income of $109 million, or $0.98 per diluted share in the prior year.
[7 ¶17] (p. 25) •
[7 ¶18] (p. 25) On an adjusted non-GAAP basis, our adjusted net income was $186 million, or $1.62 per adjusted diluted share.(a) This compares to adjusted non-GAAP net income of $167 million, or $1.50 per adjusted diluted share in the prior year.(a) • Cash flow provided by operating activities was $1.4 billion compared to $648 million in the prior year.
[7 ¶19] (p. 25) •
[7 ¶20] (p. 25) Current portion of long-term debt was reduced by $353 million through repayment of the 4.25% notes due July 2025 at maturity.
[7 ¶21] (p. 25) •
[7 ¶22] (p. 25) There were no outstanding borrowings under the revolving credit facility compared to $290 million in the prior year.
[7 ¶23] (p. 25) •
[7 ¶24] (p. 25) Long term debt increased $262 million through issuance of $360 million of 10.000% senior secured notes due 2030, partially offset by open market repurchases of $87 million of our outstanding long term debt.
[7 ¶25] (p. 25) (a)
[7 ¶26] (p. 25) Non-GAAP financial measures. Please see the “GAAP to Non-GAAP Reconciliation” for a reconciliation of adjusted operating income to operating income, adjusted net income to net income, and adjusted diluted earnings per share to diluted earnings per share.
[7 ¶27] (p. 25) Our Strategy
[7 ¶28] (p. 25) Kohl's remains committed to driving long-term shareholder value by providing our customers with great product, great value, and a great experience. To achieve this, we will offer a curated, more balanced assortment that fulfills needs across all customers, reestablish Kohl’s as a leader in value and quality, and deliver a frictionless experience to customers across our omnichannel platforms.
[7 ¶29] (p. 26) Financial and Capital Outlook
[7 ¶30] (p. 26) For fiscal year 2026, the Company currently expects the following:
[7 ¶31] (p. 26) •
[7 ¶32] (p. 26) Net sales and Comparable sales: A decrease of (2%) to flat
[7 ¶33] (p. 26) •
[7 ¶34] (p. 26) Adjusted operating margin: In the range of 2.8% to 3.4% (b)
[7 ¶35] (p. 26) •
[7 ¶36] (p. 26) Adjusted diluted EPS: In the range of $1.00 to $1.60 (b)
[7 ¶37] (p. 26) •
[7 ¶38] (p. 26) Capital Expenditures: Approximately $350 million to $400 million
[7 ¶39] (p. 26) •
[7 ¶40] (p. 26) Dividend: On February 25, 2026, Kohl’s Board of Directors declared a quarterly cash dividend on the Company’s common stock of $0.125 per share. The dividend is payable April 1, 2026 to shareholders of record at the close of business on March 18, 2026.
[7 ¶41] (p. 26) (b)
[7 ¶42] (p. 26) Non-GAAP financial measures. The Company provides adjusted operating margin and adjusted diluted earnings per share on a non-GAAP basis and does not provide a reconciliation of the Company’s forward looking guidance to the most directly comparable GAAP financial measures because of the inherent difficulty in forecasting and quantifying certain amounts that are necessary for such reconciliations.
[7 ¶43] (p. 26) Results of Operations
[7 ¶44] (p. 26) For our comparison and discussion of 2024 and 2023, see Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations in Part II of our 2024 Form 10-K.
[7 ¶45] (p. 26) Net Sales
[7 ¶46] (p. 26) Net sales includes revenue from the sale of merchandise, net of expected returns and deferrals due to future performance obligations, and shipping revenue.
[7 ¶47] (p. 26) Comparable sales is a measure that highlights the performance of our stores and digital channel by measuring the change in sales for a period over the comparable, prior-year period of equivalent length. Comparable sales includes all store and digital sales, except sales from stores open less than 12 months, stores that have been closed, and stores that have been relocated where square footage has […]
[7 ¶48] (p. 26) The following graph summarizes net sales dollars and the change in comparable sales over the prior year.
[7 ¶49] (p. 26) Digital sales were approximately flat in 2025 year-over-year. Digital penetration represented 29% of net sales in 2025 and 28% of net sales in 2024. We measure the change in digital sales by including all sales initiated online or through mobile applications, including omnichannel transactions which are fulfilled through our stores. We measure digital penetration as digital sales over net sales. […]
[7 ¶50] (p. 26) Comparable sales and digital penetration measures vary across the retail industry. As a result, our comparable sales calculation and digital penetration may not be consistent with the similarly titled measures reported by other companies.
[7 ¶51] (p. 27) 2025 compared to 2024
[7 ¶52] (p. 27) Net sales decreased $610 million, or (4.0%), to $14.8 billion for 2025.
[7 ¶53] (p. 27) •
[7 ¶54] (p. 27) The decrease was driven by an approximately 4% decrease in transaction volume.
[7 ¶55] (p. 27) •
[7 ¶56] (p. 27) Sales decreased across all lines of business, except for Accessories, which increased approximately 2% during 2025.
[7 ¶57] (p. 27) (Dollars in Millions)
[7 ¶58] (p. 27) 2025
[7 ¶59] (p. 27) 2024
[7 ¶60] (p. 27) Change
[7 ¶61] (p. 27) Women's
[7 ¶62] (p. 27) $3,601
[7 ¶63] (p. 27) $3,817
[7 ¶64] (p. 27) (5.7%)
[7 ¶65] (p. 27) Accessories (including Sephora)
[7 ¶66] (p. 27) 3,122
[7 ¶67] (p. 27) 3,060
[7 ¶68] (p. 27) 2.0%
[7 ¶69] (p. 27) Men's
[7 ¶70] (p. 27) 2,930
[7 ¶71] (p. 27) 3,079
[7 ¶72] (p. 27) (4.8%)
[7 ¶73] (p. 27) Home
[7 ¶74] (p. 27) 2,212
[7 ¶75] (p. 27) 2,311
[7 ¶76] (p. 27) (4.3%)
[7 ¶77] (p. 27) Children's
[7 ¶78] (p. 27) 1,700
[7 ¶79] (p. 27) 1,819
[7 ¶80] (p. 27) (6.5%)
[7 ¶81] (p. 27) Footwear
[7 ¶82] (p. 27) 1,210
[7 ¶83] (p. 27) 1,299
[7 ¶84] (p. 27) (6.9%)
[7 ¶85] (p. 27) Net Sales
[7 ¶86] (p. 27) $14,775
[7 ¶87] (p. 27) $15,385
[7 ¶88] (p. 27) (4.0%)
[7 ¶89] (p. 27) Other Revenue
[7 ¶90] (p. 27) Other revenue includes revenue from credit card operations, third-party advertising on our website, unused gift cards and merchandise return cards (breakage), and other non-merchandise revenue.
[7 ¶91] (p. 27) The following graph summarizes other revenue:
[7 ¶92] (p. 27) Other revenue decreased $84 million in 2025 due to lower credit revenue, which was driven by certain credit card expenses shifting against other revenue from SG&A as we moved part of our account servicing to the third party that owns the accounts and lower sales to our Kohl's credit card customer.
[7 ¶93] (p. 27) Cost of Merchandise Sold and Gross Margin
[7 ¶94] (p. 27) Cost of merchandise sold includes the total cost of products sold, including product development costs, net of vendor payments other than reimbursement of specific, incremental, and identifiable costs; inventory shrink; markdowns; freight expenses associated with moving merchandise from our vendors to our distribution centers; shipping expenses for digital sales; and terms cash discount. Our cost […]
[7 ¶95] (p. 28) The following graph summarizes cost of merchandise sold and gross margin as a percent of net sales:
[7 ¶96] (p. 28) Gross margin is calculated as net sales less cost of merchandise sold. Gross margin in 2025 was 37.5% of net sales, an increase of 34 basis points to last year. The increase was driven by strong inventory management, merchandise mix, and moderating shrink levels. Strong inventory management was driven by fewer clearance markdowns, as our inventory decreased 7% to last year, and receipts for the […]
[7 ¶97] (p. 28) Selling, General, and Administrative Expenses
[7 ¶98] (p. 28) SG&A includes compensation and benefit costs (including stores, corporate, buying, and distribution centers); occupancy and operating costs of our retail, distribution, and corporate facilities; freight expenses associated with moving merchandise from our distribution centers to our retail stores and among distribution and retail facilities other than expenses to fulfill digital sales; marketing […]
[7 ¶99] (p. 28) Many of our expenses, including store payroll and distribution costs, are variable in nature. These costs generally increase as sales increase, and decrease as sales decrease. We measure our expenses as a percentage of revenue and changes in this percentage compared to the prior year. If the expense as a percent of revenue decreased from the prior year, the expense "leveraged". If the expense as […]
[7 ¶100] (p. 28) The following graph summarizes the changes in SG&A by expense type between 2024 and 2025:
[7 ¶101] (p. 29) SG&A decreased $219 million, or 4.1%, to $5.1 billion in 2025. As a percentage of revenue, SG&A deleveraged by 5 basis points.
[7 ¶102] (p. 29) The decrease in SG&A expenses was driven by lower store payroll, marketing, and distribution costs, as well as a shift of certain corporate credit card expenses to other revenue due to moving part of our account servicing to the third party that owns the accounts, partially offset by an increase in other corporate expenses. Without the shift of certain corporate credit expenses, SG&A expenses […]
[7 ¶103] (p. 29) Other Expenses
[7 ¶104] (p. 29) (Dollars in Millions)
[7 ¶105] (p. 29) 2025
[7 ¶106] (p. 29) 2024
[7 ¶107] (p. 29) 2023
[7 ¶108] (p. 29) Depreciation and amortization
[7 ¶109] (p. 29) $700
[7 ¶110] (p. 29) $743
[7 ¶111] (p. 29) $749
[7 ¶112] (p. 29) Impairments, store closing, and other costs
[7 ¶113] (p. 29) 15
[7 ¶114] (p. 29) 76
[7 ¶115] (p. 29) —
[7 ¶116] (p. 29) (Gain) on legal settlement
[7 ¶117] (p. 29) (129)
[7 ¶118] (p. 29) —
[7 ¶119] (p. 29) —
[7 ¶120] (p. 29) Interest expense, net
[7 ¶121] (p. 29) 288
[7 ¶122] (p. 29) 319
[7 ¶123] (p. 29) 344
[7 ¶124] (p. 29) The decrease in depreciation and amortization in 2025 was primarily driven by lower capital spend and closed locations.
[7 ¶125] (p. 29) In 2025, we recognized $15 million in Impairments, store closing, and other costs. Included in this amount was $11 million of non-cash charges related to asset impairments, $10 million of severance, and $6 million of other costs primarily related to the closure of our Monroe, Ohio E-commerce Fulfillment Center. We also reversed $12 million of other exit costs initially recognized in the fourth […]
[7 ¶126] (p. 29) In 2024, we recognized $76 million in Impairments, store closing, and other costs related to the closure of our San Bernardino E-commerce Fulfillment Center and 27 underperforming stores. Included in this amount was $43 million of fixed asset impairments, $11 million of lease Right of Use (“ROU”) asset impairments, $14 million of severance, and $26 million in other costs relating to the closure […]
[7 ¶127] (p. 29) (Dollars in Millions)
[7 ¶128] (p. 29) 2025
[7 ¶129] (p. 29) 2024
[7 ¶130] (p. 29) 2023
[7 ¶131] (p. 29) Severance and other exit costs
[7 ¶132] (p. 29) $16
[7 ¶133] (p. 29) $40
[7 ¶134] (p. 29) $—
[7 ¶135] (p. 29) Other exit costs (reversals)
[7 ¶136] (p. 29) (12)
[7 ¶137] (p. 29) —
[7 ¶138] (p. 29) —
[7 ¶139] (p. 29) Lease (gains)
[7 ¶140] (p. 29) —
[7 ¶141] (p. 29) (18)
[7 ¶142] (p. 29) —
[7 ¶143] (p. 29) Impairments:
[7 ¶144] (p. 29) Buildings and other assets
[7 ¶145] (p. 29) 11
[7 ¶146] (p. 29) 43
[7 ¶147] (p. 29) —
[7 ¶148] (p. 29) Lease ROU assets
[7 ¶149] (p. 29) —
[7 ¶150] (p. 29) 11
[7 ¶151] (p. 29) —
[7 ¶152] (p. 29) Impairments, store closings, and other costs
[7 ¶153] (p. 29) $15
[7 ¶154] (p. 29) $76
[7 ¶155] (p. 29) $—
[7 ¶156] (p. 29) In 2025, Kohl’s entered into a settlement agreement to resolve a credit card interchange fee lawsuit in which we were a plaintiff. We recorded a gain, net of legal fees, and received cash of $129 million.
[7 ¶157] (p. 29) Net interest expense decreased in 2025 due to reductions in lease payments for stores closed earlier this year, a lower average outstanding balance on the revolving credit facility, a gain on extinguishment of debt related to the open market repurchases of long term debt completed in the fourth quarter of 2025, and a loss on extinguishment of debt in 2024 that was not repeated in 2025. The […]
[7 ¶158] (p. 30) Income Taxes
[7 ¶159] (p. 30) (Dollars in Millions)
[7 ¶160] (p. 30) 2025
[7 ¶161] (p. 30) 2024
[7 ¶162] (p. 30) 2023
[7 ¶163] (p. 30) Provision (benefit) for income taxes
[7 ¶164] (p. 30) $64
[7 ¶165] (p. 30) $5
[7 ¶166] (p. 30) $56
[7 ¶167] (p. 30) Effective tax rate
[7 ¶168] (p. 30) 19.0%
[7 ¶169] (p. 30) 3.9%
[7 ¶170] (p. 30) 15.1%
[7 ¶171] (p. 30) The effective tax rate for 2025 increased compared to 2024, primarily due to higher income before income taxes. The increase in 2025 resulted in a lower proportionate favorable impact from uncertain tax positions and federal tax credits when compared to the prior year.
[7 ¶172] (p. 30) GAAP to Non-GAAP Reconciliation
[7 ¶173] (p. 30) In addition to reporting our financial results in accordance with generally accepted accounting principles (GAAP), this Annual Report on Form 10-K contains certain non-GAAP financial results, including adjusted operating income, adjusted net income, and adjusted diluted earnings per share. These adjusted results exclude the gains, impairments, and other costs associated with the closing of 27 […]
[7 ¶174] (p. 30) (Dollars in Millions, Except per Share Data)
[7 ¶175] (p. 30) Operating Income
[7 ¶176] (p. 30) Net Income
[7 ¶177] (p. 30) Diluted Earnings per Share
[7 ¶178] (p. 30) 2025
[7 ¶179] (p. 30) GAAP
[7 ¶180] (p. 30) $624
[7 ¶181] (p. 30) $272
[7 ¶182] (p. 30) $2.38
[7 ¶183] (p. 30) Impairments, store closing, and other costs
[7 ¶184] (p. 30) 15
[7 ¶185] (p. 30) 15
[7 ¶186] (p. 30) 0.13
[7 ¶187] (p. 30) (Gain) on legal settlement
[7 ¶188] (p. 30) (129)
[7 ¶189] (p. 30) (129)
[7 ¶190] (p. 30) (1.13)
[7 ¶191] (p. 30) Income tax impact of items noted above
[7 ¶192] (p. 30) —
[7 ¶193] (p. 30) 28
[7 ¶194] (p. 30) 0.24
[7 ¶195] (p. 30) Adjusted (non-GAAP)
[7 ¶196] (p. 30) $510
[7 ¶197] (p. 30) $186
[7 ¶198] (p. 30) $1.62
[7 ¶199] (p. 30) 2024
[7 ¶200] (p. 30) GAAP
[7 ¶201] (p. 30) $433
[7 ¶202] (p. 30) $109
[7 ¶203] (p. 30) $0.98
[7 ¶204] (p. 30) Impairments, store closing, and other costs
[7 ¶205] (p. 30) 76
[7 ¶206] (p. 30) 76
[7 ¶207] (p. 30) 0.69
[7 ¶208] (p. 30) Income tax impact of items noted above
[7 ¶209] (p. 30) —
[7 ¶210] (p. 30) (18)
[7 ¶211] (p. 30) (0.17)
[7 ¶212] (p. 30) Adjusted (non-GAAP)
[7 ¶213] (p. 30) $509
[7 ¶214] (p. 30) $167
[7 ¶215] (p. 30) $1.50
[7 ¶216] (p. 30) Inflation, Global Economic Conditions, and Trade Policies
[7 ¶217] (p. 30) We expect that our operations will continue to be influenced by general economic conditions, including food, fuel and energy prices, higher unemployment, wage inflation, and costs to source our merchandise, including tariffs. During 2025, the U.S. government utilized the IEEPA to impose additional tariffs on a broad range of imports, including certain consumer goods. While these actions did not […]
[7 ¶218] (p. 31) Liquidity and Capital Resources
[7 ¶219] (p. 31) Capital Allocation
[7 ¶220] (p. 31) Our capital allocation strategy is to invest to maximize our overall long-term return and maintain a strong balance sheet. We follow a disciplined approach to capital allocation based on the following priorities: first we invest in our business to drive long-term profitable growth; second we pay a quarterly dividend; third we will capitalize on opportunities to further reduce our debt and overall […]
[7 ¶221] (p. 31) We will continue to invest in the business, as we plan to invest approximately $350 to $400 million in 2026 towards our strategic priorities. On February 25, 2026, our Board of Directors declared a quarterly cash dividend of $0.125 per share. The dividend will be paid on April 1, 2026 to all shareholders of record at the close of business on March 18, 2026. In the second quarter of 2025, we […]
[7 ¶222] (p. 31) Our period-end cash and cash equivalents balance increased to $674 million from $134 million in 2024. Our cash and cash equivalents balance includes short-term investments of $555 million and $9 million as of January 31, 2026, and February 1, 2025, respectively. Our investment policy is designed to preserve principal and liquidity of our short-term investments. This policy allows investments in […]
[7 ¶223] (p. 31) The following table presents our primary uses and sources of cash:
[7 ¶224] (p. 31) Cash Uses
[7 ¶225] (p. 31) Cash Sources
[7 ¶226] (p. 31) • Operational needs, including compensation and
[7 ¶227] (p. 31) benefit costs, rent, taxes, and other operating costs
[7 ¶228] (p. 31) • Inventory
[7 ¶229] (p. 31) • Capital expenditures
[7 ¶230] (p. 31) • Dividend payments
[7 ¶231] (p. 31) • Debt repayments and repurchases
[7 ¶232] (p. 31) • Share repurchases
[7 ¶233] (p. 31) • Cash flow from operations
[7 ¶234] (p. 31) • Line of credit under our revolving credit facility
[7 ¶235] (p. 31) • Issuance of debt
[7 ¶236] (p. 32) The following table includes cash balances and changes:
[7 ¶237] (p. 32) (Dollars in Millions)
[7 ¶238] (p. 32) 2025
[7 ¶239] (p. 32) 2024
[7 ¶240] (p. 32) 2023
[7 ¶241] (p. 32) Cash and cash equivalents
[7 ¶242] (p. 32) $674
[7 ¶243] (p. 32) $134
[7 ¶244] (p. 32) $183
[7 ¶245] (p. 32) Net cash provided by (used in):
[7 ¶246] (p. 32) Operating activities
[7 ¶247] (p. 32) $1,380
[7 ¶248] (p. 32) $648
[7 ¶249] (p. 32) $1,168
[7 ¶250] (p. 32) Investing activities
[7 ¶251] (p. 32) (333)
[7 ¶252] (p. 32) (467)
[7 ¶253] (p. 32) (562)
[7 ¶254] (p. 32) Financing activities
[7 ¶255] (p. 32) (507)
[7 ¶256] (p. 32) (230)
[7 ¶257] (p. 32) (576)
[7 ¶258] (p. 32) Adjusted free cash flow (a)
[7 ¶259] (p. 32) $935
[7 ¶260] (p. 32) $104
[7 ¶261] (p. 32) $519
[7 ¶262] (p. 32) (a)
[7 ¶263] (p. 32) Non-GAAP financial measure. Please see “Adjusted Free Cash Flow (Non-GAAP measure)” for a reconciliation of adjusted free cash flow to net cash provided by operating activities.
[7 ¶264] (p. 32) Operating Activities
[7 ¶265] (p. 32) Our operating cash outflows generally consist of payments to our employees for wages, salaries and other employee benefits, payments to our merchandise vendors for inventory (net of vendor allowances), payments to our shipping carriers, and payments to our landlords for rent. Operating cash outflows also include payments for income taxes and interest payments on our debt borrowings.
[7 ¶266] (p. 32) Operating activities generated cash of $1.4 billion in 2025 compared to $648 million in 2024. Operating cash flow increased due to a higher net income, partially driven by a $129 million gain recognized with respect to settlement of a credit card interchange fee lawsuit and inventory decreasing 7% to last year compared to an increase of 2% in 2024.
[7 ¶267] (p. 32) Investing Activities
[7 ¶268] (p. 32) Our investing cash outflows include payments for capital expenditures, including investments in new and existing stores, improvements to supply chain, and technology costs. Our investing cash inflows are generally from proceeds from sales of property and real estate.
[7 ¶269] (p. 32) Net cash used in investing activities decreased $134 million to $333 million in 2025. The decrease was primarily driven by lower capital spend during the year on the expansion of our E-commerce Fulfillment center in Etna, Ohio, which was completed in 2025, and fewer Sephora shop openings and other investments, consistent with our reduced capital expenditure plans for fiscal 2025. Additionally in […]
[7 ¶270] (p. 32) The following chart summarizes capital expenditures by major category:
[7 ¶271] (p. 33) At the end of 2025, we had a Sephora at Kohl's shop-in-shop ("Sephora shop") presence in over 1,100 of our stores, including 855 full size 2,500 square foot Sephora shops and 294 small format Sephora shops. We also substantially completed the rollout of impulse queuing lines across our store fleet and had two new store openings. In 2026, we anticipate capital expenditures of approximately $350 to […]
[7 ¶272] (p. 33) Financing Activities
[7 ¶273] (p. 33) Our financing strategy is to ensure adequate liquidity and access to capital markets. We also strive to maintain a balanced portfolio of debt maturities, while minimizing our borrowing costs. Our ability to access the public debt market has provided us with adequate sources of liquidity. Our continued access to these markets depends on multiple factors, including the condition of debt capital […]
[7 ¶274] (p. 33) During 2025, Moody's downgraded our corporate credit rating from Ba3 to B2 and revised their outlook to stable, and S&P downgraded our corporate credit rating from BB- to B+.
[7 ¶275] (p. 33) As of January 31, 2026, our corporate credit ratings and outlook were as follows:
[7 ¶276] (p. 33) Moody’s
[7 ¶277] (p. 33) S&P
[7 ¶278] (p. 33) Fitch
[7 ¶279] (p. 33) Corporate credit
[7 ¶280] (p. 33) B2
[7 ¶281] (p. 33) B+
[7 ¶282] (p. 33) BB-
[7 ¶283] (p. 33) Outlook
[7 ¶284] (p. 33) Stable
[7 ¶285] (p. 33) Negative
[7 ¶286] (p. 33) Negative
[7 ¶287] (p. 33) In the fourth quarter of 2024, S&P downgraded our senior unsecured credit rating from BB to BB- and Moody’s downgraded our rating from Ba3 to B1. As a result of the downgrades, the interest rate on our 3.375% notes due May 2031 increased an additional 50 basis points in the second quarter of 2025 due to the coupon adjustment provision within the notes. During the second quarter of 2025, Moody's […]
[7 ¶288] (p. 33) The majority of our financing activities generally include proceeds and/or repayments of borrowings under our revolving credit facility and long-term debt, dividend payments, and repurchases of common stock. Financing cash outflows also include payments to our landlords for leases classified as financing leases and financing obligations.
[7 ¶289] (p. 33) Financing activities used $507 million in 2025 compared to $230 million in 2024.
[7 ¶290] (p. 33) In 2025, we had $290 million of net repayments on our $1.5 billion credit facility compared to net borrowings of $198 million in 2024. There were no outstanding borrowings under the revolving credit facility, recorded as short-term debt, as of January 31, 2026. As of February 1, 2025, there was $290 million outstanding under the revolving credit facility.
[7 ¶291] (p. 33) In the second quarter of 2025, we issued $360 million aggregate principal amount of 10.000% senior secured notes due 2030 and received proceeds of $357 million, net of the debt discount. Also, during the second quarter of 2025, $353 million in aggregate principal amount of our 4.25% notes matured and were repaid.
[7 ¶292] (p. 33) In the fourth quarter of 2025, we reduced our outstanding debt by $87 million aggregate principal through repurchases of various notes on the open market.
[7 ¶293] (p. 33) In the second quarter of 2024, we completed a voluntary redemption of the remaining $113 million of outstanding 9.50% notes due May 15, 2025.
[7 ¶294] (p. 33) Cash dividend payments were $56 million ($0.50 per share) in 2025 and $222 million ($2.00 per share) in 2024.
[7 ¶295] (p. 34) There was no cash used for treasury stock purchases in 2025 or 2024. Share repurchases are discretionary in nature. The timing and amount of repurchases are based upon available cash balances, our stock price, and other factors. While we are not currently planning for share repurchases, we expect to resume share repurchases over the long-term following improvement in overall leverage.
[7 ¶296] (p. 34) Adjusted Free Cash Flow (Non-GAAP measure)
[7 ¶297] (p. 34) We generated $935 million of adjusted free cash flow for 2025 compared to $104 million in 2024. The increase was primarily driven by more cash provided by operating activities due to a higher net income and inventory decreasing 7% to last year compared to an increase of 2% in 2024. Additionally, capital expenditures decreased due to lower capital spend on the expansion of our E-commerce […]
[7 ¶298] (p. 34) In addition to net cash provided by operating activities, we provide Adjusted Free Cash Flow as a useful measure of our financial performance and position and our ability to generate additional cash flow from our business operations. We believe the presentation of Adjusted Free Cash Flow is relevant and useful for investors to evaluate the cash generated from operations consistent with the method […]
[7 ¶299] (p. 34) The following table reconciles adjusted free cash flow (a non-GAAP measure) to net cash provided by operating activities (a GAAP measure):
[7 ¶300] (p. 34) (Dollars in Millions)
[7 ¶301] (p. 34) 2025
[7 ¶302] (p. 34) 2024
[7 ¶303] (p. 34) 2023
[7 ¶304] (p. 34) Net cash provided by operating activities
[7 ¶305] (p. 34) $1,380
[7 ¶306] (p. 34) $648
[7 ¶307] (p. 34) $1,168
[7 ¶308] (p. 34) Acquisition of property and equipment
[7 ¶309] (p. 34) (372)
[7 ¶310] (p. 34) (466)
[7 ¶311] (p. 34) (577)
[7 ¶312] (p. 34) Free cash flow
[7 ¶313] (p. 34) $1,008
[7 ¶314] (p. 34) $182
[7 ¶315] (p. 34) $591
[7 ¶316] (p. 34) Finance lease and financing obligation payments
[7 ¶317] (p. 34) $(83)
[7 ¶318] (p. 34) $(79)
[7 ¶319] (p. 34) $(93)
[7 ¶320] (p. 34) Proceeds from financing obligations
[7 ¶321] (p. 34) 10
[7 ¶322] (p. 34) 1
[7 ¶323] (p. 34) 21
[7 ¶324] (p. 34) Adjusted free cash flow
[7 ¶325] (p. 34) $935
[7 ¶326] (p. 34) $104
[7 ¶327] (p. 34) $519
[7 ¶328] (p. 34) Key Financial Ratios
[7 ¶329] (p. 34) Key financial ratios that provide certain measures of our liquidity are as follows:
[7 ¶330] (p. 34) (Dollars in Millions)
[7 ¶331] (p. 34) 2025
[7 ¶332] (p. 34) 2024
[7 ¶333] (p. 34) Working capital
[7 ¶334] (p. 34) $1,160
[7 ¶335] (p. 34) $257
[7 ¶336] (p. 34) Current ratio
[7 ¶337] (p. 34) 1.46
[7 ¶338] (p. 34) 1.08
[7 ¶339] (p. 34) Our working capital and inventory levels typically build throughout the fall, peaking during the November and December holiday selling season.
[7 ¶340] (p. 34) The increase in our working capital and current ratio are driven by a higher Cash and cash equivalents balance, the repayment of $353 million of our 4.25% notes that matured during the year, and no outstanding borrowings under the revolving credit facility.
[7 ¶341] (p. 34) Debt Covenant Compliance
[7 ¶342] (p. 34) Our senior secured, asset based revolving credit facility contains customary events of default and financial, affirmative and negative covenants, including but not limited to, a springing financial covenant relating to our fixed charge coverage ratio and restrictions on indebtedness, liens, investments, asset dispositions, and restricted payments. As of January 31, 2026, we were in compliance […]
[7 ¶343] (p. 35) Contractual Obligations
[7 ¶344] (p. 35) Material contractual obligations arising in the normal course of business primarily consist of long-term debt and related interest payments, principal and interest payments for leases, and other purchase obligations. See Notes 2 and 3 to the Consolidated Financial Statements for amounts outstanding on January 31, 2026 related to debt and leases.
[7 ¶345] (p. 35) Other purchase obligations primarily include royalties, as well as payments associated with technology, marketing, and donation agreements. The obligations were $393 million as of January 31, 2026.
[7 ¶346] (p. 35) Off-Balance Sheet Arrangements
[7 ¶347] (p. 35) We have not provided any financial guarantees arising from arrangements with unconsolidated entities or persons as of January 31, 2026.
[7 ¶348] (p. 35) We have not created, and are not party to, any special-purpose or off-balance sheet entities for the purpose of raising capital, incurring debt, or operating our business. We do not have any arrangements or relationships with entities that are not consolidated into our financial statements that are reasonably likely to materially affect our financial condition, liquidity, results of operations, […]
[7 ¶349] (p. 35) Critical Accounting Policies and Estimates
[7 ¶350] (p. 35) The preparation of financial statements in conformity with accounting principles generally accepted in the United States requires us to make estimates and assumptions that affect reported amounts. Management has discussed the development, selection, and disclosure of these estimates and assumptions with the Audit Committee of our Board of Directors.
[7 ¶351] (p. 35) Retail Inventory Method and Inventory Valuation
[7 ¶352] (p. 35) The majority of our merchandise inventories are valued at the lower of cost or market using the retail inventory method (“RIM”). Under RIM, the valuation of inventory at cost and the resulting gross margins are calculated by applying a cost-to-retail ratio to the retail value of inventory. RIM is an averaging method that has been widely used in the retail industry due to its practicality. The use […]
[7 ¶353] (p. 35) RIM inherently requires management judgment and estimates, such as the amount and timing of permanent markdowns to clear unproductive or slow-moving inventory, which may impact the ending inventory valuation as well as gross margin. Factors considered in the determination of permanent markdowns include current and anticipated demand, customer preferences, age of the merchandise, fashion trends, […]
[7 ¶354] (p. 35) Inventory shrinkage is estimated as a percent of sales for the period between the last physical inventory count and the balance sheet date. Shrink is the difference between the recorded amount of inventory and the physical inventory. We perform an annual physical inventory count at the all of our stores, E-Commerce fulfillment centers, and distribution centers. The shrinkage rate from the most […]
[7 ¶355] (p. 35) Vendor Allowances
[7 ¶356] (p. 35) We frequently receive allowances from our vendors for markdowns that we have taken in order to sell the vendors' merchandise and/or to support gross margins earned on those sales. This markdown support generally relates to sold inventory or permanent markdowns and, accordingly, is reflected as a reduction to cost of merchandise sold. Markdown support related to merchandise that has not yet been […]
[7 ¶357] (p. 36) We also receive support from vendors for marketing and other costs that we have incurred to sell the vendors’ merchandise. To the extent the reimbursements are for specific, incremental, and identifiable costs incurred to sell the vendor's products and do not exceed the costs incurred, they are recognized as a reduction of Selling, General, and Administrative Expenses. If these criteria are not […]
[7 ¶358] (p. 36) Insurance Reserve Estimates
[7 ¶359] (p. 36) We are primarily self-insured for costs related to workers’ compensation, general liability, and employee-related health care benefits. We use a third-party actuary to estimate the liabilities associated with these risks. The actuary considers historical claims experience, demographic and severity factors, health care trends, and actuarial assumptions to estimate the liabilities associated with […]
[7 ¶360] (p. 36) Impairment of Long-Lived Assets
[7 ¶361] (p. 36) We review our long-lived assets for impairment when events or changes in circumstances, such as decisions to close a store or significant cash flow losses, indicate the carrying value of the asset may not be recoverable. All long-lived assets are reviewed for impairment at least annually.
[7 ¶362] (p. 36) If our evaluations, which are performed on an undiscounted cash flow basis, indicate that the carrying amount of the asset may not be recoverable, the potential impairment is measured as the excess of carrying value over the fair value of the impaired asset.
[7 ¶363] (p. 36) Identifying impaired assets and quantifying the related impairment loss, if any, requires significant estimates by management. The most significant of these estimates is the cash flow expected to result from the use and eventual disposition of the asset. When determining the stream of projected future cash flows associated with an individual store, management estimates future store performance […]
[7 ¶364] (p. 36) Income Taxes
[7 ¶365] (p. 36) We regularly evaluate the likelihood of realizing the benefit for income tax positions we have taken in various federal and state filings by considering all relevant facts, circumstances, and information available to us. If we believe it is more likely than not that our position will be sustained, we recognize a benefit at the largest amount which we believe is cumulatively greater than 50% […]
[7 ¶366] (p. 36) Unrecognized tax benefits require significant management judgment regarding applicable statutes and their related interpretation, the status of various income tax audits, and our particular facts and circumstances. Also, as audits are completed or statutes of limitations lapse, it may be necessary to record adjustments to our taxes payable, deferred tax assets, tax reserves, or income tax […]
[7 ¶367] (p. 36) Leases
[7 ¶368] (p. 36) Accounting for leased property and equipment requires compliance with technical accounting rules and judgment by management. Application of these accounting rules and assumptions made by management will determine if the lease is accounted for as a finance lease, an operating lease, or a financing obligation.
[7 ¶369] (p. 37) The following are estimates used by management in accounting for real estate and other leases:
[7 ¶370] (p. 37) •
[7 ¶371] (p. 37) Accounting lease term—Our accounting lease term includes all noncancelable periods and renewal periods that are reasonably assured of being exercised. Typically, renewal options are considered reasonably assured of being exercised if we have made significant leasehold improvements that would exceed the initial or renewal lease term and the cash flow performance of the store remains strong. The […]
[7 ¶372] (p. 37) •
[7 ¶373] (p. 37) Incremental borrowing rate—The incremental borrowing rate is the rate of interest that the lessee would have to pay to borrow on a collateralized basis over a similar term for an amount equal to the lease payments in a similar economic environment. The incremental borrowing rate is used in determining whether the lease is accounted for as an operating lease or a finance lease.
[7 ¶374] (p. 37) •
[7 ¶375] (p. 37) Fair market value of leased asset—The fair market value of leased retail property is generally estimated based on comparable market data as provided by third-party appraisers or consideration received from the landlord. Fair market value is used in determining whether the lease is accounted for as an operating lease or a finance lease.
[7 ¶376] (p. 37) Leases are further described in Note 3 of the Consolidated Financial Statements.
[7 ¶377] (p. 37) Sephora Arrangement
[7 ¶378] (p. 37) In 2020, we entered into an arrangement with Sephora to be the exclusive beauty offering at Kohl's. At the end of 2025, we had 855 full size 2,500 square foot Sephora shops and 294 small format Sephora shops in operation.
[7 ¶379] (p. 37) Both parties to the arrangement are active participants and are exposed to significant risks and rewards dependent on the success of the activities of the arrangement. The arrangement involves various activities including the merchandising, marketing, and operations of the Sephora shops and Kohls.com. Kohl’s is the principal on sales transactions with our customers and we recognize sales, cost of […]

### [7-LIQ] Item 7. Liquidity and Capital Resources
[7-LIQ ¶1] (p. 31) Liquidity and Capital Resources
[7-LIQ ¶2] (p. 31) Capital Allocation
[7-LIQ ¶3] (p. 31) Our capital allocation strategy is to invest to maximize our overall long-term return and maintain a strong balance sheet. We follow a disciplined approach to capital allocation based on the following priorities: first we invest in our business to drive long-term profitable growth; second we pay a quarterly dividend; third we will capitalize on opportunities to further reduce our debt and overall leverage, when appropriate; and fourth, we return excess cash to shareholders through our share repurchase program.
[7-LIQ ¶4] (p. 31) We will continue to invest in the business, as we plan to invest approximately $350 to $400 million in 2026 towards our strategic priorities. On February 25, 2026, our Board of Directors declared a quarterly cash dividend of $0.125 per share. The dividend will be paid on April 1, 2026 to all shareholders of record at the close of business on March 18, 2026. In the second quarter of 2025, we issued $360 million in aggregate principal amount of 10.000% senior secured notes due 2030; in addition $353 million in aggregate principal amount of our 4.25% notes matured and were repaid. In the fourth quarter of 2025, we reduced our outstanding debt by $87 million in aggregate principal through repurchases of various notes on the open market. We did not complete any share repurchases during fiscal 2025.
[7-LIQ ¶5] (p. 31) Our period-end cash and cash equivalents balance increased to $674 million from $134 million in 2024. Our cash and cash equivalents balance includes short-term investments of $555 million and $9 million as of January 31, 2026, and February 1, 2025, respectively. Our investment policy is designed to preserve principal and liquidity of our short-term investments. This policy allows investments in large money market funds or in highly rated direct short-term instruments. We also place dollar limits on our investments in individual funds or instruments.
[7-LIQ ¶6] (p. 31) The following table presents our primary uses and sources of cash:
[7-LIQ ¶7] (p. 31) Cash Uses
[7-LIQ ¶8] (p. 31) Cash Sources
[7-LIQ ¶9] (p. 31) • Operational needs, including compensation and
[7-LIQ ¶10] (p. 31) benefit costs, rent, taxes, and other operating costs
[7-LIQ ¶11] (p. 31) • Inventory
[7-LIQ ¶12] (p. 31) • Capital expenditures
[7-LIQ ¶13] (p. 31) • Dividend payments
[7-LIQ ¶14] (p. 31) • Debt repayments and repurchases
[7-LIQ ¶15] (p. 31) • Share repurchases
[7-LIQ ¶16] (p. 31) • Cash flow from operations
[7-LIQ ¶17] (p. 31) • Line of credit under our revolving credit facility
[7-LIQ ¶18] (p. 31) • Issuance of debt
[7-LIQ ¶19] (p. 32) The following table includes cash balances and changes:
[7-LIQ ¶20] (p. 32) (Dollars in Millions)
[7-LIQ ¶21] (p. 32) 2025
[7-LIQ ¶22] (p. 32) 2024
[7-LIQ ¶23] (p. 32) 2023
[7-LIQ ¶24] (p. 32) Cash and cash equivalents
[7-LIQ ¶25] (p. 32) $674
[7-LIQ ¶26] (p. 32) $134
[7-LIQ ¶27] (p. 32) $183
[7-LIQ ¶28] (p. 32) Net cash provided by (used in):
[7-LIQ ¶29] (p. 32) Operating activities
[7-LIQ ¶30] (p. 32) $1,380
[7-LIQ ¶31] (p. 32) $648
[7-LIQ ¶32] (p. 32) $1,168
[7-LIQ ¶33] (p. 32) Investing activities
[7-LIQ ¶34] (p. 32) (333)
[7-LIQ ¶35] (p. 32) (467)
[7-LIQ ¶36] (p. 32) (562)
[7-LIQ ¶37] (p. 32) Financing activities
[7-LIQ ¶38] (p. 32) (507)
[7-LIQ ¶39] (p. 32) (230)
[7-LIQ ¶40] (p. 32) (576)
[7-LIQ ¶41] (p. 32) Adjusted free cash flow (a)
[7-LIQ ¶42] (p. 32) $935
[7-LIQ ¶43] (p. 32) $104
[7-LIQ ¶44] (p. 32) $519
[7-LIQ ¶45] (p. 32) (a)
[7-LIQ ¶46] (p. 32) Non-GAAP financial measure. Please see “Adjusted Free Cash Flow (Non-GAAP measure)” for a reconciliation of adjusted free cash flow to net cash provided by operating activities.
[7-LIQ ¶47] (p. 32) Operating Activities
[7-LIQ ¶48] (p. 32) Our operating cash outflows generally consist of payments to our employees for wages, salaries and other employee benefits, payments to our merchandise vendors for inventory (net of vendor allowances), payments to our shipping carriers, and payments to our landlords for rent. Operating cash outflows also include payments for income taxes and interest payments on our debt borrowings.
[7-LIQ ¶49] (p. 32) Operating activities generated cash of $1.4 billion in 2025 compared to $648 million in 2024. Operating cash flow increased due to a higher net income, partially driven by a $129 million gain recognized with respect to settlement of a credit card interchange fee lawsuit and inventory decreasing 7% to last year compared to an increase of 2% in 2024.
[7-LIQ ¶50] (p. 32) Investing Activities
[7-LIQ ¶51] (p. 32) Our investing cash outflows include payments for capital expenditures, including investments in new and existing stores, improvements to supply chain, and technology costs. Our investing cash inflows are generally from proceeds from sales of property and real estate.
[7-LIQ ¶52] (p. 32) Net cash used in investing activities decreased $134 million to $333 million in 2025. The decrease was primarily driven by lower capital spend during the year on the expansion of our E-commerce Fulfillment center in Etna, Ohio, which was completed in 2025, and fewer Sephora shop openings and other investments, consistent with our reduced capital expenditure plans for fiscal 2025. Additionally in 2025, we received $54 million in proceeds from sale of property and equipment primarily due to the sale of corporate and other properties, compared to $6 million in proceeds in 2024.
[7-LIQ ¶53] (p. 32) The following chart summarizes capital expenditures by major category:
[7-LIQ ¶54] (p. 33) At the end of 2025, we had a Sephora at Kohl's shop-in-shop ("Sephora shop") presence in over 1,100 of our stores, including 855 full size 2,500 square foot Sephora shops and 294 small format Sephora shops. We also substantially completed the rollout of impulse queuing lines across our store fleet and had two new store openings. In 2026, we anticipate capital expenditures of approximately $350 to $400 million as we continue to invest in our business, including enhancing omnichannel capabilities.
[7-LIQ ¶55] (p. 33) Financing Activities
[7-LIQ ¶56] (p. 33) Our financing strategy is to ensure adequate liquidity and access to capital markets. We also strive to maintain a balanced portfolio of debt maturities, while minimizing our borrowing costs. Our ability to access the public debt market has provided us with adequate sources of liquidity. Our continued access to these markets depends on multiple factors, including the condition of debt capital markets, our operating performance, and our credit ratings.
[7-LIQ ¶57] (p. 33) During 2025, Moody's downgraded our corporate credit rating from Ba3 to B2 and revised their outlook to stable, and S&P downgraded our corporate credit rating from BB- to B+.
[7-LIQ ¶58] (p. 33) As of January 31, 2026, our corporate credit ratings and outlook were as follows:
[7-LIQ ¶59] (p. 33) Moody’s
[7-LIQ ¶60] (p. 33) S&P
[7-LIQ ¶61] (p. 33) Fitch
[7-LIQ ¶62] (p. 33) Corporate credit
[7-LIQ ¶63] (p. 33) B2
[7-LIQ ¶64] (p. 33) B+
[7-LIQ ¶65] (p. 33) BB-
[7-LIQ ¶66] (p. 33) Outlook
[7-LIQ ¶67] (p. 33) Stable
[7-LIQ ¶68] (p. 33) Negative
[7-LIQ ¶69] (p. 33) Negative
[7-LIQ ¶70] (p. 33) In the fourth quarter of 2024, S&P downgraded our senior unsecured credit rating from BB to BB- and Moody’s downgraded our rating from Ba3 to B1. As a result of the downgrades, the interest rate on our 3.375% notes due May 2031 increased an additional 50 basis points in the second quarter of 2025 due to the coupon adjustment provision within the notes. During the second quarter of 2025, Moody's downgraded our senior unsecured credit rating from B1 to B3; however, further downgrades by Moody's do not trigger incremental interest rate increases. In total, the interest rate on the notes due May 2031 have increased 175 basis points since their issuance due to the coupon adjustment provision within the notes.
[7-LIQ ¶71] (p. 33) The majority of our financing activities generally include proceeds and/or repayments of borrowings under our revolving credit facility and long-term debt, dividend payments, and repurchases of common stock. Financing cash outflows also include payments to our landlords for leases classified as financing leases and financing obligations.
[7-LIQ ¶72] (p. 33) Financing activities used $507 million in 2025 compared to $230 million in 2024.
[7-LIQ ¶73] (p. 33) In 2025, we had $290 million of net repayments on our $1.5 billion credit facility compared to net borrowings of $198 million in 2024. There were no outstanding borrowings under the revolving credit facility, recorded as short-term debt, as of January 31, 2026. As of February 1, 2025, there was $290 million outstanding under the revolving credit facility.
[7-LIQ ¶74] (p. 33) In the second quarter of 2025, we issued $360 million aggregate principal amount of 10.000% senior secured notes due 2030 and received proceeds of $357 million, net of the debt discount. Also, during the second quarter of 2025, $353 million in aggregate principal amount of our 4.25% notes matured and were repaid.
[7-LIQ ¶75] (p. 33) In the fourth quarter of 2025, we reduced our outstanding debt by $87 million aggregate principal through repurchases of various notes on the open market.
[7-LIQ ¶76] (p. 33) In the second quarter of 2024, we completed a voluntary redemption of the remaining $113 million of outstanding 9.50% notes due May 15, 2025.
[7-LIQ ¶77] (p. 33) Cash dividend payments were $56 million ($0.50 per share) in 2025 and $222 million ($2.00 per share) in 2024.
[7-LIQ ¶78] (p. 34) There was no cash used for treasury stock purchases in 2025 or 2024. Share repurchases are discretionary in nature. The timing and amount of repurchases are based upon available cash balances, our stock price, and other factors. While we are not currently planning for share repurchases, we expect to resume share repurchases over the long-term following improvement in overall leverage.
[7-LIQ ¶79] (p. 34) Adjusted Free Cash Flow (Non-GAAP measure)
[7-LIQ ¶80] (p. 34) We generated $935 million of adjusted free cash flow for 2025 compared to $104 million in 2024. The increase was primarily driven by more cash provided by operating activities due to a higher net income and inventory decreasing 7% to last year compared to an increase of 2% in 2024. Additionally, capital expenditures decreased due to lower capital spend on the expansion of our E-commerce Fulfillment center in Etna, Ohio, which was completed in 2025 and fewer Sephora shop openings and other investments.
[7-LIQ ¶81] (p. 34) In addition to net cash provided by operating activities, we provide Adjusted Free Cash Flow as a useful measure of our financial performance and position and our ability to generate additional cash flow from our business operations. We believe the presentation of Adjusted Free Cash Flow is relevant and useful for investors to evaluate the cash generated from operations consistent with the method used by management. Adjusted free cash flow is a non-GAAP financial measure which we define as net cash provided by operating activities and proceeds from financing obligations (which generally represent landlord reimbursements of construction costs) less capital expenditures and finance lease and financing obligation payments. Adjusted free cash flow is provided and should be evaluated in addition to, and not as an alternative to our other financial GAAP measures such as net cash provided by operating activities or net income.
[7-LIQ ¶82] (p. 34) The following table reconciles adjusted free cash flow (a non-GAAP measure) to net cash provided by operating activities (a GAAP measure):
[7-LIQ ¶83] (p. 34) (Dollars in Millions)
[7-LIQ ¶84] (p. 34) 2025
[7-LIQ ¶85] (p. 34) 2024
[7-LIQ ¶86] (p. 34) 2023
[7-LIQ ¶87] (p. 34) Net cash provided by operating activities
[7-LIQ ¶88] (p. 34) $1,380
[7-LIQ ¶89] (p. 34) $648
[7-LIQ ¶90] (p. 34) $1,168
[7-LIQ ¶91] (p. 34) Acquisition of property and equipment
[7-LIQ ¶92] (p. 34) (372)
[7-LIQ ¶93] (p. 34) (466)
[7-LIQ ¶94] (p. 34) (577)
[7-LIQ ¶95] (p. 34) Free cash flow
[7-LIQ ¶96] (p. 34) $1,008
[7-LIQ ¶97] (p. 34) $182
[7-LIQ ¶98] (p. 34) $591
[7-LIQ ¶99] (p. 34) Finance lease and financing obligation payments
[7-LIQ ¶100] (p. 34) $(83)
[7-LIQ ¶101] (p. 34) $(79)
[7-LIQ ¶102] (p. 34) $(93)
[7-LIQ ¶103] (p. 34) Proceeds from financing obligations
[7-LIQ ¶104] (p. 34) 10
[7-LIQ ¶105] (p. 34) 1
[7-LIQ ¶106] (p. 34) 21
[7-LIQ ¶107] (p. 34) Adjusted free cash flow
[7-LIQ ¶108] (p. 34) $935
[7-LIQ ¶109] (p. 34) $104
[7-LIQ ¶110] (p. 34) $519
[7-LIQ ¶111] (p. 34) Key Financial Ratios
[7-LIQ ¶112] (p. 34) Key financial ratios that provide certain measures of our liquidity are as follows:
[7-LIQ ¶113] (p. 34) (Dollars in Millions)
[7-LIQ ¶114] (p. 34) 2025
[7-LIQ ¶115] (p. 34) 2024
[7-LIQ ¶116] (p. 34) Working capital
[7-LIQ ¶117] (p. 34) $1,160
[7-LIQ ¶118] (p. 34) $257
[7-LIQ ¶119] (p. 34) Current ratio
[7-LIQ ¶120] (p. 34) 1.46
[7-LIQ ¶121] (p. 34) 1.08
[7-LIQ ¶122] (p. 34) Our working capital and inventory levels typically build throughout the fall, peaking during the November and December holiday selling season.
[7-LIQ ¶123] (p. 34) The increase in our working capital and current ratio are driven by a higher Cash and cash equivalents balance, the repayment of $353 million of our 4.25% notes that matured during the year, and no outstanding borrowings under the revolving credit facility.
[7-LIQ ¶124] (p. 34) Debt Covenant Compliance
[7-LIQ ¶125] (p. 34) Our senior secured, asset based revolving credit facility contains customary events of default and financial, affirmative and negative covenants, including but not limited to, a springing financial covenant relating to our fixed charge coverage ratio and restrictions on indebtedness, liens, investments, asset dispositions, and restricted payments. As of January 31, 2026, we were in compliance with all covenants.

### [7A] Item 7A. Quantitative and Qualitative Disclosures About Market Risk
[7A ¶1] (p. 37) Item 7A. Quantitative and Qualitative Disclosures about Market Risk
[7A ¶2] (p. 37) Our operating results are subject to interest rate risk as the remaining $425 million of notes outstanding issued in March 2021 include coupon rate step ups if our long-term debt is downgraded to below a BBB- credit rating by S&P Global Ratings or Baa3 by Moody's Investors Service, Inc., which has occurred in 2025, 2024, and 2023. All other long-term debt is at fixed interest rates and, therefore, is not affected by changes in interest rates. When our long-term debt instruments mature, we may refinance them at the existing market interest rates, which may be more or less than interest rates on the maturing debt.
[7A ¶3] (p. 37) We are also subject to interest rate risk from changes in the interest rates under our $1.5 billion revolving credit facility. Outstanding borrowings under the credit facility bear interest at a variable rate based on SOFR plus the applicable margin. There were no outstanding borrowings under the revolving credit facility as of January 31, 2026.
[7A ¶4] (p. 37) We share in the net risk-adjusted revenue of the Kohl’s credit card portfolio as defined by the sum of finance charges, late fees, and other revenue less write-offs of uncollectible accounts. We also share the costs of funding the outstanding receivables as interest rates exceed defined rates. As a result, our share of profits from the credit card portfolio may be negatively impacted by increases in interest rates. The reduced profitability, if any, will be impacted by various factors, including our ability to pass higher funding costs on to the credit card holders and the outstanding receivable balance, and cannot be reasonably estimated at this time.

### [DEBT] Debt note (financial statements)
[DEBT ¶1] (p. 53) 2. Debt
[DEBT ¶2] (p. 53) Long-term debt, which excludes borrowings on the revolving credit facility, consists of the following secured and unsecured debt:
[DEBT ¶3] (p. 53) Outstanding
[DEBT ¶4] (p. 53) Maturity (Dollars in Millions)
[DEBT ¶5] (p. 53) Effective Rate at Issuance
[DEBT ¶6] (p. 53) Coupon Rate
[DEBT ¶7] (p. 53) January 31, 2026
[DEBT ¶8] (p. 53) February 1, 2025
[DEBT ¶9] (p. 53) 2025
[DEBT ¶10] (p. 53) 4.25%
[DEBT ¶11] (p. 53) 4.25%
[DEBT ¶12] (p. 53) —
[DEBT ¶13] (p. 53) 353
[DEBT ¶14] (p. 53) 2029
[DEBT ¶15] (p. 53) 7.36%
[DEBT ¶16] (p. 53) 7.25%
[DEBT ¶17] (p. 53) 42
[DEBT ¶18] (p. 53) 42
[DEBT ¶19] (p. 53) 2030
[DEBT ¶20] (p. 53) 10.25%
[DEBT ¶21] (p. 53) 10.00%
[DEBT ¶22] (p. 53) 360
[DEBT ¶23] (p. 53) —
[DEBT ¶24] (p. 53) 2031
[DEBT ¶25] (p. 53) 3.40%
[DEBT ¶26] (p. 53) 5.13%
[DEBT ¶27] (p. 53) 425
[DEBT ¶28] (p. 53) 500
[DEBT ¶29] (p. 53) 2033
[DEBT ¶30] (p. 53) 6.05%
[DEBT ¶31] (p. 53) 6.00%
[DEBT ¶32] (p. 53) 112
[DEBT ¶33] (p. 53) 112
[DEBT ¶34] (p. 53) 2037
[DEBT ¶35] (p. 53) 6.89%
[DEBT ¶36] (p. 53) 6.88%
[DEBT ¶37] (p. 53) 89
[DEBT ¶38] (p. 53) 101
[DEBT ¶39] (p. 53) 2045
[DEBT ¶40] (p. 53) 5.57%
[DEBT ¶41] (p. 53) 5.55%
[DEBT ¶42] (p. 53) 427
[DEBT ¶43] (p. 53) 427
[DEBT ¶44] (p. 53) Outstanding secured and unsecured senior debt
[DEBT ¶45] (p. 53) 1,455
[DEBT ¶46] (p. 53) 1,535
[DEBT ¶47] (p. 53) Unamortized debt discounts and deferred financing costs
[DEBT ¶48] (p. 53) (19)
[DEBT ¶49] (p. 53) (8)
[DEBT ¶50] (p. 53) Current portion of secured and unsecured senior debt
[DEBT ¶51] (p. 53) —
[DEBT ¶52] (p. 53) (353)
[DEBT ¶53] (p. 53) Long-term secured and unsecured senior debt
[DEBT ¶54] (p. 53) $1,436
[DEBT ¶55] (p. 53) $1,174
[DEBT ¶56] (p. 53) Effective interest rate at issuance
[DEBT ¶57] (p. 53) 6.26%
[DEBT ¶58] (p. 53) 4.73%
[DEBT ¶59] (p. 54) Our estimated fair value of secured and unsecured senior long-term debt is determined using Level 1 inputs, using financial instruments with unadjusted, quoted prices listed on active market exchanges. The estimated fair value of our secured and unsecured senior debt was $1.2 billion at January 31, 2026 and $1.2 billion at February 1, 2025.
[DEBT ¶60] (p. 54) In the fourth quarter of 2024, S&P downgraded our senior unsecured credit rating from BB to BB- and Moody’s downgraded our rating from Ba3 to B1. As a result of the downgrades, the interest rate on our 3.375% notes due May 2031 increased an additional 50 basis points in the second quarter of 2025 due to the coupon adjustment provision within the notes. During the second quarter of 2025, Moody's downgraded our senior unsecured credit rating from B1 to B3; however, further downgrades by Moody's do not trigger incremental interest rate increases. In total, the interest rate on the notes due May 2031 have increased 175 basis points since their issuance due to the coupon adjustment provision within the notes.
[DEBT ¶61] (p. 54) In the second quarter of 2025, we issued $360 million aggregate principal amount of 10.000% senior secured notes due 2030 and received proceeds of $357 million, net of the debt discount. The notes are guaranteed by certain of our subsidiaries. Certain of these guarantees are secured by eleven distribution centers and E-commerce Fulfillment Centers, which are held by our subsidiaries, as well as the equity interests in one of our subsidiaries.
[DEBT ¶62] (p. 54) Also in the second quarter of 2025, $353 million in aggregate principal amount of our 4.25% notes matured and were repaid.
[DEBT ¶63] (p. 54) In the fourth quarter of 2025, we reduced our outstanding debt by $87 million through repurchases of our notes on the open market, resulting in a gain on extinguishment of debt of $11 million recognized in net interest expense.
[DEBT ¶64] (p. 54) In the second quarter of 2024, we completed a voluntary redemption of the remaining $113 million of outstanding 9.50% notes due May 15, 2025. We recognized a $5 million loss on extinguishment of debt in net interest expense which is primarily a make whole premium paid to holders as a result of the redemption.
[DEBT ¶65] (p. 54) Borrowings under the $1.5 billion revolving credit facility, recorded as short-term debt, were $0 as of January 31, 2026, and $290 million as of February 1, 2025. Outstanding borrowings under the credit facility bear interest at a variable rate based on SOFR plus the applicable margin. As of January 31, 2026, we had $44 million of standby and trade letters of credit outstanding under the credit facility, which reduces the available borrowing capacity.
[DEBT ¶66] (p. 54) Our various debt agreements contain covenants including limitations on additional indebtedness and certain financial tests. As of January 31, 2026, we were in compliance with all covenants of the various debt agreements.
[DEBT ¶67] (p. 54) We also had outstanding standby and trade letters of credit outside of the credit facility totaling approximately $5 million at January 31, 2026.