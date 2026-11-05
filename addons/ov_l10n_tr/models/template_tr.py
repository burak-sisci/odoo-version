import re

from odoo import models
from odoo.tools.translate import TranslationImporter

from odoo.addons.account.models.chart_template import template

TEMPLATE_CODE = 'tr'
MODULE = 'ov_l10n_tr'
UPSTREAM_MODULE = 'l10n_tr'
# Models whose template records this module corrects, in loading order.
CORRECTED_MODELS = ('account.tax.group', 'account.account', 'account.tax')
# Accounts whose upstream type is receivable or payable. Such an account
# needs a due date on every journal item, so a tax cannot be posted to it.
# Their type is corrected while they have no journal items.
TYPE_CORRECTIONS = ('tr193', 'tr360')
# Name of the generic current year earnings account (999999) that a company
# set up before this module keeps; the accounting module has no Turkish name
# for it.
GENERIC_EARNINGS_XMLID = 'unaffected_earnings_account'
GENERIC_EARNINGS_NAME = 'CARİ YIL KÂRI VEYA ZARARI'


def _plain(value):
    """Return the text of a translated value, without HTML tags."""
    return re.sub(r'<[^>]+>', '', value or '').strip()


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    # The method names differ from the upstream ones (``_get_tr_*``) so that
    # both are registered; templates of one model are applied by method name,
    # and these come after the upstream ones.

    @template(TEMPLATE_CODE, 'res.company')
    def _ov_l10n_tr_res_company(self):
        return {
            self.env.company.id: {
                # Without these, the generic accounts 999997/999998 and two
                # 999xxx accounts outside the uniform chart are created.
                'account_journal_early_pay_discount_loss_account_id': 'tr611',
                'account_journal_early_pay_discount_gain_account_id': 'tr649',
                'default_cash_difference_income_account_id': 'tr679',
                'default_cash_difference_expense_account_id': 'tr689',
                # Turkish documents write the total in words ("Yalnız: ...").
                'display_invoice_amount_total_words': True,
            },
        }

    @template(TEMPLATE_CODE, 'account.account')
    def _ov_l10n_tr_account_account(self):
        data = self._parse_csv(TEMPLATE_CODE, 'account.account', module=MODULE)
        for xmlid in TYPE_CORRECTIONS:
            account = self.ref(xmlid, raise_if_not_found=False)
            if account and self.env['account.move.line'].search_count([('account_id', '=', account.id)], limit=1):
                data[xmlid].pop('account_type', None)
        if self._ov_l10n_tr_can_use_590():
            # The period's net profit holds the current year earnings, as in
            # other charts that have such an account; otherwise a generic
            # 999999 account is created.
            data['tr590'] = {'account_type': 'equity_unaffected'}
        return data

    @template(TEMPLATE_CODE, 'account.tax.group')
    def _ov_l10n_tr_account_tax_group(self):
        return self._parse_csv(TEMPLATE_CODE, 'account.tax.group', module=MODULE)

    @template(TEMPLATE_CODE, 'account.tax')
    def _ov_l10n_tr_account_tax(self):
        data = self._parse_csv(TEMPLATE_CODE, 'account.tax', module=MODULE)
        self._deref_account_tags(TEMPLATE_CODE, data)
        return data

    def _ov_l10n_tr_can_use_590(self):
        """Return whether account 590 may become the current year earnings account.

        A company keeps the account it already has (usually the generic
        999999 of a company set up before this module), so that it never has
        two of them.
        """
        company = self.env.company
        current = self.env['account.account'].with_company(company).search([
            *self.env['account.account']._check_company_domain(company),
            ('account_type', '=', 'equity_unaffected'),
        ])
        return not current or current == self.ref('tr590', raise_if_not_found=False)

    def _ov_l10n_tr_update_companies(self):
        """Apply the corrections to the companies that already use the Turkish chart.

        New companies get them when the chart is loaded. For existing ones,
        the data of this module is loaded the way the accounting module does
        it when a localization module is installed (new records are created,
        existing ones updated), then the Turkish names are corrected.
        """
        companies = self.env['res.company'].search(
            [('chart_template', '=', TEMPLATE_CODE)], order='parent_path',
        )
        for company in companies:
            chart = self.with_company(company)
            data = chart._get_chart_template_data(TEMPLATE_CODE, module=MODULE)
            data.pop('template_data', None)
            chart._pre_reload_data(company, {}, data, force_update=True)
            chart._pre_load_data(TEMPLATE_CODE, company, {}, data)
            chart._load_data(data)
        for company in companies.filtered(lambda c: not c.parent_id):
            self.with_company(company)._ov_l10n_tr_update_translations(company)

    def _ov_l10n_tr_update_translations(self, company):
        """Write the corrected Turkish names of ``company``'s template records.

        A name is replaced only while it is still the upstream one, the
        English one, or missing: a name the user changed is kept. The loader
        of the accounting module never overwrites an existing translation.
        """
        langs = [code for code, _name in self.env['res.lang'].get_installed() if code.split('_')[0] == 'tr']
        if not langs:
            return
        importer = TranslationImporter(self.env.cr, verbose=False)
        for model in CORRECTED_MODELS:
            ours = self._parse_csv(TEMPLATE_CODE, model, module=MODULE)
            upstream = self._parse_csv(TEMPLATE_CODE, model, module=UPSTREAM_MODULE)
            for xmlid, values in ours.items():
                record = self.ref(xmlid, raise_if_not_found=False)
                if not record:
                    continue
                for key, value in values.items():
                    fname, _sep, lang_code = key.partition('@')
                    if lang_code != 'tr':
                        continue
                    stored = record.with_context(active_test=False)._get_stored_translations(fname) or {}
                    old_values = {_plain(upstream.get(xmlid, {}).get(key)), _plain(dict.get(stored, 'en_US')), ''}
                    for lang in langs:
                        current = dict.get(stored, lang)
                        if current is None or _plain(current) in old_values:
                            importer.model_translations[model][fname][self.company_xmlid(xmlid, company)][lang] = value
        generic = self.ref(GENERIC_EARNINGS_XMLID, raise_if_not_found=False)
        if generic:
            stored = generic._get_stored_translations('name') or {}
            for lang in langs:
                if dict.get(stored, lang) is None:
                    xmlid = self.company_xmlid(GENERIC_EARNINGS_XMLID, company)
                    importer.model_translations['account.account']['name'][xmlid][lang] = GENERIC_EARNINGS_NAME
        importer.save(force_overwrite=True)
        self.env.invalidate_all()
