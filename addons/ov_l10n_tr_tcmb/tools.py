"""Exchange rate bulletins of the Central Bank of the Republic of Türkiye (TCMB).

TCMB publishes one bulletin per business day, around 15:30 Istanbul time. The
latest one is at TODAY_URL; earlier ones stay at ARCHIVE_URL. Days without a
bulletin (weekends, public holidays) answer 404 at the archive address.
"""
import datetime
import math
import re

import requests
from lxml import etree

TODAY_URL = 'https://www.tcmb.gov.tr/kurlar/today.xml'
ARCHIVE_URL = 'https://www.tcmb.gov.tr/kurlar/{day:%Y%m}/{day:%d%m%Y}.xml'
# (connect, read) seconds: the archive answers in 0.35 s on average, slower under load.
TIMEOUT = (10, 30)
# A bulletin is about 9 KB; anything much larger is not one.
MAX_SIZE = 1024 * 1024
TRY = 'TRY'
CODE = re.compile(r'[A-Z]{3}')
# Rate types and their element in the bulletin.
RATE_FIELDS = {
    'forex_buying': 'ForexBuying',
    'forex_selling': 'ForexSelling',
    'banknote_buying': 'BanknoteBuying',
    'banknote_selling': 'BanknoteSelling',
}
# TCMB gives no banknote rate for some currencies (RUB, CNY, AED and others):
# the forex rate of the same side is used instead.
FALLBACK = {
    'banknote_buying': 'forex_buying',
    'banknote_selling': 'forex_selling',
}
PARSER = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)


class BulletinError(ValueError):
    """The answer is not a TCMB rate bulletin."""


def http_get(url, session=None):
    return (session or requests).get(url, timeout=TIMEOUT)


def _number(text):
    try:
        value = float((text or '').strip())
    except ValueError:
        return None
    return value if math.isfinite(value) and value > 0 else None


def parse_bulletin(content):
    """Read a bulletin: return (date, {code: {'unit': n, 'forex_buying': x, ...}}).

    A missing or invalid rate is None. Raise BulletinError for any other document.
    """
    if len(content) > MAX_SIZE:
        message = 'the document is too large'
        raise BulletinError(message)
    try:
        root = etree.fromstring(content, PARSER)
    except etree.XMLSyntaxError as error:
        raise BulletinError(f'not XML: {error}') from error
    if root.getroottree().docinfo.doctype:
        message = 'a document type declaration is not expected'
        raise BulletinError(message)
    if root.tag != 'Tarih_Date':
        raise BulletinError(f'unexpected root element {root.tag!r}')
    try:
        day = datetime.datetime.strptime(root.get('Tarih', ''), '%d.%m.%Y').date()
    except ValueError as error:
        raise BulletinError(f'no bulletin date: {error}') from error
    currencies = {}
    for node in root.iterfind('Currency'):
        code = (node.get('CurrencyCode') or '').strip()
        unit = _number(node.findtext('Unit'))
        if CODE.fullmatch(code) and unit:
            currencies[code] = {
                'unit': unit,
                **{rate_type: _number(node.findtext(tag)) for rate_type, tag in RATE_FIELDS.items()},
            }
    if not currencies:
        message = 'the bulletin has no currency'
        raise BulletinError(message)
    return day, currencies


def fetch_bulletin(day=None, session=None):
    """Download the bulletin of `day`, or the latest one without a day.

    Return (date, currencies), or None when TCMB published no bulletin that day.
    Raise requests.RequestException on a network error, BulletinError on an
    unexpected answer.
    """
    response = http_get(ARCHIVE_URL.format(day=day) if day else TODAY_URL, session)
    if day and response.status_code == 404:
        return None
    response.raise_for_status()
    bulletin = parse_bulletin(response.content)
    if day and bulletin[0] != day:
        raise BulletinError(f'the bulletin of {day} is dated {bulletin[0]}')
    return bulletin


def try_value(currencies, code, rate_type):
    """TRY value of one unit of the currency, None when the bulletin gives none."""
    if code == TRY:
        return 1.0
    values = currencies.get(code)
    if not values:
        return None
    value = values[rate_type] or values.get(FALLBACK.get(rate_type, rate_type))
    return value / values['unit'] if value else None


def company_rates(currencies, company_code, codes, rate_type):
    """Rates for a company: units of each currency for one unit of the company currency.

    This is the meaning of res.currency.rate.rate. A company whose currency is
    not in the bulletin gets no rate; other currencies come as cross rates over TRY.
    """
    base = try_value(currencies, company_code, rate_type)
    if not base:
        return {}
    rates = {}
    for code in codes:
        value = try_value(currencies, code, rate_type) if code != company_code else None
        if value:
            rates[code] = base / value
    return rates
