"""Pull the text sections the memo cites out of the latest 10-K.

    python -m creditmemo.sections            # all companies
    python -m creditmemo.sections DVA

Writes outputs/sections/<TICKER>.json with these sections, each split into
numbered paragraphs so the memo can cite them precisely ("[1A ¶12]"):

  1      Item 1. Business
  1A     Item 1A. Risk Factors
  7      Item 7. MD&A (whole item)
  7-LIQ  the Liquidity and Capital Resources part of Item 7
  7A     Item 7A. Quantitative and Qualitative Disclosures About Market Risk
  DEBT   the debt note in the financial statements

The text is only ever quoted or summarised by Claude. Numbers in the memo
still come from the spread, never from this text.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple

from . import ROOT
from .edgar import filings_dir, load_companies

SECTIONS_DIR = ROOT / "outputs" / "sections"
BLOCK = {"p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "h5", "h6", "table", "section"}
SKIP = {"script", "style", "head", "title", "ix:header"}


class _Text(HTMLParser):
    """HTML -> text with one line per block; table cells separated by ' | '."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: List[str] = []
        self.skip = 0
        self.hidden: List[bool] = []

    def handle_starttag(self, tag, attrs):
        style = (dict(attrs).get("style") or "").replace(" ", "").lower()
        hide = tag in SKIP or "display:none" in style
        self.hidden.append(hide)
        if hide:
            self.skip += 1
        if tag in BLOCK:
            self.out.append("\n")
        elif tag == "td":
            self.out.append(" | ")

    def handle_startendtag(self, tag, attrs):
        if tag == "br":
            self.out.append("\n")

    def handle_endtag(self, tag):
        if self.hidden:
            if self.hidden.pop():
                self.skip -= 1
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


PAGE_RE = re.compile(r"^(F-)?\d{1,3}$")
TOC_RE = re.compile(r"^(table of contents|index)$", re.I)


def html_to_lines(page: str, with_pages: bool = False):
    """Text lines of the document. Page-number footers and 'Table of Contents'
    links are removed; with_pages=True also returns each line's page number
    (taken from the footer that closes its page)."""
    p = _Text()
    p.feed(page)
    text = "".join(p.out).replace("\xa0", " ")
    lines, pages, pending = [], [], 0
    last = {"": None, "F-": None}      # last accepted page in each sequence
    for raw in text.split("\n"):
        line = re.sub(r"\s+", " ", raw).strip(" |")
        line = re.sub(r"(\s*\|\s*)+", " | ", line).strip()
        if not line or TOC_RE.match(line) or set(line) <= set("*-_ "):
            continue
        m = PAGE_RE.match(line)
        if m:
            seq, n = m.group(1) or "", int(line.replace("F-", ""))
            prev = last[seq]
            # a footer must continue its page sequence; anything else is content
            # and close a real page (an index of page numbers has almost nothing between them)
            if pending >= 4 and ((prev is None and n <= 5) or (prev is not None and prev < n <= prev + 3)):
                last[seq] = n
                pages[len(pages) - pending:] = [line] * pending
                pending = 0
                continue
        lines.append(line)
        pages.append(None)
        pending += 1
    return (lines, pages) if with_pages else lines


ITEM_RE = re.compile(r"^item\s*(\d{1,2}[a-c]?)\s*[.:\-–—]?\s*(.*)$", re.I)


def find_items(lines: List[str]) -> Dict[str, Tuple[int, int]]:
    """Map item number -> (start line, end line) using the longest span for
    each item, which skips the table of contents."""
    heads = []
    for i, line in enumerate(lines):
        m = ITEM_RE.match(line)
        if m and len(line) < 200:
            heads.append((i, m.group(1).upper()))
    spans: Dict[str, Tuple[int, int]] = {}
    for k, (i, item) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        size = sum(len(x) for x in lines[i:end])
        if item not in spans or size > sum(len(x) for x in lines[spans[item][0]:spans[item][1]]):
            spans[item] = (i, end)
    return spans


def _sub_span(lines, start, end, head_re, stop_re, max_chars=40000) -> Optional[Tuple[int, int]]:
    """A heading-delimited part of a span: first line matching head_re (a
    short heading line) up to the next line matching stop_re."""
    for i in range(start, end):
        if len(lines[i]) < 120 and re.search(head_re, lines[i], re.I):
            j, size = i + 1, 0
            while j < end and not (len(lines[j]) < 120 and re.search(stop_re, lines[j], re.I)):
                size += len(lines[j])
                if size > max_chars:
                    break
                j += 1
            if j - i > 3:
                return i, j
    return None


LIQ_HEAD = r"^liquidity and capital resources\b"
LIQ_STOP = (r"^(critical accounting|new accounting|recent(ly)? (issued )?accounting|off-balance sheet|"
            r"contractual obligations|forward-looking|other matters|non-gaap|cautionary|"
            r"reconciliation of non-gaap|accounting pronouncements)")
