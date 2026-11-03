from datetime import date

import requests

from odoo.tests import BaseCase, tagged

from odoo.addons.ov_l10n_tr_tcmb.models.res_company import business_days
from odoo.addons.ov_l10n_tr_tcmb.tests.common import (
    BULLETIN_DAY,
    FakeTcmb,
    fixture_bulletin,
    make_bulletin,
)
from odoo.addons.ov_l10n_tr_tcmb.tools import (
    ARCHIVE_URL,
    MAX_SIZE,
    TODAY_URL,
    BulletinError,
    company_rates,
    fetch_bulletin,
    parse_bulletin,
)


@tagged('post_install', '-at_install')
class TestTcmbBulletin(BaseCase):
    """Reading bulletins and computing rates, without a database."""

    def setUp(self):
        super().setUp()
        self.day, self.currencies = parse_bulletin(fixture_bulletin())

    def test_parse(self):
        self.assertEqual(self.day, BULLETIN_DAY)
        self.assertEqual(sorted(self.currencies), ['EUR', 'GBP', 'JPY', 'RUB', 'USD', 'XDR'])
        self.assertEqual(self.currencies['USD'], {
            'unit': 1.0,
            'forex_buying': 40.0,
            'forex_selling': 40.2,
            'banknote_buying': 39.9,
            'banknote_selling': 40.3,
        })
        self.assertEqual(self.currencies['JPY']['unit'], 100.0)
        # Empty values: no banknote rate for RUB, only a forex buying rate for XDR.
        self.assertIsNone(self.currencies['RUB']['banknote_buying'])
        self.assertIsNone(self.currencies['XDR']['forex_selling'])

    def test_parse_rejects_other_documents(self):
        documents = {
            'html page': b'<html><body>Not Found</body></html>',
            'not xml': b'Service unavailable',
            'no date': b'<Tarih_Date><Currency CurrencyCode="USD"><Unit>1</Unit></Currency></Tarih_Date>',
            'no currency': b'<Tarih_Date Tarih="13.01.2025"/>',
            # An external entity is neither loaded nor accepted.
            'entity': (
                b'<?xml version="1.0"?><!DOCTYPE Tarih_Date [<!ENTITY x SYSTEM "file:///etc/hostname">]>'
                b'<Tarih_Date Tarih="13.01.2025"><Currency CurrencyCode="USD"><Unit>1</Unit>'
                b'<ForexBuying>&x;</ForexBuying></Currency></Tarih_Date>'
            ),
            'too large': b' ' * (MAX_SIZE + 1),
        }
        for name, content in documents.items():
            with self.subTest(name), self.assertRaises(BulletinError):
                parse_bulletin(content)

    def test_parse_ignores_invalid_values(self):
        content = (
            b'<Tarih_Date Tarih="13.01.2025">'
            b'<Currency CurrencyCode="USD"><Unit>1</Unit><ForexBuying>-1</ForexBuying><ForexSelling>abc</ForexSelling>'
            b'<BanknoteBuying>nan</BanknoteBuying><BanknoteSelling>inf</BanknoteSelling></Currency>'
            b'<Currency CurrencyCode="usd"><Unit>1</Unit><ForexBuying>1</ForexBuying></Currency>'
            b'<Currency CurrencyCode="EUR"><Unit>0</Unit><ForexBuying>1</ForexBuying></Currency>'
            b'</Tarih_Date>'
        )
        __, currencies = parse_bulletin(content)
        self.assertEqual(list(currencies), ['USD'])
        self.assertEqual(set(currencies['USD'].values()), {1.0, None})

    def test_rates_of_a_lira_company(self):
        codes = ['USD', 'EUR', 'JPY', 'RUB', 'XDR', 'TRY', 'BRL']
        rates = company_rates(self.currencies, 'TRY', codes, 'forex_buying')
        # Units of the currency for one lira; a yen rate is given for 100 yen.
        self.assertEqual(sorted(rates), ['EUR', 'JPY', 'RUB', 'USD', 'XDR'])
        self.assertAlmostEqual(1 / rates['USD'], 40.0)
        self.assertAlmostEqual(1 / rates['EUR'], 44.0)
        self.assertAlmostEqual(1 / rates['JPY'], 0.27)
        self.assertAlmostEqual(1 / rates['RUB'], 0.5)

    def test_rate_types_and_fallback(self):
        codes = ['USD', 'RUB', 'XDR']
        banknote = company_rates(self.currencies, 'TRY', codes, 'banknote_buying')
        self.assertAlmostEqual(1 / banknote['USD'], 39.9)
        # No banknote rate for RUB: the forex rate of the same side.
        self.assertAlmostEqual(1 / banknote['RUB'], 0.5)
        self.assertAlmostEqual(1 / banknote['XDR'], 55.0)
        selling = company_rates(self.currencies, 'TRY', codes, 'banknote_selling')
        self.assertAlmostEqual(1 / selling['USD'], 40.3)
        self.assertAlmostEqual(1 / selling['RUB'], 0.51)
        # XDR has no selling rate at all.
        self.assertNotIn('XDR', selling)

    def test_cross_rates_of_a_dollar_company(self):
        rates = company_rates(self.currencies, 'USD', ['TRY', 'EUR', 'USD', 'JPY'], 'forex_buying')
        self.assertEqual(sorted(rates), ['EUR', 'JPY', 'TRY'])
        self.assertAlmostEqual(rates['TRY'], 40.0)
        self.assertAlmostEqual(rates['EUR'], 40.0 / 44.0)
        self.assertAlmostEqual(rates['JPY'], 40.0 / 0.27)

    def test_company_currency_not_in_bulletin(self):
        self.assertEqual(company_rates(self.currencies, 'BRL', ['TRY', 'USD'], 'forex_buying'), {})

    def test_fetch(self):
        tcmb = FakeTcmb(latest=fixture_bulletin(), archive={date(2025, 1, 10): make_bulletin(date(2025, 1, 10), 39.5)})
        with tcmb.serve():
            self.assertEqual(fetch_bulletin()[0], BULLETIN_DAY)
            self.assertEqual(fetch_bulletin(date(2025, 1, 10))[1]['USD']['forex_buying'], 39.5)
            # No bulletin that day (a public holiday): 404.
            self.assertIsNone(fetch_bulletin(date(2025, 1, 9)))
        self.assertEqual(tcmb.requested, [
            TODAY_URL,
            'https://www.tcmb.gov.tr/kurlar/202501/10012025.xml',
            'https://www.tcmb.gov.tr/kurlar/202501/09012025.xml',
        ])

    def test_fetch_errors(self):
        # The archive address of a day answers with the bulletin of another day.
        tcmb = FakeTcmb(archive={date(2025, 1, 10): fixture_bulletin()})
        with tcmb.serve(), self.assertRaises(BulletinError):
            fetch_bulletin(date(2025, 1, 10))
        # Without a day, even a 404 is an error.
        tcmb = FakeTcmb()
        with tcmb.serve(), self.assertRaises(requests.HTTPError):
            fetch_bulletin()

    def test_business_days(self):
        days = list(business_days(date(2025, 1, 9), date(2025, 1, 14)))
        self.assertEqual(days, [date(2025, 1, 9), date(2025, 1, 10), date(2025, 1, 13), date(2025, 1, 14)])
        self.assertEqual(ARCHIVE_URL.format(day=days[0]), 'https://www.tcmb.gov.tr/kurlar/202501/09012025.xml')
