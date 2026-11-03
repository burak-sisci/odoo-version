from lxml import etree
from markupsafe import Markup

from odoo.tests import BaseCase, TransactionCase, tagged
from odoo.tools import translate

from odoo.addons.ov_brand.rebrand import (
    adapt_tr_suffix,
    rebrand,
    rebrand_arch,
    rebrand_html,
)
from odoo.addons.ov_brand.tools import BRAND_NAME_PARAM, DEFAULT_BRAND_NAME


@tagged('post_install', '-at_install')
class TestRebrandText(BaseCase):

    def test_name(self):
        self.assertEqual(rebrand("Welcome to Odoo!", 'Nexus'), "Welcome to Nexus!")
        self.assertEqual(rebrand("managed by Odoo.", 'Nexus'), "managed by Nexus.")
        self.assertEqual(rebrand("Ask @OdooBot", 'Nexus'), "Ask @Nexus")
        self.assertEqual(rebrand("Odoobot Failed", 'Nexus'), "Nexus Failed")
        self.assertEqual(rebrand("Odoo's Discuss", 'Nexus', 'en_US'), "Nexus's Discuss")

    def test_kept_names(self):
        for text in ("Odoo S.A.", "Odoo SA", "Odoo Enterprise", "Odoo Kurumsal Sürüm", "Odoo Studio",
                     "Odoo.sh", "Odoo Online", "Odoo 18 or higher", "Odoo for Gmail", "Odoo for Outlook"):
            self.assertEqual(rebrand(text, 'Nexus'), text)

    def test_technical_names(self):
        for text in ("/odoo/action-1", "my.Odoo", "OdooEditor", "ODOO.LIST(1)", "odoo-bin",
                     "https://www.odoo.com/documentation/latest"):
            self.assertEqual(rebrand(text, 'Nexus'), text)

    def test_examples(self):
        self.assertEqual(rebrand("e.g. https://www.odoo.com", 'Nexus'), "e.g. https://www.example.com")
        self.assertEqual(rebrand('"notification@odoo.com" or "odoo.com"', 'Nexus'),
                         '"notification@example.com" or "example.com"')
        self.assertEqual(rebrand("visit odoo.com/pricing", 'Nexus'), "visit odoo.com/pricing")
        self.assertEqual(rebrand("Link: http://yourcompany.odoo.com", 'Nexus'), "Link: http://yourcompany.example.com")

    def test_support(self):
        self.assertEqual(rebrand("An error occurred. Submit a support ticket at odoo.com/help.", 'Nexus'),
                         "An error occurred.")
        self.assertEqual(rebrand("Retry later. Contact odoo.com/help if the problem persists.", 'Nexus'),
                         "Retry later.")
        self.assertEqual(rebrand("Hata oluştu. odoo.com/help adresinden destek talebi gönderin.", 'Nexus', 'tr_TR'),
                         "Hata oluştu.")
        # A text that would be left empty is kept
        self.assertEqual(rebrand("See odoo.com/help", 'Nexus'), "See odoo.com/help")

    def test_html(self):
        self.assertEqual(
            rebrand_html(Markup('<b>X</b> uses <a href="https://odoo.com" style="color: red;">Odoo</a>.'), 'Nexus'),
            Markup('<b>X</b> uses Nexus.'))
        source = '<a href="https://www.odoo.com/documentation">Odoo</a>'
        self.assertEqual(rebrand_html(source, 'Nexus'), '<a href="https://www.odoo.com/documentation">Nexus</a>')
        self.assertEqual(rebrand("'example.com' in 'odoo@example.com'", 'Nexus'), "'example.com' in 'info@example.com'")
        self.assertEqual(rebrand("<jobs@example.odoo.com>", 'Nexus'), "<jobs@example.com>")
        self.assertEqual(rebrand("notification@odoo.com", 'Nexus'), "notification@example.com")

    def test_turkish_suffixes(self):
        cases = {
            "Odoo'da": "Nexus'ta", "Odoo’da": "Nexus’ta", "Odoo'dan": "Nexus'tan", "Odoo'daki": "Nexus'taki",
            "Odoo'nun": "Nexus'un", "Odoo'ya": "Nexus'a", "Odoo'yu": "Nexus'u", "Odoo'yla": "Nexus'la",
            "Odoo'su": "Nexus'u", "OdooBot'u": "Nexus'u",
        }
        for text, expected in cases.items():
            self.assertEqual(rebrand(text, 'Nexus', 'tr_TR'), expected)
        # The suffixes stay in the other languages
        self.assertEqual(rebrand("Odoo'da", 'Nexus', 'en_US'), "Nexus'da")

    def test_turkish_suffixes_other_brands(self):
        suffixes = ('da', 'nun', 'ya', 'dan', 'daki', 'yu', 'yla', 'su', 'suz')
        expected = {
            'Nova': ['da', 'nın', 'ya', 'dan', 'daki', 'yı', 'yla', 'sı', 'sız'],
            'Kelebek': ['te', 'in', 'e', 'ten', 'teki', 'i', 'le', 'i', 'siz'],
            'Atlas': ['ta', 'ın', 'a', 'tan', 'taki', 'ı', 'la', 'ı', 'sız'],
            'ÖRÜM': ['de', 'ün', 'e', 'den', 'deki', 'ü', 'le', 'ü', 'süz'],
        }
        for brand, brand_suffixes in expected.items():
            self.assertEqual([adapt_tr_suffix(suffix, 'Odoo', brand) for suffix in suffixes], brand_suffixes, brand)
        # From a word ending with a consonant to a brand ending with a vowel
        self.assertEqual([adapt_tr_suffix(suffix, 'OdooBot', 'Nova') for suffix in ('a', 'u', 'un', 'ta', 'la', 'lar')],
                         ['ya', 'yı', 'nın', 'da', 'yla', 'lar'])

    def test_markup(self):
        result = rebrand(Markup("<p>Odoo</p>"), 'A & B')
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, Markup("<p>A &amp; B</p>"))

    def test_arch(self):
        arch = etree.fromstring(
            '<form string="Odoo"><p title="Odoo" t-att-title="\'Odoo\'">Odoo<b>x</b>Odoo</p>'
            '<script>var a = "Odoo";<t t-out="x"/>var b = "Odoo";</script><field name="x" invisible="Odoo"/></form>')
        rebrand_arch(arch, 'Nexus')
        self.assertEqual(
            etree.tostring(arch, encoding='unicode'),
            '<form string="Nexus"><p title="Nexus" t-att-title="\'Odoo\'">Nexus<b>x</b>Nexus</p>'
            '<script>var a = "Odoo";<t t-out="x"/>var b = "Odoo";</script><field name="x" invisible="Odoo"/></form>')


