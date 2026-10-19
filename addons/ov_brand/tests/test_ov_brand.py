from lxml import html

from odoo.tests import HttpCase, TransactionCase, tagged

from odoo.addons.ov_brand.tools import (
    BRAND_COLOR,
    BRAND_NAME_PARAM,
    DEFAULT_BRAND_NAME,
    SUPPORT_URL_PARAM,
    get_brand_name,
)


def visible_text(tree):
    """Return the text a visitor sees: everything but scripts and styles."""
    for node in tree.xpath('//script | //style'):
        node.drop_tree()
    return tree.text_content()


@tagged('post_install', '-at_install')
class TestOvBrandName(TransactionCase):

    def test_brand_name(self):
        self.assertEqual(get_brand_name(self.env), DEFAULT_BRAND_NAME)
        self.env['ir.config_parameter'].set_str(BRAND_NAME_PARAM, 'Test ERP')
        self.assertEqual(get_brand_name(self.env), 'Test ERP')
        self.env['ir.config_parameter'].set_str(BRAND_NAME_PARAM, False)
        self.assertEqual(get_brand_name(self.env), DEFAULT_BRAND_NAME)


@tagged('post_install', '-at_install')
class TestOvBrandPages(HttpCase):

    def assertNoOdooText(self, tree):
        self.assertNotIn('Odoo', visible_text(tree))

    def test_session_info(self):
        self.authenticate('admin', 'admin')
        info = self.make_jsonrpc_request('/web/session/get_session_info')
        self.assertEqual(info['ov_brand_name'], DEFAULT_BRAND_NAME)
        self.assertEqual(info['support_url'], '')

        params = self.env['ir.config_parameter']
        params.set_str(BRAND_NAME_PARAM, 'Test ERP')
        params.set_str(SUPPORT_URL_PARAM, 'https://support.example.com')
        info = self.make_jsonrpc_request('/web/session/get_session_info')
        self.assertEqual(info['ov_brand_name'], 'Test ERP')
        self.assertEqual(info['support_url'], 'https://support.example.com')

    def test_frontend_session_info(self):
        page = self.url_open('/web/login').text
        self.assertIn(f'"ov_brand_name": "{DEFAULT_BRAND_NAME}"', page)

    def test_login_page(self):
        response = self.url_open('/web/login')
        self.assertEqual(response.status_code, 200)
        tree = html.fromstring(response.content)
        self.assertEqual(tree.findtext('.//title'), DEFAULT_BRAND_NAME)
        self.assertEqual(tree.xpath("//link[@rel='shortcut icon']/@href"), ['/ov_brand/static/img/favicon.ico'])
        self.assertFalse(tree.xpath("//a[contains(@href, 'odoo.com')]"))
        self.assertNoOdooText(tree)

    def test_login_page_link_preview(self):
        # Open Graph tags are only rendered for links to the web client
        tree = html.fromstring(self.url_open('/web/login?redirect=/odoo').content)
        self.assertEqual(tree.xpath("//meta[@property='og:site_name']/@content"), [DEFAULT_BRAND_NAME])
        self.assertEqual(tree.xpath("//meta[@property='og:title']/@content"), [DEFAULT_BRAND_NAME])
        image = tree.xpath("//meta[@property='og:image']/@content")
        self.assertEqual(len(image), 1)
        self.assertTrue(image[0].endswith('/ov_brand/static/img/icon_512.png'))
        self.assertFalse(tree.xpath("//meta[@property='og:description' or @name='twitter:site']"))
        metas = ' '.join(tree.xpath('//meta/@content'))
        self.assertNotIn('Odoo', metas)

    def test_brand_name_parameter(self):
        self.env['ir.config_parameter'].set_str(BRAND_NAME_PARAM, 'Test ERP')
        tree = html.fromstring(self.url_open('/web/login').content)
        self.assertEqual(tree.findtext('.//title'), 'Test ERP')

    def test_webmanifest(self):
        manifest = self.url_open('/web/manifest.webmanifest').json()
        self.assertEqual(manifest['name'], DEFAULT_BRAND_NAME)
        self.assertEqual(manifest['theme_color'], BRAND_COLOR)
        self.assertEqual(manifest['background_color'], BRAND_COLOR)
        self.assertEqual(
            [icon['src'] for icon in manifest['icons']],
            ['/ov_brand/static/img/icon_192.png', '/ov_brand/static/img/icon_512.png'],
        )
        for icon in manifest['icons']:
            self.assertEqual(self.url_open(icon['src']).status_code, 200)

        # The name set in General Settings still wins
        self.env['ir.config_parameter'].set_str('web.web_app_name', 'My Company')
        manifest = self.url_open('/web/manifest.webmanifest').json()
        self.assertEqual(manifest['name'], 'My Company')

    def test_scoped_app_manifest(self):
        response = self.url_open('/web/manifest.scoped_app_manifest?app_id=test&path=/test&app_name=Test')
        self.assertEqual(response.headers['Content-Type'], 'application/manifest+json')
        manifest = response.json()
        self.assertEqual(manifest['name'], 'Test')
        self.assertEqual(manifest['theme_color'], BRAND_COLOR)
        self.assertEqual(manifest['background_color'], BRAND_COLOR)
        # An app without its own icon gets the product icon
        self.assertEqual([icon['src'] for icon in manifest['icons']], ['/ov_brand/static/img/icon_192.png'])

    def test_offline_page(self):
        response = self.url_open('/odoo/offline')
        self.assertEqual(response.status_code, 200)
        self.assertNoOdooText(html.fromstring(response.content))

    def test_webclient_page(self):
        self.authenticate('admin', 'admin')
        response = self.url_open('/odoo')
        self.assertEqual(response.status_code, 200)
        tree = html.fromstring(response.content)
        self.assertEqual(tree.findtext('.//title'), DEFAULT_BRAND_NAME)
        self.assertEqual(tree.xpath("//meta[@name='theme-color']/@content"), [BRAND_COLOR])
        self.assertEqual(tree.xpath("//link[@rel='apple-touch-icon']/@href"), ['/ov_brand/static/img/icon_ios.png'])

    def test_webclient_js(self):
        # Fails on any JS error, e.g. a broken patch or template extension.
        # A fixed action: with mail installed, the default app (Discuss) can put
        # a conversation name in the title; "OdooBot" was seen (T2.5).
        self.browser_js('/odoo/action-base.action_res_users', """
            const { session } = odoo.loader.modules.get("@web/session");
            const { registry } = odoo.loader.modules.get("@web/core/registry");
            if (session.ov_brand_name !== "%s") {
                throw new Error(`unexpected brand name: ${session.ov_brand_name}`);
            }
            if (registry.category("user_menuitems").contains("support")) {
                throw new Error("the Help item should be hidden without ov_brand.support_url");
            }
            if (document.title.includes("Odoo")) {
                throw new Error(`unexpected title: ${document.title}`);
            }
            console.log("test successful");
        """ % DEFAULT_BRAND_NAME, login='admin')

    def test_login_page_js(self):
        # The patches also run in the public bundle (lazy loaded after the page).
        # Pending jobs of other modules are fine: test tours wait for their own bundle.
        self.browser_js('/web/login', """
            const ours = [...odoo.loader.failed, ...odoo.loader.jobs].filter((name) => name.startsWith("@ov_brand/"));
            if (odoo.loader.failed.size || ours.length) {
                throw new Error(`modules not loaded: ${[...odoo.loader.failed, ...ours]}`);
            }
            if (document.querySelector(".oe_login_form").classList.contains("d-none")) {
                throw new Error("the login form is hidden");
            }
            console.log("test successful");
        """, ready="""
            odoo.loader.modules.has("@ov_brand/public/error_notifications")
            && !document.querySelector(".oe_login_form").classList.contains("d-none")
        """)


@tagged('post_install', '-at_install')
class TestOvBrandEnterpriseApps(TransactionCase):

    def test_apps_to_buy_hidden(self):
        # The apps of the paid edition stay in the database but are never listed
        self.env.cr.execute("SELECT count(*) FROM ir_module_module WHERE to_buy")
        self.assertTrue(self.env.cr.fetchone()[0])
        self.assertFalse(self.env['ir.module.module'].search_count([('to_buy', '=', True)]))
