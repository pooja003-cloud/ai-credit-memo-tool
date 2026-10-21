"""Layer 2: the standard bank spread, built only from as-reported lines.

Every company lands in the same template (see DECISIONS.md). Each standard
line keeps the list of as-reported lines it was built from. Lines that
don't match a specific standard line go to a visible "other" line in their
section, so nothing is dropped.

Tie-outs check the arithmetic against the statement's own totals:
  income   revenue - costs - D&A - unusual items = operating income
           operating income - interest + other = pre-tax income
           pre-tax - tax + discontinued - NCI = net income to the company
  balance  current assets, total assets, current liabilities, total
           liabilities (when reported), liabilities + equity = assets
  cashflow each section's lines add up to CFO / CFI / CFF, and
           CFO + CFI + CFF + FX = change in cash
Signs follow the cash flow statement as printed (inflows positive). On the
income statement, costs are positive numbers and gains reduce costs.
"""

from __future__ import annotations

import re
from typing import Callable, Dict, List, Optional

TIE_UNITS = 2  # allowed rounding difference, in the statement's own units


def local(tag: str) -> str:
    return tag.split("_", 1)[-1]


def _z(x):
    return 0.0 if x is None else x


class Section:
    """Collects as-reported rows into standard lines, period by period."""

    def __init__(self, n: int):
        self.n = n
        self.lines: Dict[str, dict] = {}

    def line(self, key: str, label: str) -> dict:
        if key not in self.lines:
            self.lines[key] = {"key": key, "label": label, "values": [0.0] * self.n, "sources": []}
        return self.lines[key]

    def add(self, key: str, label: str, row: dict, sign: float = 1.0, periods=None):
        ln = self.line(key, label)
        used = False
        for p in range(self.n) if periods is None else periods:
            v = row["values"][p]
            if v is not None:
                ln["values"][p] += sign * v
                used = True
        ln["sources"].append({"id": row.get("id"), "label": row["label"], "tag": row["tag"],
                              "sign": sign, "periods": periods})
        return used

    def set(self, key: str, label: str, values: List[Optional[float]], note: str = ""):
        ln = self.line(key, label)
        ln["values"] = list(values)
        if note:
            ln["note"] = note
        return ln


def _money(rows):
    return [r for r in rows if not r["abstract"] and r.get("kind") == "money"]


def _find(rows, names, start=0, end=None, pred=None) -> Optional[int]:
    end = len(rows) if end is None else end
    for i in range(start, end):
        if local(rows[i]["tag"]) in names and (pred is None or pred(rows[i])):
            return i
    return None


def _is_match(row, tag_re=None, label_re=None) -> bool:
    t, l = local(row["tag"]), row["label"].lower()
    return bool((tag_re and re.search(tag_re, t)) or (label_re and re.search(label_re, l)))


class Ties:
    def __init__(self, periods, scale):
        self.periods = periods
        self.tol = TIE_UNITS * scale
        self.items = []

    def check(self, statement, name, reported, computed):
        for p, lab in enumerate(self.periods):
            r, c = reported[p], computed[p]
            if r is None:
                continue
            diff = _z(c) - r
            self.items.append({"statement": statement, "check": name, "period": lab,
                               "reported": r, "computed": c, "diff": diff,
                               "ok": abs(diff) <= self.tol})


def _vals(row, n):
    return [None] * n if row is None else list(row["values"])


# ----------------------------------------------------------------- income

REVENUE = {"Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
           "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet",
           "RevenuesNetOfInterestExpense", "SalesRevenueGoodsNet"}
COST_TOTALS = {"CostsAndExpenses", "OperatingExpenses", "OperatingCostsAndExpenses",
               "CostOfRevenueAndOperatingExpenses", "GrossProfit"}
PRETAX = {"IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
          "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
          "IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic"}
DA_TAG = r"^Depreciation|AmortizationOfIntangibleAssets$|^DepreciationAmortization"
UNUSUAL_TAG = (r"Impairment|Restructuring|GainLoss|Gain(?!.*EquityMethod)|Litigation|Settlement|"
               r"Remeasurement|StoreClosing|Divestiture|Disposal|Severance")
UNUSUAL_LABEL = r"impairment|\bgain\b|restructuring|settlement|store closing|write-?down|severance"
INTEREST_TAG = r"InterestExpense|InterestAndDebtExpense|InterestIncomeExpense"
INTEREST_LABEL = r"interest expense|debt expense"