@tagged('post_install', '-at_install')
class TestRebrandSurfaces(TransactionCase):

    def set_brand(self, brand):
        self.env['ir.config_parameter'].set_str(BRAND_NAME_PARAM, brand)

    def test_code_translations(self):
        self.assertEqual(translate.get_translation('base', 'en_US', "Welcome to Odoo", ()), f"Welcome to {DEFAULT_BRAND_NAME}")
        self.assertEqual(translate.get_translation('base', 'tr_TR', "Odoo'da %s", ('x',)), f"{DEFAULT_BRAND_NAME}'ta x")
        self.assertEqual(self.env._("Welcome to Odoo"), f"Welcome to {DEFAULT_BRAND_NAME}")
        self.set_brand('Test ERP')
        self.assertEqual(self.env._("Welcome to Odoo"), "Welcome to Test ERP")

    def test_web_translations(self):
        def string(lang):
            translations, _params = self.env['ir.http']._get_translations_for_webclient(['web'], lang)
            messages = {message['id']: message['string'] for message in translations['web']['messages']}
            return messages["Your Odoo session expired. The current page is about to be refreshed."]

        self.assertIn(DEFAULT_BRAND_NAME, string('en_US'))
        self.set_brand('Test ERP')
        self.assertIn('Test ERP', string('en_US'))

    def test_field_labels(self):
        def padding_help():
            return self.env['ir.sequence'].with_context(lang='en_US').fields_get(['padding'])['padding']['help']

        self.assertIn(f"{DEFAULT_BRAND_NAME} will", padding_help())
        self.set_brand('Test ERP')
        self.assertIn("Test ERP will", padding_help())

    def test_views(self):
        view = self.env.ref('base.wizard_lang_export')
        self.assertIn(f"translating {DEFAULT_BRAND_NAME}", self.env['base.language.export'].get_view(view.id)['arch'])
        self.set_brand('Test ERP')
        self.assertIn("translating Test ERP", self.env['base.language.export'].get_view(view.id)['arch'])
        # The stored view does not change
        self.assertIn("translating Odoo", view.arch_db)

    def test_records(self):
        action = self.env.ref('base.action_partner_form')
        self.assertIn(f"{DEFAULT_BRAND_NAME} helps you", action._get_action_dict()['help'])
        self.assertIn("Odoo helps you", action.help)
