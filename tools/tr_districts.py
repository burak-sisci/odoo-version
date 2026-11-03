"""Build the Turkish district list of ov_l10n_tr from the official inventory (T3.4).

Source: the administrative divisions inventory of the Turkish Ministry of the
Interior (e-icisleri.gov.tr, "Mülki İdare Bölümleri Envanteri"). Two of its
list reports are used:
  - the district list ("İlçeler Genel Listesi", 922 districts), which leaves
    out the central district of the 51 provinces without a metropolitan
    municipality;
  - the provincial municipality list ("İl Belediyesi"), which gives those 51
    provinces. Each of them gets a "Merkez" district.

Usage (needs xlrd, from the .venv):
  .venv/Scripts/python tools/tr_districts.py            download and write the CSV
  .venv/Scripts/python tools/tr_districts.py --check    exit 1 if the CSV differs
  .venv/Scripts/python tools/tr_districts.py --from-dir DIR
      use reports downloaded before (ilceler.xls, il_belediyeleri.xls in DIR)
  --save-dir DIR keeps the downloaded reports.

The reports are parsed as data only; nothing in them is executed.
"""
import argparse
import csv
import html
import http.cookiejar
import io
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import xlrd

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'addons' / 'ov_l10n_tr' / 'data' / 'res.city.csv'
STATES = ROOT / 'upstream' / 'odoo' / 'odoo' / 'addons' / 'base' / 'data' / 'res.country.state.csv'
URL = 'https://www.e-icisleri.gov.tr/Anasayfa/MulkiIdariBolumleri.aspx'
HEADERS = {'User-Agent': 'Mozilla/5.0 (nexus-erp-data-check)'}
BUTTONS = {
    'ilceler.xls': 'ctl00$cph1$CografiBirimControl$ImageButton3',  # district list
    'il_belediyeleri.xls': 'ctl00$cph1$CografiBirimControl$ImageButton6',  # provincial municipalities
}
# Columns of the district list: the province row has its name in column 1 and
# "İlçe Sayısı : N" in column 12; district rows have up to four names.
PROVINCE_COLUMN, COUNT_COLUMN, DISTRICT_COLUMNS = 1, 12, (1, 5, 10, 15)
COUNT = re.compile(r'İlçe Sayısı\s*:\s*(\d+)')
TOTAL = re.compile(r'Toplam İlçe Sayısı\s*:\s*(\d+)')
CENTRE = 'Merkez'
ASCII = str.maketrans('çğıöşüÇĞİÖŞÜâîûÂÎÛ', 'cgiosuCGIOSUaiuAIU')


def turkish_upper(text):
    return text.replace('i', 'İ').replace('ı', 'I').upper()


def turkish_lower(text):
    return text.replace('I', 'ı').replace('İ', 'i').lower()


def turkish_title(text):
    """'KARAİSALI' -> 'Karaisalı', '19 MAYIS' -> '19 Mayıs'."""
    words = []
    for word in turkish_lower(text).split():
        words.append(turkish_upper(word[0]) + word[1:])
    return ' '.join(words)


def slug(text):
    return re.sub(r'[^a-z0-9]+', '_', turkish_lower(text).translate(ASCII)).strip('_')


def download(button):
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    page = opener.open(urllib.request.Request(URL, headers=HEADERS), timeout=60).read().decode('utf-8')
    fields = {'__EVENTTARGET': '', '__EVENTARGUMENT': '', '__LASTFOCUS': '', f'{button}.x': '8', f'{button}.y': '8'}
    for name in ('__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION'):
        fields[name] = html.unescape(re.search(rf'name="{name}" id="{name}" value="([^"]*)"', page).group(1))
    request = urllib.request.Request(
        URL, data=urllib.parse.urlencode(fields).encode(),
        headers={**HEADERS, 'Content-Type': 'application/x-www-form-urlencoded', 'Referer': URL},
    )
    response = opener.open(request, timeout=180)
    if 'excel' not in (response.headers.get('Content-Type') or ''):
        sys.exit(f'unexpected answer for {button}: {response.headers.get("Content-Type")}')
    return response.read()