def build_income(stmt: dict, da_cf: List[Optional[float]], ties: Ties) -> Section:
    rows = _money(stmt["rows"])
    n = len(stmt["periods"])
    S = Section(n)
    oi = _find(rows, {"OperatingIncomeLoss"})
    pt = _find(rows, PRETAX)
    if oi is None or pt is None:
        raise ValueError("income statement needs operating income and pre-tax income lines")
    revs = [i for i in range(oi) if local(rows[i]["tag"]) in REVENUE]
    if not revs:
        raise ValueError("no revenue line above operating income")
    rv = max(revs, key=lambda i: abs(_z(rows[i]["values"][-1])))
    S.add("revenue", "Revenue", rows[rv])

    # Operating block: costs printed as positives, gains as negatives.
    block = [i for i in range(rv + 1, oi)
             if local(rows[i]["tag"]) not in COST_TOTALS | REVENUE and not
             (rows[i]["total"] and rows[i]["label"].lower().startswith("total"))]
    da_is = [0.0] * n
    for i in block:
        r = rows[i]
        if _is_match(r, DA_TAG, r"depreciation"):
            S.add("_da_is", "D&A on the income statement", r)
            for p in range(n):
                da_is[p] += _z(r["values"][p])
        elif _is_match(r, UNUSUAL_TAG, UNUSUAL_LABEL) and "EquityMethod" not in r["tag"]:
            S.add("unusual_operating", "Unusual operating items (gains negative)", r)
        else:
            S.add("_opex", "Operating costs as printed", r)
    opex = S.line("_opex", "")["values"]
    unusual = S.line("unusual_operating", "Unusual operating items (gains negative)")["values"]
    da = [da_cf[p] if da_cf[p] is not None else da_is[p] for p in range(n)]
    S.set("operating_costs", "Operating costs excl. D&A",
          [opex[p] + da_is[p] - _z(da[p]) for p in range(n)],
          note="Costs as printed, with D&A moved to its own line (D&A from the cash flow statement)")
    S.lines["operating_costs"]["sources"] = S.lines["_opex"]["sources"] + S.lines.get(
        "_da_is", {"sources": []})["sources"]
    S.set("da", "Depreciation & amortization", da,
          note="From the cash flow statement" if any(x is not None for x in da_cf) else
          "From the income statement")
    S.add("operating_income", "Operating income", rows[oi])
    ties.check("income", "Revenue - costs - D&A - unusual = operating income", rows[oi]["values"],
               [S.lines["revenue"]["values"][p] - S.lines["operating_costs"]["values"][p]
                - _z(da[p]) - unusual[p] for p in range(n)])

    # Non-operating block: some filers print it income-positive, some expense-positive.
    nb = list(range(oi + 1, pt))
    tot = [sum(_z(rows[i]["values"][p]) for i in nb) for p in range(n)]
    oiv, ptv = rows[oi]["values"], rows[pt]["values"]
    plus = all(ptv[p] is None or abs(_z(oiv[p]) + tot[p] - ptv[p]) <= ties.tol for p in range(n))
    s = 1.0 if plus else -1.0
    for i in nb:
        r = rows[i]
        if _is_match(r, INTEREST_TAG, INTEREST_LABEL):
            S.add("interest_expense", "Interest expense", r, sign=-s)
        else:
            S.add("other_nonoperating", "Other non-operating income (expense)", r, sign=s)
    S.line("interest_expense", "Interest expense")
    S.line("other_nonoperating", "Other non-operating income (expense)")
    S.add("pretax_income", "Pre-tax income", rows[pt])
    ties.check("income", "Operating income - interest + other = pre-tax income", ptv,
               [_z(oiv[p]) - S.lines["interest_expense"]["values"][p]
                + S.lines["other_nonoperating"]["values"][p] for p in range(n)])

    # Below pre-tax
    tx = _find(rows, {"IncomeTaxExpenseBenefit"}, pt + 1)
    total_ni = _find(rows, {"ProfitLoss"}, pt + 1)
    co_ni = _find(rows, {"NetIncomeLoss"}, pt + 1)
    if co_ni is None:
        raise ValueError("no net income line")
    after_tax = _find(rows, {"IncomeLossFromContinuingOperations",
                             "IncomeLossFromContinuingOperationsIncludingPortionAttributableToNoncontrollingInterest"},
                      pt + 1)
    target = after_tax if after_tax is not None else (total_ni if total_ni is not None else co_ni)
    if tx is not None:
        tv, tg = rows[tx]["values"], rows[target]["values"]
        expense_positive = all(tg[p] is None or tv[p] is None or abs(ptv[p] - tv[p] - tg[p]) <= ties.tol
                               for p in range(n))
        S.add("income_tax", "Income tax", rows[tx], sign=1.0 if expense_positive else -1.0)
    S.line("income_tax", "Income tax")
    disc_rows = [i for i in range(pt + 1, (total_ni if total_ni is not None else co_ni) + 1)
                 if "DiscontinuedOperation" in rows[i]["tag"]]
    for i in disc_rows[:1]:
        S.add("discontinued", "Discontinued operations", rows[i])
    S.line("discontinued", "Discontinued operations")
    ni_total = rows[total_ni]["values"] if total_ni is not None else rows[co_ni]["values"]
    S.set("net_income_total", "Net income incl. NCI", ni_total)
    S.set("nci", "Less: non-controlling interests",
          [None if ni_total[p] is None else ni_total[p] - _z(rows[co_ni]["values"][p]) for p in range(n)])
    S.add("net_income", "Net income to the company", rows[co_ni])
    ties.check("income", "Pre-tax - tax + discontinued - NCI = net income", rows[co_ni]["values"],
               [ptv[p] - S.lines["income_tax"]["values"][p] + S.lines["discontinued"]["values"][p]
                - _z(S.lines["nci"]["values"][p]) for p in range(n)])
    S.set("ebitda", "EBITDA (operating income + D&A)",
          [None if oiv[p] is None or da[p] is None else oiv[p] + da[p] for p in range(n)])
    return S


