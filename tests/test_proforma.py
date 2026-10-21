import pytest
from test_stress import BASE, SCEN, TH

from creditmemo.proforma import proforma_inputs, run


def test_proforma_worked_example():
    # Base: debt 600, EBITDA 200, interest 40. Add 100 at 5%: debt 700, interest 45.
    pf = proforma_inputs(BASE, 100.0, 0.05)
    assert pf["noncurrent_ltd"] == 650.0 and pf["interest_expense"] == pytest.approx(45.0)
    r = run(BASE, 100.0, 0.05, 0.5, SCEN, TH)
    assert r["ratios"]["debt_ebitda"] == pytest.approx(700 / 200)
    assert r["ratios"]["interest_coverage"] == pytest.approx(200 / 45)
    assert r["ratios"]["dscr"] == pytest.approx((200 - 60 - 20) / (45 + 50))   # principal unchanged (bullet)
    # stress on pro forma: EBITDA 136; extra interest 2% x 50% x 700 = 7
    assert r["stress"]["stressed"]["ratios"]["debt_ebitda"] == pytest.approx(700 / 136)
    assert r["stress"]["stressed"]["ratios"]["interest_coverage"] == pytest.approx(136 / 52)
    assert BASE["noncurrent_ltd"] == 550.0      # base inputs untouched
