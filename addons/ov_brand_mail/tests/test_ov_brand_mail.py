from unittest.mock import patch

from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestOvBrandMail(TransactionCase):

    def test_publisher_warranty_not_sent(self):
        with patch('odoo.addons.mail.models.update.requests.post') as post:
            # cron_mode=False: an error would raise instead of being swallowed
            result = self.env['publisher_warranty.contract'].update_notification(cron_mode=False)
        post.assert_not_called()
        self.assertTrue(result)

    def test_publisher_warranty_cron_inactive(self):
        cron = self.env.ref('mail.ir_cron_module_update_notification')
        self.assertFalse(cron.active)
