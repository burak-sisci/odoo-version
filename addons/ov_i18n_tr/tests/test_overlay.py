from pathlib import Path
from unittest.mock import patch

from odoo.tests import TransactionCase, tagged
from odoo.tools import file_open, translate
from odoo.tools.translate import (
    JAVASCRIPT_TRANSLATION_COMMENT,
    PYTHON_TRANSLATION_COMMENT,
    code_translations,
    translation_file_reader,
)

from odoo.addons.base.models import ir_module
from odoo.addons.ov_i18n_tr import tools

FIXTURES = Path(__file__).resolve().parent / 'overlay'
PYTHON_SOURCE = '%(action_name)s is not a valid action on %(model_name)s'
PYTHON_VALUE = '%(action_name)s, %(model_name)s için geçerli bir işlem değil (ov test)'

# Upstream mistranslations of web terms that the overlay corrects: (modules, source, translation)
CORRECTIONS = [
    # upstream: 'Sil' (delete) on the button that only discards the changes
    (('web', 'html_editor', 'spreadsheet'), 'Discard', 'Vazgeç'),
    # upstream machine translations: 'Şal' (shawl), 'Donmak' (to freeze, intransitive),
    # 'Maç bitmek üzere' (the game is about to end), 'kulüp kıyafeti' (club outfit)
    (('spreadsheet',), 'Wrap', 'Kaydırma'),
    (('spreadsheet',), 'Freeze', 'Dondur'),
    (('spreadsheet',), 'Match to end', 'Metin sonunu eşleşme say'),
    (('web',), 'club suit', 'sinek (iskambil)'),
    # upstream: 'Kabul Et' (accept, a button) where the sentence lists the supported sources
    (('html_editor',), 'Accepts', 'Desteklenenler:'),
]

# Upstream mistranslations of record terms (fields, views, selections): (module, source, translation)
RECORD_CORRECTIONS = [
    # upstream: 'Yanlızca Vergiden Muaf Satırlar' (only the tax exempt lines), the opposite
    ('account', 'Only Tax Exigible Lines', 'Yalnızca Vergisi Doğmuş Satırlar'),
    # upstream: 'Vergi Münhasırlığı' (tax exclusivity)
    ('account', 'Tax Exigibility', 'Vergi Doğuşu'),
    # default terms and conditions, upstream: '... münhasıran tarafından yönetilecektir <country> kanun.'
    ('account', 'law.', 'hukukuna tabidir.'),
    # upstream: an unrelated sentence (fill in the EAS code)
    ('account_edi_ubl_cii', 'VATEX-EU-132 - Exempt based on article 132 of Council Directive 2006/112/EC',
     "VATEX-EU-132 - 2006/112/EC sayılı AB Konsey Direktifi'nin 132. maddesi uyarınca muaf"),
    # upstream: 'Atama Alan Adı' (an internet domain name), the filter of the leads a team gets
    ('crm', 'Assignment Domain', 'Atama Filtresi'),
    # upstream: 'Manuel Yakalama' (catching), the capture of an authorized payment
    ('payment', 'Manual Capture', 'Elle Tahsilat'),
    # upstream: 'Kontak' (an electrical contact), the link of '... the website administrator.'
    ('payment', 'Contact', 'Web sitesi yöneticisiyle'),
    # upstream: "Ödeme Token'ı kaydet" (save the payment token), a field label
    ('account_payment', 'Saved Payment Token', 'Kayıtlı Ödeme Belirteci'),
]


def forget_code_translations():
    code_translations.python_translations.clear()
    code_translations.web_translations.clear()


