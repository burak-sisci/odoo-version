from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    # 20.0.1.2.0: districts (ilçe) and the Turkish address settings.
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.country']._ov_l10n_tr_setup()
    env['res.partner']._ov_l10n_tr_match_districts()
