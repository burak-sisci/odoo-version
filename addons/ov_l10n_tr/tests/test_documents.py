from odoo.tests import tagged

from odoo.addons.ov_l10n_tr.tests.common import (
    COMPANY_VKN,
    CUSTOMER_VKN,
    MERSIS,
    PERSON_TCKN,
    TRADE_REGISTRY,
    WEBSITE,
    TurkishDocumentsCommon,
)
from odoo.addons.ov_l10n_tr.tools import turkish_capitalize

# Amounts in words as Turkish documents write them (docs/research/tr-documents.md):
# numbers joined (TDK spelling rule 3), Turkish capital letters, no 've'.
AMOUNTS_IN_WORDS = [
    (2000, 'İkibin Türk Lirası'),
    (200, 'İkiyüz Türk Lirası'),
    (11, 'Onbir Türk Lirası'),
    (1234.56, 'Binikiyüzotuzdört Türk Lirası Ellialtı Kuruş'),
    (5344.42, 'Beşbinüçyüzkırkdört Türk Lirası Kırkiki Kuruş'),
    (0.5, 'Sıfır Türk Lirası Elli Kuruş'),
    (1000000, 'Birmilyon Türk Lirası'),
]


@tagged('post_install', '-at_install')
class TestTurkishDocuments(TurkishDocumentsCommon):

    def _payment(self, payment_type, partner_type, amount=1234.56):
        return self.env['account.payment'].create({
            'payment_type': payment_type,
            'partner_type': partner_type,
            'partner_id': self.customer.id,
            'amount': amount,
            'journal_id': self.company_data['default_journal_bank'].id,
        })

    def _make_foreign(self):
        belgium = self.env.ref('base.be')
        self.company.vat = False
        self.company.write({'country_id': belgium.id, 'account_fiscal_country_id': belgium.id})

    def test_turkish_capitalize(self):
        for text, expected in (('iki', 'İki'), ('ılık', 'Ilık'), ('beş', 'Beş'), ('', '')):
            with self.subTest(text=text):
                self.assertEqual(turkish_capitalize(text), expected)

    def test_amount_to_text(self):
        lira = self.company.currency_id.with_context(lang='tr_TR')
        for amount, expected in AMOUNTS_IN_WORDS:
            with self.subTest(amount=amount):
                self.assertEqual(lira.amount_to_text(amount), expected)

    def test_amount_to_text_other_language(self):
        # upstream's words in the other languages
        lira = self.company.currency_id.with_context(lang='en_US')
        self.assertNotIn('Türk Lirası', lira.amount_to_text(2000))
        self.assertIn('Thousand', lira.amount_to_text(2000))

    def test_amount_in_words_enabled(self):
        # the Turkish chart turns the total in words on
        self.assertTrue(self.company.display_invoice_amount_total_words)

    def test_partner_ident_line(self):
        invoice = self.init_invoice('out_invoice', partner=self.customer, amounts=[1000])
        self.assertEqual(invoice._get_document_partner_ident_line(), f'VKN: {CUSTOMER_VKN}')
        invoice.partner_id = self.person
        self.assertEqual(invoice._get_document_partner_ident_line(), f'TCKN: {PERSON_TCKN}')
        invoice.partner_id = self.partner_a
        self.assertNotIn('VKN', invoice._get_document_partner_ident_line() or '')

    def test_receipt_titles(self):
        self.assertEqual(self._payment('inbound', 'customer').payment_receipt_title, 'Collection Receipt')
        self.assertEqual(self._payment('inbound', 'supplier').payment_receipt_title, 'Collection Receipt')
        self.assertEqual(self._payment('outbound', 'supplier').payment_receipt_title, 'Payment Voucher')
        self.assertEqual(self._payment('outbound', 'customer').payment_receipt_title, 'Payment Voucher')

    def test_receipt_titles_foreign_company(self):
        self._make_foreign()
        self.assertNotIn(self._payment('inbound', 'customer').payment_receipt_title, ('Collection Receipt', 'Payment Voucher'))

    def test_company_block(self):
        # Turkish Commercial Code art. 39: registry numbers and website on the documents
        invoice = self.init_invoice('out_invoice', partner=self.customer, amounts=[1000], post=True)
        document = self.render('account.account_invoices', invoice)
        self.assertEqual(self.texts(document, 'ov_l10n_tr_registry'), [
            f'MERSİS No: {MERSIS}',
            f'Ticaret Sicil No: {TRADE_REGISTRY}',
        ])
        self.assertEqual(self.texts(document, 'ov_l10n_tr_website'), [WEBSITE])
        company_block = ' '.join(self.texts(document, 'company_address_list'))
        self.assertRegex(company_block, rf'\bVKN\W+{COMPANY_VKN}')
        self.assertNotIn('VKN/TCKN', company_block)

    def test_invoice(self):
        invoice = self.init_invoice('out_invoice', partner=self.customer, amounts=[1000], post=True)
        document = self.render('account.account_invoices', invoice)
        text = self.text(document)
        self.assertIn(f'VKN: {CUSTOMER_VKN}', text)
        words = invoice.currency_id.with_context(lang='tr_TR').amount_to_text(invoice.amount_total)
        self.assertIn(words, text)

    def test_receipt(self):
        payment = self._payment('inbound', 'customer')
        document = self.render('account.action_report_payment_receipt', payment)
        self.assertEqual(len(self.texts(document, 'ov_l10n_tr_amount_in_words')), 1)
        self.assertIn('Binikiyüzotuzdört Türk Lirası Ellialtı Kuruş', self.texts(document, 'ov_l10n_tr_amount_in_words')[0])
        self.assertIn('Tahsilat Makbuzu', self.text(document))

    def test_foreign_company(self):
        # a company outside Turkey prints upstream's documents
        self._make_foreign()
        invoice = self.init_invoice('out_invoice', partner=self.customer, amounts=[1000], post=True)
        document = self.render('account.account_invoices', invoice)
        self.assertFalse(self.texts(document, 'ov_l10n_tr_registry'))
        self.assertFalse(self.texts(document, 'ov_l10n_tr_website'))
        payment = self._payment('inbound', 'customer')
        document = self.render('account.action_report_payment_receipt', payment)
        self.assertFalse(self.texts(document, 'ov_l10n_tr_amount_in_words'))
