from odoo import Command
from odoo.tests import tagged

from odoo.addons.ov_l10n_tr.tests.common import (
    CUSTOMER_VKN,
    PERSON_TCKN,
    TurkishDocumentsCommon,
)


@tagged('post_install', '-at_install')
class TestTurkishSaleDocuments(TurkishDocumentsCommon):

    @classmethod
    def get_default_groups(cls):
        return super().get_default_groups() | cls.env.ref('sales_team.group_sale_manager')

    def _order(self, partner):
        return self.env['sale.order'].create({
            'partner_id': partner.id,
            'order_line': [Command.create({'product_id': self.product_a.id, 'product_uom_qty': 2, 'price_unit': 1000.25})],
        })

    def _words(self, order):
        return order.currency_id.with_context(lang='tr_TR').amount_to_text(order.amount_total)

    def test_quotation(self):
        order = self._order(self.customer)
        document = self.render('sale.action_report_saleorder', order)
        self.assertIn(f'VKN: {CUSTOMER_VKN}', self.text(document))
        self.assertNotIn('VKN/TCKN', self.text(document))
        amount_in_words = self.texts(document, 'ov_l10n_tr_amount_in_words')
        self.assertEqual(len(amount_in_words), 1)
        self.assertIn(self._words(order), amount_in_words[0])
        self.assertIn('Kuruş', amount_in_words[0])

    def test_quotation_person(self):
        document = self.render('sale.action_report_saleorder', self._order(self.person))
        self.assertIn(f'TCKN: {PERSON_TCKN}', self.text(document))

    def test_pro_forma(self):
        order = self._order(self.customer)
        document = self.render('sale.action_report_pro_forma_invoice', order)
        self.assertIn(f'VKN: {CUSTOMER_VKN}', self.text(document))
        self.assertIn(self._words(order), ' '.join(self.texts(document, 'ov_l10n_tr_amount_in_words')))

    def test_foreign_company(self):
        self.company.vat = False
        belgium = self.env.ref('base.be')
        self.company.write({'country_id': belgium.id, 'account_fiscal_country_id': belgium.id})
        document = self.render('sale.action_report_saleorder', self._order(self.customer))
        self.assertFalse(self.texts(document, 'ov_l10n_tr_amount_in_words'))
