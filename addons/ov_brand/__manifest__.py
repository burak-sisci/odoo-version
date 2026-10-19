{
    'name': 'Branding',
    'version': '20.0.1.0.0',
    'summary': 'Product name, logo and icons of the web client',
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'web',
        'base_setup',
        'base_import_module',
        'remove_odoo_enterprise',
    ],
    'data': [
        'security/ir.access.csv',
        'views/webclient_templates.xml',
        'views/ir_module_views.xml',
        'views/report_templates.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'web/static/src/scss/primary_variables.scss', 'ov_brand/static/src/scss/primary_variables.scss'),
        ],
        'web.assets_backend': [
            'ov_brand/static/src/brand.js',
            'ov_brand/static/src/core/**/*',
            'ov_brand/static/src/webclient/**/*',
        ],
        'web.assets_frontend': [
            'ov_brand/static/src/brand.js',
            'ov_brand/static/src/core/**/*',
            'ov_brand/static/src/public/**/*',
        ],
    },
}