INCOME_ORDER = ["revenue", "operating_costs", "da", "unusual_operating", "operating_income",
                "interest_expense", "other_nonoperating", "pretax_income", "income_tax",
                "discontinued", "net_income_total", "nci", "net_income", "ebitda"]

# ----------------------------------------------------------------- balance

DEBT_TAG = r"Debt|Borrowing|CommercialPaper|LinesOfCredit|FinanceLease|CapitalLease|NotesPayable|LoansPayable"
DEBT_LABEL = (r"\bdebt\b|borrowings|finance lease|financing obligation|notes payable|commercial paper|"
              r"credit facility")
EQUITY_START = r"^(CommonStock|PreferredStock|AdditionalPaidInCapital|StockholdersEquity|MinorityInterest|" \
               r"RedeemableNoncontrollingInterest|TemporaryEquity|RetainedEarnings|TreasuryStock)"


def build_balance(stmt: dict, ties: Ties) -> Section:
    rows = _money(stmt["rows"])
    n = len(stmt["periods"])
    S = Section(n)
    ac = _find(rows, {"AssetsCurrent"})
    a = _find(rows, {"Assets"})
    lc = _find(rows, {"LiabilitiesCurrent"})
    le = _find(rows, {"LiabilitiesAndStockholdersEquity"})
    if None in (ac, a, lc, le):
        raise ValueError("balance sheet needs current assets, total assets, current liabilities "
                         "and total liabilities and equity lines")
    for i in range(0, ac):
        r = rows[i]
        t = local(r["tag"])
        if t in {"CashAndCashEquivalentsAtCarryingValue", "Cash", "CashAndDueFromBanks"}:
            S.add("cash", "Cash and equivalents", r)
        elif "Receivable" in t:
            S.add("receivables", "Receivables", r)
        elif _is_match(r, r"Inventor|MaterialsSupplies", r"inventor"):
            S.add("inventory", "Inventory", r)
        else:
            S.add("other_current_assets", "Other current assets", r)
    S.add("current_assets", "Total current assets", rows[ac])
    for k, lab in [("cash", "Cash and equivalents"), ("receivables", "Receivables"),
                   ("inventory", "Inventory"), ("other_current_assets", "Other current assets")]:
        S.line(k, lab)
    ties.check("balance", "Current asset lines = total current assets", rows[ac]["values"],
               [sum(S.lines[k]["values"][p] for k in ("cash", "receivables", "inventory",
                                                       "other_current_assets")) for p in range(n)])
    for i in range(ac + 1, a):
        r = rows[i]
        t = local(r["tag"])
        if "PropertyPlantAndEquipment" in t:
            S.add("ppe", "PP&E, net", r)
        elif t == "OperatingLeaseRightOfUseAsset":
            S.add("lease_assets", "Operating lease assets", r)
        elif "Goodwill" in t or "Intangible" in t:
            S.add("goodwill_intangibles", "Goodwill and intangibles", r)
        else:
            S.add("other_noncurrent_assets", "Other non-current assets", r)
    nca = ["ppe", "lease_assets", "goodwill_intangibles", "other_noncurrent_assets"]
    for k, lab in zip(nca, ["PP&E, net", "Operating lease assets", "Goodwill and intangibles",
                            "Other non-current assets"]):
        S.line(k, lab)
    S.add("total_assets", "Total assets", rows[a])
    ties.check("balance", "Current + non-current assets = total assets", rows[a]["values"],
               [_z(rows[ac]["values"][p]) + sum(S.lines[k]["values"][p] for k in nca) for p in range(n)])

    for i in range(a + 1, lc):
        r = rows[i]
        t = local(r["tag"])
        if t == "OperatingLeaseLiabilityCurrent":
            S.add("lease_liab_current", "Operating lease liabilities, current", r)
        elif _is_match(r, DEBT_TAG, DEBT_LABEL) and "Interest" not in t:
            S.add("debt_current", "Short-term debt and current LTD (incl. finance leases)", r)
        elif t.startswith("AccountsPayable"):
            S.add("payables", "Accounts payable", r)
        else:
            S.add("other_current_liabilities", "Other current liabilities", r)
    cl = ["debt_current", "payables", "lease_liab_current", "other_current_liabilities"]
    for k, lab in zip(cl, ["Short-term debt and current LTD (incl. finance leases)", "Accounts payable",
                           "Operating lease liabilities, current", "Other current liabilities"]):
        S.line(k, lab)
    S.add("current_liabilities", "Total current liabilities", rows[lc])
    ties.check("balance", "Current liability lines = total current liabilities", rows[lc]["values"],
               [sum(S.lines[k]["values"][p] for k in cl) for p in range(n)])

    l_tot = _find(rows, {"Liabilities"}, lc + 1)
    end = l_tot
    if end is None:
        end = next((i for i in range(lc + 1, le) if re.search(EQUITY_START, local(rows[i]["tag"]))), le)
    for i in range(lc + 1, end):
        r = rows[i]
        t = local(r["tag"])
        if t == "OperatingLeaseLiabilityNoncurrent":
            S.add("lease_liab_noncurrent", "Operating lease liabilities, non-current", r)
        elif _is_match(r, DEBT_TAG, DEBT_LABEL) and "Interest" not in t:
            S.add("ltd", "Long-term debt (incl. finance leases)", r)
        else:
            S.add("other_noncurrent_liabilities", "Other non-current liabilities", r)
    ncl = ["ltd", "lease_liab_noncurrent", "other_noncurrent_liabilities"]
    for k, lab in zip(ncl, ["Long-term debt (incl. finance leases)", "Operating lease liabilities, non-current",
                            "Other non-current liabilities"]):
        S.line(k, lab)
    tl = [_z(rows[lc]["values"][p]) + sum(S.lines[k]["values"][p] for k in ncl) for p in range(n)]
    S.set("total_liabilities", "Total liabilities", tl)
    if l_tot is not None:
        ties.check("balance", "Current + non-current liabilities = total liabilities",
                   rows[l_tot]["values"], tl)

    after = range((l_tot if l_tot is not None else end), le)
    red = [i for i in after if re.search(r"RedeemableNoncontrollingInterest|TemporaryEquity",
                                         local(rows[i]["tag"]))]
    for i in red[:1]:
        S.add("redeemable_nci", "Redeemable non-controlling interests", rows[i])
    S.line("redeemable_nci", "Redeemable non-controlling interests")
    se = _find(rows, {"StockholdersEquity"}, lc + 1, le)
    if se is None:
        raise ValueError("no shareholders' equity line")
    S.add("equity", "Shareholders' equity (company)", rows[se])
    nci = _find(rows, {"MinorityInterest"}, se, le)
    if nci is not None:
        S.add("nci", "Non-controlling interests", rows[nci])
    S.line("nci", "Non-controlling interests")
    S.add("total_liabilities_equity", "Total liabilities and equity", rows[le])
    ties.check("balance", "Liabilities + equity lines = total liabilities and equity", rows[le]["values"],
               [tl[p] + S.lines["redeemable_nci"]["values"][p] + _z(rows[se]["values"][p])
                + S.lines["nci"]["values"][p] for p in range(n)])
    ties.check("balance", "Total liabilities and equity = total assets", rows[a]["values"],
               rows[le]["values"])
    S.set("total_debt", "Total debt",
          [S.lines["debt_current"]["values"][p] + S.lines["ltd"]["values"][p] for p in range(n)])
    S.set("lease_liabilities", "Operating lease liabilities (on the balance sheet)",
          [S.lines["lease_liab_current"]["values"][p] + S.lines["lease_liab_noncurrent"]["values"][p]
           for p in range(n)])
    return S


