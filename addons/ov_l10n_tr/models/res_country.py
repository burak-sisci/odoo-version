from odoo import api, models

from odoo.addons.ov_l10n_tr.tools import TURKEY

# Address settings of Turkey. The country is a no-update record of base: they
# are written by the install hook and the migrations, not by a data file.
TURKEY_VALUES = {
    'vat_label': 'VKN/TCKN',
    # The district (ilçe) is chosen from the list of the province (il).
    'enforce_cities': True,
    'state_required': True,
    # Postal codes exist but are not used by everyone; e-documents do not require them.
    'zip_applicability': 'optional',
    # "34710 Kadıköy/İstanbul", the order of the national postal service.
    'address_format': '%(street)s\n%(street2)s\n%(zip)s %(city)s/%(state_name)s\n%(country_name)s',
}


class ResCountry(models.Model):
    _inherit = 'res.country'

    def _enforce_city_choice(self):
        # The address forms of the portal and the shop list the districts of
        # the chosen province; upstream enables this for a few countries only.
        if self and self.code == TURKEY:
            return self.enforce_cities and bool(self.env['res.city'].search_count([('country_id', '=', self.id)], limit=1))
        return super()._enforce_city_choice()

    @api.model
    def _ov_l10n_tr_setup(self):
        """Write the Turkish address and tax ID settings on the country."""
        self.env.ref('base.tr').write(TURKEY_VALUES)
