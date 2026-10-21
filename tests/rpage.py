"""Build small fake SEC statement pages (R files) in the real page format."""

import json


def page(title, dates, rows, months=12):
    """rows: (tag, label, [values as printed]) or (tag, label) for an abstract
    heading; a tag starting with '!' marks a total row; ('rh', label) starts
    a member breakdown."""
    head = (f'<tr>\n<th class="tl" colspan="1" rowspan="2"><div><strong>{title}</strong></div></th>\n'
            + (f'<th class="th" colspan="{len(dates)}">{months} Months Ended</th>\n</tr>\n<tr>\n'
               if months else "")
            + "".join(f'<th class="th"><div>{d}</div></th>\n' for d in dates) + "</tr>\n")
    body = []
    for r in rows:
        if r[0] == "rh":
            body.append(f'<tr class="rh"><td colspan="4">{r[1]}</td></tr>')
            continue
        tag, label = r[0], r[1]
        total = tag.startswith("!")
        tag = tag.lstrip("!")
        link = (f'<a class="a" onclick="Show.showAR( this, \'defref_{tag}\', window );">'
                f'{"<strong>" + label + "</strong>" if len(r) == 2 else label}</a>')
        cls = "rou" if total else "ro"
        if len(r) == 2:
            cells = "".join('<td class="text">&#160;<span></span></td>' for _ in dates)
        else:
            cells = "".join(f'<td class="nump">{v}<span></span></td>' for v in r[2])
        body.append(f'<tr class="{cls}">\n<td class="pl">{link}</td>\n{cells}\n</tr>')
    return ('<html><body><table class="report" border="0" cellspacing="2">\n' + head
            + "\n".join(body) + "\n</table></body></html>")


def write_filing(folder, accn, filed, period, pages):
    """pages: list of (short_name, html). Writes R files and index.json."""
    folder.mkdir(parents=True, exist_ok=True)
    stmts = []
    for i, (name, html) in enumerate(pages, 2):
        (folder / f"R{i}.htm").write_text(html)
        stmts.append({"position": i, "short_name": name, "long_name": name, "file": f"R{i}.htm"})
    (folder / "index.json").write_text(json.dumps({
        "accessionNumber": accn, "filingDate": filed, "reportDate": period,
        "base_url": f"https://www.sec.gov/Archives/edgar/data/1/{accn}", "statements": stmts}))
