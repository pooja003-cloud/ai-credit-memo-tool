"""AI credit memo tool: Python computes every number, Claude only writes."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
CACHE_DIR = ROOT / "data" / "cache"
SPREAD_DIR = ROOT / "outputs" / "spreads"
