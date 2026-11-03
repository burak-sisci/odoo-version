from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.ov_l10n_tr.tests.turkish_names import (
    name_problems,
    upper_case_problems,
)

TRANSLATED_FIELDS = {
    'account.account': ('name',),
    'account.tax.group': ('name',),
    'account.tax': ('name', 'description', 'invoice_label'),
    'account.fiscal.position': ('name',),
}

# Names of the upstream chart that the rules must flag (docs/research/l10n-tr.md, T3.1):
# {model: {translated column: xmlids}}.
UPSTREAM_ERRORS = {
    'account.account': {'name@tr': (
        'tr35', 'tr76', 'tr102997', 'tr102998', 'tr102999', 'tr224', 'tr247', 'tr301', 'tr302',
        'tr336', 'tr350', 'tr397', 'tr401', 'tr436', 'tr492', 'tr646', 'tr647', 'tr648', 'tr656',
        'tr657', 'tr658', 'tr721', 'tr760', 'tr391005', 'tr152', 'tr620',
    )},
    'account.tax.group': {'name@tr': (
        'tr_tax_group_wh_20', 'tr_tax_group_wh_4', 'tr_tax_group_wh_10', 'tr_tax_group_wh_14',
        'tr_tax_group_wh_18', 'tr_tax_group_wh_6', 'tr_tax_group_wh_8',
    )},
    'account.tax': {'description@tr': ('tr_s_0_ex', 'tr_p_0')},
}


