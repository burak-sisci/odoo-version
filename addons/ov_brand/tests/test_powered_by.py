from lxml import html

from odoo.tests import TransactionCase, tagged

from odoo.addons.ov_brand.tools import (
    BRAND_NAME_PARAM,
    DEFAULT_BRAND_NAME,
    POWERED_BY_PARAM,
    show_powered_by,
)


def powered_by_lines(content):
    """Return the text of the elements holding "Powered by", spaces normalized."""
    if not content.strip():
        return []
    tree = html.fromstring(f'<div>{content}</div>')
    return [
        ' '.join(node.text_content().split())
        for node in tree.xpath("//*[text()[contains(., 'Powered by') or contains(., 'Altyapı:')]]")
    ]


@tagged('post_install', '-at_install')
class TestPoweredBy(TransactionCase):
    """"Powered by" and the product name under the e-mails and portal pages (K17)."""

    def render(self, template='ov_brand.powered_by', lang=None, **options):
        qweb = self.env['ir.qweb'].with_context(lang=lang) if lang else self.env['ir.qweb']
        return str(qweb._render(template, {}, **options))

    def test_powered_by(self):
        expected = [f'Powered by {DEFAULT_BRAND_NAME}']
        self.assertEqual(powered_by_lines(self.render()), expected)
        # E-mails are rendered with the minimal context
        self.assertEqual(powered_by_lines(self.render(minimal_qcontext=True)), expected)
        # Without a link
        self.assertNotIn('<a', self.render())

    def test_brand_name(self):
        self.env['ir.config_parameter'].sudo().set_str(BRAND_NAME_PARAM, 'Fictional <b>ERP</b>')
        content = self.render()
        self.assertIn('Powered by Fictional &lt;b&gt;ERP&lt;/b&gt;', content)
        self.assertNotIn('<b>', content)

    def test_portal_footer(self):
        content = self.render('web.brand_promotion')
        self.assertEqual(powered_by_lines(content), [f'Powered by {DEFAULT_BRAND_NAME}'])
        self.assertNotIn('<a', content)

    def test_setting(self):
        settings = self.env['res.config.settings'].create({})
        # Shown by default, also without the parameter
        self.assertTrue(settings.ov_powered_by)
        self.assertTrue(show_powered_by(self.env))
        settings.ov_powered_by = False
        settings.execute()
        self.assertEqual(self.env['ir.config_parameter'].sudo().get_str(POWERED_BY_PARAM), 'False')
        self.assertFalse(self.env['res.config.settings'].create({}).ov_powered_by)
        self.assertEqual(powered_by_lines(self.render()), [])
        self.assertEqual(powered_by_lines(self.render('web.brand_promotion')), [])
        settings = self.env['res.config.settings'].create({'ov_powered_by': True})
        settings.execute()
        self.assertEqual(powered_by_lines(self.render()), [f'Powered by {DEFAULT_BRAND_NAME}'])

    def test_settings_view(self):
        arch = self.env['res.config.settings'].get_view(view_type='form')['arch']
        self.assertIn('name="ov_powered_by"', arch)

    def test_turkish(self):
        # The name comes first in Turkish; upstream translates "Powered by" alone
        self.env['res.lang']._activate_lang('tr_TR')
        self.env['ir.module.module']._load_module_terms(['ov_brand'], ['tr_TR'], overwrite=True)
        expected = [f'Altyapı: {DEFAULT_BRAND_NAME}']
        self.assertEqual(powered_by_lines(self.render(lang='tr_TR')), expected)
        self.assertEqual(powered_by_lines(self.render('web.brand_promotion', lang='tr_TR')), expected)
