from odoo import api, models

from odoo.addons.ov_brand.tools import BRAND_NAME_PARAM, get_brand_name


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    def _register_hook(self):
        super()._register_hook()
        # Give the code translations the product name of this database
        get_brand_name(self.env)

    @api.model_create_multi
    def create(self, vals_list):
        params = super().create(vals_list)
        if BRAND_NAME_PARAM in params.mapped('key'):
            self._ov_brand_changed()
        return params

    def write(self, vals):
        brand_name = BRAND_NAME_PARAM in self.mapped('key')
        result = super().write(vals)
        if brand_name or BRAND_NAME_PARAM in self.mapped('key'):
            self._ov_brand_changed()
        return result

    def unlink(self):
        brand_name = BRAND_NAME_PARAM in self.mapped('key')
        result = super().unlink()
        if brand_name:
            self._ov_brand_changed()
        return result

    @api.model
    def _ov_brand_changed(self):
        """Called when the product name changes. The views, templates and field
        labels are cached with the name in them; the parameters themselves
        clear the default cache, which holds the web client translations."""
        get_brand_name(self.env)
        for cache_name in ('templates', 'stable'):
            self.env.transaction.invalidate_ormcache(cache_name)