@tagged('post_install', '-at_install')
class TestTurkishChart(AccountTestInvoicingCommon):

    @classmethod
    @AccountTestInvoicingCommon.setup_country('tr')
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.company_data['company']
        # As when Turkish is installed: the chart translations are loaded then.
        cls.env['res.lang']._activate_lang('tr_TR')
        cls.env['account.chart.template']._load_translations(langs=['tr_TR'], companies=cls.company)
        cls.chart = cls.env['account.chart.template'].with_company(cls.company)

    def _template_records(self, model):
        """Return the records the chart created for the company (not the test copies)."""
        prefix = f'{self.company.id}_'
        data = self.env['ir.model.data'].search([
            ('model', '=', model), ('module', '=', 'account'), ('name', '=like', f'{prefix}%'),
        ])
        records = self.env[model].with_context(active_test=False).browse(data.mapped('res_id')).exists()
        if model == 'account.account':
            # The accounts of the journals the test case creates carry their names.
            records -= (self.company_data['default_journal_credit'] + self.company_data['default_journal_cash']).default_account_id
        return records

    def _account(self, xmlid):
        return self.chart.ref(xmlid)

    def _name_problems(self, model):
        problems = []
        for record in self._template_records(model):
            for fname in TRANSLATED_FIELDS[model]:
                turkish = record.with_context(lang='tr_TR')[fname]
                english = record.with_context(lang='en_US')[fname]
                if fname == 'description':
                    turkish, english = (str(value or '').replace('<p>', '').replace('</p>', '') for value in (turkish, english))
                    if not turkish:
                        continue
                if fname == 'invoice_label' and not turkish:
                    continue
                found = name_problems(turkish, english)
                if model == 'account.tax' and 'stopaj' in turkish.lower() and record.tax_group_id.with_context(lang='tr_TR').name.startswith('Tevkifat'):
                    found.append('"stopaj" for VAT withholding')
                problems += [f'{record.display_name} [{fname}]: {problem}' for problem in found]
        return problems

    def test_turkish_names(self):
        for model in TRANSLATED_FIELDS:
            with self.subTest(model=model):
                self.assertTrue(self._template_records(model))
                self.assertEqual(self._name_problems(model), [])

    def test_rules_flag_the_upstream_errors(self):
        """The rules find every known error of the upstream names."""
        for model, columns in UPSTREAM_ERRORS.items():
            upstream = self.chart._parse_csv('tr', model, module='l10n_tr')
            for column, xmlids in columns.items():
                english_column = column.split('@')[0]
                for xmlid in xmlids:
                    with self.subTest(model=model, xmlid=xmlid):
                        values = upstream[xmlid]
                        self.assertTrue(name_problems(values[column], values.get(english_column)), values[column])

    def test_upper_case_rule(self):
        self.assertEqual(upper_case_problems('TAHSIL EDILMEYEN ÖDEMELER'), ['TAHSIL', 'EDILMEYEN'])
        self.assertEqual(upper_case_problems('KAMBIYO KARLARI'), ['KAMBIYO'])
        self.assertEqual(upper_case_problems('DİĞER ÇEŞİTLİ BORÇLAR'), [])
        self.assertEqual(upper_case_problems('YURTDIŞI SATIŞLAR, KÂR, OLAĞANDIŞI'), [])
        # Mixed case is outside the rule.
        self.assertEqual(upper_case_problems('Isparta Vergi Dairesi'), [])

    def test_corrected_accounts(self):
        Account = self.env['account.account'].with_context(lang='tr_TR')
        self.assertRecordValues(Account.browse([self._account(x).id for x in ('tr391004', 'tr391005', 'tr437', 'tr438')]), [
            {'name': 'SATIŞLARDA TEVKİF EDİLEN KDV'},
            {'name': 'ALIŞLARDA TEVKİF EDİLEN KDV'},
            {'name': 'DİĞER BORÇ SENETLERİ REESKONTU (-)'},
            {'name': 'KAMUYA OLAN ERTELENMİŞ VEYA TAKSİTLENDİRİLMİŞ BORÇLAR'},
        ])
        for lang in ('tr_TR', 'en_US'):
            with self.subTest(lang=lang):
                self.assertNotEqual(self._account('tr690').with_context(lang=lang).name,
                                    self._account('tr692').with_context(lang=lang).name)

    def test_new_accounts(self):
        expected = {
            'tr170': ('170000', 'asset_current'),
            'tr178': ('178000', 'asset_current'),
            'tr179': ('179000', 'asset_current'),
            'tr480': ('480000', 'liability_non_current'),
            'tr481': ('481000', 'liability_non_current'),
            'tr502': ('502000', 'equity'),
            'tr503': ('503000', 'equity'),
            'tr523': ('523000', 'equity'),
        }
        for xmlid, (code, account_type) in expected.items():
            with self.subTest(xmlid=xmlid):
                account = self._account(xmlid).with_company(self.company)
                self.assertEqual((account.code, account.account_type, account.active), (code, account_type, True))
        group = self._account('tr17').with_company(self.company)
        self.assertEqual((group.code, group.active), ('17', False))
        self.assertEqual(self._account('tr170').parent_id, group)

    def test_special_accounts(self):
        """The company's special accounts are in the uniform chart; no 999xxx account is created."""
        company = self.company.with_company(self.company)
        codes = {
            fname: company[fname].with_company(self.company).code
            for fname in (
                'account_journal_early_pay_discount_loss_account_id',
                'account_journal_early_pay_discount_gain_account_id',
                'default_cash_difference_income_account_id',
                'default_cash_difference_expense_account_id',
            )
        }
        self.assertEqual(codes, {
            'account_journal_early_pay_discount_loss_account_id': '611000',
            'account_journal_early_pay_discount_gain_account_id': '649000',
            'default_cash_difference_income_account_id': '679000',
            'default_cash_difference_expense_account_id': '689000',
        })
        self.assertEqual(company.get_unaffected_earnings_account(), self._account('tr590'))
        self.assertFalse(self._template_records('account.account').with_company(self.company).filtered(
            lambda a: a.code.startswith('999'),
        ))

    def test_income_tax_withholding(self):
        """Rent and self-employment withholding is a liability (360), not deductible VAT (191)."""
        payable = self._account('tr360')
        for xmlid in ('ov_tr_p_wh_rent_20', 'ov_tr_p_wh_freelance_20'):
            with self.subTest(xmlid=xmlid):
                tax = self.chart.ref(xmlid)
                self.assertRecordValues(tax, [{'amount': -20.0, 'type_tax_use': 'purchase', 'active': True}])
                self.assertEqual(tax.repartition_line_ids.filtered(lambda line: line.repartition_type == 'tax').account_id, payable)
                bill = self.init_invoice('in_invoice', amounts=[1000.0], taxes=tax, post=True)
                withheld = bill.line_ids.filtered(lambda line: line.account_id == payable)
                self.assertEqual((withheld.balance, bill.amount_total), (-200.0, 800.0))
        self.assertFalse(self.chart.ref('tr_pr_wh_20').active)

    def test_update_existing_company(self):
        """A company set up before this module gets the corrections, but keeps the names the user changed."""
        env = self.env
        account = self._account('tr102997')
        renamed = self._account('tr646')
        tax = self.chart.ref('tr_s_wh_20_2_10')
        group = self.chart.ref('tr_tax_group_wh_20')
        old_tax = self.chart.ref('tr_pr_wh_20')
        # Back to the upstream state.
        account.with_context(lang='tr_TR').name = 'TAHSIL EDILMEYEN ÖDEMELER'
        renamed.with_context(lang='tr_TR').name = 'KUR FARKI GELİRLERİ'
        group.with_context(lang='tr_TR').name = 'ne zaman %-20'
        env.flush_all()
        env.cr.execute("UPDATE account_tax SET name = name - 'tr_TR' WHERE id = %s", [tax.id])
        new_tax = self.chart.ref('ov_tr_p_wh_rent_20')
        new_tax.unlink()
        self._account('tr480').unlink()
        old_tax.active = True
        self.company.account_journal_early_pay_discount_gain_account_id = self._account('tr679')
        env.invalidate_all()

        env['account.chart.template']._ov_l10n_tr_update_companies()

        self.assertEqual(account.with_context(lang='tr_TR').name, 'TAHSİL EDİLMEYEN ÖDEMELER')
        self.assertEqual(renamed.with_context(lang='tr_TR').name, 'KUR FARKI GELİRLERİ')
        self.assertEqual(group.with_context(lang='tr_TR').name, 'Tevkifat %-20')
        self.assertEqual(tax.with_context(lang='tr_TR').name, '%20 Tevkifatlı 2/10')
        self.assertEqual(tax.with_context(lang='en_US').name, 'WH 20% (2/10)')
        self.assertEqual(self.chart.ref('ov_tr_p_wh_rent_20').with_context(lang='tr_TR').name, 'Kira Stopajı %-20')
        self.assertEqual(self._account('tr480').with_context(lang='tr_TR').name, 'GELECEK YILLARA AİT GELİRLER')
        self.assertFalse(old_tax.active)
        self.assertEqual(self.company.account_journal_early_pay_discount_gain_account_id, self._account('tr649'))
        self.assertEqual(self._name_problems('account.account'), [])

    def test_existing_unaffected_earnings_account_is_kept(self):
        """A company that already has a current year earnings account does not get a second one."""
        self._account('tr590').account_type = 'equity'
        generic = self.company.get_unaffected_earnings_account()  # the generic 999999, as before this module
        self.assertEqual(generic.with_company(self.company).code, '999999')

        self.env['account.chart.template']._ov_l10n_tr_update_companies()

        self.assertEqual(self._account('tr590').account_type, 'equity')
        self.assertEqual(self.company.get_unaffected_earnings_account(), generic)
        self.assertEqual(generic.with_context(lang='tr_TR').name, 'CARİ YIL KÂRI VEYA ZARARI')
