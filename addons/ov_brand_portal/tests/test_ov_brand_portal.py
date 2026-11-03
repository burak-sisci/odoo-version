from lxml import etree

from odoo.tests import TransactionCase, tagged

from odoo.addons.ov_brand.tests.test_powered_by import powered_by_lines
from odoo.addons.ov_brand.tools import DEFAULT_BRAND_NAME, POWERED_BY_PARAM


@tagged('post_install', '-at_install')
class TestOvBrandPortal(TransactionCase):

    def _render_sidebar(self):
        content = str(self.env['ir.qweb']._render('portal.portal_record_sidebar', {
            'classes': '',
            'title': 'Fictional Document',
            'entries': '',
        }))
        self.assertIn('Fictional Document', content)
        self.assertNotIn('odoo.com', content)
        self.assertNotIn('/web/static/img/logo.png', content)
        return content

    def test_record_sidebar(self):
        # "Powered by" and the product name, without a link (K17)
        content = self._render_sidebar()
        self.assertEqual(powered_by_lines(content), [f'Powered by {DEFAULT_BRAND_NAME}'])
        self.assertNotIn('<a', content)
        # Hidden in the settings
        self.env['ir.config_parameter'].sudo().set_bool(POWERED_BY_PARAM, False)
        content = self._render_sidebar()
        self.assertNotIn('Powered by', content)
        self.assertNotIn(DEFAULT_BRAND_NAME, content)

    def test_security_page(self):
        arch = self.env.ref('portal.portal_my_security')._get_combined_arch()
        self.assertNotIn('odoo.com', etree.tostring(arch, encoding='unicode'))
