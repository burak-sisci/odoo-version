from datetime import timedelta

import requests

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools import format_date

from odoo.addons.ov_l10n_tr_tcmb.models.res_company import FETCH_ERRORS, business_days
from odoo.addons.ov_l10n_tr_tcmb.tools import fetch_bulletin

# One request per business day; TCMB answers in 0.35 s on average, up to a few
# seconds. Two months stay well within the time limit of a web request.
MAX_IMPORT_DAYS = 62


class OvTcmbRateImport(models.TransientModel):
    _name = 'ov.tcmb.rate.import'
    _description = 'Import TCMB Exchange Rates'

    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.company.root_id,
        domain=[('parent_id', '=', False)],
    )
    rate_type = fields.Selection(related='company_id.ov_tcmb_rate_type')
    date_from = fields.Date(
        string='From',
        required=True,
        default=lambda self: fields.Date.context_today(self) - timedelta(days=30),
    )
    date_to = fields.Date(string='To', required=True, default=fields.Date.context_today)

    def _notification(self, kind, message):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': kind,
                'message': message,
                'sticky': kind != 'success',
                'next': {'type': 'ir.actions.act_window_close'},
            },
        }

    def action_import(self):
        """Store the bulletins of the period; days without a bulletin are skipped."""
        self.ensure_one()
        date_to = min(self.date_to, fields.Date.context_today(self))
        if self.date_from > date_to:
            raise UserError(self.env._('The period must start before it ends, and not in the future.'))
        if (date_to - self.date_from).days >= MAX_IMPORT_DAYS:
            raise UserError(self.env._('Import at most %(days)s days at a time.', days=MAX_IMPORT_DAYS))
        bulletins = rates = 0
        with requests.Session() as session:
            for day in business_days(self.date_from, date_to):
                try:
                    bulletin = fetch_bulletin(day, session)
                except FETCH_ERRORS as error:
                    # Keep what was stored: the import can go on from this day.
                    return self._notification('warning', self.env._(
                        '%(bulletins)s TCMB bulletins stored (%(rates)s rates). '
                        'The bulletin of %(date)s could not be fetched: %(error)s. Import again from that day.',
                        bulletins=bulletins,
                        rates=rates,
                        date=format_date(self.env, day),
                        error=error,
                    ))
                if bulletin:
                    rates += self.company_id._ov_tcmb_apply(day, bulletin[1])
                    bulletins += 1
        if not bulletins:
            return self._notification('warning', self.env._('TCMB published no bulletin in this period.'))
        return self._notification('success', self.env._(
            '%(bulletins)s TCMB bulletins stored (%(rates)s rates).',
            bulletins=bulletins,
            rates=rates,
        ))
