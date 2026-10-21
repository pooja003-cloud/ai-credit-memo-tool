from datetime import date

from factsbuilder import CF

from creditmemo.facts import annual_flows, fiscal_label, fiscal_year_ends, instants


def test_restated_value_from_later_10k_wins():
    cf = CF()
    cf.flow("Revenues", 100, 2023, accn="A-23", filed="2024-02-10")   # original
    cf.flow("Revenues", 105, 2023, accn="A-24", filed="2025-02-10")   # restated in next 10-K
    cf.flow("Revenues", 98, 2023, accn="A-25", filed="2026-02-10", form="10-Q")  # not a 10-K
    got = annual_flows(cf.data, "Revenues")[date(2023, 12, 31)]
    assert got.value == 105 and got.accn == "A-24"


def test_quarterly_and_ytd_durations_are_dropped():
    cf = CF()
    cf.add("Revenues", 25, "2024-12-31", start="2024-10-01")   # Q4 shown in a 10-K
    cf.add("Revenues", 75, "2024-09-30", start="2024-01-01")   # nine months
    cf.flow("Revenues", 100, 2024)
    flows = annual_flows(cf.data, "Revenues")
    assert list(flows) == [date(2024, 12, 31)]
    assert flows[date(2024, 12, 31)].value == 100


def test_53_week_year_is_kept():
    cf = CF()
    cf.add("Revenues", 100, "2024-02-03", start="2023-01-29")  # 370 days
    assert date(2024, 2, 3) in annual_flows(cf.data, "Revenues")


def test_instants_ignore_durations_and_pick_latest_filing():
    cf = CF()
    cf.inst("AssetsCurrent", 50, 2024, accn="A-25", filed="2025-02-10")
    cf.inst("AssetsCurrent", 52, 2024, accn="A-26", filed="2026-02-10")
    cf.flow("AssetsCurrent", 999, 2024)  # malformed duration fact, must be ignored
    assert instants(cf.data, "AssetsCurrent")[date(2024, 12, 31)].value == 52


def test_fiscal_year_ends_takes_latest_n_from_first_anchor_with_data():
    cf = CF()
    for y in (2021, 2022, 2023, 2024, 2025):
        cf.flow("RevenueFromContractWithCustomerExcludingAssessedTax", y, y)
    ends = fiscal_year_ends(cf.data, ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax"], 3)
    assert ends == [date(2023, 12, 31), date(2024, 12, 31), date(2025, 12, 31)]


def test_missing_tag_returns_empty():
    assert annual_flows(CF().data, "Nope") == {}
    assert instants(CF().data, "Nope") == {}


def test_fiscal_labels():
    assert fiscal_label(date(2025, 12, 31), "end_year") == "FY2025"
    # Kohl's: year ended 1 Feb 2025 is fiscal 2024; year ended 31 Jan 2026 is fiscal 2025.
    assert fiscal_label(date(2025, 2, 1), "start_year") == "FY2024"
    assert fiscal_label(date(2026, 1, 31), "start_year") == "FY2025"
