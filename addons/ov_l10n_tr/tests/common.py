import io
import os
import re
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

from lxml import html
from stdnum.tr import tckimlik, vkn

from odoo.tests import HttpCase
from odoo.tests.common import TEST_CURSOR_COOKIE_NAME, release_test_lock
from odoo.tools.pdf import PdfFileReader

from odoo.addons.account.tests.common import AccountTestInvoicingCommon

# Fictional numbers, valid for their check digits.
COMPANY_VKN = '100000001' + vkn.calc_check_digit('100000001')
CUSTOMER_VKN = '100000002' + vkn.calc_check_digit('100000002')
PERSON_TCKN = '100000001' + tckimlik.calc_check_digits('100000001')
MERSIS = f'0{COMPANY_VKN}00015'
TRADE_REGISTRY = '123456'
WEBSITE = 'https://www.example.com'

PDF_ENGINES = ('wkhtmltopdf', 'paper-muncher')
# A4 in points, the paper format of the Turkish companies
A4 = (595.3, 841.9)


class TurkishDocumentsCommon(AccountTestInvoicingCommon):
    """A Turkish company printing its documents for Turkish customers."""

    @classmethod
    @AccountTestInvoicingCommon.setup_country('tr')
    def setUpClass(cls):
        super().setUpClass()
        cls.env['res.lang']._activate_lang('tr_TR')
        cls.company = cls.company_data['company']
        cls.company.write({'vat': COMPANY_VKN, 'website': WEBSITE})
        cls.company.partner_id.additional_identifiers = {
            'TR_MERSIS': MERSIS,
            'TR_TICARET_SICIL': TRADE_REGISTRY,
        }
        turkey = cls.env.ref('base.tr')
        cls.customer = cls.env['res.partner'].create({
            'name': 'Deneme Ticaret Ltd. Şti.',
            'country_id': turkey.id,
            'vat': CUSTOMER_VKN,
            'lang': 'tr_TR',
        })
        cls.person = cls.env['res.partner'].create({
            'name': 'Ayşe Örnek',
            'country_id': turkey.id,
            'vat': PERSON_TCKN,
            'lang': 'tr_TR',
        })
        # as the Turkish translations give them
        lira = cls.company.currency_id.with_context(lang='tr_TR')
        lira.currency_unit_label = 'Türk Lirası'
        lira.currency_subunit_label = 'Kuruş'

    def render(self, report_ref, records):
        """Return the HTML tree of the report printed for ``records``."""
        content = self.env['ir.actions.report']._render_qweb_html(report_ref, records.ids)[0]
        return html.fromstring(content)

    def texts(self, document, name):
        """Return the text of the elements named ``name``, spaces normalized."""
        return [' '.join(element.text_content().split()) for element in document.xpath(f'//*[@name="{name}"]')]

    def text(self, document):
        return ' '.join(document.text_content().split())


def squash(text):
    """Return ``text`` without white space: PDF text extraction splits and joins words freely."""
    return re.sub(r'\s+', '', text)


def unembedded_fonts(reader):
    """Return the names of the fonts the PDF uses without embedding them."""
    missing = set()
    for page in reader.pages:
        resources = page.get('/Resources')
        fonts = resources.get_object().get('/Font') if resources else None
        for font in (fonts.get_object() if fonts else {}).values():
            font = font.get_object()
            descendants = font.get('/DescendantFonts')
            for part in [d.get_object() for d in descendants.get_object()] if descendants else [font]:
                if part.get('/Subtype') == '/Type3':
                    continue
                descriptor = part.get('/FontDescriptor')
                descriptor = descriptor.get_object() if descriptor else {}
                if not any(key in descriptor for key in ('/FontFile', '/FontFile2', '/FontFile3')):
                    missing.add(str(part.get('/BaseFont')))
    return missing


class TurkishPdfCommon(TurkishDocumentsCommon, HttpCase):
    """Print the Turkish documents to PDF with the real engines.

    The engines named in the ``OV_PDF_ENGINES`` environment variable (comma
    separated, as CI sets it) must work; the others are skipped when missing.
    With ``OV_PDF_DIR`` set, the PDFs are also written there to be looked at.
    The Turkish translations are loaded: the test database has none.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        modules = cls.env['ir.module.module'].search([('state', '=', 'installed')])
        modules._load_module_terms(modules.mapped('name'), ['tr_TR'], overwrite=True)

    def render_pdf(self, engine, report_ref, records):
        """Return the PDF of the report printed by ``engine`` for ``records``."""
        Report = self.env['ir.actions.report']
        if Report.get_pdf_engine_state(engine) != 'ok':
            required = os.environ.get('OV_PDF_ENGINES', '').split(',')
            if engine in required:
                self.fail(f'PDF engine {engine} is not working')
            self.skipTest(f'PDF engine {engine} is not installed')
        self.env['ir.config_parameter'].sudo().set_str('report.pdf_engine_default', engine)
        with ExitStack() as stack:
            if engine == 'paper-muncher':
                self._allow_paper_muncher(stack)
            content = Report.with_context(force_report_rendering=True)._render_qweb_pdf(report_ref, records.ids)[0]
        self.assertTrue(content.startswith(b'%PDF-'), f'{engine} did not print a PDF')
        if out_dir := os.environ.get('OV_PDF_DIR'):
            path = Path(out_dir) / f'{engine}-{self._testMethodName}.pdf'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        return content

    def _allow_paper_muncher(self, stack):
        """Let Paper Muncher fetch the assets from the test server.

        HttpCase does it for wkhtmltopdf: the test cursor cookie, the registry
        lock released while the engine runs.
        """
        from odoo.addons.base_report_paper_muncher import paper_muncher  # noqa: PLC0415

        case = self
        server_class = paper_muncher.PaperMuncherServer
        serve = server_class.serve

        def patched_serve(server, *args, **kwargs):
            cookie = f'{TEST_CURSOR_COOKIE_NAME}=ov-pdf'
            environ = server._wsgi_environ
            environ['HTTP_COOKIE'] = f"{environ['HTTP_COOKIE']}, {cookie}" if environ.get('HTTP_COOKIE') else cookie
            with (
                patch.object(case, 'http_request_key', 'ov-pdf'),
                release_test_lock(),
                patch('odoo.tests.common._disable_flushing_cursor', True),
            ):
                return serve(server, *args, **kwargs)

        stack.enter_context(patch.object(server_class, 'serve', patched_serve))

    def assertPdf(self, content, expected_texts):
        """Check the text, the fonts, the paper and the metadata of a printed document."""
        reader = PdfFileReader(io.BytesIO(content))
        text = ' '.join(page.extract_text() or '' for page in reader.pages)
        for expected in expected_texts:
            self.assertIn(squash(expected), squash(text), f'"{expected}" is not in the PDF text: {text}')
        self.assertNotIn('odoo', text.lower())
        self.assertFalse(unembedded_fonts(reader), 'fonts not embedded')
        box = reader.pages[0].mediabox
        self.assertAlmostEqual(float(box.width), A4[0], delta=2)
        self.assertAlmostEqual(float(box.height), A4[1], delta=2)
        metadata = {key: str(value) for key, value in (reader.metadata or {}).items()}
        for key, value in metadata.items():
            self.assertNotIn('odoo', value.lower(), f'brand in the PDF metadata {key}')
        return text
