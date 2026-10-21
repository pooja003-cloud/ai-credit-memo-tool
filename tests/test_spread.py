import pytest
from factsbuilder import CF

from creditmemo.spread import build_spread, load_override, load_tag_spec

SPEC = load_tag_spec()
COMPANY = {"cik": 1, "name": "Test Co", "fiscal_label": "end_year"}


def full_company(years=(2023, 2024, 2025)):
    """A borrower with every standard tag present."""
    cf = CF()
    for y in years:
        cf.flow("Revenues", 1000, y)
        cf.flow("OperatingIncomeLoss", 150, y)
        cf.flow("DepreciationDepletionAndAmortization", 50, y)
        cf.flow("InterestExpense", 40, y)
        cf.flow("NetIncomeLoss", 80, y)
        cf.flow("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", 105, y)
        cf.flow("NetCashProvidedByUsedInOperatingActivities", 170, y)
        cf.flow("PaymentsToAcquirePropertyPlantAndEquipment", 60, y)
        cf.flow("IncomeTaxesPaidNet", 20, y)
        cf.flow("OperatingLeaseCost", 50, y)
        cf.inst("CashAndCashEquivalentsAtCarryingValue", 100, y)
        cf.inst("AssetsCurrent", 400, y)
        cf.inst("LiabilitiesCurrent", 250, y)
        cf.inst("Assets", 2000, y)
        cf.inst("StockholdersEquity", 700, y)
        cf.inst("ShortTermBorrowings", 20, y)
        cf.inst("CommercialPaper", 30, y)
        cf.inst("LongTermDebtCurrent", 50, y)
        cf.inst("LongTermDebtNoncurrent", 450, y)
        cf.inst("FinanceLeaseLiability", 50, y)
        cf.inst("OperatingLeaseLiability", 300, y)
        cf.inst("LongTermDebtMaturitiesRepaymentsOfPrincipalInNextTwelveMonths", 50, y)
    return cf


def test_real_tag_config_loads():
    for concept, cs in SPEC.items():
        assert cs["kind"] in ("flow", "instant"), concept
        assert cs["label"]
    for t in ("DVA", "UNP", "KSS"):
        load_override(t)


def test_full_spread_matches_worked_example():
    s = build_spread(full_company().data, "TST", COMPANY, SPEC)
    assert [p["label"] for p in s["periods"]] == ["FY2023", "FY2024", "FY2025"]
    x = s["ratios"]["FY2025"]
    assert x["debt_ebitda"] == pytest.approx(3.0)
    assert x["lease_adj_debt_ebitdar"] == pytest.approx(3.6)
    assert x["dscr"] == pytest.approx(120 / 90)
    assert s["warnings"] == []
    rec = s["lines"]["revenue"]["FY2025"]
    assert rec["tag"] == "Revenues" and rec["source"] == "xbrl" and rec["unit"] == "USD"
    assert rec["filing_url"].startswith("https://www.sec.gov/Archives/edgar/data/1/")


def test_missing_tag_falls_through_the_priority_list():
    cf = CF()
    for y in (2024, 2025):
        cf.flow("RevenueFromContractWithCustomerExcludingAssessedTax", 900, y)
        cf.flow("Depreciation", 30, y)  # UNP-style: only Depreciation
    s = build_spread(cf.data, "TST", COMPANY, SPEC, years=2)
    assert s["lines"]["revenue"]["FY2025"]["tag"] == "RevenueFromContractWithCustomerExcludingAssessedTax"
    da = s["lines"]["da"]["FY2025"]
    assert da["tag"] == "Depreciation" and "amortization" in da["note"]
    assert s["lines"]["operating_income"]["FY2025"]["source"] == "missing"
    assert s["ratios"]["FY2025"]["debt_ebitda"] is None
    assert any("Operating income: missing" in w for w in s["warnings"])


def test_cash_interest_is_flagged_as_proxy():
    cf = full_company()
    del cf.data["facts"]["us-gaap"]["InterestExpense"]
    for y in (2023, 2024, 2025):
        cf.flow("InterestPaidNet", 42, y)
    s = build_spread(cf.data, "TST", COMPANY, SPEC)
    rec = s["lines"]["interest_expense"]["FY2025"]
    assert rec["proxy"] is True and rec["value"] == 42
    assert any("PROXY" in w and "Interest expense" in w for w in s["warnings"])


