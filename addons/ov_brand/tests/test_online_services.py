from lxml import etree

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged

from odoo.addons.ov_brand.tools import ONLINE_SERVICE_MODULES


@tagged('post_install', '-at_install')
class TestOvBrandOnlineServices(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Module = cls.env['ir.module.module']
        cls.online = cls.Module.search([('name', 'in', ONLINE_SERVICE_MODULES)])

    def test_online_services_removed(self):
        # Both come with every new database; ov_brand removed them
        self.assertEqual(sorted(self.online.mapped('name')), sorted(ONLINE_SERVICE_MODULES))
        self.assertEqual(set(self.online.mapped('state')), {'uninstalled'})
        self.assertFalse(self.online.downstream_dependencies(exclude_states=('uninstalled', 'uninstallable')))

    def test_install_online_service_refused(self):
        sms = self.env.ref('base.module_sms')
        with self.assertRaises(UserError):
            sms.button_install()

    def test_install_other_module(self):
        # Installing a module that only optionally works with the online
        # services does not bring them back
        crm = self.env.ref('base.module_crm')
        crm.button_install()
        self.assertEqual(crm.state, 'to install')
        self.assertEqual(set(self.online.mapped('state')), {'uninstalled'})

    def test_settings_hidden(self):
        arch = etree.fromstring(self.env['res.config.settings'].get_view(view_type='form')['arch'])
        fields = set(arch.xpath('//field/@name'))
        self.assertNotIn('module_sms', fields)
        self.assertNotIn('module_partner_autocomplete', fields)
        self.assertIn('module_auth_oauth', fields)
        # The block holding only these two settings is gone with them
        self.assertFalse(arch.xpath("//block[@name='contacts_setting_container']"))
