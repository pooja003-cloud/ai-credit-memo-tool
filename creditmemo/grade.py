"""The 1-to-10 internal risk grade (1 = best). Rules in config/grade.json.

  metric score  1-10 from fixed bands (n.m. gets the metric's nm_score)
  base grade    weighted average of the metric scores, rounded half up
  final grade   base grade, one notch worse per stress threshold broken
                (at most two), capped at 10

The thresholds are fixed before any agency rating is looked at, so the
comparison with S&P and Moody's is a real test rather than a fit.
"""

from __future__ import annotations

import json
import math
from typing import Dict, Optional

from . import CONFIG_DIR


def load_config(path=CONFIG_DIR / "grade.json") -> dict:
    return json.loads(path.read_text())


def metric_score(value: Optional[float], spec: dict) -> int:
    if value is None:
        return spec["nm_score"]
    bands = spec["bands"]
    if spec["direction"] == "lower_is_better":
        for i, cut in enumerate(bands):
            if value <= cut:
                return i + 1
        return len(bands) + 1
    for i, cut in enumerate(bands):
        if value >= cut:
            return i + 1
    return len(bands) + 1


def round_half_up(x: float) -> int:
    """Half rounds up. Rounding to 6 decimals first stops floating-point noise
    (4.4999999999 from summing weights in a different order) from pushing a
    score that is exactly on a boundary down a grade."""
    return math.floor(round(x, 6) + 0.5)


def grade(ratios: Dict[str, Optional[float]], stress_breaches: Dict[str, bool], cfg: dict) -> dict:
    scores, weighted = {}, 0.0
    for key, spec in cfg["metrics"].items():
        s = metric_score(ratios.get(key), spec)
        scores[key] = {"value": ratios.get(key), "score": s, "weight": spec["weight"]}
        weighted += s * spec["weight"]
    total_w = sum(spec["weight"] for spec in cfg["metrics"].values())
    avg = weighted / total_w
    base = min(10, max(1, round_half_up(avg)))
    ov = cfg["stress_overlay"]
    broken = [k for k, b in stress_breaches.items() if b]
    notches = min(ov["max_notches"], ov["notch_per_breach"] * len(broken))
    final = min(10, base + notches)
    return {"grade": final, "base_grade": base, "weighted_score": round(avg, 3),
            "stress_notches": notches, "stress_breaches": broken, "scores": scores,
            "status": cfg.get("status")}


def agency_equivalent(rating: str, cfg: dict) -> Optional[int]:
    r = rating.strip().rstrip("*")
    for g, names in cfg["agency_map"].items():
        if g.startswith("_"):
            continue
        if r in names:
            return int(g)
    return None
