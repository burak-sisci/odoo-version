from odoo import api, models

from odoo.addons.ov_l10n_tr.tools import TURKEY


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.depends('country_id', 'account_fiscal_country_id')
    def _compute_company_vat_placeholder(self):
        res = super()._compute_company_vat_placeholder()
        for company in self:
            if (company.country_id or company.account_fiscal_country_id).code == TURKEY:
                company.company_vat_placeholder = self.env._('2222222222 (VKN) or 11111111111 (TCKN)')
        return res
