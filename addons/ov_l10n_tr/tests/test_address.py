from collections import Counter

from lxml import etree

from odoo.tests import Form, TransactionCase, tagged
from odoo.tools.safe_eval import safe_eval

from odoo.addons.ov_l10n_tr.tools import fold_name

# Official inventory of the Ministry of the Interior: 922 listed districts and
# the central district ("Merkez") of the 51 provinces without a metropolitan municipality.
DISTRICT_COUNT = 973
CENTRAL_DISTRICT_COUNT = 51
PROVINCE_DISTRICT_COUNTS = {'state_tr_34': 39, 'state_tr_06': 25, 'state_tr_35': 30, 'state_tr_14': 9}


def turkish_lower(text):
    return text.replace('I', 'ı').replace('İ', 'i').lower()


@tagged('post_install', '-at_install')
class TestTurkishAddress(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env['res.lang']._activate_lang('tr_TR')
        cls.turkey = cls.env.ref('base.tr')
        cls.City = cls.env['res.city']
        cls.Partner = cls.env['res.partner']
        cls.istanbul = cls.env.ref('base.state_tr_34')
        cls.ankara = cls.env.ref('base.state_tr_06')
        cls.konya = cls.env.ref('base.state_tr_42')
        cls.bolu = cls.env.ref('base.state_tr_14')
        cls.kadikoy = cls.env.ref('ov_l10n_tr.city_tr_34_kadikoy')

    def _partner(self, **values):
        return self.Partner.create({'name': 'Örnek Ltd.', 'country_id': self.turkey.id, **values})

    # District list

    def test_district_list(self):
        districts = self.City.search([('country_id', '=', self.turkey.id)])
        self.assertEqual(len(districts), DISTRICT_COUNT)
        self.assertEqual(districts.state_id, self.turkey.state_ids, 'every province has its districts, all of Turkey')
        self.assertEqual(len(self.turkey.state_ids), 81)
        for xml_id, count in PROVINCE_DISTRICT_COUNTS.items():
            state = self.env.ref(f'base.{xml_id}')
            self.assertEqual(len(districts.filtered(lambda d, s=state: d.state_id == s)), count, state.name)
        centres = districts.filtered(lambda d: d.name == 'Merkez')
        self.assertEqual(len(centres), CENTRAL_DISTRICT_COUNT)
        self.assertNotIn(self.istanbul, centres.state_id, 'a metropolitan province has no central district')
        self.assertIn(self.bolu, centres.state_id)
        duplicates = [key for key, n in Counter((d.state_id.id, d.name) for d in districts).items() if n > 1]
        self.assertFalse(duplicates, 'a district name appears once in its province')

    def test_district_names(self):
        """Names are written as in Turkish: 'Karaisalı', '19 Mayıs', not 'KARAİSALI' or 'Karai̇sali'."""
        self.assertEqual(self.kadikoy.name, 'Kadıköy')
        self.assertEqual(self.kadikoy.state_id, self.istanbul)
        self.assertEqual(self.env.ref('ov_l10n_tr.city_tr_01_karaisali').name, 'Karaisalı')
        self.assertEqual(self.env.ref('ov_l10n_tr.city_tr_55_19_mayis').name, '19 Mayıs')
        badly_written = []
        for district in self.City.search([('country_id', '=', self.turkey.id)]):
            for word in district.name.split(' '):
                if not word or word[1:] != turkish_lower(word[1:]) or not (word[0].isdigit() or word[0].isupper()):
                    badly_written.append(district.name)
        self.assertFalse(badly_written)

    def test_fold_name(self):
        self.assertEqual(fold_name(' KADIKÖY '), fold_name('Kadıköy'))
        self.assertEqual(fold_name('İZMİR'), 'izmir')
        self.assertEqual(fold_name('ISPARTA'), 'ısparta')
        self.assertEqual(fold_name('Balâ'), fold_name('Bala'))
        self.assertEqual(fold_name('19   MAYIS'), '19 mayıs')
        self.assertEqual(fold_name(False), '')

    # Country settings

    def test_country_settings(self):
        self.assertTrue(self.turkey.enforce_cities)
        self.assertTrue(self.turkey.state_required)
        self.assertEqual(self.turkey.zip_applicability, 'optional')
        self.assertEqual(self.turkey.vat_label, 'VKN/TCKN')
        self.turkey.write({'enforce_cities': False, 'state_required': False})
        self.env['res.country']._ov_l10n_tr_setup()
        self.assertTrue(self.turkey.enforce_cities)
        self.assertTrue(self.turkey.state_required)

    def test_display_address(self):
        partner = self._partner(street='Örnek Sokak No: 1', zip='34710', city='Kadıköy', city_id=self.kadikoy.id, state_id=self.istanbul.id)
        self.assertEqual(partner._display_address(), f'Örnek Sokak No: 1\n34710 Kadıköy/İstanbul\n{self.turkey.name}')
        # District chosen but not copied to the city text (import, API).
        partner.city = False
        self.assertEqual(partner._display_address(), f'Örnek Sokak No: 1\n34710 Kadıköy/İstanbul\n{self.turkey.name}')
        # No lone slash without the district or the province.
        partner.write({'city_id': False, 'city': False})
        self.assertEqual(partner._display_address(), f'Örnek Sokak No: 1\n34710 İstanbul\n{self.turkey.name}')
        partner.write({'city': 'Kadıköy', 'state_id': False, 'zip': False})
        self.assertEqual(partner._display_address(), f'Örnek Sokak No: 1\nKadıköy\n{self.turkey.name}')

    def test_display_address_other_country(self):
        italy = self.env.ref('base.it')
        partner = self.Partner.create({'name': 'Esempio', 'country_id': italy.id, 'city': 'Roma', 'zip': '00100'})
        address_format, __ = partner._prepare_display_address()
        self.assertEqual(address_format, partner._get_address_format())

    # Forms

    def test_form_district_sets_province(self):
        with Form(self.Partner) as form:
            form.name = 'Örnek Ltd.'
            form.country_id = self.turkey
            form.city_id = self.kadikoy
            self.assertEqual(form.state_id, self.istanbul)
            self.assertEqual(form.city, 'Kadıköy')
        partner = form.record
        self.assertEqual((partner.city_id, partner.city, partner.state_id), (self.kadikoy, 'Kadıköy', self.istanbul))

    def test_district_choice_limited_to_province(self):
        """The district fields of the contact form list the districts of the chosen province."""
        arch = etree.fromstring(self.Partner.get_views([(False, 'form')])['views']['form']['arch'])
        fields = arch.xpath("//field[@name='city_id']")
        self.assertEqual(len(fields), 2, 'the contact and the contacts of the contact')
        tr_ereglis = self.City.search([('country_id', '=', self.turkey.id), ('name', '=', 'Ereğli')])
        self.assertEqual(len(tr_ereglis), 2, 'Ereğli of Konya and of Zonguldak')
        for field in fields:
            domain = field.get('domain')
            in_konya = safe_eval(domain, {'country_id': self.turkey.id, 'country_code': 'TR', 'state_id': self.konya.id})
            self.assertEqual(self.City.search(in_konya + [('name', '=', 'Ereğli')]).state_id, self.konya)
            no_province = safe_eval(domain, {'country_id': self.turkey.id, 'country_code': 'TR', 'state_id': False})
            self.assertEqual(self.City.search(no_province + [('name', '=', 'Ereğli')]), tr_ereglis)
            other_country = safe_eval(domain, {'country_id': self.turkey.id, 'country_code': 'DE', 'state_id': self.konya.id})
            self.assertEqual(self.City.search(other_country + [('name', '=', 'Ereğli')]), tr_ereglis, 'only Turkey filters by province')

    # Portal and shop address forms

    def test_portal_address_fields(self):
        self.assertTrue(self.turkey._enforce_city_choice())
        self.assertEqual(self.turkey._get_partner_city_field(), 'city_id')
        self.assertEqual(self.turkey._get_address_fields(), ['street', 'street2', 'zip', 'city_id', 'state_id', 'country_id'])
        self.assertTrue(self.turkey._is_zip_before_city())
        cities = self.turkey._get_cities_data(self.istanbul.id)
        self.assertEqual(len(cities), PROVINCE_DISTRICT_COUNTS['state_tr_34'])
        self.assertEqual({city['state_id'] for city in cities}, {self.istanbul.id})

    def test_portal_rule_is_turkish_only(self):
        germany = self.env.ref('base.de')
        germany.enforce_cities = True
        self.City.create({'name': 'Berlin', 'country_id': germany.id})
        self.assertFalse(germany._enforce_city_choice())

    # Partners typed before the district list

    def test_match_districts(self):
        italy = self.env.ref('base.it')
        linked = {
            'lower case, province given': (self._partner(city='kadıköy', state_id=self.istanbul.id), self.kadikoy),
            'upper case, no province': (self._partner(city='KARAİSALI '), self.env.ref('ov_l10n_tr.city_tr_01_karaisali')),
            'province as city': (self._partner(city='BOLU', state_id=self.bolu.id), self.env.ref('ov_l10n_tr.city_tr_14_merkez')),
            'circumflex': (self._partner(city='Balâ', state_id=self.ankara.id), self.env.ref('ov_l10n_tr.city_tr_06_bala')),
            'archived': (self._partner(city='Kadıköy', state_id=self.istanbul.id, active=False), self.kadikoy),
        }
        unchanged = {
            'two provinces': self._partner(city='Ereğli'),
            'central district without province': self._partner(city='Merkez'),
            'district of another province': self._partner(city='Kadıköy', state_id=self.ankara.id),
            'metropolitan province as city': self._partner(city='İstanbul', state_id=self.istanbul.id),
            'unknown': self._partner(city='Yokköy', state_id=self.istanbul.id),
            'other country': self.Partner.create({'name': 'Esempio', 'country_id': italy.id, 'city': 'Kadıköy'}),
        }
        texts = {case: partner.city for case, partner in unchanged.items()}
        self.assertGreaterEqual(self.Partner._ov_l10n_tr_match_districts(), len(linked))
        for case, (partner, district) in linked.items():
            self.assertEqual(
                (partner.city_id, partner.city, partner.state_id),
                (district, district.name, district.state_id),
                case,
            )
        for case, partner in unchanged.items():
            self.assertFalse(partner.city_id, case)
            self.assertEqual(partner.city, texts[case], case)
        self.assertFalse(unchanged['two provinces'].state_id)
        self.assertEqual(self.Partner._ov_l10n_tr_match_districts(), 0, 'nothing left to link')
