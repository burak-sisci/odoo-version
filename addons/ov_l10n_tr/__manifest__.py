{
    'name': 'Turkish Accounting Corrections',
    'version': '20.0.1.0.0',
    'summary': 'Corrects the names, accounts and taxes of the Turkish chart of accounts',
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'l10n_tr',
    ],
    'data': [
        'security/ir.access.csv',
    ],
    'post_init_hook': 'post_init_hook',
    'auto_install': True,
}
