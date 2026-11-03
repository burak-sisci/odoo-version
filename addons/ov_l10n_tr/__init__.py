from . import models


def post_init_hook(env):
    env['account.chart.template']._ov_l10n_tr_update_companies()
    env['res.partner']._ov_l10n_tr_recompute_is_company()