def test_net_interest_tag_is_sign_flipped():
    cf = full_company()
    del cf.data["facts"]["us-gaap"]["InterestExpense"]
    for y in (2023, 2024, 2025):
        cf.flow("InterestIncomeExpenseNonoperatingNet", -40, y)
    s = build_spread(cf.data, "TST", COMPANY, SPEC)
    assert s["lines"]["interest_expense"]["FY2025"]["value"] == 40
    assert s["ratios"]["FY2025"]["interest_coverage"] == pytest.approx(5.0)


def test_maturities_fall_back_to_current_ltd():
    cf = full_company()
    del cf.data["facts"]["us-gaap"]["LongTermDebtMaturitiesRepaymentsOfPrincipalInNextTwelveMonths"]
    s = build_spread(cf.data, "TST", COMPANY, SPEC)
    rec = s["lines"]["scheduled_principal"]["FY2025"]
    assert rec["source"] == "fallback:current_ltd" and rec["value"] == 50
    assert rec["tag"] == "LongTermDebtCurrent"


def test_lease_liability_built_from_current_plus_noncurrent():
    cf = full_company()
    del cf.data["facts"]["us-gaap"]["OperatingLeaseLiability"]
    for y in (2023, 2024, 2025):
        cf.inst("OperatingLeaseLiabilityCurrent", 60, y)
        cf.inst("OperatingLeaseLiabilityNoncurrent", 240, y)
    s = build_spread(cf.data, "TST", COMPANY, SPEC)
    rec = s["lines"]["operating_lease_liabilities"]["FY2025"]
    assert rec["source"] == "sum" and rec["value"] == 300 and len(rec["components"]) == 2


def test_untagged_optional_debt_counts_as_zero_and_is_flagged():
    cf = full_company()
    del cf.data["facts"]["us-gaap"]["CommercialPaper"]
    s = build_spread(cf.data, "TST", COMPANY, SPEC)
    assert s["lines"]["commercial_paper"]["FY2025"]["source"] == "assumed_zero"
    assert s["derived"]["FY2025"]["total_debt"] == 570
    assert any("Commercial paper: not tagged" in w for w in s["warnings"])


def test_manual_override_wins_and_needs_a_source():
    cf = full_company()
    ov = {"manual": {"cash_taxes": {"FY2025": {"value": 35, "source": "10-K FY2025 p. 60"}}}}
    s = build_spread(cf.data, "TST", COMPANY, SPEC, ov)
    rec = s["lines"]["cash_taxes"]["FY2025"]
    assert rec["source"] == "manual" and rec["value"] == 35
    assert s["lines"]["cash_taxes"]["FY2024"]["source"] == "xbrl"
    with pytest.raises(ValueError):
        build_spread(cf.data, "TST", COMPANY, SPEC,
                     {"manual": {"cash_taxes": {"FY2025": {"value": 35}}}})


def test_manual_todo_placeholder_is_ignored():
    s = build_spread(full_company().data, "TST", COMPANY, SPEC,
                     {"manual": {"cash_taxes": {"_todo": "fill me"}}})
    assert s["lines"]["cash_taxes"]["FY2025"]["source"] == "xbrl"


def test_finance_leases_not_double_counted():
    s = build_spread(full_company().data, "TST", COMPANY, SPEC, {"finance_leases_in_debt": True})
    rec = s["lines"]["finance_lease_liabilities"]["FY2025"]
    assert rec["value"] == 0 and rec["reported_value"] == 50
    assert s["derived"]["FY2025"]["total_debt"] == 550


def test_company_override_tags_go_first():
    cf = full_company()
    for y in (2023, 2024, 2025):
        cf.flow("CostsAndExpenses", 1, y)
        cf.flow("DepreciationAndAmortization", 55, y)
    s = build_spread(cf.data, "TST", COMPANY, SPEC, {"tags": {"da": ["DepreciationAndAmortization"]}})
    assert s["lines"]["da"]["FY2025"]["value"] == 55


def test_no_revenue_raises():
    with pytest.raises(ValueError):
        build_spread(CF().data, "TST", COMPANY, SPEC)
