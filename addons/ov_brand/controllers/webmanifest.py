import json
import re

from odoo import http
from odoo.http import request

from odoo.addons.ov_brand.tools import (
    BRAND_COLOR,
    IMG_PATH,
    UPSTREAM_WEB_PATH,
    WEB_PATH,
    get_brand_name,
    web_path,
)
from odoo.addons.web.controllers.webmanifest import WebManifest

# Quoted web client paths in the service worker script
SCRIPT_UPSTREAM_WEB_PATH = re.compile(rf'''(["'`]){UPSTREAM_WEB_PATH}(?=["'`/?])''')


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
        manifest['scope'] = web_path(manifest['scope'])
        manifest['start_url'] = web_path(manifest['start_url'])
        for shortcut in manifest['shortcuts']:
            shortcut['url'] = web_path(shortcut['url'])
        if 'share_target' in manifest:
            manifest['share_target']['action'] = web_path(manifest['share_target']['action'])
        return manifest

    @http.route()
    def service_worker(self):
        # Scope of the web client path (T2.4). The paths in the script follow,
        # also those of the modules extending it (mail).
        response = super().service_worker()
        response.set_data(SCRIPT_UPSTREAM_WEB_PATH.sub(rf'\1{WEB_PATH}', response.get_data(as_text=True)))
        response.headers['Service-Worker-Allowed'] = WEB_PATH
        return response

    @http.route([f'{UPSTREAM_WEB_PATH}/offline', f'{WEB_PATH}/offline'])
    def offline(self):
        return super().offline()

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
