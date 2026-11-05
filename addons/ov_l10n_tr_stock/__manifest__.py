{
    'name': 'Turkey - Delivery Slips',
    'version': '20.0.1.0.0',
    'summary': 'Turkish delivery slip (sevk irsaliyesi) content',
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'ov_l10n_tr',
    ],
    'data': [
        'security/ir.access.csv',
        'views/report_deliveryslip.xml',
    ],
    'auto_install': True,
}
