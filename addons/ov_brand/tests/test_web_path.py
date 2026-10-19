from urllib.parse import parse_qs, urlsplit

from lxml import html

from odoo.tests import HttpCase, new_test_user, tagged

from odoo.addons.ov_brand.tools import WEB_PATH


@tagged('post_install', '-at_install')
class TestOvBrandWebPath(HttpCase):

    def assertRedirect(self, url, location):
        response = self.url_open(url, allow_redirects=False)
        self.assertEqual(response.status_code, 303)
        self.assertEqual(urlsplit(response.headers['Location'])._replace(scheme='', netloc='').geturl(), location)

    def test_upstream_path_redirected(self):
        # The server still builds links with the upstream path, users saved some
        self.authenticate('admin', 'admin')
        self.assertRedirect('/odoo', WEB_PATH)
        self.assertRedirect('/odoo/res.partner/3?debug=1', f'{WEB_PATH}/res.partner/3?debug=1')
        self.authenticate(None, None)
        self.assertRedirect('/odoo/settings', f'{WEB_PATH}/settings')

    def test_web_client(self):
        response = self.url_open(f'{WEB_PATH}/settings', allow_redirects=False)
        location = urlsplit(response.headers['Location'])
        self.assertEqual(location.path, '/web/login')
        self.assertEqual(urlsplit(parse_qs(location.query)['redirect'][0]).path, f'{WEB_PATH}/settings')

        self.authenticate('admin', 'admin')
        response = self.url_open(f'{WEB_PATH}/res.partner/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path_url, f'{WEB_PATH}/res.partner/3')
        self.assertIn('odoo.__session_info__', response.text)

    def test_login(self):
        new_test_user(self.env, 'ov_internal')

        def login(**params):
            self.authenticate(None, None)
            return self.url_open('/web/login', data={
                'login': 'ov_internal',
                'password': 'ov_internal',
                'csrf_token': self.csrf_token(),
                **params,
            })

        self.assertEqual(login().request.path_url, WEB_PATH)
        self.assertEqual(login(redirect=f'{WEB_PATH}/settings').request.path_url, f'{WEB_PATH}/settings')
        self.assertEqual(login(redirect='/odoo/settings').request.path_url, f'{WEB_PATH}/settings')

    def test_login_page_link_preview(self):
        # Links to the web client get a preview with the name of the action
        tree = html.fromstring(self.url_open(f'/web/login?redirect={WEB_PATH}/settings').content)
        self.assertEqual(tree.xpath("//meta[@property='og:title']/@content"), ['Settings'])
        og_url = tree.xpath("//meta[@property='og:url']/@content")
        self.assertEqual(len(og_url), 1)
        self.assertEqual(urlsplit(og_url[0]).path, f'{WEB_PATH}/settings')
        self.assertEqual(tree.xpath("//input[@name='redirect']/@value"), [f'{WEB_PATH}/settings'])

    def test_webmanifest(self):
        self.authenticate('admin', 'admin')
        manifest = self.url_open('/web/manifest.webmanifest').json()
        self.assertEqual(manifest['scope'], WEB_PATH)
        self.assertEqual(manifest['start_url'], WEB_PATH)
        for shortcut in manifest['shortcuts']:
            self.assertTrue(shortcut['url'].startswith(f'{WEB_PATH}?menu_id='), shortcut['url'])
        if 'share_target' in manifest:
            self.assertEqual(manifest['share_target']['action'], f'{WEB_PATH}?share_target=trigger')

    def test_service_worker(self):
        self.authenticate('admin', 'admin')
        response = self.url_open('/web/service-worker.js')
        self.assertEqual(response.headers['Service-Worker-Allowed'], WEB_PATH)
        self.assertIn(f'const homepageURL = "{WEB_PATH}";', response.text)
        self.assertNotRegex(response.text, r'''["'`]/odoo\b''')
        # The offline page the service worker caches, at both paths
        for path in (f'{WEB_PATH}/offline', '/odoo/offline'):
            self.assertEqual(self.url_open(path).status_code, 200)

    def test_web_path_js(self):
        self.browser_js('/odoo/action-base.action_res_users', """
            const { router } = odoo.loader.modules.get("@web/core/browser/router");
            if (!location.pathname.startsWith("/app/")) {
                throw new Error(`unexpected path: ${location.pathname}`);
            }
            if (!router.current.action) {
                throw new Error("the router did not read the action from the URL");
            }
            if (router.stateToUrl({ action: "settings" }) !== "/app/settings") {
                throw new Error(`unexpected URL: ${router.stateToUrl({ action: "settings" })}`);
            }
            const hrefs = [...document.querySelectorAll(".o_navbar a[href]")].map((a) => a.getAttribute("href"));
            if (!hrefs.some((href) => href.startsWith("/app/")) || hrefs.some((href) => href.startsWith("/odoo"))) {
                throw new Error(`unexpected menu links: ${hrefs}`);
            }
            // An internal link with the upstream path opens in place, without reloading the page
            window.ovNotReloaded = true;
            const link = document.createElement("a");
            link.href = "/odoo/settings";
            document.body.appendChild(link);
            link.click();
            const start = Date.now();
            const interval = setInterval(() => {
                if (location.pathname === "/app/settings" && document.querySelector(".o_setting_right_pane")) {
                    clearInterval(interval);
                    if (!window.ovNotReloaded) {
                        console.error("the page was reloaded");
                    } else {
                        console.log("test successful");
                    }
                } else if (Date.now() - start > 10000) {
                    clearInterval(interval);
                    console.error(`internal link not followed: ${location.pathname}`);
                }
            }, 100);
        """, ready="!!document.querySelector('.o_list_view')", login='admin')
