from lxml import etree

from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestOvBrandPortal(TransactionCase):

    def test_record_sidebar(self):
        content = self.env['ir.qweb']._render('portal.portal_record_sidebar', {
            'classes': '',
            'title': 'Fictional Document',
            'entries': '',
        })
        self.assertIn('Fictional Document', content)
        self.assertNotIn('Powered by', content)
        self.assertNotIn('odoo.com', content)
        self.assertNotIn('/web/static/img/logo.png', content)

    def test_security_page(self):
        arch = self.env.ref('portal.portal_my_security')._get_combined_arch()
        self.assertNotIn('odoo.com', etree.tostring(arch, encoding='unicode'))
