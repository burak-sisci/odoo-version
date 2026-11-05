from odoo import Command
from odoo.tests import tagged

from odoo.addons.ov_l10n_tr.tests.common import (
    PDF_ENGINES,
    PERSON_TCKN,
    TurkishPdfCommon,
)


@tagged('post_install', '-at_install', '-standard', 'ov_pdf')
class TestTurkishSaleDocumentsPdf(TurkishPdfCommon):

    @classmethod
    def get_default_groups(cls):
        return super().get_default_groups() | cls.env.ref('sales_team.group_sale_manager')

    def test_quotation_pdf(self):
        order = self.env['sale.order'].create({
            'partner_id': self.person.id,
            'order_line': [Command.create({'product_id': self.product_a.id, 'product_uom_qty': 2, 'price_unit': 1000.25})],
        })
        words = order.currency_id.with_context(lang='tr_TR').amount_to_text(order.amount_total)
        for engine in PDF_ENGINES:
            with self.subTest(engine=engine):
                content = self.render_pdf(engine, 'sale.action_report_saleorder', order)
                self.assertPdf(content, [f'TCKN: {PERSON_TCKN}', words, 'Ayşe Örnek'])
