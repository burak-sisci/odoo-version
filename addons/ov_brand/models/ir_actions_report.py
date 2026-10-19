from contextvars import ContextVar

from odoo import models
from odoo.tools import pdf

from odoo.addons.ov_brand.tools import DEFAULT_BRAND_NAME, get_brand_name

# Creator and producer of the PDF files the server writes itself: documents split
# per record, merged or converted to PDF/A. Upstream writes its own name there.
# The writer is not a model, so its method is replaced; the reports give the
# product name of the database.
_pdf_producer = ContextVar('ov_brand_pdf_producer', default=DEFAULT_BRAND_NAME)


def _write_stream(self, *args, **kwargs):
    name = _pdf_producer.get()
    self.add_metadata({'/Creator': name, '/Producer': name})
    pdf.PdfWriter.write_stream(self, *args, **kwargs)


pdf.BrandedFileWriter.write_stream = _write_stream


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        token = _pdf_producer.set(get_brand_name(self.env))
        try:
            return super()._render_qweb_pdf(report_ref, res_ids=res_ids, data=data)
        finally:
            _pdf_producer.reset(token)
