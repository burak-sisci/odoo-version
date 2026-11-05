from odoo.tests import tagged

from odoo.addons.ov_l10n_tr.tests.common import (
    CUSTOMER_VKN,
    MERSIS,
    PDF_ENGINES,
    TRADE_REGISTRY,
    TurkishPdfCommon,
)


@tagged('post_install', '-at_install', '-standard', 'ov_pdf')
class TestTurkishDocumentsPdf(TurkishPdfCommon):
    """The invoice and the receipt printed to PDF (python tools/run_tests.py ... --tags ov_pdf)."""

    def test_invoice_pdf(self):
        invoice = self.init_invoice('out_invoice', partner=self.customer, amounts=[1000], post=True)
        words = invoice.currency_id.with_context(lang='tr_TR').amount_to_text(invoice.amount_total)
        for engine in PDF_ENGINES:
            with self.subTest(engine=engine):
                content = self.render_pdf(engine, 'account.account_invoices', invoice)
                self.assertPdf(content, [
                    f'VKN: {CUSTOMER_VKN}',
                    f'MERSİS No: {MERSIS}',
                    f'Ticaret Sicil No: {TRADE_REGISTRY}',
                    f'Yalnız: {words}',
                    'Deneme Ticaret Ltd. Şti.',
                ])

    def test_receipt_pdf(self):
        payment = self.env['account.payment'].create({
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'partner_id': self.customer.id,
            'amount': 1234.56,
            'journal_id': self.company_data['default_journal_bank'].id,
        })
        for engine in PDF_ENGINES:
            with self.subTest(engine=engine):
                content = self.render_pdf(engine, 'account.action_report_payment_receipt', payment)
                self.assertPdf(content, ['Tahsilat Makbuzu', 'Binikiyüzotuzdört Türk Lirası Ellialtı Kuruş'])
