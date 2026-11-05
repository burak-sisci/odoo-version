from lxml import html
from stdnum.tr import tckimlik, vkn

from odoo.addons.account.tests.common import AccountTestInvoicingCommon

# Fictional numbers, valid for their check digits.
COMPANY_VKN = '100000001' + vkn.calc_check_digit('100000001')
CUSTOMER_VKN = '100000002' + vkn.calc_check_digit('100000002')
PERSON_TCKN = '100000001' + tckimlik.calc_check_digits('100000001')
MERSIS = f'0{COMPANY_VKN}00015'
TRADE_REGISTRY = '123456'
WEBSITE = 'https://www.example.com'


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
