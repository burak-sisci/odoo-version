{
    'name': 'Mail Branding',
    'version': '20.0.1.0.0',
    'summary': "Removes the publisher's name from e-mails and stops its weekly report",
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'ov_brand',
        'mail',
    ],
    'data': [
        'security/ir.access.csv',
        'data/ir_cron_data.xml',
        'data/res_partner_data.xml',
        'views/mail_templates.xml',
    ],
    'auto_install': True,
}
