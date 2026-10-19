{
    'name': 'Editor Branding',
    'version': '20.0.1.0.0',
    'summary': "Turns off the publisher's online services of the text editor",
    'author': 'burak-sisci',
    'license': 'AGPL-3',
    'depends': [
        'ov_brand',
        'html_editor',
    ],
    'data': [
        'security/ir.access.csv',
    ],
    'assets': {
        'html_editor.assets_editor': [
            'ov_brand_html_editor/static/src/editor/**/*',
        ],
        'html_editor.assets_media_dialog': [
            'ov_brand_html_editor/static/src/media_dialog/**/*',
        ],
    },
    'auto_install': True,
}
