from lxml import etree

from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestOvBrandAccount(TransactionCase):

    def test_invoice_qr_codes(self):
        arch = self.env.ref('account.report_invoice_document')._get_combined_arch()
        self.assertTrue(arch.xpath("//div[@id='qrcode']"))
        self.assertTrue(arch.xpath("//div[@id='payment_link_qrcode']"))
        self.assertFalse(arch.xpath("//img[@id='qrcode_odoo_logo']"))
        self.assertNotIn('Odoo_logo_O.svg', etree.tostring(arch, encoding='unicode'))

    def test_default_terms(self):
        content = self.env['ir.qweb']._render('account.account_default_terms_and_conditions', {
            'company_name': 'Fictional Company',
            'company_country': 'Fictional Country',
        })
        self.assertIn('only a suggestion', content)
        self.assertNotIn('Odoo', content)

    def test_einvoice_notification_logo(self):
        template = self.env.ref('account.mail_template_einvoice_notification')
        journal = self.env['account.journal'].search([('company_id', '=', self.env.company.id)], limit=1)
        if not journal:
            journal = self.env['account.journal'].create({'name': 'Fictional Journal', 'code': 'FIC', 'type': 'general'})
        body = template._render_field('body_html', journal.ids)[journal.id]
        self.assertIn('electronic invoice', body)
        self.assertNotIn('logo_inverse_white_206px', body)
