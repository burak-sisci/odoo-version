from odoo import models

from odoo.addons.ov_brand.tools import IMG_PATH

UPSTREAM_PUSH_ICON = '/web/static/img/odoo-icon-192x192.png'


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _notify_by_web_push_prepare_payload(self, message, force_record_name=False):
        """Browser notifications of the messages without author show the
        publisher's icon."""
        payload = super()._notify_by_web_push_prepare_payload(message, force_record_name=force_record_name)
        if payload['options'].get('icon') == UPSTREAM_PUSH_ICON:
            payload['options']['icon'] = f'{IMG_PATH}/icon_192.png'
        return payload
