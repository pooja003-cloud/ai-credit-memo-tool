"""Credit ratios. Pure functions, no I/O.

Definitions are fixed in DECISIONS.md. Every function returns a float or
None. None means the ratio can't be computed (missing input) or isn't
meaningful (for example leverage on negative EBITDA). compute_period()
records the reason for each None in `notes`.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

Num = Optional[float]


def _all(*xs) -> bool:
    return all(x is not None for x in xs)


def ebitda(operating_income: Num, da: Num) -> Num:
    return operating_income + da if _all(operating_income, da) else None


def total_debt(short_term_borrowings: Num, commercial_paper: Num, current_ltd: Num,
               noncurrent_ltd: Num, finance_lease_liabilities: Num) -> Num:
    parts = (short_term_borrowings, commercial_paper, current_ltd,
             noncurrent_ltd, finance_lease_liabilities)
    return sum(parts) if _all(*parts) else None


def leverage(debt: Num, earnings: Num) -> Num:
    """Debt / EBITDA (or EBITDAR). Not meaningful when earnings <= 0."""
    if not _all(debt, earnings) or earnings <= 0:
        return None
    return debt / earnings


def coverage(numerator: Num, denominator: Num) -> Num:
    """A coverage ratio. A negative numerator is kept: it is a real result
    (cash flow doesn't cover the charge at all). A zero or negative
    denominator is not meaningful."""
    if not _all(numerator, denominator) or denominator <= 0:
        return None
    return numerator / denominator


def interest_coverage(ebitda_: Num, interest: Num) -> Num:
    return coverage(ebitda_, interest)


def dscr(ebitda_: Num, capex: Num, cash_taxes: Num, interest: Num, principal: Num) -> Num:
    """(EBITDA - capex - cash taxes) / (interest + scheduled principal)."""
    if not _all(ebitda_, capex, cash_taxes, interest, principal):
        return None
    return coverage(ebitda_ - capex - cash_taxes, interest + principal)


def current_ratio(current_assets: Num, current_liabilities: Num) -> Num:
    return coverage(current_assets, current_liabilities)


RATIO_LABELS = {
    "debt_ebitda": "Debt / EBITDA",
    "net_debt_ebitda": "Net debt / EBITDA",
    "lease_adj_debt_ebitdar": "(Debt + leases) / EBITDAR",
    "lease_adj_net_debt_ebitdar": "(Net debt + leases) / EBITDAR",
    "interest_coverage": "EBITDA / interest",
    "dscr": "DSCR",
    "current_ratio": "Current ratio",
}

DERIVED_LABELS = {
    "ebitda": "EBITDA",
    "ebitda_margin": "EBITDA margin",
    "ebitdar": "EBITDAR",
    "total_debt": "Total debt",
    "net_debt": "Net debt",
    "lease_adj_debt": "Debt + operating leases",
    "fcf": "Free cash flow (CFO - capex)",
}


def compute_period(v: Dict[str, Num]) -> Tuple[Dict[str, Num], Dict[str, Num], Dict[str, str]]:
    """Derive EBITDA, debt etc. and the ratios for one fiscal year.

    `v` maps spread concept -> value (None when missing).
    Returns (derived, ratios, notes).
    """
    g = v.get
    notes: Dict[str, str] = {}

    e = ebitda(g("operating_income"), g("da"))
    rev = g("revenue")
    debt = total_debt(g("short_term_borrowings"), g("commercial_paper"), g("current_ltd"),
                      g("noncurrent_ltd"), g("finance_lease_liabilities"))
    cash = g("cash")
    net = debt - cash if _all(debt, cash) else None
    lease_cost, lease_liab = g("operating_lease_cost"), g("operating_lease_liabilities")
    ebitdar = e + lease_cost if _all(e, lease_cost) else None
    adj_debt = debt + lease_liab if _all(debt, lease_liab) else None
    adj_net = net + lease_liab if _all(net, lease_liab) else None

    derived = {
        "ebitda": e,
        "ebitda_margin": e / rev if _all(e, rev) and rev > 0 else None,
        "ebitdar": ebitdar,
        "total_debt": debt,
        "net_debt": net,
        "lease_adj_debt": adj_debt,
        "fcf": g("cfo") - g("capex") if _all(g("cfo"), g("capex")) else None,
    }

    interest = g("interest_expense")
    ratios = {
        "debt_ebitda": leverage(debt, e),
        "net_debt_ebitda": leverage(net, e),
        "lease_adj_debt_ebitdar": leverage(adj_debt, ebitdar),
        "lease_adj_net_debt_ebitdar": leverage(adj_net, ebitdar),
        "interest_coverage": interest_coverage(e, interest),
        "dscr": dscr(e, g("capex"), g("cash_taxes"), interest, g("scheduled_principal")),
        "current_ratio": current_ratio(g("current_assets"), g("current_liabilities")),
    }

    # Explain each None so the memo and demo can say "n.m." with a reason.
    inputs = {
        "debt_ebitda": ("total_debt", debt, "ebitda", e),
        "net_debt_ebitda": ("net_debt", net, "ebitda", e),
        "lease_adj_debt_ebitdar": ("lease_adj_debt", adj_debt, "ebitdar", ebitdar),
        "lease_adj_net_debt_ebitdar": ("lease_adj_net_debt", adj_net, "ebitdar", ebitdar),
        "interest_coverage": ("ebitda", e, "interest_expense", interest),
        "current_ratio": ("current_assets", g("current_assets"),
                          "current_liabilities", g("current_liabilities")),
    }
    for name, value in ratios.items():
        if value is not None:
            continue
        if name == "dscr":
            missing = [k for k in ("capex", "cash_taxes", "interest_expense", "scheduled_principal")
                       if g(k) is None] + ([] if e is not None else ["ebitda"])
            notes[name] = ("missing input: " + ", ".join(missing)) if missing else \
                "n.m.: no debt service"
            continue
        n_name, n_val, d_name, d_val = inputs[name]
        if n_val is None or d_val is None:
            missing = [k for k, x in ((n_name, n_val), (d_name, d_val)) if x is None]
            notes[name] = "missing input: " + ", ".join(missing)
        else:
            notes[name] = f"n.m.: {d_name} is zero or negative"
    return derived, ratios, notes
