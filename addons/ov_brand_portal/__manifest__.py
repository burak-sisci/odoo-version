{
    'name': 'Portal Branding',
    'version': '20.0.1.0.0',
    'summary': "Removes the publisher's name and logo from the customer portal",
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'ov_brand',
        'portal',
        'auth_totp_portal',
    ],
    'data': [
        'security/ir.access.csv',
        'views/portal_templates.xml',
    ],
    'auto_install': True,
}
