import json

from odoo import http
from odoo.http import request

from odoo.addons.ov_brand.tools import BRAND_COLOR, IMG_PATH, get_brand_name
from odoo.addons.web.controllers.webmanifest import WebManifest


class OvBrandWebManifest(WebManifest):

    def _get_webmanifest(self):
        manifest = super()._get_webmanifest()
        # web.web_app_name (General Settings) still wins over the product name
        if not request.env['ir.config_parameter'].sudo().get_str('web.web_app_name'):
            manifest['name'] = get_brand_name(request.env)
        manifest['background_color'] = BRAND_COLOR
        manifest['theme_color'] = BRAND_COLOR
        manifest['icons'] = [{
            'src': f'{IMG_PATH}/icon_{size}.png',
            'sizes': f'{size}x{size}',
            'type': 'image/png',
        } for size in (192, 512)]
        return manifest

    @http.route()
    def scoped_app_manifest(self, app_id, path, app_name=''):
        # Manifest of a single app installed from the browser
        response = super().scoped_app_manifest(app_id, path, app_name=app_name)
        manifest = json.loads(response.get_data())
        manifest['background_color'] = BRAND_COLOR
        manifest['theme_color'] = BRAND_COLOR
        return request.make_json_response(manifest, {
            'Content-Type': 'application/manifest+json',
        })

    def _icon_path(self):
        return 'ov_brand/static/img/icon_192.png'
