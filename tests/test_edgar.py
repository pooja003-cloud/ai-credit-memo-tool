from creditmemo.edgar import latest_10ks, statement_reports

SUMMARY = b"""<?xml version="1.0" encoding="utf-8"?>
<FilingSummary><MyReports>
 <Report instance="dva-20251231.htm"><IsDefault>false</IsDefault><HtmlFileName>R1.htm</HtmlFileName>
  <LongName>0000001 - Document - Cover</LongName><ShortName>Cover</ShortName>
  <MenuCategory>Cover</MenuCategory><Position>1</Position></Report>
 <Report instance="dva-20251231.htm"><HtmlFileName>R4.htm</HtmlFileName>
  <LongName>0000004 - Statement - CONSOLIDATED BALANCE SHEETS</LongName>
  <ShortName>CONSOLIDATED BALANCE SHEETS</ShortName><MenuCategory>Statements</MenuCategory>
  <Position>4</Position></Report>
 <Report instance="dva-20251231.htm"><HtmlFileName>R2.htm</HtmlFileName>
  <LongName>0000002 - Statement - CONSOLIDATED STATEMENTS OF INCOME</LongName>
  <ShortName>CONSOLIDATED STATEMENTS OF INCOME</ShortName><MenuCategory>Statements</MenuCategory>
  <Position>2</Position></Report>
 <Report instance="dva-20251231.htm"><HtmlFileName>R9.htm</HtmlFileName>
  <LongName>0000009 - Disclosure - Leases</LongName><ShortName>Leases</ShortName>
  <MenuCategory>Notes</MenuCategory><Position>9</Position></Report>
</MyReports></FilingSummary>"""


def test_statement_reports_keeps_only_statements_in_order():
    reps = statement_reports(SUMMARY)
    assert [r["file"] for r in reps] == ["R2.htm", "R4.htm"]
    assert reps[0]["short_name"] == "CONSOLIDATED STATEMENTS OF INCOME"


def test_latest_10ks_skips_amendments_and_other_forms():
    sub = {"filings": {"recent": {
        "accessionNumber": ["a1", "a2", "a3", "a4", "a5"],
        "form": ["10-Q", "10-K", "10-K/A", "10-K", "10-K"],
        "filingDate": ["2026-04-30", "2026-02-11", "2025-04-01", "2025-02-13", "2024-02-15"],
        "reportDate": ["2026-03-31", "2025-12-31", "2024-12-31", "2024-12-31", "2023-12-31"],
        "primaryDocument": ["q.htm", "k25.htm", "ka.htm", "k24.htm", "k23.htm"],
    }}}
    got = latest_10ks(sub)
    assert [g["accessionNumber"] for g in got] == ["a2", "a4"]
    assert got[0]["primaryDocument"] == "k25.htm"
