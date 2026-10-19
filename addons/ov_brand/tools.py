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


def get_brand_name(env):
    """Return the product name users see, from the ``ov_brand.name`` system parameter."""
    return env['ir.config_parameter'].sudo().get_str(BRAND_NAME_PARAM) or DEFAULT_BRAND_NAME


def get_support_url(env):
    """Return the URL of the "Help" item of the user menu, empty to hide the item."""
    return env['ir.config_parameter'].sudo().get_str(SUPPORT_URL_PARAM)
