"""Pick one value per fiscal period from SEC company-facts JSON.

The rule (see DECISIONS.md):
  * Only facts filed on a 10-K (or 10-K/A).
  * Flows (income statement, cash flow) must cover 340-380 days, so
    quarterly and nine-month figures are dropped.
  * Balance-sheet items are instants (no start date).
  * When several 10-Ks report the same period, the most recently filed
    one wins. Restated figures therefore replace the originals.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict, Iterator, Optional

ANNUAL_FORMS = {"10-K", "10-K/A"}
MIN_DAYS, MAX_DAYS = 340, 380


@dataclass(frozen=True)
class Fact:
    tag: str
    unit: str
    value: float
    start: Optional[date]
    end: date
    accn: str
    form: str
    filed: date
    taxonomy: str = "us-gaap"

    @property
    def days(self) -> Optional[int]:
        return None if self.start is None else (self.end - self.start).days


def _d(s: Optional[str]) -> Optional[date]:
    return date.fromisoformat(s) if s else None


def iter_facts(companyfacts: dict, tag: str, taxonomy: str = "us-gaap",
               unit: str = "USD") -> Iterator[Fact]:
    node = companyfacts.get("facts", {}).get(taxonomy, {}).get(tag)
    if not node:
        return
    for row in node.get("units", {}).get(unit, []):
        yield Fact(
            tag=tag, unit=unit, value=float(row["val"]),
            start=_d(row.get("start")), end=_d(row["end"]),
            accn=row["accn"], form=row.get("form", ""), filed=_d(row["filed"]),
            taxonomy=taxonomy,
        )


def _newer(a: Fact, b: Optional[Fact]) -> bool:
    return b is None or (a.filed, a.accn) > (b.filed, b.accn)


def annual_flows(companyfacts: dict, tag: str, **kw) -> Dict[date, Fact]:
    """Map period end date -> the chosen annual fact for a flow tag."""
    best: Dict[date, Fact] = {}
    for f in iter_facts(companyfacts, tag, **kw):
        if f.form not in ANNUAL_FORMS or f.start is None:
            continue
        if not MIN_DAYS <= f.days <= MAX_DAYS:
            continue
        if _newer(f, best.get(f.end)):
            best[f.end] = f
    return best


def instants(companyfacts: dict, tag: str, **kw) -> Dict[date, Fact]:
    """Map balance-sheet date -> the chosen fact for an instant tag."""
    best: Dict[date, Fact] = {}
    for f in iter_facts(companyfacts, tag, **kw):
        if f.form not in ANNUAL_FORMS or f.start is not None:
            continue
        if _newer(f, best.get(f.end)):
            best[f.end] = f
    return best


def fiscal_year_ends(companyfacts: dict, anchor_tags, n: int) -> list:
    """The latest n fiscal year-end dates, oldest first.

    Taken from all anchor tags combined (normally the revenue tags).
    Companies switch tags over time: Union Pacific used Revenues up to
    2020 and RevenueFromContractWithCustomerExcludingAssessedTax after.
    """
    ends = set()
    for tag in anchor_tags:
        ends.update(annual_flows(companyfacts, tag))
    return sorted(ends)[-n:]


def fiscal_label(end: date, convention: str = "end_year") -> str:
    """Label a fiscal year the way the company does.

    end_year:   year ending 2025-12-31 -> FY2025 (UNP, DaVita).
    start_year: retail calendar, year ending 2026-01-31 -> FY2025 (Kohl's).
    """
    if convention == "end_year":
        year = end.year
    elif convention == "start_year":
        year = (end - timedelta(days=364)).year
    else:
        raise ValueError(f"unknown fiscal_label convention: {convention}")
    return f"FY{year}"
