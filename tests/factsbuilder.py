"""Build small synthetic company-facts JSON for tests."""


class CF:
    def __init__(self, name="TEST CO"):
        self.data = {"cik": 1, "entityName": name, "facts": {"us-gaap": {}}}

    def add(self, tag, val, end, start=None, accn="0000000001-25-000001",
            form="10-K", filed="2025-02-15", unit="USD"):
        node = self.data["facts"]["us-gaap"].setdefault(tag, {"units": {}})
        row = {"end": end, "val": val, "accn": accn, "form": form, "filed": filed}
        if start:
            row["start"] = start
        node["units"].setdefault(unit, []).append(row)
        return self

    def flow(self, tag, val, year, **kw):
        """A calendar-year flow."""
        return self.add(tag, val, f"{year}-12-31", start=f"{year}-01-01", **kw)

    def inst(self, tag, val, year, **kw):
        return self.add(tag, val, f"{year}-12-31", **kw)
