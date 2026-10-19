{
    'name': 'Invoicing Branding',
    'version': '20.0.1.0.0',
    'summary': "Removes the publisher's name and logo from invoices",
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'ov_brand',
        'account',
    ],
    'data': [
        'security/ir.access.csv',
        'views/report_invoice.xml',
        'views/terms_template.xml',
    ],
    'auto_install': True,
}
