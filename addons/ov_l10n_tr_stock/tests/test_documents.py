from odoo import Command
from odoo.tests import tagged

from odoo.addons.ov_l10n_tr.tests.common import (
    CUSTOMER_VKN,
    MERSIS,
    TRADE_REGISTRY,
    TurkishDocumentsCommon,
)

BLANK_DATE = '....../....../..........'


@tagged('post_install', '-at_install')
class TestTurkishDeliverySlip(TurkishDocumentsCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse = cls.env['stock.warehouse'].search([('company_id', '=', cls.company.id)], limit=1)

    def _picking(self, picking_type):
        return self.env['stock.picking'].create({
            'picking_type_id': picking_type.id,
            'partner_id': self.customer.id,
            'move_ids': [Command.create({'product_id': self.product_a.id, 'product_uom_qty': 3})],
        })

    def _render(self, picking):
        return self.render('stock.action_report_delivery', picking)

    def test_title(self):
        self.assertEqual(self._picking(self.warehouse.out_type_id)._get_deliveryslip_report_title(), 'Dispatch Note')
        self.assertNotEqual(self._picking(self.warehouse.in_type_id)._get_deliveryslip_report_title(), 'Dispatch Note')

    def test_dispatch_note(self):
        # Tax Procedure Law art. 230/5: the recipient, the issue date and the
        # actual dispatch date, apart; written by hand before the goods leave
        picking = self._picking(self.warehouse.out_type_id)
        picking.action_confirm()
        document = self._render(picking)
        self.assertIn('Sevk İrsaliyesi', self.text(document))
        self.assertEqual(len(self.texts(document, 'customer_address')), 1)
        self.assertIn(CUSTOMER_VKN, self.text(document))
        self.assertFalse(self.texts(document, 'div_sched_date'))
        self.assertEqual(len(self.texts(document, 'ov_l10n_tr_issue_date')), 1)
        self.assertIn(BLANK_DATE, ' '.join(self.texts(document, 'ov_l10n_tr_dispatch_date')))
        # the company block in the language of the document, not of the user
        self.assertEqual(self.env.user.lang, 'en_US')
        self.assertEqual(self.texts(document, 'ov_l10n_tr_registry'), [
            f'MERSİS No: {MERSIS}',
            f'Ticaret Sicil No: {TRADE_REGISTRY}',
        ])

    def test_dispatch_note_done(self):
        picking = self._picking(self.warehouse.out_type_id)
        picking.action_confirm()
        picking.move_ids.write({'quantity': 3, 'picked': True})
        picking.button_validate()
        self.assertEqual(picking.state, 'done')
        document = self._render(picking)
        dispatch_date = ' '.join(self.texts(document, 'ov_l10n_tr_dispatch_date'))
        self.assertNotIn(BLANK_DATE, dispatch_date)
        self.assertRegex(dispatch_date, r'\d{2}:\d{2}')
        self.assertIn(str(picking.date_done.year), ' '.join(self.texts(document, 'ov_l10n_tr_issue_date')))

    def test_receipt(self):
        # incoming goods: upstream's slip
        document = self._render(self._picking(self.warehouse.in_type_id))
        self.assertFalse(self.texts(document, 'ov_l10n_tr_issue_date'))
        self.assertNotIn('Sevk İrsaliyesi', self.text(document))

    def test_foreign_company(self):
        self.company.vat = False
        belgium = self.env.ref('base.be')
        self.company.write({'country_id': belgium.id, 'account_fiscal_country_id': belgium.id})
        document = self._render(self._picking(self.warehouse.out_type_id))
        self.assertFalse(self.texts(document, 'ov_l10n_tr_issue_date'))
        self.assertFalse(self.texts(document, 'customer_address'))
