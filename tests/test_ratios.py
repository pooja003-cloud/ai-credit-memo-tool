"""Ratio tests from worked examples. The arithmetic is shown in each test."""

import pytest

from creditmemo import ratios as r
from creditmemo.ratios import compute_period

# A textbook-style borrower ($ millions).
#   Revenue 1,000; operating income 150; D&A 50      -> EBITDA 200, margin 20%
#   Debt: ST borrowings 20 + CP 30 + current LTD 50 + LTD 450 + finance leases 50 = 600
#   Cash 100 -> net debt 500
#   Operating leases: liability 300, annual cost 50  -> EBITDAR 250
#   Interest 40; capex 60; cash taxes 20; principal due next year 50
#   Current assets 400; current liabilities 250
BASE = {
    "revenue": 1000.0, "operating_income": 150.0, "da": 50.0,
    "short_term_borrowings": 20.0, "commercial_paper": 30.0, "current_ltd": 50.0,
    "noncurrent_ltd": 450.0, "finance_lease_liabilities": 50.0,
    "cash": 100.0, "operating_lease_liabilities": 300.0, "operating_lease_cost": 50.0,
    "interest_expense": 40.0, "capex": 60.0, "cash_taxes": 20.0, "scheduled_principal": 50.0,
    "current_assets": 400.0, "current_liabilities": 250.0, "cfo": 170.0,
}


def test_worked_example_derived():
    d, _, _ = compute_period(BASE)
    assert d["ebitda"] == 200.0
    assert d["ebitda_margin"] == pytest.approx(0.20)
    assert d["total_debt"] == 600.0
    assert d["net_debt"] == 500.0
    assert d["ebitdar"] == 250.0
    assert d["lease_adj_debt"] == 900.0
    assert d["fcf"] == 110.0  # 170 - 60


def test_worked_example_ratios():
    _, x, notes = compute_period(BASE)
    assert x["debt_ebitda"] == pytest.approx(3.0)                 # 600 / 200
    assert x["net_debt_ebitda"] == pytest.approx(2.5)             # 500 / 200
    assert x["lease_adj_debt_ebitdar"] == pytest.approx(3.6)      # (600+300) / (200+50)
    assert x["lease_adj_net_debt_ebitdar"] == pytest.approx(3.2)  # (500+300) / 250
    assert x["interest_coverage"] == pytest.approx(5.0)           # 200 / 40
    assert x["dscr"] == pytest.approx(120 / 90)                   # (200-60-20) / (40+50)
    assert x["current_ratio"] == pytest.approx(1.6)               # 400 / 250
    assert notes == {}


def test_lease_adjustment_lowers_leverage_for_a_lease_heavy_retailer():
    # Why EBITDAR matters: rent is already deducted inside EBITDA under ASC 842.
    # Debt 200, EBITDA 100 -> 2.0x. Leases 800 at cost 100 a year.
    # Wrong pairing (debt + leases) / EBITDA = 10.0x. Right pairing / EBITDAR = 5.0x.
    v = dict(BASE, short_term_borrowings=0, commercial_paper=0, current_ltd=0,
             noncurrent_ltd=200, finance_lease_liabilities=0, operating_income=60, da=40,
             operating_lease_liabilities=800, operating_lease_cost=100)
    _, x, _ = compute_period(v)
    assert x["debt_ebitda"] == pytest.approx(2.0)
    assert x["lease_adj_debt_ebitdar"] == pytest.approx(5.0)


def test_negative_ebitda_makes_leverage_nm_but_keeps_negative_coverage():
    v = dict(BASE, operating_income=-80.0, da=30.0)  # EBITDA -50
    _, x, notes = compute_period(v)
    assert x["debt_ebitda"] is None
    assert notes["debt_ebitda"] == "n.m.: ebitda is zero or negative"
    assert x["interest_coverage"] == pytest.approx(-1.25)  # -50 / 40: a real, failing result
    assert x["dscr"] == pytest.approx((-50 - 60 - 20) / 90)


def test_zero_interest_coverage_is_nm():
    v = dict(BASE, interest_expense=0.0)
    _, x, notes = compute_period(v)
    assert x["interest_coverage"] is None
    assert notes["interest_coverage"].startswith("n.m.")
    # DSCR still works because principal is due.
    assert x["dscr"] == pytest.approx(120 / 50)


def test_no_debt_service_at_all():
    v = dict(BASE, interest_expense=0.0, scheduled_principal=0.0)
    _, x, notes = compute_period(v)
    assert x["dscr"] is None
    assert notes["dscr"] == "n.m.: no debt service"


def test_missing_input_is_reported_not_guessed():
    v = dict(BASE)
    v["cash_taxes"] = None
    v["operating_lease_cost"] = None
    _, x, notes = compute_period(v)
    assert x["dscr"] is None and "cash_taxes" in notes["dscr"]
    assert x["lease_adj_debt_ebitdar"] is None
    assert notes["lease_adj_debt_ebitdar"] == "missing input: ebitdar"
    assert x["debt_ebitda"] == pytest.approx(3.0)  # unaffected


def test_net_cash_position_gives_negative_net_leverage():
    v = dict(BASE, cash=700.0)
    _, x, _ = compute_period(v)
    assert x["net_debt_ebitda"] == pytest.approx(-0.5)  # (600 - 700) / 200


def test_helpers():
    assert r.ebitda(None, 5) is None
    assert r.leverage(100, 0) is None
    assert r.coverage(10, -1) is None
    assert r.current_ratio(1, 2) == 0.5
