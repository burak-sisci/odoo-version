from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools import format_date

from odoo.addons.ov_l10n_tr_tcmb.models.res_company import FETCH_ERRORS


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Rates live on the root company; a branch shows and changes the settings of its root.
    ov_tcmb_auto = fields.Boolean(related='company_id.root_id.ov_tcmb_auto', readonly=False)
    ov_tcmb_rate_type = fields.Selection(related='company_id.root_id.ov_tcmb_rate_type', readonly=False)
    ov_tcmb_last_date = fields.Date(related='company_id.root_id.ov_tcmb_last_date')

    def ov_tcmb_action_update(self):
        self.ensure_one()
        try:
            day, count = self.company_id.root_id._ov_tcmb_update()
        except FETCH_ERRORS as error:
            raise UserError(self.env._('The TCMB exchange rates could not be fetched: %s', error)) from error
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'message': self.env._(
                    'TCMB bulletin of %(date)s: %(count)s exchange rates stored.',
                    date=format_date(self.env, day),
                    count=count,
                ),
                'next': {'type': 'ir.actions.client', 'tag': 'soft_reload'},
            },
        }
