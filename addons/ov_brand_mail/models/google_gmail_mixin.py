from odoo import models
from odoo.exceptions import UserError


class GoogleGmailMixin(models.AbstractModel):
    _inherit = 'google.gmail.mixin'

    def _fetch_gmail_access_token_iap(self, refresh_token):
        """Without the Gmail credentials of the database, the access token is
        not asked from the publisher's proxy (T2.7): the refresh token would be
        sent to it. The proxy only connects the paid edition; this happens when
        the credentials are removed after the account was connected."""
        raise UserError(self.env._(
            "The %(service)s credentials are missing in the Settings. Enter them, then connect the account again.",
            service='Gmail',
        ))
