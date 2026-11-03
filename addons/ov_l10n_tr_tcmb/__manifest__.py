{
    'name': 'Turkey - TCMB Exchange Rates',
    'version': '20.0.1.0.0',
    'summary': 'Daily exchange rates of the Central Bank of the Republic of Türkiye (TCMB)',
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'ov_l10n_tr',
    ],
    'data': [
        'security/ir.access.csv',
        'data/ir_cron_data.xml',
        'wizard/tcmb_rate_import_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'auto_install': True,
}
