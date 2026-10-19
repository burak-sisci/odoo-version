{
    'name': 'Mail Branding',
    'version': '20.0.1.0.0',
    'summary': 'Turns off the weekly database report sent to the publisher',
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'ov_brand',
        'mail',
    ],
    'data': [
        'security/ir.access.csv',
        'data/ir_cron_data.xml',
    ],
    'auto_install': True,
}
