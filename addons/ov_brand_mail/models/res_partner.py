from odoo import api, models
from odoo.tools import BinaryBytes, file_open

from odoo.addons.ov_brand.tools import get_brand_name


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _ov_brand_update_bot(self):
        """Give the partner of the system user the product name and icon. It is
        the author of automatic messages and the chat bot; upstream names it
        after the publisher."""
        bot = self.env.ref('base.partner_root', raise_if_not_found=False)
        if not bot:
            return
        with file_open('ov_brand/static/img/icon_512.png', 'rb') as icon:
            image = BinaryBytes(icon.read())
        bot.sudo().write({'name': get_brand_name(self.env), 'image_1920': image})
