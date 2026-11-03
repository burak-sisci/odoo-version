import re

from odoo import api, models
from odoo.tools import LazyTranslate

from odoo.addons.ov_l10n_tr.tools import TCKN, TURKEY, mersis_validate, tax_id_type

_lt = LazyTranslate(__name__)

# Labels and formats of the Turkish additional identifiers, over the generic ones.
TURKISH_IDENTIFIERS = {
    'TR_MERSIS': {
        'label': _lt('MERSIS Number'),
        'help': _lt('16-digit number of the Central Registry System (MERSIS).'),
        'placeholder': '1111111111111111',
        'validation_function': mersis_validate,
    },
    'TR_TICARET_SICIL': {
        'label': _lt('Trade Registry Number'),
    },
    'TR_SUBE': {
        'label': _lt('Branch Number'),
    },
}
# The name in the record label the VAT check builds: "partner [name]".
RECORD_NAME = re.compile(r'\[(.*)\]\s*$', re.DOTALL)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends('vat', 'country_id')
    def _compute_is_company(self):
        """A Turkish partner with a citizen number (TCKN) is a natural person.

        The generic rule makes every partner with a tax ID a company. In Turkey
        a person, a sole proprietor included, is taxed with their citizen
        number; e-documents describe them as a person, not as a party name.
        """
        res = super()._compute_is_company()
        for partner in self:
            if partner.is_company and partner.country_id.code == TURKEY and tax_id_type(partner.vat) == TCKN:
                partner.is_company = False
        return res

    def _ov_l10n_tr_tax_id_type(self):
        """Return VKN or TCKN for a Turkish commercial partner with a tax ID, '' otherwise."""
        self.ensure_one()
        partner = self.commercial_partner_id
        if partner.country_id.code != TURKEY or not partner.has_vat:
            return ''
        return tax_id_type(partner.vat)

    @api.depends('country_id')
    def _compute_partner_vat_placeholder(self):
        res = super()._compute_partner_vat_placeholder()
        for partner in self:
            if partner.country_id.code == TURKEY:
                partner.partner_vat_placeholder = self.env._('2222222222 (VKN) or 11111111111 (TCKN)')
        return res

    @api.model
    def _build_vat_error_message(self, country_code, wrong_vat, record_label):
        if (country_code or '').upper() != TURKEY:
            return super()._build_vat_error_message(country_code, wrong_vat, record_label)
        name = RECORD_NAME.search(record_label or '')
        if name and name.group(1) != 'False':
            return '\n' + self.env._(
                'The tax ID [%(wrong_vat)s] of %(name)s is not valid. A VKN has 10 digits and a TCKN 11 digits.',
                wrong_vat=wrong_vat,
                name=name.group(1),
            )
        return '\n' + self.env._(
            'The tax ID [%(wrong_vat)s] is not valid. A VKN has 10 digits and a TCKN 11 digits.',
            wrong_vat=wrong_vat,
        )

    @api.model
    def _get_all_additional_identifiers_metadata(self):
        metadata = super()._get_all_additional_identifiers_metadata()
        for key, values in TURKISH_IDENTIFIERS.items():
            if key in metadata:
                metadata[key] = {**metadata[key], **values}
        return metadata

    @api.model
    def _ov_l10n_tr_recompute_is_company(self):
        """Apply the person rule to the Turkish partners that existed before this module."""
        partners = self.with_context(active_test=False).search([('country_id.code', '=', TURKEY), ('vat', '!=', False)])
        self.env.add_to_compute(self._fields['is_company'], partners)
        partners.flush_recordset(['is_company'])
