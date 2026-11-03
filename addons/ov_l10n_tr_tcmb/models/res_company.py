import logging
from datetime import timedelta

import requests

from odoo import api, fields, models

from odoo.addons.ov_l10n_tr.tools import TURKEY
from odoo.addons.ov_l10n_tr_tcmb.tools import (
    TRY,
    BulletinError,
    company_rates,
    fetch_bulletin,
)

_logger = logging.getLogger(__name__)

ONE_DAY = timedelta(days=1)
# Missed bulletins the daily job fetches back; older gaps go through the import wizard.
CATCH_UP_DAYS = 31
RETRY_DELAY = timedelta(hours=1)
FETCH_ERRORS = (requests.RequestException, BulletinError)
RATE_TYPES = [
    ('forex_buying', 'Forex Buying'),
    ('forex_selling', 'Forex Selling'),
    ('banknote_buying', 'Banknote Buying'),
    ('banknote_selling', 'Banknote Selling'),
]


def business_days(start, end):
    """Days from start to end (both included) on which TCMB may publish a bulletin."""
    day = start
    while day <= end:
        if day.weekday() < 5:
            yield day
        day += ONE_DAY


class ResCompany(models.Model):
    _inherit = 'res.company'

    ov_tcmb_auto = fields.Boolean(
        string='Daily TCMB Rates',
        compute='_compute_ov_tcmb_auto',
        store=True,
        readonly=False,
        help='Fetch the exchange rates of the Central Bank of the Republic of Türkiye (TCMB) every business day.',
    )
    ov_tcmb_rate_type = fields.Selection(
        selection=RATE_TYPES,
        string='TCMB Rate Type',
        required=True,
        default='forex_buying',
        help='Rate of the TCMB bulletin stored as the exchange rate. '
        'Where TCMB gives no banknote rate, the forex rate of the same side is used.',
    )
    ov_tcmb_last_date = fields.Date(string='Last TCMB Bulletin', readonly=True, copy=False)

    @api.depends('country_id')
    def _compute_ov_tcmb_auto(self):
        for company in self:
            company.ov_tcmb_auto = company.country_id.code == TURKEY

    def _ov_tcmb_apply(self, day, currencies):
        """Store the rates of a bulletin as the rates dated `day` of these root companies.

        A rate applies from the day after its date: the bulletin of a day,
        published in the afternoon, gives the rates of the next business day,
        as is the practice in Türkiye. Only active currencies get a rate; a
        rate already stored for the day is replaced. Return the number of rates.
        """
        Rate = self.env['res.currency.rate']
        active = {
            currency.name: currency
            for currency in self.env['res.currency'].search([('name', 'in', [*currencies, TRY])])
        }
        count = 0
        for company in self:
            rates = company_rates(currencies, company.currency_id.name, active, company.ov_tcmb_rate_type)
            if not rates:
                continue
            stored = {
                rate.currency_id.name: rate
                for rate in Rate.search([
                    ('company_id', '=', company.id),
                    ('name', '=', day),
                    ('currency_id', 'in', [active[code].id for code in rates]),
                ])
            }
            for code, value in rates.items():
                if code in stored and stored[code].rate != value:
                    stored[code].rate = value
            Rate.create([
                {'name': day, 'rate': value, 'currency_id': active[code].id, 'company_id': company.id}
                for code, value in rates.items()
                if code not in stored
            ])
            count += len(rates)
        return count

    def _ov_tcmb_update(self):
        """Store the latest bulletin and the ones missed since the last update.

        Return (date of the latest bulletin, number of rates stored). Raise the
        fetch errors; what was stored before an error stays, and the next
        update goes on from the day that failed.
        """
        count = 0
        fetched = {}
        with requests.Session() as session:
            latest_day, latest = fetch_bulletin(session=session)
            for company in self:
                last = company.ov_tcmb_last_date
                if last and last >= latest_day:
                    continue
                start = max(last + ONE_DAY, latest_day - timedelta(days=CATCH_UP_DAYS)) if last else latest_day
                for day in business_days(start, latest_day - ONE_DAY):
                    if day not in fetched:
                        fetched[day] = fetch_bulletin(day, session)
                    if fetched[day]:
                        count += company._ov_tcmb_apply(day, fetched[day][1])
                    company.ov_tcmb_last_date = day
                count += company._ov_tcmb_apply(latest_day, latest)
                company.ov_tcmb_last_date = latest_day
        return latest_day, count

    @api.model
    def _ov_tcmb_cron(self):
        """Daily job: update the root companies that fetch TCMB rates and use another currency.

        A system job: every company of the database, whatever the companies of the job's user.
        """
        Currency = self.env['res.currency']
        companies = self.sudo().search([('parent_id', '=', False), ('ov_tcmb_auto', '=', True)])
        companies = companies.filtered(
            lambda company: Currency.search_count([('id', '!=', company.currency_id.id)], limit=1),
        )
        if not companies:
            return
        try:
            day, count = companies._ov_tcmb_update()
        except FETCH_ERRORS as error:
            _logger.warning('TCMB exchange rates could not be fetched, next try in an hour: %s', error)
            self.env.ref('ov_l10n_tr_tcmb.ir_cron_tcmb_rates')._trigger(fields.Datetime.now() + RETRY_DELAY)
            return
        _logger.info('TCMB bulletin of %s: %s rates stored', day, count)
