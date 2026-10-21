import pytest
from rpage import page, write_filing

from creditmemo.asreported import build_as_reported, classify, parse_r_page, parse_value, row_kind
from creditmemo.standard import build_standard, value

D3 = ["Dec. 31, 2025", "Dec. 31, 2024", "Dec. 31, 2023"]
D2 = ["Dec. 31, 2025", "Dec. 31, 2024"]
CO = {"cik": 1, "name": "Test Co", "fiscal_label": "end_year"}


def test_parse_value():
    assert parse_value("$ 13,643,069") == 13643069
    assert parse_value("(579,926)") == -579926
    assert parse_value("&#160;") is None
    assert parse_value("$ (1.5) [1]") == -1.5


def test_row_kind():
    assert row_kind("us-gaap_EarningsPerShareBasic") == "per_share"
    assert row_kind("us-gaap_IncomeLossFromContinuingOperationsPerBasicShare") == "per_share"
    assert row_kind("us-gaap_WeightedAverageNumberOfSharesOutstandingBasic") == "shares"
    assert row_kind("kss_SharesWithheldForTaxesOnVestedRestrictedShares") == "money"  # cash, not a count


def test_classify():
    assert classify("CONSOLIDATED STATEMENTS OF INCOME") == "income"
    assert classify("Consolidated Statements of Comprehensive Income") is None
    assert classify("CONSOLIDATED STATEMENTS OF OPERATIONS") == "income"
    assert classify("Consolidated Statements of Financial Position") == "balance"
    assert classify("CONSOLIDATED BALANCE SHEETS (Parenthetical)") is None
    assert classify("CONSOLIDATED STATEMENTS OF CASH FLOWS") == "cashflow"
    assert classify("CONSOLIDATED STATEMENTS OF CHANGES IN SHAREHOLDERS' EQUITY") is None


def test_parse_page_scales_and_skips_member_rows():
    html = page("STATEMENTS OF INCOME - USD ($)<br> $ in Millions", D3, [
        ("us-gaap_IncomeStatementAbstract", "Income Statement [Abstract]"),
        ("!us-gaap_Revenues", "Total revenue", ["$ 100", "$ 90", "$ 80"]),
        ("us-gaap_EarningsPerShareBasic", "Basic", ["$ 2.43", "$ 0.98", "$ 2.88"]),
        ("rh", "Net Sales [Member]"),
        ("us-gaap_Revenues", "Total revenue", ["95", "85", "75"]),
    ])
    p = parse_r_page(html)
    assert p["money_scale"] == 1e6
    assert [c["end"] for c in p["columns"]] == ["2025-12-31", "2024-12-31", "2023-12-31"]
    assert [c["months"] for c in p["columns"]] == [12, 12, 12]
    money = [r for r in p["rows"] if not r["abstract"]]
    assert len(money) == 2                       # the member row is dropped
    assert money[0]["values"] == [100e6, 90e6, 80e6] and money[0]["total"]
    assert money[1]["values"] == [2.43, 0.98, 2.88]  # per-share not scaled


# A small company whose statements tie, in DaVita's printing style
# (non-operating items printed as negatives), $ in millions.
def income(style="dva"):
    if style == "dva":
        nonop = [("us-gaap_InterestAndDebtExpense", "Debt expense", ["(50)", "(45)", "(40)"]),
                 ("us-gaap_OtherNonoperatingIncomeExpense", "Other loss, net", ["(10)", "(5)", "0"])]
        tax = ("us-gaap_IncomeTaxExpenseBenefit", "Income tax expense", ["35", "37", "30"])
    else:  # Kohl's style: interest printed as a positive cost, tax positive
        nonop = [("us-gaap_InterestIncomeExpenseNet", "Interest expense, net", ["60", "50", "40"])]
        tax = ("us-gaap_IncomeTaxExpenseBenefit", "Provision for income taxes", ["35", "37", "30"])
    pre = ["140", "150", "160"] if style == "dva" else ["140", "150", "160"]
    return page("STATEMENTS OF INCOME - USD ($)<br> $ in Millions", D3, [
        ("!us-gaap_Revenues", "Total revenues", ["1,000", "950", "900"]),
        ("us-gaap_CostsAndExpensesAbstract", "Operating expenses:"),
        ("dva_PatientCareCosts", "Patient care costs", ["750", "710", "650"]),
        ("us-gaap_DepreciationAndAmortization", "Depreciation and amortization", ["50", "48", "46"]),
        ("us-gaap_GoodwillImpairmentLoss", "Goodwill impairment charges", ["0", "0", "4"]),
        ("us-gaap_BusinessCombinationStepAcquisitionEquityInterestInAcquireeRemeasurementGain",
         "Gain on changes in ownership interests", ["0", "(8)", "0"]),
        ("!us-gaap_CostsAndExpenses", "Total operating expenses", ["800", "750", "700"]),
        ("!us-gaap_OperatingIncomeLoss", "Operating income", ["200", "200", "200"]),
        *nonop,
        ("!us-gaap_IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
         "Income before income taxes", pre),
        tax,
        ("!us-gaap_ProfitLoss", "Net income", ["105", "113", "130"]),
        ("us-gaap_NetIncomeLossAttributableToNoncontrollingInterest", "Less: NCI", ["(5)", "(3)", "0"]),
        ("!us-gaap_NetIncomeLoss", "Net income attributable to Test Co", ["100", "110", "130"]),
    ])


