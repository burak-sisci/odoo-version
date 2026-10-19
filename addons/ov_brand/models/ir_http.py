from odoo import api, models

from odoo.addons.ov_brand.tools import get_brand_name, get_support_url


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        session_info = super().session_info()
        session_info['ov_brand_name'] = get_brand_name(self.env)
        # Odoo points the "Help" item to odoo.com
        session_info['support_url'] = get_support_url(self.env)
        return session_info

    @api.model
    def get_frontend_session_info(self):
        session_info = super().get_frontend_session_info()
        session_info['ov_brand_name'] = get_brand_name(self.env)
        return session_info
