from odoo import api, models
from odoo.tools import frozendict

from odoo.addons.ov_brand.rebrand import rebrand
from odoo.addons.ov_brand.tools import get_brand_name

# Selections naming the publisher's licences
KEEP_SELECTIONS = {('ir.module.module', 'license')}


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    @api.model
    @api.ormcache('model_name', 'self.env.lang', cache='stable')
    def _get_fields_cached(self, model_name):
        """Rebrand the labels, help texts and selections of the fields (T2.6)."""
        result = super()._get_fields_cached(model_name)
        brand = get_brand_name(self.env)
        lang = self.env.lang
        rebranded = {}
        for field_name, values in result.items():
            new_values = dict(values)
            new_values['field_description'] = rebrand(values['field_description'], brand, lang)
            new_values['help'] = rebrand(values['help'], brand, lang)
            if 'selection' in values and (model_name, field_name) not in KEEP_SELECTIONS:
                new_values['selection'] = [(value, rebrand(name, brand, lang)) for value, name in values['selection']]
            if new_values != values:
                rebranded[field_name] = new_values
        return frozendict(result, **rebranded) if rebranded else result
