import pytest

from creditmemo.stress import breaches, load_config, run, stressed_inputs

# Worked example ($m): revenue 1,000, EBITDA 200 (20% margin), D&A 50, debt 600
# of which 50% floating, interest 40, capex 60, cash taxes 20, principal 50.
BASE = {
    "revenue": 1000.0, "operating_income": 150.0, "da": 50.0,
    "short_term_borrowings": 0.0, "commercial_paper": 0.0, "current_ltd": 50.0,
    "noncurrent_ltd": 550.0, "finance_lease_liabilities": 0.0, "cash": 100.0,
    "operating_lease_liabilities": 300.0, "operating_lease_cost": 50.0,
    "interest_expense": 40.0, "capex": 60.0, "cash_taxes": 20.0, "scheduled_principal": 50.0,
    "current_assets": 400.0, "current_liabilities": 250.0, "cfo": 170.0,
}
SCEN = {"revenue_shock": 0.20, "margin_shock": 0.03, "rate_shock": 0.02}
TH = load_config()["thresholds"]


def test_stressed_inputs_worked_example():
    s = stressed_inputs(BASE, 0.5, **SCEN)
    # revenue 800; margin 20% - 3pp = 17% -> EBITDA 136; extra interest 2% x 50% x 600 = 6
    assert s["revenue"] == pytest.approx(800)
    assert s["operating_income"] + s["da"] == pytest.approx(136)
    assert s["_extra_interest"] == pytest.approx(6)
    assert s["interest_expense"] == pytest.approx(46)
    assert s["capex"] == 60 and s["cash_taxes"] == 20 and s["scheduled_principal"] == 50


def test_run_worked_example():
    r = run(BASE, 0.5, SCEN, TH)
    st = r["stressed"]["ratios"]
    assert st["debt_ebitda"] == pytest.approx(600 / 136)                # 4.41x: breaks 4.0x
    assert st["interest_coverage"] == pytest.approx(136 / 46)           # 2.96x: holds
    assert st["dscr"] == pytest.approx((136 - 60 - 20) / (46 + 50))     # 0.58x: breaks 1.0x
    assert st["lease_adj_debt_ebitdar"] == pytest.approx(900 / 186)
    assert r["stressed"]["breaches"] == {"debt_ebitda": True, "interest_coverage": False, "dscr": True}
    assert r["base"]["breaches"] == {"debt_ebitda": False, "interest_coverage": False, "dscr": False}


def test_zero_floating_share_means_no_extra_interest():
    r = run(BASE, 0.0, SCEN, TH)
    assert r["extra_interest"] == 0
    assert r["stressed"]["ratios"]["interest_coverage"] == pytest.approx(136 / 40)


def test_margin_wiped_out_counts_as_leverage_breach():
    scen = dict(SCEN, margin_shock=0.25)          # 20% margin - 25pp -> negative EBITDA
    r = run(BASE, 0.5, scen, TH)
    assert r["stressed"]["ratios"]["debt_ebitda"] is None
    assert r["stressed"]["breaches"]["debt_ebitda"] is True
    assert r["stressed"]["ratios"]["interest_coverage"] < 0


def test_no_interest_coverage_nm_is_not_a_breach():
    assert breaches({"debt_ebitda": 1.0, "interest_coverage": None, "dscr": 3.0}, TH) == \
        {"debt_ebitda": False, "interest_coverage": False, "dscr": False}


def test_zero_shocks_reproduce_base():
    r = run(BASE, 0.5, {"revenue_shock": 0, "margin_shock": 0, "rate_shock": 0}, TH)
    for k, v in r["base"]["ratios"].items():
        assert r["stressed"]["ratios"][k] == pytest.approx(v)
