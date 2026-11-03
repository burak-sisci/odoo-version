from odoo import api, models


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    @api.model
    def _ov_brand_changed(self):
        result = super()._ov_brand_changed()
        self.env['res.partner']._ov_brand_update_bot()
        return result
