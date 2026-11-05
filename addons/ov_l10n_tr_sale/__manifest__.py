{
    'name': 'Turkey - Sales Documents',
    'version': '20.0.1.0.0',
    'summary': 'Turkish quotations, sales orders and pro forma invoices',
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'ov_l10n_tr',
    ],
    'data': [
        'security/ir.access.csv',
        'views/report_saleorder.xml',
    ],
    'auto_install': True,
}
