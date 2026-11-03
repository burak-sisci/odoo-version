from datetime import date, timedelta

import requests

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged

from odoo.addons.ov_l10n_tr_tcmb.models.res_company import CATCH_UP_DAYS, business_days
from odoo.addons.ov_l10n_tr_tcmb.tests.common import (
    BULLETIN_DAY,
    FakeTcmb,
    fixture_bulletin,
    make_bulletin,
)
from odoo.addons.ov_l10n_tr_tcmb.tools import ARCHIVE_URL, TODAY_URL, parse_bulletin
from odoo.addons.ov_l10n_tr_tcmb.wizard.tcmb_rate_import import MAX_IMPORT_DAYS

# Days around the fixture bulletin (Monday 13.01.2025): the Thursday before has a
# bulletin, the Friday is taken as a public holiday (404), then the weekend.
THURSDAY = date(2025, 1, 9)
FRIDAY = date(2025, 1, 10)
WEDNESDAY = date(2025, 1, 8)


def archive(day):
    return ARCHIVE_URL.format(day=day)


@tagged('post_install', '-at_install')
class TestTcmbRates(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.try_ = cls.env.ref('base.TRY')
        cls.usd = cls.env.ref('base.USD')
        currencies = cls.try_ | cls.usd | cls.env.ref('base.EUR') | cls.env.ref('base.JPY') | cls.env.ref('base.RUB')
        currencies.active = True
        cls.env.ref('base.GBP').active = False
        cls.turkey = cls.env.ref('base.tr')
        cls.company = cls.env['res.company'].create({
            'name': 'Kurgu Dış Ticaret A.Ş.',
            'country_id': cls.turkey.id,
            'currency_id': cls.try_.id,
        })
        # Only the test company fetches rates.
        cls.env['res.company'].search([('id', '!=', cls.company.id)]).ov_tcmb_auto = False
        cls.Rate = cls.env['res.currency.rate']
        cls.Company = cls.env['res.company']

    def rates_of(self, day, company=None):
        rates = self.Rate.search([('company_id', '=', (company or self.company).id), ('name', '=', day)])
        return {rate.currency_id.name: rate.rate for rate in rates}

    def stored_days(self, company=None):
        return sorted(set(self.Rate.search([('company_id', '=', (company or self.company).id)]).mapped('name')))

    def convert_usd(self, day, company=None):
        return self.usd._convert(1.0, self.try_, company or self.company, day, round=False)

    def test_company_defaults(self):
        self.assertTrue(self.company.ov_tcmb_auto)
        self.assertEqual(self.company.ov_tcmb_rate_type, 'forex_buying')
        self.assertFalse(self.company.ov_tcmb_last_date)
        german = self.Company.create({'name': 'Fiktiv GmbH', 'country_id': self.env.ref('base.de').id})
        self.assertFalse(german.ov_tcmb_auto)
        german.country_id = self.turkey
        self.assertTrue(german.ov_tcmb_auto)

    def test_apply(self):
        __, currencies = parse_bulletin(fixture_bulletin())
        count = self.company._ov_tcmb_apply(BULLETIN_DAY, currencies)
        rates = self.rates_of(BULLETIN_DAY)
        # GBP is not active, XDR is not a currency of the database, TRY is the company currency.
        self.assertEqual(sorted(rates), ['EUR', 'JPY', 'RUB', 'USD'])
        self.assertEqual(count, 4)
        self.assertAlmostEqual(1 / rates['USD'], 40.0)
        self.assertAlmostEqual(1 / rates['JPY'], 0.27)
        # The rates belong to the company only.
        self.assertFalse(self.Rate.search([('company_id', '=', False), ('name', '=', BULLETIN_DAY)]))

    def test_rate_applies_from_the_next_day(self):
        self.Rate.create({
            'name': BULLETIN_DAY - timedelta(days=3),
            'rate': 1 / 30.0,
            'currency_id': self.usd.id,
            'company_id': self.company.id,
        })
        self.company._ov_tcmb_apply(BULLETIN_DAY, parse_bulletin(fixture_bulletin())[1])
        # The bulletin of Monday afternoon gives the rate of Tuesday.
        self.assertAlmostEqual(self.convert_usd(BULLETIN_DAY), 30.0)
        self.assertAlmostEqual(self.convert_usd(BULLETIN_DAY + timedelta(days=1)), 40.0)
        self.assertAlmostEqual(self.convert_usd(BULLETIN_DAY + timedelta(days=5)), 40.0)

    def test_apply_replaces_the_rate_of_the_day(self):
        self.company._ov_tcmb_apply(BULLETIN_DAY, parse_bulletin(fixture_bulletin())[1])
        self.company._ov_tcmb_apply(BULLETIN_DAY, parse_bulletin(make_bulletin(BULLETIN_DAY, 41.0))[1])
        rates = self.Rate.search([('company_id', '=', self.company.id), ('name', '=', BULLETIN_DAY)])
        self.assertEqual(len(rates.filtered(lambda rate: rate.currency_id == self.usd)), 1)
        self.assertAlmostEqual(1 / self.rates_of(BULLETIN_DAY)['USD'], 41.0)
        # A currency missing from the second bulletin keeps its rate.
        self.assertAlmostEqual(1 / self.rates_of(BULLETIN_DAY)['EUR'], 44.0)

    def test_rate_type(self):
        self.company.ov_tcmb_rate_type = 'banknote_selling'
        self.company._ov_tcmb_apply(BULLETIN_DAY, parse_bulletin(fixture_bulletin())[1])
        rates = self.rates_of(BULLETIN_DAY)
        self.assertAlmostEqual(1 / rates['USD'], 40.3)
        # No banknote rate for RUB: forex selling.
        self.assertAlmostEqual(1 / rates['RUB'], 0.51)

    def test_dollar_company(self):
        company = self.Company.create({
            'name': 'Kurgu Holding A.Ş.',
            'country_id': self.turkey.id,
            'currency_id': self.usd.id,
        })
        company._ov_tcmb_apply(BULLETIN_DAY, parse_bulletin(fixture_bulletin())[1])
        rates = self.rates_of(BULLETIN_DAY, company)
        self.assertNotIn('USD', rates)
        self.assertAlmostEqual(rates['TRY'], 40.0)
        self.assertAlmostEqual(rates['EUR'], 40.0 / 44.0)
        amount = self.try_._convert(400.0, self.usd, company, BULLETIN_DAY + timedelta(days=1), round=False)
        self.assertAlmostEqual(amount, 10.0)

    def test_cron_catches_up(self):
        self.company.ov_tcmb_last_date = WEDNESDAY
        tcmb = FakeTcmb(latest=fixture_bulletin(), archive={THURSDAY: make_bulletin(THURSDAY, 39.0)})
        with tcmb.serve():
            self.Company._ov_tcmb_cron()
        # The weekend is not requested; the Friday answers 404.
        self.assertEqual(tcmb.requested, [TODAY_URL, archive(THURSDAY), archive(FRIDAY)])
        self.assertEqual(self.stored_days(), [THURSDAY, BULLETIN_DAY])
        self.assertAlmostEqual(1 / self.rates_of(THURSDAY)['USD'], 39.0)
        self.assertAlmostEqual(1 / self.rates_of(BULLETIN_DAY)['USD'], 40.0)
        self.assertEqual(self.company.ov_tcmb_last_date, BULLETIN_DAY)
        # Next run, same bulletin: one request, nothing new.
        with tcmb.serve():
            self.Company._ov_tcmb_cron()
        self.assertEqual(tcmb.requested[3:], [TODAY_URL])
        self.assertEqual(self.stored_days(), [THURSDAY, BULLETIN_DAY])

    def test_cron_first_run(self):
        tcmb = FakeTcmb(latest=fixture_bulletin())
        with tcmb.serve():
            self.Company._ov_tcmb_cron()
        self.assertEqual(tcmb.requested, [TODAY_URL])
        self.assertEqual(self.stored_days(), [BULLETIN_DAY])
        self.assertEqual(self.company.ov_tcmb_last_date, BULLETIN_DAY)

    def test_cron_catch_up_limit(self):
        self.company.ov_tcmb_last_date = BULLETIN_DAY - timedelta(days=60)
        tcmb = FakeTcmb(latest=fixture_bulletin())
        with tcmb.serve():
            self.Company._ov_tcmb_cron()
        start = BULLETIN_DAY - timedelta(days=CATCH_UP_DAYS)
        expected = [archive(day) for day in business_days(start, BULLETIN_DAY - timedelta(days=1))]
        self.assertEqual(tcmb.requested[1:], expected)
        self.assertEqual(len(expected), 21)

    def test_cron_network_error(self):
        self.company.ov_tcmb_last_date = WEDNESDAY
        cron = self.env.ref('ov_l10n_tr_tcmb.ir_cron_tcmb_rates')
        Trigger = self.env['ir.cron.trigger']
        before = Trigger.search([('cron_id', '=', cron.id)])
        tcmb = FakeTcmb(latest=requests.ConnectionError('TCMB unreachable'))
        with tcmb.serve(), self.assertLogs('odoo.addons.ov_l10n_tr_tcmb.models.res_company', 'WARNING') as logs:
            self.Company._ov_tcmb_cron()
        self.assertIn('TCMB unreachable', logs.output[0])
        self.assertEqual(self.company.ov_tcmb_last_date, WEDNESDAY)
        self.assertFalse(self.stored_days())
        # Another try in an hour.
        trigger = Trigger.search([('cron_id', '=', cron.id)]) - before
        self.assertEqual(len(trigger), 1)
        delay = trigger.call_at - fields.Datetime.now()
        self.assertTrue(timedelta(minutes=58) < delay <= timedelta(hours=1), delay)

    def test_cron_error_while_catching_up(self):
        self.company.ov_tcmb_last_date = WEDNESDAY
        tcmb = FakeTcmb(
            latest=fixture_bulletin(),
            archive={THURSDAY: make_bulletin(THURSDAY, 39.0), FRIDAY: requests.Timeout('read timed out')},
        )
        with tcmb.serve(), self.assertLogs('odoo.addons.ov_l10n_tr_tcmb.models.res_company', 'WARNING'):
            self.Company._ov_tcmb_cron()
        # The Thursday stays; the next run goes on from the Friday.
        self.assertEqual(self.stored_days(), [THURSDAY])
        self.assertEqual(self.company.ov_tcmb_last_date, THURSDAY)
        tcmb.archive[FRIDAY] = None
        with tcmb.serve():
            self.Company._ov_tcmb_cron()
        self.assertEqual(tcmb.requested[-2:], [TODAY_URL, archive(FRIDAY)])
        self.assertEqual(self.stored_days(), [THURSDAY, BULLETIN_DAY])

    def test_cron_skips_companies(self):
        self.company.ov_tcmb_auto = False
        branch = self.Company.create({
            'name': 'Kurgu Dış Ticaret İzmir Şubesi',
            'parent_id': self.company.id,
            'country_id': self.turkey.id,
        })
        self.assertTrue(branch.ov_tcmb_auto)
        tcmb = FakeTcmb(latest=fixture_bulletin())
        with tcmb.serve():
            self.Company._ov_tcmb_cron()
        # The root company is off; a branch never fetches on its own.
        self.assertEqual(tcmb.requested, [])

    def test_cron_record(self):
        cron = self.env.ref('ov_l10n_tr_tcmb.ir_cron_tcmb_rates')
        self.assertTrue(cron.active)
        self.assertEqual((cron.interval_number, cron.interval_type), (1, 'days'))
        # 13:00 UTC is 16:00 in Istanbul, after the bulletin of about 15:30.
        self.assertEqual((cron.nextcall.hour, cron.nextcall.minute), (13, 0))
        # The job's action, as its user runs it (the scheduler would use another cursor).
        tcmb = FakeTcmb(latest=fixture_bulletin())
        with tcmb.serve():
            cron.ir_actions_server_id.with_user(cron.user_id).run()
        self.assertEqual(self.company.ov_tcmb_last_date, BULLETIN_DAY)

    def test_import(self):
        tcmb = FakeTcmb(archive={THURSDAY: make_bulletin(THURSDAY, 39.0), BULLETIN_DAY: fixture_bulletin()})
        wizard = self.env['ov.tcmb.rate.import'].with_company(self.company).create({
            'date_from': THURSDAY,
            'date_to': BULLETIN_DAY,
        })
        self.assertEqual(wizard.company_id, self.company)
        self.assertEqual(wizard.rate_type, 'forex_buying')
        with tcmb.serve():
            action = wizard.action_import()
        self.assertEqual(tcmb.requested, [archive(THURSDAY), archive(FRIDAY), archive(BULLETIN_DAY)])
        self.assertEqual(action['params']['type'], 'success')
        self.assertIn('2', action['params']['message'])
        self.assertEqual(self.stored_days(), [THURSDAY, BULLETIN_DAY])
        # The daily job keeps its own track.
        self.assertFalse(self.company.ov_tcmb_last_date)

    def test_import_stops_at_an_error(self):
        tcmb = FakeTcmb(archive={THURSDAY: make_bulletin(THURSDAY, 39.0), FRIDAY: requests.ConnectionError('reset')})
        wizard = self.env['ov.tcmb.rate.import'].create({
            'company_id': self.company.id,
            'date_from': THURSDAY,
            'date_to': BULLETIN_DAY,
        })
        with tcmb.serve():
            action = wizard.action_import()
        self.assertEqual(action['params']['type'], 'warning')
        self.assertTrue(action['params']['sticky'])
        self.assertIn('reset', action['params']['message'])
        self.assertEqual(self.stored_days(), [THURSDAY])

    def test_import_period(self):
        Import = self.env['ov.tcmb.rate.import']
        wizard = Import.create({'company_id': self.company.id, 'date_from': BULLETIN_DAY, 'date_to': THURSDAY})
        with self.assertRaises(UserError):
            wizard.action_import()
        wizard.date_from = BULLETIN_DAY - timedelta(days=MAX_IMPORT_DAYS)
        wizard.date_to = BULLETIN_DAY
        with self.assertRaises(UserError):
            wizard.action_import()
        # The future is not requested.
        today = fields.Date.context_today(wizard)
        wizard.date_from = today - timedelta(days=6)
        wizard.date_to = today + timedelta(days=10)
        tcmb = FakeTcmb()
        with tcmb.serve():
            action = wizard.action_import()
        self.assertEqual(tcmb.requested, [archive(day) for day in business_days(today - timedelta(days=6), today)])
        self.assertEqual(action['params']['type'], 'warning')

    def test_settings(self):
        branch = self.Company.create({'name': 'Kurgu Dış Ticaret Ankara Şubesi', 'parent_id': self.company.id})
        settings = self.env['res.config.settings'].with_company(branch).create({})
        self.assertTrue(settings.ov_tcmb_auto)
        # A branch changes the settings of its root company.
        settings.ov_tcmb_rate_type = 'forex_selling'
        settings.ov_tcmb_auto = False
        settings.execute()
        self.assertEqual(self.company.ov_tcmb_rate_type, 'forex_selling')
        self.assertFalse(self.company.ov_tcmb_auto)
        tcmb = FakeTcmb(latest=fixture_bulletin())
        with tcmb.serve():
            action = settings.ov_tcmb_action_update()
        self.assertEqual(action['params']['type'], 'success')
        self.assertIn('4', action['params']['message'])
        self.assertEqual(self.company.ov_tcmb_last_date, BULLETIN_DAY)
        self.assertAlmostEqual(1 / self.rates_of(BULLETIN_DAY)['USD'], 40.2)
        self.assertFalse(self.stored_days(branch))
        with FakeTcmb(latest=requests.ConnectionError('down')).serve(), self.assertRaises(UserError):
            settings.ov_tcmb_action_update()

    def test_views(self):
        arch = self.env['res.config.settings'].get_view(view_type='form')['arch']
        for name in ('ov_tcmb_auto', 'ov_tcmb_rate_type', 'ov_tcmb_last_date', 'ov_tcmb_action_update'):
            self.assertIn(f'name="{name}"', arch)
        arch = self.env['ov.tcmb.rate.import'].get_view(view_type='form')['arch']
        self.assertIn('name="action_import"', arch)
