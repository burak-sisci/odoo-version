from odoo import models

from odoo.addons.ov_brand.rebrand import rebrand_arch
from odoo.addons.ov_brand.tools import get_brand_name


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    def _get_combined_archs(self):
        """Rebrand the texts of the views and QWeb templates (T2.6): web client
        views, pages, reports and e-mail layouts all start from here."""
        archs = super()._get_combined_archs()
        # The editors save what they show: they get the views as they are
        if self.env.context.get('edit_translations') or self.env.context.get('inherit_branding'):
            return archs
        brand = get_brand_name(self.env)
        for arch in archs:
            rebrand_arch(arch, brand, self.env.lang)
        return archs
