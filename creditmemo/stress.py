"""The stress case (definitions in DECISIONS.md).

  stressed revenue = revenue x (1 - revenue shock)
  stressed EBITDA  = stressed revenue x (base EBITDA margin - margin shock)
  extra interest   = rate shock x floating-rate share x total debt
  capex, cash taxes, lease cost and scheduled principal held at base

Thresholds come from config/stress.json. A ratio that becomes not
meaningful (leverage on negative EBITDA) counts as a breach, because it is
worse than any threshold.

The hosted demo page (not in this repo) implements the same formulas for its
live sliders; tests/test_stress.py pins the numbers both must produce.
"""

from __future__ import annotations

import json
from typing import Dict, Optional

from . import CONFIG_DIR
from .ratios import compute_period


def load_config(path=CONFIG_DIR / "stress.json") -> dict:
    return json.loads(path.read_text())


def stressed_inputs(base: Dict[str, Optional[float]], floating_share: float,
                    revenue_shock: float, margin_shock: float, rate_shock: float) -> Dict[str, Optional[float]]:
    """Ratio inputs after the shocks. Operating income is rebuilt so that
    compute_period() gives EBITDA = stressed revenue x stressed margin."""
    rev, oi, da = base.get("revenue"), base.get("operating_income"), base.get("da")
    if None in (rev, oi, da) or rev <= 0:
        raise ValueError("stress needs revenue, operating income and D&A")
    margin = (oi + da) / rev
    s_rev = rev * (1 - revenue_shock)
    s_ebitda = s_rev * (margin - margin_shock)
    debt = sum(base.get(k) or 0.0 for k in ("short_term_borrowings", "commercial_paper", "current_ltd",
                                            "noncurrent_ltd", "finance_lease_liabilities"))
    extra = rate_shock * (floating_share or 0.0) * debt
    out = dict(base)
    out.update({
        "revenue": s_rev,
        "operating_income": s_ebitda - da,
        "interest_expense": None if base.get("interest_expense") is None
        else base["interest_expense"] + extra,
    })
    out["_extra_interest"] = extra
    out["_base_margin"] = margin
    out["_stressed_margin"] = margin - margin_shock
    return out


def breaches(ratios: Dict[str, Optional[float]], thresholds: dict) -> Dict[str, bool]:
    out = {}
    for key, t in thresholds.items():
        v = ratios.get(key)
        if v is None:
            # n.m. leverage (EBITDA <= 0) is a breach; n.m. coverage with no
            # interest at all is not
            out[key] = key == "debt_ebitda"
        else:
            out[key] = v > t["value"] if t["op"] == ">" else v < t["value"]
    return out


def run(base: Dict[str, Optional[float]], floating_share: float, scenario: dict, thresholds: dict) -> dict:
    s_in = stressed_inputs(base, floating_share, **scenario)
    b_derived, b_ratios, _ = compute_period(base)
    s_derived, s_ratios, s_notes = compute_period({k: v for k, v in s_in.items() if not k.startswith("_")})
    return {
        "scenario": scenario,
        "floating_rate_share": floating_share,
        "extra_interest": s_in["_extra_interest"],
        "base_margin": s_in["_base_margin"],
        "stressed_margin": s_in["_stressed_margin"],
        "base": {"derived": b_derived, "ratios": b_ratios,
                 "breaches": breaches(b_ratios, thresholds)},
        "stressed": {"derived": s_derived, "ratios": s_ratios, "ratio_notes": s_notes,
                     "breaches": breaches(s_ratios, thresholds)},
        "thresholds": thresholds,
    }
