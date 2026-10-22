import pytest

from creditmemo.grade import agency_equivalent, grade, load_config, metric_score

CFG = load_config()
M = CFG["metrics"]


@pytest.mark.parametrize("value,score", [(0.8, 1), (1.0, 1), (2.6, 5), (4.0, 7), (4.01, 8), (6.5, 10), (None, 10)])
def test_leverage_bands(value, score):
    assert metric_score(value, M["lease_adj_debt_ebitdar"]) == score


@pytest.mark.parametrize("value,score", [(20, 1), (15, 1), (9.5, 3), (4.6, 6), (1.4, 10), (None, 1)])
def test_coverage_bands(value, score):
    assert metric_score(value, M["interest_coverage"]) == score


def test_weights_sum_to_one():
    assert sum(m["weight"] for m in M.values()) == pytest.approx(1.0)


def test_grade_worked_example():
    # leverage 3.2x -> 6, coverage 8x -> 4, DSCR 2.0x -> 5, current 1.3x -> 5
    # 0.4*6 + 0.3*4 + 0.2*5 + 0.1*5 = 5.1 -> base 5; one stress breach -> 6
    r = grade({"lease_adj_debt_ebitdar": 3.2, "interest_coverage": 8.0, "dscr": 2.0, "current_ratio": 1.3},
              {"debt_ebitda": True, "interest_coverage": False, "dscr": False}, CFG)
    assert r["weighted_score"] == pytest.approx(5.1)
    assert r["base_grade"] == 5 and r["stress_notches"] == 1 and r["grade"] == 6


def test_stress_overlay_capped_at_two_and_grade_at_ten():
    r = grade({"lease_adj_debt_ebitdar": 7.0, "interest_coverage": 1.0, "dscr": 0.5, "current_ratio": 0.5},
              {"a": True, "b": True, "c": True}, CFG)
    assert r["base_grade"] == 10 and r["stress_notches"] == 2 and r["grade"] == 10


def test_half_rounds_up():
    # 0.4*2 + 0.3*3 + 0.2*3 + 0.1*3 = 2.6 -> 3
    r = grade({"lease_adj_debt_ebitdar": 1.2, "interest_coverage": 10, "dscr": 3.0, "current_ratio": 1.9}, {}, CFG)
    assert r["base_grade"] == 3


def test_agency_map():
    assert agency_equivalent("BBB-", CFG) == 6
    assert agency_equivalent("Ba2", CFG) == 7
    assert agency_equivalent("A-", CFG) == 4
    assert agency_equivalent("XYZ", CFG) is None


def test_grade_config_is_frozen():
    """config/grade.json was signed off before any agency rating was looked up.
    Changing it means re-opening that decision, so the hash is pinned."""
    import hashlib
    from creditmemo import CONFIG_DIR
    expected = (CONFIG_DIR / "grade.sha256").read_text().split()[0]
    assert hashlib.sha256((CONFIG_DIR / "grade.json").read_bytes()).hexdigest() == expected
    assert CFG["status"].startswith("FROZEN")


def test_exact_boundary_rounds_up_despite_float_noise():
    from creditmemo.grade import round_half_up
    assert round_half_up(4.5) == 5
    assert round_half_up(4.499999999999) == 5      # float noise on an exact 4.5
    assert round_half_up(4.4999) == 4               # genuinely below the boundary
    # UNP's FY2025 pattern: scores 5, 3, 4, 8 -> 0.4*5 + 0.3*3 + 0.2*4 + 0.1*8 = 4.50 -> base 5
    r = grade({"lease_adj_debt_ebitdar": 2.7, "interest_coverage": 9.5, "dscr": 2.3, "current_ratio": 0.9}, {}, CFG)
    assert [r["scores"][k]["score"] for k in ("lease_adj_debt_ebitdar", "interest_coverage", "dscr", "current_ratio")] == [5, 3, 4, 8]
    assert r["weighted_score"] == 4.5 and r["base_grade"] == 5