BALANCE_ORDER = ["cash", "receivables", "inventory", "other_current_assets", "current_assets",
                 "ppe", "lease_assets", "goodwill_intangibles", "other_noncurrent_assets", "total_assets",
                 "debt_current", "payables", "lease_liab_current", "other_current_liabilities",
                 "current_liabilities", "ltd", "lease_liab_noncurrent", "other_noncurrent_liabilities",
                 "total_liabilities", "redeemable_nci", "equity", "nci", "total_liabilities_equity",
                 "total_debt", "lease_liabilities"]

# ---------------------------------------------------------------- cashflow

CFO = {"NetCashProvidedByUsedInOperatingActivities",
       "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"}
CFI = {"NetCashProvidedByUsedInInvestingActivities",
       "NetCashProvidedByUsedInInvestingActivitiesContinuingOperations"}
CFF = {"NetCashProvidedByUsedInFinancingActivities",
       "NetCashProvidedByUsedInFinancingActivitiesContinuingOperations"}
CAPEX_TAG = r"^(PaymentsToAcquirePropertyPlantAndEquipment|PaymentsToAcquireProductiveAssets|" \
            r"PaymentsForCapitalImprovements|PaymentsToAcquireOtherPropertyPlantAndEquipment)$"
CAPEX_LABEL = r"capital (expenditure|investment)|(additions|acquisitions?|purchases?) (of|to) property"


