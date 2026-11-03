from odoo.tests import HttpCase, tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged('post_install', '-at_install')
class TestTurkishPortalAddress(BaseCommon, HttpCase):
    """The address form of the portal (and of the shop, which uses it) with a Turkish address."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.turkey = cls.env.ref('base.tr')
        cls.istanbul = cls.env.ref('base.state_tr_34')
        cls.kadikoy = cls.env.ref('ov_l10n_tr.city_tr_34_kadikoy')
        cls.portal_user = cls._create_new_portal_user()
        cls.address = {
            'name': 'Örnek Kişi',
            'email': 'ornek@example.com',
            'phone': '+90 555 000 00 00',
            'street': 'Örnek Sokak No: 1',
            'country_id': cls.turkey.id,
            'state_id': cls.istanbul.id,
            'city_id': cls.kadikoy.id,
        }

    def _submit(self, **values):
        self.authenticate(self.portal_user.login, self.portal_user.login)
        return self.url_open('/my/address/submit', data={
            **self.address,
            'partner_id': self.portal_user.partner_id.id,
            'csrf_token': self.csrf_token(),
            **values,
        }).json()

    def test_country_info(self):
        info = self.make_jsonrpc_request(f'/my/address/country_info/{self.turkey.id}', {'address_type': 'billing'})
        self.assertEqual(info['address_fields'], ['street', 'street2', 'zip', 'city_id', 'state_id', 'country_id'])
        self.assertTrue({'street', 'city_id', 'state_id', 'country_id'} <= set(info['required_fields']))
        self.assertNotIn('zip', info['required_fields'])
        self.assertTrue(info['zip_before_city'])
        self.assertEqual(len(info['selection']['state_id']), 81)
        self.assertEqual(info['selection']['city_id'], [], 'the districts come with the province')
        self.assertEqual(info['vat_label'], 'VKN/TCKN')

    def test_districts_of_province(self):
        info = self.make_jsonrpc_request('/my/address/state_info/', {'country_id': self.turkey.id, 'state_id': self.istanbul.id})
        self.assertEqual(len(info['cities']), 39)
        self.assertEqual({city['state_id'] for city in info['cities']}, {self.istanbul.id})
        self.assertIn('Kadıköy', {city['name'] for city in info['cities']})

    def test_submit_turkish_address(self):
        result = self._submit()
        self.assertNotIn('invalid_fields', result, result)
        partner = self.portal_user.partner_id
        self.assertEqual((partner.city_id, partner.city, partner.state_id, partner.zip), (self.kadikoy, 'Kadıköy', self.istanbul, False))
        self.assertEqual(partner._display_address(without_name=True), f'Örnek Sokak No: 1\nKadıköy/İstanbul\n{self.turkey.name}')

    def test_submit_requires_district_and_province(self):
        self.assertIn('city_id', self._submit(city_id='')['invalid_fields'])
        self.assertIn('state_id', self._submit(state_id='')['invalid_fields'])
