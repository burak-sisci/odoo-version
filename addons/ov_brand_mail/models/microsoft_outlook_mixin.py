from odoo import models
from odoo.exceptions import UserError


class MicrosoftOutlookMixin(models.AbstractModel):
    _inherit = 'microsoft.outlook.mixin'

    def _fetch_outlook_access_token_iap(self, refresh_token):
        """Without the Outlook credentials of the database, the access token is
        not asked from the publisher's proxy (T2.7): the refresh token would be
        sent to it. The proxy only connects the paid edition; this happens when
        the credentials are removed after the account was connected."""
        raise UserError(self.env._(
            "The %(service)s credentials are missing in the Settings. Enter them, then connect the account again.",
            service='Outlook',
        ))