def build_cashflow(stmt: dict, ties: Ties) -> Section:
    rows = _money(stmt["rows"])
    n = len(stmt["periods"])
    S = Section(n)
    o, i_, f = _find(rows, CFO), _find(rows, CFI), _find(rows, CFF)
    if None in (o, i_, f):
        raise ValueError("cash flow statement needs CFO, CFI and CFF lines")
    for i in range(0, o):
        r = rows[i]
        if _is_match(r, DA_TAG, r"^depreciation"):
            S.add("da", "of which D&A", r)
        else:
            S.add("_other_operating", "Other operating lines", r)
    S.line("da", "of which D&A")
    S.add("cfo", "Cash from operations", rows[o])
    ties.check("cashflow", "Operating lines = cash from operations", rows[o]["values"],
               [S.lines["da"]["values"][p] + S.lines["_other_operating"]["values"][p] for p in range(n)])

    for i in range(o + 1, i_):
        r = rows[i]
        t = local(r["tag"])
        if _is_match(r, CAPEX_TAG, CAPEX_LABEL):
            S.add("capex", "Capex", r)
        elif t.startswith("PaymentsToAcquireBusinesses"):
            S.add("acquisitions", "Acquisitions", r)
        else:
            S.add("other_investing", "Other investing", r)
    inv = ["capex", "acquisitions", "other_investing"]
    for k, lab in zip(inv, ["Capex", "Acquisitions", "Other investing"]):
        S.line(k, lab)
    S.add("cfi", "Cash from investing", rows[i_])
    ties.check("cashflow", "Investing lines = cash from investing", rows[i_]["values"],
               [sum(S.lines[k]["values"][p] for k in inv) for p in range(n)])

    for i in range(i_ + 1, f):
        r = rows[i]
        t = local(r["tag"])
        is_debt = re.search(r"Debt|Borrowing|Notes|LinesOfCredit|CommercialPaper|Loans", t) or \
            re.search(r"borrowings|\bdebt\b|credit facility", r["label"].lower())
        if t.startswith("ProceedsFromRepayments") and is_debt:      # net revolver line
            pos = [p for p in range(n) if _z(r["values"][p]) >= 0]
            neg = [p for p in range(n) if _z(r["values"][p]) < 0]
            S.add("debt_issued", "Debt issued", r, periods=pos)
            S.add("debt_repaid", "Debt repaid", r, periods=neg)
        elif t.startswith("ProceedsFrom") and is_debt and "Financing" not in t:
            S.add("debt_issued", "Debt issued", r)
        elif t.startswith("Repayments") and is_debt:
            S.add("debt_repaid", "Debt repaid", r)
        elif t.startswith("PaymentsOfDividends") or "dividends paid" in r["label"].lower():
            S.add("dividends", "Dividends", r)
        elif _is_match(r, r"RepurchaseOfCommonStock|PurchaseOfTreasuryStock|TreasuryStockAcquired",
                       r"repurchase|treasury stock"):
            S.add("buybacks", "Share buybacks", r)
        else:
            S.add("other_financing", "Other financing (incl. NCI distributions, lease payments)", r)
    fin = ["debt_issued", "debt_repaid", "dividends", "buybacks", "other_financing"]
    for k, lab in zip(fin, ["Debt issued", "Debt repaid", "Dividends", "Share buybacks",
                            "Other financing (incl. NCI distributions, lease payments)"]):
        S.line(k, lab)
    S.add("cff", "Cash from financing", rows[f])
    ties.check("cashflow", "Financing lines = cash from financing", rows[f]["values"],
               [sum(S.lines[k]["values"][p] for k in fin) for p in range(n)])

    chg = _find(rows, {"CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect",
                       "CashAndCashEquivalentsPeriodIncreaseDecrease",
                       "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseExcludingExchangeRateEffect"},
                f + 1)
    if chg is not None:
        fx = [sum(_z(rows[j]["values"][p]) for j in range(f + 1, chg)) for p in range(n)]
        ties.check("cashflow", "CFO + CFI + CFF + FX = change in cash", rows[chg]["values"],
                   [_z(rows[o]["values"][p]) + _z(rows[i_]["values"][p]) + _z(rows[f]["values"][p]) + fx[p]
                    for p in range(n)])
    S.set("fcf", "Free cash flow (CFO + capex)",
          [_z(rows[o]["values"][p]) + S.lines["capex"]["values"][p] for p in range(n)])
    return S


