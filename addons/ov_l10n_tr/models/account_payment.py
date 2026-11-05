from odoo import api, models

from odoo.addons.ov_l10n_tr.tools import TURKEY


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.depends('payment_type', 'partner_type', 'company_id')
    def _compute_payment_receipt_title(self):
        """Turkish bookkeeping names the voucher after the cash flow.

        Money received gets a collection receipt (tahsilat makbuzu), money
        paid a payment voucher (tediye makbuzu), whoever the partner is.
        """
        res = super()._compute_payment_receipt_title()
        for payment in self:
            if payment.company_id.account_fiscal_country_id.code != TURKEY:
                continue
            if payment.payment_type == 'inbound':
                payment.payment_receipt_title = self.env._("Collection Receipt")
            else:
                payment.payment_receipt_title = self.env._("Payment Voucher")
        return res
