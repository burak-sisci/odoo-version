from odoo import api, models

from odoo.addons.ov_brand.tools import BRAND_NAME_PARAM


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    @api.model_create_multi
    def create(self, vals_list):
        params = super().create(vals_list)
        if BRAND_NAME_PARAM in params.mapped('key'):
            self.env['res.partner']._ov_brand_update_bot()
        return params

    def write(self, vals):
        result = super().write(vals)
        if BRAND_NAME_PARAM in self.mapped('key'):
            self.env['res.partner']._ov_brand_update_bot()
        return result

    def unlink(self):
        brand_name = BRAND_NAME_PARAM in self.mapped('key')
        result = super().unlink()
        if brand_name:
            self.env['res.partner']._ov_brand_update_bot()
        return result