CASHFLOW_ORDER = ["cfo", "da", "capex", "acquisitions", "other_investing", "cfi", "debt_issued",
                  "debt_repaid", "dividends", "buybacks", "other_financing", "cff", "fcf"]


def _export(S: Section, order: List[str]) -> List[dict]:
    out = []
    for k in order:
        if k in S.lines:
            ln = dict(S.lines[k])
            ln["values"] = [None if v is None else round(v, 2) for v in ln["values"]]
            out.append(ln)
    return out


def build_standard(asrep: dict) -> dict:
    """Standard spread for all three statements, with tie-outs."""
    st = asrep["statements"]
    ties = {}
    cf_ties = Ties([p["label"] for p in st["cashflow"]["periods"]], st["cashflow"]["money_scale"])
    cf = build_cashflow(st["cashflow"], cf_ties)
    cf_da = dict(zip([p["end"] for p in st["cashflow"]["periods"]], cf.lines["da"]["values"]))
    is_periods = st["income"]["periods"]
    da_cf = [cf_da.get(p["end"]) if cf.lines["da"]["sources"] else None for p in is_periods]
    is_ties = Ties([p["label"] for p in is_periods], st["income"]["money_scale"])
    inc = build_income(st["income"], da_cf, is_ties)
    bs_ties = Ties([p["label"] for p in st["balance"]["periods"]], st["balance"]["money_scale"])
    bal = build_balance(st["balance"], bs_ties)
    ties = is_ties.items + bs_ties.items + cf_ties.items
    return {
        "periods": {k: [p["label"] for p in st[k]["periods"]] for k in st},
        "income": _export(inc, INCOME_ORDER),
        "balance": _export(bal, BALANCE_ORDER),
        "cashflow": _export(cf, CASHFLOW_ORDER),
        "ties": ties,
        "ties_ok": all(t["ok"] for t in ties),
    }


def value(std: dict, statement: str, key: str, label: str) -> Optional[float]:
    periods = std["periods"]["income" if statement == "income" else statement]
    for ln in std[statement]:
        if ln["key"] == key:
            return ln["values"][periods.index(label)] if label in periods else None
    return None
