from odoo import http
from odoo.exceptions import UserError
from odoo.http import request

from odoo.addons.html_editor.controllers.main import HTML_Editor


class HtmlEditor(HTML_Editor):
    # These services of the publisher receive the edited text or the search
    # terms, with the database identifier (T2.3, KVKK). The editor no longer
    # offers them; a direct call is refused without reaching the network.

    def _ov_service_unavailable(self):
        raise UserError(request.env._("This service is not available in this product."))

    @http.route()
    def generate_text(self, prompt, conversation_history):
        self._ov_service_unavailable()

    @http.route()
    def google_translate(self, originalText, targetLang):
        self._ov_service_unavailable()

    @http.route()
    def save_library_media(self, media):
        self._ov_service_unavailable()

    @http.route()
    def media_library_search(self, **params):
        # Same answer as an empty search, the media dialog shows no illustrations
        return {'media': [], 'results': 0}
