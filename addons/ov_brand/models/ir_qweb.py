from odoo import models

from odoo.addons.ov_brand.tools import BRAND_COLOR, get_brand_name


class IrQweb(models.AbstractModel):
    _inherit = 'ir.qweb'

    def _prepare_environment(self, values):
        """Give every template the brand name and colour (``ov_brand_name``, ``ov_brand_color``)."""
        irqweb = super()._prepare_environment(values)
        if not irqweb.env.context.get('minimal_qcontext'):
            values.setdefault('ov_brand_name', get_brand_name(irqweb.env))
            values.setdefault('ov_brand_color', BRAND_COLOR)
        return irqweb
