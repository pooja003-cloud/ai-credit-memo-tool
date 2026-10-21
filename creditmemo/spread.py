"""Build the standard spread from company facts.

For each concept and fiscal year, the value is resolved in this order:
  1. a manual entry in config/overrides/<TICKER>.json (must cite a source)
  2. the tag list: company override tags first, then the defaults in
     config/tags.json; the first tag with a value for that year wins
  3. sum_of: component tags added together (all must be present)
  4. fallback: another concept (e.g. current portion of LTD for
     next-12-month maturities)
  5. default_zero: counted as 0 and flagged
  6. otherwise missing (None)

Every value carries where it came from: tag, unit, accession number,
form, filing date and period, or the manual source text.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Dict, Optional

from . import CONFIG_DIR
from .facts import annual_flows, fiscal_label, fiscal_year_ends, instants
from .ratios import compute_period

SPREAD_VERSION = 1


def load_json(path: Path) -> dict:
    with open(path) as fh:
        return json.load(fh)


def load_tag_spec(path: Path = CONFIG_DIR / "tags.json") -> dict:
    return {k: v for k, v in load_json(path).items() if not k.startswith("_")}


def load_override(ticker: str, folder: Path = CONFIG_DIR / "overrides") -> dict:
    path = folder / f"{ticker}.json"
    return load_json(path) if path.exists() else {}


def _norm(tag_entry) -> dict:
    return {"tag": tag_entry} if isinstance(tag_entry, str) else dict(tag_entry)


def filing_url(cik: int, accn: str) -> str:
    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accn.replace('-', '')}/{accn}-index.htm"


class _Resolver:
    def __init__(self, companyfacts: dict, cik: int, spec: dict, override: dict):
        self.cf = companyfacts
        self.cik = cik
        self.spec = spec
        self.override = override or {}
        self._maps: Dict[tuple, dict] = {}

    def facts_for(self, tag: str, kind: str) -> dict:
        key = (tag, kind)
        if key not in self._maps:
            fn = annual_flows if kind == "flow" else instants
            self._maps[key] = fn(self.cf, tag)
        return self._maps[key]

    def _from_fact(self, fact, entry: dict, source: str = "xbrl") -> dict:
        sign = -1.0 if entry.get("negate") else 1.0
        return {
            "value": sign * fact.value,
            "source": source,
            "tag": fact.tag,
            "unit": fact.unit,
            "accn": fact.accn,
            "form": fact.form,
            "filed": fact.filed.isoformat(),
            "start": fact.start.isoformat() if fact.start else None,
            "end": fact.end.isoformat(),
            "filing_url": filing_url(self.cik, fact.accn),
            "proxy": bool(entry.get("proxy", False)),
            "note": entry.get("note"),
        }

    def resolve(self, concept: str, end: date, label: str, _seen=()) -> dict:
        rec = self._resolve(concept, end, label, _seen)
        if self.spec[concept].get("abs") and rec.get("value") is not None and rec["value"] < 0:
            rec["value"] = -rec["value"]
            rec["note"] = ((rec.get("note") or "") + " Sign flipped: filer reports it as negative.").strip()
        return rec

    def _resolve(self, concept: str, end: date, label: str, _seen=()) -> dict:
        cs = self.spec[concept]
        kind = cs["kind"]

        manual = self.override.get("manual", {}).get(concept, {}).get(label)
        if manual is not None and manual.get("value") is not None:
            if not manual.get("source"):
                raise ValueError(f"manual value for {concept} {label} has no source")
            return {"value": float(manual["value"]), "source": "manual",
                    "manual_source": manual["source"], "proxy": bool(manual.get("proxy", False)),
                    "note": manual.get("note"), "end": end.isoformat()}

        # Three tiers: company override tags, default tags, proxy tags.
        # Within a tier the fact from the newest 10-K wins (same rule as
        # facts.py); ties go to the earlier tag in the list. This stops an
        # old tag from an old 10-K beating the tag the latest 10-K uses.
        defaults = [_norm(t) for t in cs.get("tags", [])]
        tiers = [
            [_norm(t) for t in self.override.get("tags", {}).get(concept, [])],
            [e for e in defaults if not e.get("proxy")],
            [e for e in defaults if e.get("proxy")],
        ]
        for tier in tiers:
            best = None
            for rank, entry in enumerate(tier):
                fact = self.facts_for(entry["tag"], kind).get(end)
                if fact is None:
                    continue
                key = (fact.filed, fact.accn, -rank)
                if best is None or key > best[0]:
                    best = (key, fact, entry)
            if best is not None:
                return self._from_fact(best[1], best[2])

        sums = cs.get("sum_of") or []
        if sums and isinstance(sums[0], str):
            sums = [sums]
        for parts in sums:
            found = [self.facts_for(t, kind).get(end) for t in parts]
            if all(found):
                rec = self._from_fact(found[0], {})
                rec.update({
                    "value": sum(f.value for f in found),
                    "source": "sum",
                    "tag": " + ".join(parts),
                    "components": [self._from_fact(f, {}) for f in found],
                    "note": None,
                })
                return rec

        fb = cs.get("fallback")
        if fb and fb not in _seen:
            rec = dict(self.resolve(fb, end, label, _seen + (concept,)))
            if rec.get("value") is not None:
                zero = " (itself not tagged, counted as 0)" if rec["source"] == "assumed_zero" else ""
                rec["source"] = f"fallback:{fb}"
                rec["note"] = (f"{self.spec[concept]['label']} not tagged; "
                               f"used {self.spec[fb]['label']}{zero}")
                return rec

        for entry in (_norm(t) for t in cs.get("proxy_tags", [])):
            fact = self.facts_for(entry["tag"], kind).get(end)
            if fact is not None:
                entry.setdefault("proxy", True)
                return self._from_fact(fact, entry)

        if cs.get("default_zero"):
            return {"value": 0.0, "source": "assumed_zero", "proxy": False,
                    "note": "Not tagged; counted as 0. Confirm in the 10-K.", "end": end.isoformat()}

        return {"value": None, "source": "missing", "proxy": False,
                "note": "No tag found", "end": end.isoformat()}


def build_spread(companyfacts: dict, ticker: str, company: dict, spec: dict,
                 override: Optional[dict] = None, years: int = 3) -> dict:
    override = override or {}
    cik = int(company["cik"])
    res = _Resolver(companyfacts, cik, spec, override)

    anchors = [_norm(t)["tag"] for t in spec["revenue"]["tags"]] + ["NetIncomeLoss"]
    ends = fiscal_year_ends(companyfacts, anchors, years)
    if not ends:
        raise ValueError(f"{ticker}: no annual 10-K revenue facts found")
    convention = company.get("fiscal_label", "end_year")
    periods = [{"label": fiscal_label(e, convention), "end": e.isoformat()} for e in ends]

    lines: Dict[str, Dict[str, dict]] = {c: {} for c in spec}
    for p, end in zip(periods, ends):
        for concept in spec:
            lines[concept][p["label"]] = res.resolve(concept, end, p["label"])

    # Finance leases are already inside the debt figure when the debt tag
    # says so (LongTermDebtAndCapitalLeaseObligations...). The override
    # finance_leases_in_debt (true/false) beats this detection.
    forced = override.get("finance_leases_in_debt")
    for label, rec in lines["finance_lease_liabilities"].items():
        debt_tags = " ".join(str(lines[c][label].get("tag") or "")
                             for c in ("current_ltd", "noncurrent_ltd"))
        included = forced if forced is not None else (
            "CapitalLease" in debt_tags or "FinanceLease" in debt_tags)
        if included:
            rec["reported_value"] = rec["value"]
            rec["value"] = 0.0
            rec["source"] = "included_in_debt"
            rec["note"] = "Already inside the long-term debt tags; not added again"

    derived, ratios, ratio_notes = {}, {}, {}
    for p in periods:
        values = {c: lines[c][p["label"]]["value"] for c in spec}
        d, r, n = compute_period(values)
        derived[p["label"]], ratios[p["label"]], ratio_notes[p["label"]] = d, r, n

    warnings = []
    for concept, by_period in lines.items():
        for label, rec in by_period.items():
            name = spec[concept]["label"]
            if rec["source"] == "missing":
                warnings.append(f"{label} {name}: missing")
            elif rec["source"] == "assumed_zero":
                warnings.append(f"{label} {name}: not tagged, counted as 0")
            elif rec["source"].startswith("fallback:"):
                warnings.append(f"{label} {name}: {rec['note']}")
            if rec.get("proxy"):
                warnings.append(f"{label} {name}: PROXY ({rec.get('note')})")

    return {
        "spread_version": SPREAD_VERSION,
        "ticker": ticker,
        "name": company["name"],
        "cik": cik,
        "role": company.get("role"),
        "entity_name_sec": companyfacts.get("entityName"),
        "source": "SEC EDGAR XBRL company facts API",
        "rule": "Latest 10-K reporting each period; flows 340-380 days",
        "periods": periods,
        "concept_labels": {c: spec[c]["label"] for c in spec},
        "lines": lines,
        "derived": derived,
        "ratios": ratios,
        "ratio_notes": ratio_notes,
        "warnings": warnings,
    }


LOG_FIELDS = ["ticker", "period", "concept", "value", "source", "proxy", "tag", "unit",
              "accn", "form", "filed", "start", "end", "filing_url", "manual_source", "note"]


def log_rows(spread: dict):
    """One row per spread value, for the trace log CSV."""
    for concept, by_period in spread["lines"].items():
        for label, rec in by_period.items():
            row = {k: rec.get(k) for k in LOG_FIELDS}
            row.update({"ticker": spread["ticker"], "period": label, "concept": concept})
            yield row
