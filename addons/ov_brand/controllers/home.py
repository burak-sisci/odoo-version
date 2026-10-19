from odoo import http
from odoo.http import request

from odoo.addons.ov_brand.tools import WEB_PATH, upstream_path, web_path
from odoo.addons.web.controllers.home import Home


class OvBrandHome(Home):

    @http.route([
        '/web', '/odoo', '/odoo/<path:subpath>', '/scoped_app/<path:subpath>',
        WEB_PATH, f'{WEB_PATH}/<path:subpath>',
    ])
    def web_client(self, s_action=None, **kw):
        # The upstream path keeps working: the server still builds links with
        # it (e-mails, notifications, redirections) and users may have saved it
        path = request.httprequest.path
        if web_path(path) != path:
            query = request.httprequest.query_string.decode()
            return request.redirect(web_path(path) + (f'?{query}' if query else ''))
        return super().web_client(s_action=s_action, **kw)

    def _login_redirect(self, uid, redirect=None):
        return web_path(super()._login_redirect(uid, redirect=redirect))

    @http.route()
    def web_login(self, redirect=None, **kw):
        # The login page recognizes the links to the web client by the upstream
        # path, to give them a link preview
        response = super().web_login(redirect=upstream_path(redirect), **kw)
        if response.is_qweb and response.qcontext.get('og_url'):
            response.qcontext['og_url'] = web_path(response.qcontext['og_url'])
        return response