def sheet(content):
    return xlrd.open_workbook(file_contents=content, logfile=io.StringIO()).sheet_by_index(0)


def parse_districts(content):
    """Return {province: [district, ...]} in upper case, checked against the counts in the report."""
    rows = sheet(content)
    provinces, declared, total = {}, {}, None
    current = None
    for r in range(rows.nrows):
        cells = [str(rows.cell_value(r, c)).strip() for c in range(rows.ncols)]
        if match := TOTAL.search(' '.join(cells)):
            total = int(match.group(1))
        elif match := COUNT.search(cells[COUNT_COLUMN]):
            current = cells[PROVINCE_COLUMN]
            provinces[current] = []
            declared[current] = int(match.group(1))
        elif current:
            provinces[current] += [cells[c] for c in DISTRICT_COLUMNS if c < len(cells) and cells[c]]
    for province, districts in provinces.items():
        if len(districts) != declared[province] or len(set(districts)) != len(districts):
            sys.exit(f'{province}: {len(districts)} districts read, {declared[province]} declared')
    if total is None or sum(map(len, provinces.values())) != total:
        sys.exit(f'total: {sum(map(len, provinces.values()))} districts read, {total} declared')
    return provinces


def parse_provincial_centres(content):
    """Return the provinces with a provincial municipality ("İL BELEDİYESİ"), in upper case."""
    rows = sheet(content)
    centres = set()
    for r in range(rows.nrows):
        cells = [str(rows.cell_value(r, c)).strip() for c in range(rows.ncols)]
        if 'İL BELEDİYESİ' in cells:
            centres.add(cells[6])
    return centres


def states():
    """Return {upper-case name: (xml id, code)} of the Turkish provinces in the base data."""
    with STATES.open(encoding='utf-8') as file:
        return {
            turkish_upper(row['name']): (f'base.{row["id"]}', row['code'])
            for row in csv.DictReader(file) if row['country_id:id'] == 'tr'
        }


def build(districts, centres):
    known = states()
    if set(districts) != set(known) or not centres <= set(known):
        sys.exit(f'provinces not in the base data: {sorted(set(districts) ^ set(known)) or sorted(centres - set(known))}')
    lines = []
    for province, names in districts.items():
        state, code = known[province]
        plate = code.split('-')[1]
        names = [turkish_title(name) for name in names] + ([CENTRE] if province in centres else [])
        for name in names:
            lines.append((f'city_tr_{plate}_{slug(name)}', name, state, 'base.tr'))
    if len({line[0] for line in lines}) != len(lines):
        sys.exit('duplicate xml ids')
    lines.sort(key=lambda line: line[0])
    out = io.StringIO()
    writer = csv.writer(out, lineterminator='\n')
    writer.writerow(['id', 'name', 'state_id:id', 'country_id:id'])
    writer.writerows(lines)
    return out.getvalue(), len(lines), len(centres)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--check', action='store_true', help='exit 1 if the CSV is not up to date')
    parser.add_argument('--from-dir', type=Path, help='use reports downloaded before')
    parser.add_argument('--save-dir', type=Path, help='keep the downloaded reports')
    args = parser.parse_args()
    reports = {}
    for name, button in BUTTONS.items():
        if args.from_dir:
            reports[name] = (args.from_dir / name).read_bytes()
        else:
            reports[name] = download(button)
            if args.save_dir:
                args.save_dir.mkdir(parents=True, exist_ok=True)
                (args.save_dir / name).write_bytes(reports[name])
    text, count, centres = build(parse_districts(reports['ilceler.xls']), parse_provincial_centres(reports['il_belediyeleri.xls']))
    print(f'{count} districts ({count - centres} listed + {centres} provincial centres)')
    current = TARGET.read_text(encoding='utf-8') if TARGET.exists() else ''
    if args.check:
        if current != text:
            print(f'{TARGET.relative_to(ROOT)} is not up to date')
            return 1
        print(f'{TARGET.relative_to(ROOT)} is up to date')
        return 0
    TARGET.write_text(text, encoding='utf-8', newline='\n')
    print(f'written {TARGET.relative_to(ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
