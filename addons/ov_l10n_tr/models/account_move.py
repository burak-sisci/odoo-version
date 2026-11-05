from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_document_partner_ident_line(self):
        """Name the Turkish tax ID of the customer: 'VKN: …' or 'TCKN: …'."""
        partner = self.partner_id.commercial_partner_id
        kind = partner and partner._ov_l10n_tr_tax_id_type()
        if kind:
            return f"{kind}: {partner.vat}"
        return super()._get_document_partner_ident_line()
