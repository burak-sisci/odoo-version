from unittest.mock import patch

from odoo.tests import HttpCase, tagged
from odoo.tests.common import JsonRpcException

CONTROLLER = 'odoo.addons.html_editor.controllers.main'


@tagged('post_install', '-at_install')
class TestOvBrandHtmlEditor(HttpCase):

    def setUp(self):
        super().setUp()
        self.authenticate('admin', 'admin')

    def test_online_services_refused(self):
        calls = [
            ('/html_editor/generate_text', {'prompt': 'Hello', 'conversation_history': []}),
            ('/html_editor/google_translate', {'originalText': 'Merhaba', 'targetLang': 'en'}),
            ('/html_editor/save_library_media', {'media': {'1': {'query': 'test'}}}),
        ]
        with patch(f'{CONTROLLER}.iap_tools.iap_jsonrpc') as iap_jsonrpc, patch(f'{CONTROLLER}.requests.post') as post:
            for route, params in calls:
                with self.subTest(route=route), self.assertRaises(JsonRpcException) as error:
                    self.make_jsonrpc_request(route, params)
                self.assertEqual(str(error.exception), 'odoo.exceptions.UserError')
            self.assertEqual(
                self.make_jsonrpc_request('/html_editor/media_library_search', {'query': 'test', 'offset': 0}),
                {'media': [], 'results': 0},
            )
        iap_jsonrpc.assert_not_called()
        post.assert_not_called()

    def test_editor_js(self):
        self.browser_js('/odoo', """
            const ours = [...odoo.loader.failed, ...odoo.loader.jobs].filter((name) => name.startsWith("@ov_brand_html_editor/"));
            if (odoo.loader.failed.size || ours.length) {
                throw new Error(`modules not loaded: ${[...odoo.loader.failed, ...ours]}`);
            }
            for (const name of ["@ov_brand_html_editor/editor/editor_patch", "@ov_brand_html_editor/media_dialog/image_selector_patch"]) {
                if (!odoo.loader.modules.has(name)) {
                    throw new Error(`module missing: ${name}`);
                }
            }
            const { ImageSelector } = odoo.loader.modules.get("@html_editor/main/media/media_dialog/image_selector");
            ImageSelector.prototype.fetchLibraryMedia.call({ state: { needle: "test" } }, 0).then(({ media }) => {
                if (media.length) {
                    console.error("the media library should give no result");
                } else {
                    console.log("test successful");
                }
            });
        """, login='admin')
