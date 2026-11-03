"""Fictional TCMB bulletins and a fake TCMB server for the tests (no network)."""
from contextlib import contextmanager
from datetime import date
from unittest.mock import patch

import requests

from odoo.tools.misc import file_open

from odoo.addons.ov_l10n_tr_tcmb.tools import ARCHIVE_URL, TODAY_URL

# Day of the fixture bulletin (tests/data/bulletin.xml), a Monday.
BULLETIN_DAY = date(2025, 1, 13)


def fixture_bulletin():
    with file_open('ov_l10n_tr_tcmb/tests/data/bulletin.xml', 'rb') as file:
        return file.read()


def make_bulletin(day, usd, eur=None):
    """A small bulletin with fictional USD (and EUR) forex and banknote rates."""
    rows = [('USD', usd)] + ([('EUR', eur)] if eur else [])
    currencies = ''.join(
        f'<Currency Kod="{code}" CurrencyCode="{code}"><Unit>1</Unit>'
        f'<ForexBuying>{value:.4f}</ForexBuying><ForexSelling>{value + 0.1:.4f}</ForexSelling>'
        f'<BanknoteBuying>{value - 0.05:.4f}</BanknoteBuying><BanknoteSelling>{value + 0.15:.4f}</BanknoteSelling>'
        '</Currency>'
        for code, value in rows
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<Tarih_Date Tarih="{day:%d.%m.%Y}" Date="{day:%m/%d/%Y}" Bulten_No="0">{currencies}</Tarih_Date>'
    ).encode()


class FakeResponse:
    def __init__(self, status_code, content=b''):
        self.status_code = status_code
        self.content = content

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f'{self.status_code} Error', response=self)


class FakeTcmb:
    """Answer like TCMB: `latest` at the today address, `archive` by day, 404 for other days.

    An archive value may be an exception, raised as a network error.
    """

    def __init__(self, latest=None, archive=None):
        self.latest = latest
        self.archive = archive or {}
        self.requested = []

    def get(self, url, session=None):
        self.requested.append(url)
        if url == TODAY_URL:
            answer = self.latest
        else:
            answer = next((value for day, value in self.archive.items() if ARCHIVE_URL.format(day=day) == url), None)
        if isinstance(answer, Exception):
            raise answer
        return FakeResponse(200, answer) if answer is not None else FakeResponse(404, b'<html>Not Found</html>')

    @contextmanager
    def serve(self):
        with patch('odoo.addons.ov_l10n_tr_tcmb.tools.http_get', self.get):
            yield self
