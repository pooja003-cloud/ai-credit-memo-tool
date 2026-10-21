"""Pro forma for the requested facility: the borrower's latest year as if the
new loan were already on the balance sheet.

  debt      + facility amount (added to long-term debt)
  interest  + facility amount x rate, where the rate is a cited 10-K fact
              (DaVita: weighted average effective rate on all debt, Debt note)
  unchanged EBITDA, cash (proceeds assumed spent on general corporate purposes,
            not held), capex, cash taxes, leases and next-year principal
            (the loan is assumed to be a bullet repaid at maturity)

The stress case is then rerun on the pro forma inputs, with the company's
floating-rate share applied to pro forma debt. The grade stays on reported
figures; pro forma is shown alongside, not graded.
"""

from __future__ import annotations

from typing import Dict, Optional

from .ratios import compute_period
from .stress import run as run_stress


def proforma_inputs(base: Dict[str, Optional[float]], amount: float, rate: float) -> Dict[str, Optional[float]]:
    out = dict(base)
    out["noncurrent_ltd"] = (base.get("noncurrent_ltd") or 0.0) + amount
    if base.get("interest_expense") is not None:
        out["interest_expense"] = base["interest_expense"] + amount * rate
    return out


def run(base: Dict[str, Optional[float]], amount: float, rate: float, floating_share: float,
        scenario: dict, thresholds: dict) -> dict:
    pf = proforma_inputs(base, amount, rate)
    derived, ratios, notes = compute_period(pf)
    stress = run_stress(pf, floating_share, scenario, thresholds)
    return {"amount": amount, "rate": rate, "added_interest": amount * rate,
            "inputs": pf, "derived": derived, "ratios": ratios, "ratio_notes": notes,
            "stress": stress}
