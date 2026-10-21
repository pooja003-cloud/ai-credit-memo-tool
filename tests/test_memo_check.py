from creditmemo.memo_check import Values, check, fmt_money, render

SPREAD = {
    "periods": [{"label": "FY2024"}, {"label": "FY2025"}],
    "ratios": {"FY2024": {"debt_ebitda": 3.3567, "dscr": None},
               "FY2025": {"debt_ebitda": 3.7236, "dscr": 2.9115}},
    "derived": {"FY2024": {"ebitda": 2814343000.0, "ebitda_margin": 0.2196},
                "FY2025": {"ebitda": 2758963000.0, "ebitda_margin": 0.2022}},
    "ratio_inputs": {"FY2024": {"cash_taxes": 387940000.0}, "FY2025": {"cash_taxes": 176688000.0}},
    "standard": {"periods": {"income": ["FY2024", "FY2025"], "balance": ["FY2024", "FY2025"],
                             "cashflow": ["FY2024", "FY2025"]},
                 "income": [{"key": "revenue", "values": [12815550000.0, 13643069000.0]},
                            {"key": "da", "values": [723860000.0, 715348000.0]}],
                 "balance": [{"key": "cash", "values": [794933000.0, 676438000.0]}],
                 "cashflow": [{"key": "da", "values": [723860000.0, 715348000.0]}]},
    "stress": {"scenario": {"revenue_shock": 0.2, "margin_shock": 0.03, "rate_shock": 0.02},
               "floating_rate_share": 0.381, "extra_interest": 78300000.0,
               "base_margin": 0.2022, "stressed_margin": 0.1722,
               "stressed": {"ratios": {"debt_ebitda": 5.47}, "derived": {"ebitda": 1879000000.0}}},
    "facility": {"type": "Senior unsecured term loan", "amount_usd": 500000000, "tenor_years": 5},
    "floating_rate_share": 0.381,
}
SECTIONS = {"url": "https://www.sec.gov/x.htm", "sections": {
    "1A": {"paragraphs": [{"text": "Item 1A. Risk Factors", "page": "23"},
                          {"text": "Changes in reimbursement rates for dialysis could reduce our revenues.",
                           "page": "24"}]},
    "7-LIQ": {"paragraphs": [{"text": "Liquidity and capital resources", "page": "61"},
                             {"text": "Our primary recurrent sources of liquidity are cash from operations and cash from borrowings.",
                              "page": "61"}]},
}}
V = Values(SPREAD)

GOOD = """# Credit memo: DaVita Inc.

## Financial analysis
Revenue reached {{FY2025.revenue}} in FY2025, up {{growth.FY2025.revenue}} on FY2024.
Leverage rose to {{FY2025.debt_ebitda}} as EBITDA fell to {{FY2025.ebitda}}.
Management says "Our primary recurrent sources of liquidity are cash from operations" [7-LIQ ¶2].
Reimbursement risk is the main threat to revenue [1A ¶2].

| Metric | FY2025 | Stress |
|---|---|---|
| Debt / EBITDA | {{FY2025.debt_ebitda}} | {{stress.debt_ebitda}} |

Recommendation: Decline
"""


def test_values_and_formats():
    assert V.resolve("FY2025.debt_ebitda") == (True, "3.72x")
    assert V.resolve("FY2025.ebitda") == (True, "$2.8 billion")
    assert V.resolve("FY2025.ebitda_margin") == (True, "20.2%")
    assert V.resolve("FY2025.revenue") == (True, "$13.6 billion")
    assert V.resolve("FY2025.balance.cash") == (True, "$676 million")
    assert V.resolve("FY2025.cash_taxes") == (True, "$177 million")
    assert V.resolve("FY2024.dscr") == (True, "n.m.")
    assert V.resolve("growth.FY2025.revenue") == (True, "6.5%")
    assert V.resolve("stress.debt_ebitda") == (True, "5.47x")
    assert V.resolve("stress.extra_interest") == (True, "$78 million")
    assert V.resolve("facility.amount_usd") == (True, "$500 million")
    assert V.resolve("facility.tenor_years") == (True, "5")
    assert V.resolve("floating_rate_share") == (True, "38.1%")
    assert V.resolve("FY2026.revenue")[0] is False
    assert V.resolve("growth.FY2024.revenue")[0] is False   # no prior year
    assert fmt_money(-25e6) == "-$25 million"


def test_good_draft_passes_and_renders():
    r = check(GOOD, V, SECTIONS)
    assert r["ok"], r["errors"]
    assert r["recommendation"] == "Decline"
    out = render(GOOD, V, SECTIONS)
    assert "{{" not in out
    assert "3.72x" in out and "$13.6 billion" in out
    assert "[10-K Item 7, Liquidity ¶2, p. 61](https://www.sec.gov/x.htm)" in out


def errors(draft):
    return [e["type"] for e in check(draft, V, SECTIONS)["errors"]]


def test_typed_number_fails():
    assert "typed_number" in errors(GOOD.replace("{{FY2025.debt_ebitda}} as", "3.7x as"))
    assert "typed_number" in errors(GOOD.replace("Reimbursement risk", "About 80% of revenue"))


def test_allowed_numbers_pass():
    d = GOOD.replace("Reimbursement risk is", "In FY2025 and 2024, per Item 1A and Note 12 of the 10-K, "
                     "on our 1-to-10 scale, Term Loan A-2 risk is")
    assert errors(d) == []


def test_unknown_placeholder_fails():
    assert "unknown_placeholder" in errors(GOOD.replace("{{FY2025.ebitda}}", "{{FY2025.ebitdaa}}"))


def test_uncited_claim_fails():
    assert "uncited_claim" in errors(GOOD.replace(" [1A ¶2]", ""))


def test_bad_citation_fails():
    assert "bad_citation" in errors(GOOD.replace("[1A ¶2]", "[1A ¶9]"))
    assert "bad_citation" in errors(GOOD.replace("[1A ¶2]", "[7A ¶1]"))   # section not extracted
    assert "bad_citation" in errors(GOOD.replace("[1A ¶2]", "[Item 1A ¶2]"))


def test_misquote_fails():
    d = GOOD.replace("cash from operations\"", "cash from asset sales\"")
    assert "quote_not_found" in errors(d)


def test_missing_recommendation_fails():
    assert "no_recommendation" in errors(GOOD.replace("Recommendation: Decline", ""))
