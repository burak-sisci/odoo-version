from odoo import models

from odoo.addons.ov_brand.rebrand import rebrand
from odoo.addons.ov_brand.tools import get_brand_name


def rebrand_values(records, values_list, fnames):
    """Rebrand the texts ``fnames`` of the values read by ``_read_format``."""
    brand = get_brand_name(records.env)
    lang = records.env.lang
    for values in values_list:
        for fname in fnames:
            if isinstance(values.get(fname), str):
                values[fname] = rebrand(values[fname], brand, lang)
    return values_list


# Records with application texts naming the publisher's product: action
# names and help texts, group names and descriptions, module names (T2.6)

class IrActionsActions(models.Model):
    _inherit = 'ir.actions.actions'

    def _read_format(self, fnames, load='_classic_read'):
        values_list = super()._read_format(fnames, load)
        return rebrand_values(self, values_list, ('name', 'display_name', 'help'))


class ResGroups(models.Model):
    _inherit = 'res.groups'

    def _read_format(self, fnames, load='_classic_read'):
        values_list = super()._read_format(fnames, load)
        return rebrand_values(self, values_list, ('name', 'display_name', 'full_name', 'comment'))


class IrModuleCategory(models.Model):
    _inherit = 'ir.module.category'

    def _read_format(self, fnames, load='_classic_read'):
        values_list = super()._read_format(fnames, load)
        return rebrand_values(self, values_list, ('name', 'display_name', 'description'))