DEBT_HEAD = (r"^(note\s*)?\d{1,2}\s*[.:\-–—]?\s*(long-term )?(debt|borrowings|debt and credit agreements|"
             r"long-term debt and other borrowings|debt obligations|financing arrangements)\b(?!.*\|)")
DEBT_STOP = r"^(note\s*)?\d{1,2}\s*[.:\-–—]?\s*[A-Z][A-Za-z ,'’&-]{3,60}$"


def paragraphs(lines: List[str], pages: List[Optional[str]]) -> List[dict]:
    """Join wrapped lines into paragraphs, each with the page it starts on.
    Table rows and short heading lines (no closing punctuation) stand alone."""
    paras: List[dict] = []
    cur: List[str] = []
    cur_page: List[Optional[str]] = [None]

    def flush():
        if cur:
            paras.append({"text": " ".join(cur), "page": cur_page[0]})
            cur.clear()

    for line, page in zip(lines, pages):
        heading = len(line) < 100 and not line.endswith((".", ":", ";", ",", "?", "!"))
        if " | " in line or (heading and not cur):
            flush()
            paras.append({"text": line, "page": page})
            continue
        if not cur:
            cur_page[0] = page
        cur.append(line)
        if line.endswith((".", ":", "?", "!", ";")):
            flush()
    flush()
    return paras


XREF_RE = re.compile(r"set forth (?:under|in) .*?[-–—]\s*([A-Z][A-Za-z ,&'’]+?),\s*Item 7\b")
CAPS_HEAD = r"^[A-Z][A-Z0-9 ,&'’()/-]{5,}$"


def extract(page: str, extra: Optional[dict] = None) -> dict:
    lines, pages = html_to_lines(page, with_pages=True)
    items = find_items(lines)
    out = {}

    def add(key, title, span, note=None):
        if span:
            ps = paragraphs(lines[span[0]:span[1]], pages[span[0]:span[1]])
            out[key] = {"title": title, "heading": lines[span[0]], "paragraphs": ps,
                        "chars": sum(len(p["text"]) for p in ps)}
            if note:
                out[key]["note"] = note

    add("1", "Item 1. Business", items.get("1"))
    add("1A", "Item 1A. Risk Factors", items.get("1A"))
    add("7", "Item 7. Management's Discussion and Analysis", items.get("7"))
    if "7" in items:
        add("7-LIQ", "Item 7. Liquidity and Capital Resources",
            _sub_span(lines, *items["7"], LIQ_HEAD, LIQ_STOP))
    add("7A", "Item 7A. Quantitative and Qualitative Disclosures About Market Risk", items.get("7A"))
    # Item 7A that only points elsewhere ("set forth under MD&A - Other Matters, Item 7"):
    # follow the reference and keep that part of Item 7 as 7A.
    if "7A" in out and out["7A"]["chars"] < 800 and "7" in items:
        m = XREF_RE.search(" ".join(p["text"] for p in out["7A"]["paragraphs"]))
        if m:
            target = m.group(1).strip()
            span = _sub_span(lines, *items["7"], r"^" + re.escape(target) + r"$", CAPS_HEAD)
            if span:
                add("7A", "Item 7A. Market Risk (in Item 7, " + target + ")", span,
                    note=f"Item 7A refers to '{target}' in Item 7; that part is used here")
    for key, spec in (extra or {}).items():     # company-specific notes, from config/companies.json
        if "8" in items:
            add(key, spec["title"], _sub_span(lines, items["8"][0], len(lines), spec["head"],
                                              DEBT_STOP + r"|^item\s+\d", 60000))
    if "8" in items:
        add("DEBT", "Debt note (financial statements)",
            _sub_span(lines, items["8"][0], len(lines), DEBT_HEAD, DEBT_STOP, 60000))
    return out


def main(argv=None) -> int:
    cfg = load_companies()
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*", default=list(cfg["companies"]))
    args = ap.parse_args(argv)
    SECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    ok = True
    for t in [x.upper() for x in args.tickers]:
        folders = sorted((d for d in filings_dir(t).iterdir() if (d / "index.json").exists()),
                         key=lambda d: json.loads((d / "index.json").read_text())["filingDate"])
        index = json.loads((folders[-1] / "index.json").read_text())
        doc = folders[-1] / index["main_document"]
        extra = cfg["companies"][t].get("extra_sections")
        secs = extract(doc.read_text(errors="replace"), extra)
        result = {"ticker": t, "accn": index["accessionNumber"], "filed": index["filingDate"],
                  "url": f"{index['base_url']}/{index['main_document']}", "sections": secs}
        (SECTIONS_DIR / f"{t}.json").write_text(json.dumps(result, indent=1))
        print(f"{t}: " + ", ".join(f"{k} {v['chars']:,} chars/{len(v['paragraphs'])} ¶"
                                    for k, v in secs.items()))
        missing = [k for k in ("1", "1A", "7", "7-LIQ", "7A", "DEBT", *(extra or {})) if k not in secs]
        if missing:
            print(f"  missing: {missing}", file=sys.stderr)
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
