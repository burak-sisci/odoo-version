from urllib.parse import urlsplit, urlunsplit

BRAND_NAME_PARAM = 'ov_brand.name'
SUPPORT_URL_PARAM = 'ov_brand.support_url'

# Product name (D-014). The working name of the repository must not reach
# users (D-007).
DEFAULT_BRAND_NAME = 'Nexus'
# Same value as $o-community-color in static/src/scss/primary_variables.scss
BRAND_COLOR = '#1f5f8b'
IMG_PATH = '/ov_brand/static/img'

# Modules of the publisher's online services (T2.3). Every new database gets them
# (auto_install on web and base_setup); ov_brand removes them together with the
# modules depending on them: SMS, partner autocomplete, lead enrichment and lead
# mining, postal mail, the subscription page.
ONLINE_SERVICE_MODULES = ('iap', 'mysubscription')

# Path of the web client (T2.4). Upstream serves it at /odoo; ov_brand serves it
# here and redirects the upstream path, which the links built by the server
# still use. Same value in static/src/webclient/web_path.js.
WEB_PATH = '/app'
UPSTREAM_WEB_PATH = '/odoo'


def get_brand_name(env):
    """Return the product name users see, from the ``ov_brand.name`` system parameter."""
    return env['ir.config_parameter'].sudo().get_str(BRAND_NAME_PARAM) or DEFAULT_BRAND_NAME


def get_support_url(env):
    """Return the URL of the "Help" item of the user menu, empty to hide the item."""
    return env['ir.config_parameter'].sudo().get_str(SUPPORT_URL_PARAM)


def _replace_path_prefix(url, old, new):
    if not url:
        return url
    parts = urlsplit(url)
    if parts.path != old and not parts.path.startswith(f'{old}/'):
        return url
    return urlunsplit(parts._replace(path=new + parts.path.removeprefix(old)))


def web_path(url):
    """Return the URL with the path of the web client in place of the upstream one."""
    return _replace_path_prefix(url, UPSTREAM_WEB_PATH, WEB_PATH)


def upstream_path(url):
    """Return the URL with the upstream path of the web client in place of ours."""
    return _replace_path_prefix(url, WEB_PATH, UPSTREAM_WEB_PATH)
