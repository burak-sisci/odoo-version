"""Brand leak test (T2.6).

Scans what users see, in English and Turkish, in every installed module: the
code translations of the server and of the web client, the field labels, the
views and QWeb templates (pages, reports, e-mail layouts), the records with
application texts and the main pages. The upstream product name or a link to
the publisher's site is a leak, unless brand_leak.ALLOWLIST accepts it.
"""
from lxml import html

from odoo.tests import HttpCase, tagged
from odoo.tools import translate
from odoo.tools.translate import code_translations

from odoo.addons.ov_brand.rebrand import HINT_RE, code_sources
from odoo.addons.ov_brand.tests.brand_leak import (
    LANGS,
    LINK_RE,
    find_leak,
    is_allowed,
    scan_arch,
)
from odoo.addons.ov_brand.tools import WEB_PATH


@tagged('post_install', '-at_install', 'ov_brand_leak')
class TestBrandLeak(HttpCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls.env['res.lang']._lang_get('tr_TR').active:
            cls.env['res.lang']._activate_lang('tr_TR')
            cls.env['ir.module.module'].search([('state', '=', 'installed')])._update_translations(['tr_TR'])
        cls.modules = cls.env['ir.module.module'].search([('state', '=', 'installed')]).mapped('name')

    def setUp(self):
        super().setUp()
        self.leaks = []

    def add_leak(self, surface, key, lang, text):
        if not is_allowed(surface, key):
            self.leaks.append(f"[{surface}] {key} ({lang}): {' '.join(str(text).split())[:200]}")

    def assertNoLeak(self):
        self.assertFalse(self.leaks, "Brand leaks:\n" + "\n".join(sorted(set(self.leaks))))

    def test_python_translations(self):
        for module in self.modules:
            for lang in LANGS:
                sources = set(code_sources(module, 'odoo-python'))
                if lang != 'en_US':
                    translations = code_translations.get_python_translations(module, lang)
                    sources.update(source for source, value in translations.items() if HINT_RE.search(value))
                for source in sources:
                    text = translate.get_translation(module, lang, source, ())
                    if find_leak(text):
                        self.add_leak('python', f'{module}:{source}', lang, text)
        self.assertNoLeak()

    def test_web_translations(self):
        for lang in LANGS:
            translations, _lang_params = self.env['ir.http']._get_translations_for_webclient(self.modules, lang)
            for module in self.modules:
                strings = {message['id']: message['string'] for message in translations[module]['messages']}
                for source in code_sources(module):
                    strings.setdefault(source, source)
                for source, string in strings.items():
                    if find_leak(string):
                        self.add_leak('web', f'{module}:{source}', lang, string)
        self.assertNoLeak()

    def test_fields(self):
        for lang in LANGS:
            env = self.env(context={'lang': lang})
            for model_name in self.env.registry:
                description = env[model_name].fields_get(attributes=['string', 'help', 'selection'])
                for field_name, attributes in description.items():
                    for attribute in ('string', 'help'):
                        if find_leak(attributes.get(attribute)):
                            self.add_leak('field', f'{model_name}.{field_name}.{attribute}', lang, attributes[attribute])
                    for _value, label in attributes.get('selection') or ():
                        if isinstance(label, str) and find_leak(label):
                            self.add_leak('field', f'{model_name}.{field_name}.selection', lang, label)
        self.assertNoLeak()

    def test_views(self):
        views = self.env['ir.ui.view'].search([
            ('active', '=', True), '|', ('inherit_id', '=', False), ('mode', '=', 'primary'),
        ])
        xmlids = views.get_external_id()
        for lang in LANGS:
            for view in views.with_context(lang=lang):
                key = xmlids[view.id] or view.key or f'ir.ui.view:{view.id}'
                for leak in scan_arch(view._get_combined_arch()):
                    self.add_leak('view', key, lang, leak)
        self.assertNoLeak()

    def test_records(self):
        texts = {
            'ir.actions.actions': ['name'],
            'ir.actions.act_window': ['help'],
            'res.groups': ['name', 'comment'],
            'ir.module.category': ['name', 'description'],
            'ir.module.module': ['shortdesc', 'summary'],
        }
        for lang in LANGS:
            env = self.env(context={'lang': lang, 'active_test': False})
            for model_name, fnames in texts.items():
                records = env[model_name].search([])
                if model_name == 'ir.module.module':
                    records = records.filtered(lambda module: module.state == 'installed')
                xmlids = records.get_external_id()
                for values in records.read(fnames):
                    for fname in fnames:
                        text = values[fname]
                        if isinstance(text, str) and fname == 'help':
                            text = html.fromstring(f'<div>{text}</div>').text_content()
                        if find_leak(text):
                            self.add_leak('record', f'{model_name}:{xmlids[values["id"]]}.{fname}', lang, text)
            menus = env['ir.ui.menu'].load_menus(False)
            for menu in menus.values():
                if find_leak(menu.get('name')):
                    self.add_leak('record', f'ir.ui.menu:{menu.get("xmlid")}.name', lang, menu['name'])
        bot = self.env.ref('base.partner_root')
        for fname in ('name', 'email'):
            if find_leak(bot[fname]):
                self.add_leak('record', f'res.partner:base.partner_root.{fname}', 'en_US', bot[fname])
        self.assertNoLeak()

    def scan_page(self, path, lang):
        response = self.url_open(path, headers={'Accept-Language': lang.replace('_', '-')})
        self.assertEqual(response.status_code, 200, path)
        if 'html' not in response.headers.get('Content-Type', ''):
            if find_leak(response.text) or LINK_RE.search(response.text):
                self.add_leak('page', path, lang, response.text)
            return
        tree = html.fromstring(response.content)
        for leak in scan_arch(tree):
            self.add_leak('page', path, lang, leak)

    def test_pages(self):
        for lang in LANGS:
            for path in ('/web/login', '/web/manifest.webmanifest', f'{WEB_PATH}/offline'):
                self.scan_page(path, lang)
        self.authenticate('admin', 'admin')
        for lang in LANGS:
            self.env.ref('base.user_admin').lang = lang
            self.scan_page(WEB_PATH, lang)
        self.assertNoLeak()
