import logging

import requests

from odoo.tests import HttpCase, TransactionCase, tagged
from odoo.tools import mute_logger

from odoo.addons.ov_brand.tests.external_requests import (
    ExternalRequestsMixin,
    is_publisher_url,
)
from odoo.addons.ov_brand.tools import WEB_PATH

_logger = logging.getLogger(__name__)

# An outside address that is not the publisher's: it shows that the recording works
PROBE_URL = 'https://example.com/ov_external_probe.png'
PAGE_CODE = """(async () => {
    // A request to an outside host, recorded like the page's own
    await new Promise((resolve) => {
        const probe = new Image();
        probe.onload = probe.onerror = resolve;
        probe.src = "%s";
    });
    // Time for the lazy loaded assets and pictures of the page
    await new Promise((resolve) => setTimeout(resolve, 1000));
    console.log("test successful");
})()""" % PROBE_URL


@tagged('post_install', '-at_install', 'ov_external')
class TestExternalRequestsRecorder(ExternalRequestsMixin, TransactionCase):

    def test_publisher_domains(self):
        for url in ('https://www.odoo.com/help', 'https://gmail.api.odoo.com/x', 'http://odoo.com',
                    'https://download.odoocdn.com/x', 'https://x.odoo.sh/', 'https://ODOO.COM./'):
            self.assertTrue(is_publisher_url(url), url)
        for url in ('https://example.com/odoo.com', 'https://notodoo.com/', 'https://odoo-community.org/',
                    'https://odoo.com.example.com/', '/odoo/action-1', 'mailto:odoo.com'):
            self.assertFalse(is_publisher_url(url), url)

    def test_python_request_recorded(self):
        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.get(PROBE_URL, timeout=10)
        self.assertEqual(self.external_requests, [('python', PROBE_URL)])
        self.assertNoPublisherRequest()


@tagged('post_install', '-at_install', 'ov_external')
class TestExternalRequestsCrons(ExternalRequestsMixin, TransactionCase):

    def test_crons(self):
        # The scheduled jobs run outside the tests in production; here every
        # one of them, active or not, runs once. Their errors in an empty
        # test database do not matter, only their requests.
        crons = self.env['ir.cron'].with_context(active_test=False).search([])
        failed = []
        for cron in crons:
            try:
                with self.env.cr.savepoint(), mute_logger('odoo.addons.base.models.ir_cron'):
                    cron.method_direct_trigger()
            except Exception as error:  # noqa: BLE001
                failed.append(f'{cron.name}: {error.__cause__ or error}')
        _logger.info("%d scheduled jobs run, %d failed in the test database%s",
                     len(crons), len(failed), ''.join(f'\n  {line}' for line in failed))
        self.assertTrue(crons)
        self.assertNoPublisherRequest()


@tagged('post_install', '-at_install', 'ov_external')
class TestExternalRequestsPages(ExternalRequestsMixin, HttpCase):

    def test_pages(self):
        # The page's own requests (pictures, fonts, scripts) and the server's
        # while it serves them
        pages = [
            ('/web/login', None),
            (WEB_PATH, 'admin'),
            (f'{WEB_PATH}/settings', 'admin'),
            (f'{WEB_PATH}/action-base.open_module_tree', 'admin'),
        ]
        if 'discuss.channel' in self.env:
            pages.append((f'{WEB_PATH}/discuss', 'admin'))
        if self.env.ref('portal.portal_my_home', raise_if_not_found=False):
            pages.append(('/my', 'admin'))
        for url, login in pages:
            with self.subTest(url=url):
                # The web client tells when it has started; the other pages are
                # ready when loaded
                ready = 'odoo.isReady' if url.startswith(WEB_PATH) else ''
                self.browser_js(url, PAGE_CODE, ready=ready, login=login)
        self.assertEqual(self.external_requests.count(('browser', PROBE_URL)), len(pages))
        self.assertNoPublisherRequest()
