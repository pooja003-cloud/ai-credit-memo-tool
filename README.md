# AI credit memo tool

**Python does every number, Claude only writes, and a script proves it.**

Turns a public company's 10-K into a bank-style credit memo with an approve-or-decline recommendation, built so that no number in the memo can come from the language model.

## Situation

A commercial-bank credit memo stands or falls on its numbers. Language models write fluent credit analysis, but they can misstate a figure or invent one, and a reader can't tell which.

## Task

Build a tool that reads a company's 10-K and produces a credit memo a credit committee could use, where every figure is computed in Python and provably traced to the filing, and the model only writes the words.

## Action

1. **Spread.** Python pulls the income statement, balance sheet and cash flow statement from SEC EDGAR exactly as printed, then maps them into a standard bank spread. Tie-outs check every subtotal against the filing.
2. **Analysis.** Credit ratios (leverage with and without leases, coverage, DSCR), a stress case, a pro forma for the requested loan, and a 1-to-10 risk grade frozen before any agency rating was looked up.
3. **Memo.** Claude (`claude -p`) drafts the memo using placeholders like `{{FY2025.debt_ebitda}}` instead of numbers, and cites the 10-K paragraph behind each claim.
4. **Checker.** A script fills in the numbers and rejects any draft with a typed number, an unknown placeholder, a missing or wrong citation, or a misquote. Failed drafts go back to Claude with the errors.

## Result

| Company | Risk grade (1 = best) | Recommendation | What the memo found |
|---|---|---|---|
| [DaVita](memos/DVA_memo.md) | 7 | Approve with conditions | Under stress, leverage would likely breach DaVita's own loan covenant |
| [Union Pacific](memos/UNP_memo.md) | 5 | Approve with conditions | Strong on its own; the ~$20B debt-funded Norfolk Southern deal is the real risk |
| [Kohl's](memos/KSS_memo.md) | 8 | Decline | The FY2025 earnings "recovery" rests on a one-off $129M legal settlement |

Each memo's recommendation agrees with its grade. Full table: [docs/memos.md](docs/memos.md).

- **Numbers verified by hand:** 228 of 228 DaVita lines match the 10-K exactly ([hand check](docs/validation.md#hand-check-against-the-10-k)).
- **Grade vs agency ratings:** matches for DaVita and Kohl's; Union Pacific is one notch harsher, because its score sits exactly on a grade boundary ([details](docs/validation.md#grade-vs-agency-ratings)).
- **The checker works, including on people:** every first draft failed it, and it also rejected numbers the human reviewer typed by hand.
- **What it doesn't prove:** the checker proves the numbers and citations, not the reasoning. A reversed interest-rate-cap argument passed every check and was caught in human review, so a credit reviewer is still part of the process.

## See it

- Example memo: [DaVita](memos/DVA_memo.md) (approve with conditions). Also [Union Pacific](memos/UNP_memo.md) and [Kohl's](memos/KSS_memo.md).
- [Ratio and stress tables](docs/tables.md)

## Run it

```bash
pip install -r requirements.txt
export SEC_USER_AGENT="Your Name you@example.com"
python -m creditmemo.edgar DVA UNP KSS     # download SEC data (cached)
python -m creditmemo.build                 # spreads, ratios, stress, grade
python -m creditmemo.draft DVA             # draft, check and render a memo (needs claude -p)
pytest
```

Only drafting needs Claude Code; the committed memos can be re-checked without it. Full commands and code layout: [docs/reference.md](docs/reference.md).

## More detail

- [docs/validation.md](docs/validation.md): checker, human review, tie-outs, hand check, agency benchmark, limits
- [docs/memos.md](docs/memos.md): how each memo was drafted and reviewed
- [DECISIONS.md](DECISIONS.md): every definition and rule, fixed before coding