def balance(dates, cols):
    """cols: dict of row values per column, $ in millions."""
    def v(k):
        return [str(c[k]) for c in cols]
    return page("BALANCE SHEETS - USD ($)<br> $ in Millions", dates, [
        ("us-gaap_CashAndCashEquivalentsAtCarryingValue", "Cash and cash equivalents", v("cash")),
        ("us-gaap_AccountsReceivableNetCurrent", "Accounts receivable", v("ar")),
        ("!us-gaap_AssetsCurrent", "Total current assets", v("ca")),
        ("us-gaap_PropertyPlantAndEquipmentNet", "Property and equipment, net", v("ppe")),
        ("us-gaap_OperatingLeaseRightOfUseAsset", "Operating lease assets", v("rou")),
        ("!us-gaap_Assets", "Total assets", v("ta")),
        ("us-gaap_AccountsPayableCurrent", "Accounts payable", v("ap")),
        ("us-gaap_LinesOfCreditCurrent", "Borrowings under revolving credit facility", v("rev")),
        ("us-gaap_OperatingLeaseLiabilityCurrent", "Current operating leases", v("olc")),
        ("!us-gaap_LiabilitiesCurrent", "Total current liabilities", v("cl")),
        ("us-gaap_LongTermDebtNoncurrent", "Long-term debt", v("ltd")),
        ("kss_FinanceLeaseLiabilityAndFinancingObligationsNoncurrent",
         "Finance leases and financing obligations", v("fl")),
        ("us-gaap_OperatingLeaseLiabilityNoncurrent", "Operating leases", v("oln")),
        ("us-gaap_StockholdersEquityAbstract", "Shareholders' equity:"),
        ("us-gaap_CommonStockValue", "Common stock", v("cs")),
        ("us-gaap_RetainedEarningsAccumulatedDeficit", "Retained earnings", v("re")),
        ("!us-gaap_StockholdersEquity", "Total shareholders' equity", v("se")),
        ("!us-gaap_LiabilitiesAndStockholdersEquity", "Total liabilities and equity", v("ta")),
    ], months=None)


BS = {"cash": 50, "ar": 150, "ca": 200, "ppe": 600, "rou": 200, "ta": 1000, "ap": 100, "rev": 20,
      "olc": 30, "cl": 150, "ltd": 300, "fl": 80, "oln": 170, "cs": 10, "re": 290, "se": 300}


def cashflow():
    return page("STATEMENTS OF CASH FLOWS - USD ($)<br> $ in Millions", D3, [
        ("us-gaap_ProfitLoss", "Net income", ["105", "113", "130"]),
        ("us-gaap_DepreciationAmortizationAndAccretionNet", "Depreciation and amortization", ["52", "50", "48"]),
        ("us-gaap_IncreaseDecreaseInAccountsReceivable", "Accounts receivable", ["(7)", "(3)", "2"]),
        ("!us-gaap_NetCashProvidedByUsedInOperatingActivities", "Net cash from operations", ["150", "160", "180"]),
        ("us-gaap_PaymentsToAcquirePropertyPlantAndEquipment", "Additions of property and equipment",
         ["(60)", "(55)", "(50)"]),
        ("us-gaap_PaymentsToAcquireBusinessesNetOfCashAcquired", "Acquisitions", ["(10)", "0", "0"]),
        ("!us-gaap_NetCashProvidedByUsedInInvestingActivities", "Net cash from investing", ["(70)", "(55)", "(50)"]),
        ("us-gaap_ProceedsFromRepaymentsOfLinesOfCredit", "Net (repayments) borrowings under revolver",
         ["(20)", "15", "5"]),
        ("us-gaap_PaymentsOfDividends", "Dividends paid", ["(30)", "(30)", "(30)"]),
        ("us-gaap_PaymentsForRepurchaseOfCommonStock", "Purchase of treasury stock", ["(40)", "(60)", "(20)"]),
        ("!us-gaap_NetCashProvidedByUsedInFinancingActivities", "Net cash from financing", ["(90)", "(75)", "(45)"]),
        ("!us-gaap_CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect",
         "Net change in cash", ["(10)", "30", "85"]),
    ])


