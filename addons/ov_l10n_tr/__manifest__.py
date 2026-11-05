{
    'name': 'Turkey - Localization',
    'version': '20.0.1.3.0',
    'summary': 'Corrects the Turkish chart of accounts and taxes; tax ID, registry numbers, districts and documents',
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'base_address_extended',
        'l10n_tr',
        'portal',
    ],
    'data': [
        'security/ir.access.csv',
        'data/res.city.csv',
        'views/res_partner_views.xml',
        'views/report_templates.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'auto_install': True,
}
