import io
from unittest.mock import patch

from lxml import html

from odoo.tests import TransactionCase, tagged
from odoo.tools.pdf import PdfFileReader, PdfFileWriter

from odoo.addons.ov_brand.tools import BRAND_NAME_PARAM, DEFAULT_BRAND_NAME

REPORT = 'base.ir_module_reference_print'


def blank_pdf(pages):
    writer = PdfFileWriter()
    for _page in range(pages):
        writer.add_blank_page(100, 100)
    stream = io.BytesIO()
    writer.write(stream)
    return stream.getvalue()


@tagged('post_install', '-at_install')
class TestOvBrandReport(TransactionCase):

    def test_report_title(self):
        modules = self.env['ir.module.module'].search([('name', '=', 'ov_brand')])
        content = self.env['ir.actions.report']._render_qweb_html(REPORT, modules.ids)[0]
        self.assertEqual(html.fromstring(content).xpath('//title/text()'), [DEFAULT_BRAND_NAME])

    def test_pdf_metadata(self):
        metadata = PdfFileReader(io.BytesIO(blank_pdf(1))).metadata
        self.assertEqual(metadata['/Creator'], DEFAULT_BRAND_NAME)
        self.assertEqual(metadata['/Producer'], DEFAULT_BRAND_NAME)

    def test_report_pdf_metadata(self):
        # Several records: the server splits the document of the PDF engine per
        # record, then merges the parts
        self.env['ir.config_parameter'].sudo().set_str(BRAND_NAME_PARAM, 'Fictional ERP')
        modules = self.env['ir.module.module'].search([('name', 'in', ('base', 'web'))])
        # In tests the server renders HTML instead of PDF unless forced
        report = self.env['ir.actions.report'].with_context(force_report_rendering=True)
        with (
            patch.object(type(report), 'get_pdf_engine_state', return_value='ok'),
            patch.object(type(report), '_run_pdf_engine', return_value=(blank_pdf(2), modules.ids)),
        ):
            content = report._render_qweb_pdf(REPORT, modules.ids)[0]
        metadata = PdfFileReader(io.BytesIO(content)).metadata
        self.assertEqual(metadata['/Producer'], 'Fictional ERP')
        # Outside the reports, the default name
        self.assertEqual(PdfFileReader(io.BytesIO(blank_pdf(1))).metadata['/Producer'], DEFAULT_BRAND_NAME)