@pytest.fixture
def company(tmp_path):
    def make(style="dva"):
        latest = tmp_path / "TST" / "A-26"
        prior = tmp_path / "TST" / "A-25"
        bs_old = dict(BS, cash=40, ca=190, ta=990, re=280, se=290)
        bs23 = dict(BS, cash=30, ca=180, ta=980, re=270, se=280)
        write_filing(latest, "A-26", "2026-02-11", "2025-12-31", [
            ("CONSOLIDATED STATEMENTS OF INCOME", income(style)),
            ("CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME", "<html></html>"),
            ("CONSOLIDATED BALANCE SHEETS", balance(D2, [BS, bs_old])),
            ("CONSOLIDATED STATEMENTS OF CASH FLOWS", cashflow())])
        write_filing(prior, "A-25", "2025-02-13", "2024-12-31", [
            ("CONSOLIDATED STATEMENTS OF INCOME", income(style)),
            ("CONSOLIDATED BALANCE SHEETS",
             balance(["Dec. 31, 2024", "Dec. 31, 2023"], [bs_old, bs23])),
            ("CONSOLIDATED STATEMENTS OF CASH FLOWS", cashflow())])
        return build_as_reported("TST", CO, folder=tmp_path / "TST")
    return make


def test_as_reported_merges_third_balance_sheet(company):
    ar = company()
    bs = ar["statements"]["balance"]
    assert [p["label"] for p in bs["periods"]] == ["FY2023", "FY2024", "FY2025"]
    assert bs["periods"][0]["accn"] == "A-25" and bs["periods"][2]["accn"] == "A-26"
    cash = next(r for r in bs["rows"] if r["tag"].endswith("CashAndCashEquivalentsAtCarryingValue"))
    assert cash["values"] == [30e6, 40e6, 50e6]
    inc = ar["statements"]["income"]
    assert [p["label"] for p in inc["periods"]] == ["FY2023", "FY2024", "FY2025"]


@pytest.mark.parametrize("style", ["dva", "kss"])
def test_standard_spread_ties_in_both_sign_styles(company, style):
    std = build_standard(company(style))
    assert std["ties_ok"], [t for t in std["ties"] if not t["ok"]]
    v = lambda st, k: value(std, st, k, "FY2025")
    assert v("income", "revenue") == 1000e6
    assert v("income", "da") == 52e6                       # from the cash flow statement
    assert v("income", "operating_costs") == 748e6         # 750 + 50 - 52
    assert v("income", "ebitda") == 252e6
    assert v("income", "interest_expense") == (50e6 if style == "dva" else 60e6)
    assert v("income", "income_tax") == 35e6
    assert v("income", "nci") == 5e6
    assert value(std, "income", "unusual_operating", "FY2024") == -8e6   # a gain


def test_standard_balance_sheet_debt_includes_revolver_and_financing_obligations(company):
    std = build_standard(company())
    v = lambda k: value(std, "balance", k, "FY2025")
    assert v("debt_current") == 20e6
    assert v("ltd") == 380e6                                # 300 LTD + 80 finance leases/obligations
    assert v("total_debt") == 400e6
    assert v("lease_liabilities") == 200e6
    assert v("receivables") == 150e6


def test_cash_flow_lines_and_net_revolver_split(company):
    std = build_standard(company())
    v = lambda k, p="FY2025": value(std, "cashflow", k, p)
    assert v("capex") == -60e6 and v("acquisitions") == -10e6
    assert v("debt_repaid") == -20e6 and v("debt_issued") == 0
    assert v("debt_issued", "FY2024") == 15e6 and v("debt_repaid", "FY2024") == 0
    assert v("fcf") == 90e6
    src = next(ln for ln in std["cashflow"] if ln["key"] == "capex")["sources"][0]
    assert src["label"] == "Additions of property and equipment" and src["id"] is not None


def test_broken_statement_fails_a_tie(company, tmp_path):
    ar = company()
    rows = ar["statements"]["income"]["rows"]
    pcc = next(r for r in rows if r["label"] == "Patient care costs")
    pcc["values"][-1] += 5e6     # a mis-read number
    std = build_standard(ar)
    assert not std["ties_ok"]
    bad = [t for t in std["ties"] if not t["ok"]]
    assert bad[0]["check"].startswith("Revenue - costs") and bad[0]["period"] == "FY2025"
