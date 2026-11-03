from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    # 20.0.1.1.0: a Turkish partner with a citizen number (TCKN) is a natural person.
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.partner']._ov_l10n_tr_recompute_is_company()
    # The country is a no-update record: data/res_country_data.xml sets the
    # label only when the module is installed.
    env.ref('base.tr').vat_label = 'VKN/TCKN'