@tagged('post_install', '-at_install')
class TestOverlay(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # fictional translations, see tests/overlay/; the code translations
        # read with them are forgotten (process-wide cache)
        cls.startClassPatcher(patch.object(tools, 'OVERLAY_DIR', FIXTURES))
        forget_code_translations()
        cls.addClassCleanup(forget_code_translations)
        cls.env['res.lang']._activate_lang('tr_TR')
        cls.turkey = cls.env.ref('base.tr')
        cls.menu = cls.env.ref('base.menu_administration')
        cls.view = cls.env.ref('base.view_users_form')

    def setUp(self):
        super().setUp()
        forget_code_translations()

    def remove_translation(self, record, field_name):
        self.env.flush_all()
        self.env.cr.execute(
            f'UPDATE "{record._table}" SET "{field_name}" = "{field_name}" - %s WHERE id = %s',
            ['tr_TR', record.id],
        )
        record.invalidate_recordset([field_name])

    def name_tr(self, record):
        return record.with_context(lang='tr_TR').name

    def test_po_paths(self):
        overlay = str(FIXTURES / 'base.po')
        # code terms, for every database
        self.assertEqual(list(translate.get_po_paths('base', 'tr_TR'))[-1], overlay)
        self.assertNotIn(overlay, translate.get_po_paths('base', 'de_DE'))
        self.assertNotIn(str(FIXTURES / 'mail.po'), translate.get_po_paths('mail', 'tr_TR'))
        # record terms, while this module loads them
        self.assertNotIn(overlay, ir_module.get_po_paths('base', 'tr_TR'))
        token = tools.loading_records.set(True)
        try:
            self.assertEqual(list(ir_module.get_po_paths('base', 'tr_TR'))[-1], overlay)
        finally:
            tools.loading_records.reset(token)

    def test_python_translation(self):
        self.assertEqual(translate.get_translation('base', 'tr_TR', PYTHON_SOURCE, ()), PYTHON_VALUE)

    def test_web_translation(self):
        messages = code_translations.get_web_translations('web', 'tr_TR')['messages']
        self.assertIn({'id': 'Discard', 'string': 'Vazgeç (ov test)'}, messages)

    def test_record_missing_translation(self):
        # filled without overwriting, like upstream fills the missing ones
        self.remove_translation(self.turkey, 'name')
        self.env['ir.module.module']._load_module_terms(['base'], ['tr_TR'])
        self.assertEqual(self.name_tr(self.turkey), 'Türkiye (ov test)')

    def test_record_existing_translation(self):
        # kept without overwriting, replaced when overwriting
        self.menu.with_context(lang='tr_TR').name = 'Yönetim'
        self.env['ir.module.module']._load_module_terms(['base'], ['tr_TR'])
        self.assertEqual(self.name_tr(self.menu), 'Yönetim')
        self.env['ir.module.module']._load_module_terms(['base'], ['tr_TR'], overwrite=True)
        self.assertEqual(self.name_tr(self.menu), 'Ayarlar (ov test)')

    def test_record_noupdate(self):
        # records the customer may change (noupdate) keep their translation, like upstream's
        self.turkey.with_context(lang='tr_TR').name = 'Türkiye Cumhuriyeti'
        self.env['ir.module.module']._load_module_terms(['base'], ['tr_TR'], overwrite=True)
        self.assertEqual(self.name_tr(self.turkey), 'Türkiye Cumhuriyeti')

    def test_record_terms(self):
        # a term of a view: the overlay wins over upstream's translation in the same import
        self.env['ir.module.module']._load_module_terms(['base'], ['tr_TR'], overwrite=True)
        arch = self.view.with_context(lang='tr_TR').arch_db
        self.assertIn('Erişim Hakları (ov test)', arch)
        self.assertNotIn('Erişim Yetkileri', arch)

    def test_this_module_loaded(self):
        # the overlay of the modules installed before this one
        self.remove_translation(self.turkey, 'name')
        self.env['ir.module.module']._load_module_terms([tools.MODULE], ['tr_TR'])
        self.assertEqual(self.name_tr(self.turkey), 'Türkiye (ov test)')

    def test_this_module_installed(self):
        # on installation, the overlay replaces the existing translations
        self.menu.with_context(lang='tr_TR').name = 'Yönetim'
        module = self.env['ir.module.module'].search([('name', '=', tools.MODULE)])
        self.env['ir.module.module']._load_module_terms([tools.MODULE], ['tr_TR'])
        self.assertEqual(self.name_tr(self.menu), 'Yönetim')
        module.state = 'to install'
        self.env['ir.module.module']._load_module_terms([tools.MODULE], ['tr_TR'])
        self.assertEqual(self.name_tr(self.menu), 'Ayarlar (ov test)')

    def test_module_name(self):
        # names of the modules not installed, in the applications list (the
        # fixture module may be installed with other modules: seen as not installed)
        account = self.env['ir.module.module'].search([('name', '=', 'account')])
        if account.state == 'installed':
            account.state = 'uninstalled'
        self.env['ir.module.module']._load_non_installed_modules_manifest_terms(['tr_TR'])
        self.assertEqual(account.with_context(lang='tr_TR').shortdesc, 'Faturalama (ov test)')


@tagged('post_install', '-at_install')
class TestOverlayFiles(TransactionCase):
    """The overlay files of the module, as Odoo reads them."""

    def test_files(self):
        forget_code_translations()
        for path in sorted(tools.OVERLAY_DIR.glob('*.po')):
            module = path.stem
            with self.subTest(module=module), file_open(str(path), 'rb') as fileobj:
                rows = list(translation_file_reader(fileobj, fileformat='po'))
                self.assertTrue(rows)
                for row in rows:
                    self.assertTrue(row['value'], row['src'])
                for kind, comment, get in (
                    ('python', PYTHON_TRANSLATION_COMMENT, code_translations.get_python_translations),
                    ('web', JAVASCRIPT_TRANSLATION_COMMENT, None),
                ):
                    expected = {
                        row['src']: row['value']
                        for row in rows if row['type'] == 'code' and comment in row['comments']
                    }
                    if not expected:
                        continue
                    if get:
                        actual = get(module, 'tr_TR')
                    else:
                        messages = code_translations.get_web_translations(module, 'tr_TR')['messages']
                        actual = {message['id']: message['string'] for message in messages}
                    for src, value in expected.items():
                        self.assertEqual(actual.get(src), value, f'{kind} term of {module}: {src!r}')

    def test_corrections(self):
        forget_code_translations()
        for modules, src, value in CORRECTIONS:
            for module in modules:
                with self.subTest(module=module, src=src):
                    messages = code_translations.get_web_translations(module, 'tr_TR')['messages']
                    actual = {message['id']: message['string'] for message in messages}
                    self.assertEqual(actual.get(src), value)

    def test_record_corrections(self):
        for module, src, value in RECORD_CORRECTIONS:
            path = str(tools.OVERLAY_DIR / f'{module}.po')
            with self.subTest(module=module, src=src), file_open(path, 'rb') as fileobj:
                rows = translation_file_reader(fileobj, fileformat='po')
                actual = {row['src']: row['value'] for row in rows if row['type'] != 'code'}
                self.assertEqual(actual.get(src), value)
