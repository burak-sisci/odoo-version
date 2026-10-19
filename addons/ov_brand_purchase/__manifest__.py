{
    'name': 'Purchase Branding',
    'version': '20.0.1.0.0',
    'summary': "Removes the publisher's advertisement from the purchase portal",
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'ov_brand',
        'purchase',
    ],
    'data': [
        'security/ir.access.csv',
        'views/portal_templates.xml',
    ],
    'auto_install': True,
}
