from stdnum.tr import tckimlik, vkn

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged

from odoo.addons.ov_l10n_tr.tools import mersis_validate, tax_id_type

# Fictional numbers: a made-up base with the check digits of the official algorithm.
TCKN = '100000001' + tckimlik.calc_check_digits('100000001')
VKN = '100000001' + vkn.calc_check_digit('100000001')
# A company MERSIS number has the shape 0 + tax number + 5 digits.
MERSIS = f'0{VKN}00015'


@tagged('post_install', '-at_install')
class TestPartnerIdentifiers(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env['res.lang']._activate_lang('tr_TR')
        cls.turkey = cls.env.ref('base.tr')
        cls.Partner = cls.env['res.partner']

    def _partner(self, vat, **values):
        return self.Partner.create({'name': 'Örnek', 'country_id': self.turkey.id, 'vat': vat, **values})

    def test_fictional_numbers_are_valid(self):
        self.assertTrue(tckimlik.is_valid(TCKN))
        self.assertTrue(vkn.is_valid(VKN))

    def test_tax_id_type(self):
        self.assertEqual(tax_id_type(VKN), 'VKN')
        self.assertEqual(tax_id_type(TCKN), 'TCKN')
        self.assertEqual(tax_id_type(f'{VKN[:5]} {VKN[5:]}'), 'VKN')
        self.assertEqual(tax_id_type(''), '')
        self.assertEqual(tax_id_type('12345'), '')

    def test_person_with_citizen_number(self):
        """A partner with a TCKN is a natural person (the generic rule made it a company)."""
        person = self._partner(TCKN)
        self.assertFalse(person.is_company)
        self.assertEqual(person._ov_l10n_tr_tax_id_type(), 'TCKN')
        contact = self.Partner.create({'name': 'Muhasebe', 'parent_id': person.id, 'type': 'invoice'})
        self.assertEqual(contact.commercial_partner_id, person)
        self.assertEqual(contact._ov_l10n_tr_tax_id_type(), 'TCKN')

    def test_company_with_tax_number(self):
        company = self._partner(VKN)
        self.assertTrue(company.is_company)
        self.assertEqual(company._ov_l10n_tr_tax_id_type(), 'VKN')

    def test_rule_is_turkish_only(self):
        """An 11-digit tax ID of another country keeps the generic rule."""
        foreign = self.Partner.with_context(no_vat_validation=True).create({
            'name': 'Foreign', 'country_id': self.env.ref('base.it').id, 'vat': '12345678901',
        })
        self.assertTrue(foreign.is_company)
        self.assertEqual(foreign._ov_l10n_tr_tax_id_type(), '')

    def test_changing_the_number_changes_the_type(self):
        partner = self._partner(VKN)
        partner.vat = TCKN
        self.assertFalse(partner.is_company)
        partner.vat = VKN
        self.assertTrue(partner.is_company)

    def test_existing_partners_are_recomputed(self):
        person = self._partner(TCKN)
        self.env.flush_all()
        self.env.cr.execute('UPDATE res_partner SET is_company = TRUE WHERE id = %s', [person.id])
        self.env.invalidate_all()
        self.assertTrue(person.is_company)
        self.Partner._ov_l10n_tr_recompute_is_company()
        self.env.invalidate_all()
        self.assertFalse(person.is_company)

    def test_turkish_labels(self):
        self.assertEqual(self.turkey.vat_label, 'VKN/TCKN')
        person = self._partner(TCKN).with_context(lang='tr_TR')
        self.assertEqual(person.partner_vat_placeholder, '2222222222 (VKN) veya 11111111111 (TCKN)')
        company = self.env['res.company'].create({'name': 'Örnek Şirket', 'country_id': self.turkey.id})
        self.assertEqual(company.with_context(lang='tr_TR').company_vat_placeholder, '2222222222 (VKN) veya 11111111111 (TCKN)')
        labels = {
            key: metadata['label']
            for key, metadata in person.available_additional_identifiers_metadata.items()
            if key in ('TR_MERSIS', 'TR_TICARET_SICIL', 'TR_SUBE')
        }
        self.assertEqual(labels, {'TR_MERSIS': 'MERSİS No', 'TR_TICARET_SICIL': 'Ticaret Sicil No', 'TR_SUBE': 'Şube No'})

    def test_invalid_tax_id_message(self):
        wrong = TCKN[:-1] + str((int(TCKN[-1]) + 1) % 10)
        Partner = self.Partner.with_context(lang='tr_TR')
        with self.assertRaises(ValidationError) as caught:
            Partner.create({'name': 'Ayşe Örnek', 'country_id': self.turkey.id, 'vat': wrong})
        message = str(caught.exception)
        self.assertIn(f'Ayşe Örnek için girilen VKN/TCKN [{wrong}] geçerli değil.', message)
        self.assertNotIn('NIN', message)
        self.assertNotIn('does not seem', message)

    def test_mersis_number(self):
        self.assertEqual(mersis_validate(f'{MERSIS[:4]} {MERSIS[4:8]}-{MERSIS[8:12]} {MERSIS[12:]}'), MERSIS)
        partner = self._partner(VKN, additional_identifiers={'TR_MERSIS': f' {MERSIS[:8]} {MERSIS[8:]} '})
        self.assertEqual(partner.additional_identifiers['TR_MERSIS'], MERSIS)
        for wrong in ('12AB', MERSIS[:-1], MERSIS + '1', MERSIS[:-1] + 'X'):
            with self.subTest(wrong=wrong), self.assertRaises(ValidationError):
                self._partner(VKN, additional_identifiers={'TR_MERSIS': wrong})
