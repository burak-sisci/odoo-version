"""External request test (T2.7): helpers.

The test framework blocks the requests of the tests to outside hosts (Python,
requests library) and answers those of the browser itself. These helpers
record them, to assert that none goes to the publisher's domains. The
installation and the other libraries are watched by tools/netguard.py, which
tools/run_tests.py runs Odoo with.
"""
from urllib.parse import urlsplit

from odoo.tests.common import HOST

# Same list as tools/netguard.py
PUBLISHER_DOMAINS = ('odoo.com', 'odoocdn.com', 'odoo.sh')


def is_publisher_url(url):
    host = (urlsplit(url).hostname or '').rstrip('.').lower()
    return any(host == domain or host.endswith(f'.{domain}') for domain in PUBLISHER_DOMAINS)


class ExternalRequestsMixin:
    """Mixin of the test cases that record the external requests: in Python
    through the requests library, and in the browser (HttpCase)."""

    @classmethod
    def setUpClass(cls):
        # The test framework starts sending the requests to the handler below
        # in its own set-up
        cls.external_requests = []
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self.external_requests.clear()

    @classmethod
    def _request_handler(cls, s, r, /, **kw):
        url = urlsplit(r.url)
        if url.hostname not in (HOST, 'localhost') and url.scheme != 'file':
            cls.external_requests.append(('python', r.url))
        return super()._request_handler(s, r, **kw)

    def fetch_proxy(self, url):
        self.external_requests.append(('browser', url))
        return super().fetch_proxy(url)

    def assertNoPublisherRequest(self):
        found = [f'{source}: {url}' for source, url in self.external_requests if is_publisher_url(url)]
        self.assertFalse(found, "Requests to the publisher's domains:\n" + "\n".join(found))
