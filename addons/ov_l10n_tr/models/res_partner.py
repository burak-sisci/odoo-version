import re

from odoo import api, models
from odoo.tools import LazyTranslate

from odoo.addons.ov_l10n_tr.tools import (
    CENTRAL_DISTRICT,
    TCKN,
    TURKEY,
    fold_name,
    mersis_validate,
    tax_id_type,
)

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

    def _prepare_display_address(self, without_name=False):
        address_format, args = super()._prepare_display_address(without_name)
        if self.country_id.code != TURKEY:
            return address_format, args
        # The form copies the district to the city text; an import or an API call may not.
        if not args['city'] and self.city_id:
            args['city'] = self.city_id.name
        # "Kadıköy/İstanbul": without the district or the province, no lone slash.
        if not (args['city'] and args['state_name']):
            address_format = address_format.replace('%(city)s/%(state_name)s', '%(city)s %(state_name)s')
        return address_format, args

    @api.model
    def _ov_l10n_tr_match_districts(self):
        """Link the Turkish partners typed before the district list to their district.

        A partner is linked when its city text names one district only:
        - a district of its province;
        - the province itself, for a province with a central district ("Merkez");
        - without a province, a district name used by one province only.
        Other partners keep their text. Return the number of linked partners.
        """
        Partner = self.with_context(active_test=False)
        partners = Partner.search([('country_id.code', '=', TURKEY), ('city_id', '=', False), ('city', '!=', False)])
        if not partners:
            return 0
        districts = self.env['res.city'].search([('country_id.code', '=', TURKEY)])
        by_province, by_name = {}, {}
        for district in districts:
            by_province[district.state_id.id, fold_name(district.name)] = district
            by_name.setdefault(fold_name(district.name), []).append(district)
        centres = {district.state_id.id: district for district in districts if district.name == CENTRAL_DISTRICT}
        linked = 0
        for partner in partners:
            name = fold_name(partner.city)
            if partner.state_id:
                district = by_province.get((partner.state_id.id, name))
                if not district and name == fold_name(partner.state_id.name):
                    district = centres.get(partner.state_id.id)
            else:
                candidates = by_name.get(name, [])
                district = candidates[0] if len(candidates) == 1 and candidates[0].name != CENTRAL_DISTRICT else None
            if district:
                partner.write({'city_id': district.id, 'city': district.name, 'state_id': district.state_id.id})
                linked += 1
        return linked
