{
    'name': 'Digest Branding',
    'version': '20.0.1.0.0',
    'summary': "Removes the publisher's name, tips and app banner from the digest e-mails",
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'ov_brand',
        'digest',
    ],
    'data': [
        'security/ir.access.csv',
        'data/digest_data.xml',
        'views/digest_templates.xml',
    ],
    'auto_install': True,
}
