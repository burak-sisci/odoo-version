from odoo import fields, models

from odoo.addons.ov_l10n_tr.tools import TURKEY


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _ov_l10n_tr_is_dispatch_note(self):
        """Whether the delivery slip of this transfer is a Turkish dispatch note (sevk irsaliyesi).

        Goods that leave a Turkish company travel with a dispatch note (Tax
        Procedure Law, art. 230/5).
        """
        self.ensure_one()
        return self.company_id.account_fiscal_country_id.code == TURKEY and self.picking_type_code == 'outgoing'

    def _ov_l10n_tr_issue_date(self):
        """Issue date of the dispatch note: the day the goods left, or today before that."""
        self.ensure_one()
        if self.date_done:
            return fields.Datetime.context_timestamp(self, self.date_done).date()
        return fields.Date.context_today(self)

    def _get_deliveryslip_report_title(self):
        if self._ov_l10n_tr_is_dispatch_note():
            return self.env._("Dispatch Note")
        return super()._get_deliveryslip_report_title()
