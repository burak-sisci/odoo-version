{
    'name': 'Turkey - Localization',
    'version': '20.0.1.1.0',
    'summary': 'Corrects the Turkish chart of accounts and taxes; Turkish tax ID and registry numbers',
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'l10n_tr',
    ],
    'data': [
        'security/ir.access.csv',
        'data/res_country_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'auto_install': True,
}
