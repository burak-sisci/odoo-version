from odoo import Command
from odoo.tests import tagged

from odoo.addons.ov_l10n_tr.tests.common import (
    CUSTOMER_VKN,
    PDF_ENGINES,
    TurkishPdfCommon,
)


@tagged('post_install', '-at_install', '-standard', 'ov_pdf')
class TestTurkishDeliverySlipPdf(TurkishPdfCommon):

    def test_dispatch_note_pdf(self):
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.company.id)], limit=1)
        picking = self.env['stock.picking'].create({
            'picking_type_id': warehouse.out_type_id.id,
            'partner_id': self.customer.id,
            'move_ids': [Command.create({'product_id': self.product_a.id, 'product_uom_qty': 3})],
        })
        picking.action_confirm()
        for engine in PDF_ENGINES:
            with self.subTest(engine=engine):
                content = self.render_pdf(engine, 'stock.action_report_delivery', picking)
                self.assertPdf(content, ['Sevk İrsaliyesi', 'Düzenleme Tarihi', 'Fiili Sevk Tarihi', CUSTOMER_VKN, 'MERSİS No'])
