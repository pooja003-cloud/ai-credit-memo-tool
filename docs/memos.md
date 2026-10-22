# The memos

Back to the [README](../README.md).

| Company | Grade | Recommendation | Draft attempts | Agrees with grade? | Notable |
|---|---|---|---|---|---|
| [DaVita](../memos/DVA_memo.md) | 7 | Approve with conditions | 2 (7 errors, then pass) | Yes | Stressed leverage likely breaches DaVita's own 5.00x covenant [DEBT ¶58] |
| [Union Pacific](../memos/UNP_memo.md) | 5 | Approve with conditions | 2 (5 errors, then pass) | Yes; argues the grade understates standalone quality (structural working-capital deficit) | ~$20B debt-funded Norfolk Southern acquisition is the main risk; requires combined projections and a re-grade at closing |
| [Kohl's](../memos/KSS_memo.md) | 8 | Decline | 2 (7 errors, then pass) | Yes | FY2025 EBITDA "recovery" rests on a one-off $129M settlement gain; unsecured lender behind secured debt; stressed pro forma DSCR below 1.0x |

## The DaVita memo, step by step

How it was made (`python -m creditmemo.draft DVA`):
- Claude (`claude -p`) got a fact sheet of placeholder names with their values, two analyst points on the interest-rate caps, and 1,052 numbered 10-K paragraphs. It wrote placeholders only.
- **Attempt 1 failed the checker with 7 errors**: six sentences with no placeholder or citation, and one stray number ("Section 8"). The errors went back to Claude; **attempt 2 passed** (94 placeholders, 46 citations, 0 errors). Every prompt, draft and check report is in `memos/`.
- Review after the pass: 21 citations read against the full 10-K paragraphs, and all support their sentence. Two wording edits, both re-checked: the stress notch was described in the wrong direction, and "roughly a third" became "more than a third" (the 10-K says about 36%). The first version of one edit typed "4.0x" by hand, and the checker rejected it. Edits are logged in `memos/DVA_result.json`.
- Recommendation vs grade: consistent. Grade 7 is sub-investment-grade but serviceable; the conditions target what the stress test flags (a leverage covenant set between base and stressed debt / EBITDA, no buybacks from proceeds, matching subsidiary guarantees, hedging past 2028). Claude also spotted that stressed leverage would likely breach DaVita's own 5.00x credit-agreement covenant [DEBT ¶58].
- Second review round (all re-checked, logged in `memos/DVA_result.json`): summary box with grade, recommendation and agency ratings; the covenant step-down to 4.50x after 2028 inside the tenor; NCI puts of $1.4B due in 2026 against $676M of cash, with the undrawn $1.5B revolver as mitigant; EBITDA excluding the FY2024 ownership gain, which turns the FY2025 decline into 2.0% growth; an NCI risk; sign-safe `{{abs:...}}` amounts. 10-K figures that aren't in the spread (covenant levels, puts, revolver, caps) are typed into `config/companies.json` with their 10-K citation, like the floating-rate share, so the no-typed-numbers rule still holds.
- Third review round: a pro forma layer (`creditmemo/proforma.py`) adds the $500M loan: debt / EBITDA 3.72x to 3.90x, just under the 4.00x level above which the credit agreement's restrictions apply; stressed 5.73x. The grade stays on reported figures.
- Known weakness, now addressed: the every-sentence-cited rule pushed Claude to attach decorative citations to opinions. Opinions in the Recommendation section may now carry `[judgment]` instead, and the checker rejects `[judgment]` anywhere else.
