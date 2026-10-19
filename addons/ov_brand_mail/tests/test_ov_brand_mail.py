from unittest.mock import patch

from odoo.tests import TransactionCase, tagged
from odoo.tools import file_open

from odoo.addons.ov_brand.tools import BRAND_NAME_PARAM, DEFAULT_BRAND_NAME


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

    def test_notification_layouts(self):
        admin = self.env.ref('base.user_admin')
        customer = self.env['res.partner'].create({'name': 'Fictional Customer', 'email': 'customer@example.com'})
        for layout in ('mail.mail_notification_layout', 'mail.mail_notification_light'):
            with self.subTest(layout=layout):
                message = customer.with_user(admin).message_post(
                    body='Hello',
                    partner_ids=customer.ids,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment',
                    email_layout_xmlid=layout,
                )
                mail = self.env['mail.mail'].sudo().search([('mail_message_id', '=', message.id)])
                self.assertTrue(mail)
                self.assertIn('Hello', mail.body_html)
                self.assertNotIn('Powered by', mail.body_html)
                self.assertNotIn('odoo.com', mail.body_html)

    def test_upstream_logo_removed(self):
        partner = self.env['res.partner'].create({'name': 'Fictional Customer'})
        template = (
            '<div><img alt="Odoo" src="/web/static/img/logo_inverse_white_206px.png" style="height: 2em;"/>'
            '<span t-out="object.name"/></div>'
        )
        rendered = self.env['mail.render.mixin']._render_template(template, 'res.partner', partner.ids, engine='qweb')
        self.assertNotIn('logo_inverse_white_206px', rendered[partner.id])
        self.assertIn('Fictional Customer', rendered[partner.id])

    def test_bot(self):
        bot = self.env.ref('base.partner_root')
        self.assertEqual(bot.name, DEFAULT_BRAND_NAME)
        with file_open('mail/static/src/img/odoobot.webp', 'rb') as upstream_avatar:
            self.assertNotEqual(bot.image_1920.content, upstream_avatar.read())
        # The name follows the product name
        params = self.env['ir.config_parameter'].sudo()
        params.set_str(BRAND_NAME_PARAM, 'Fictional ERP')
        self.assertEqual(bot.name, 'Fictional ERP')
        params.search([('key', '=', BRAND_NAME_PARAM)]).unlink()
        self.assertEqual(bot.name, DEFAULT_BRAND_NAME)

    def test_public_channel_page(self):
        arch = self.env.ref('mail.discuss_public_channel_template')._get_combined_arch()
        self.assertEqual(arch.xpath('//title/@t-out'), ['title or ov_brand_name'])
        self.assertNotIn('/web/static/img/favicon.ico', arch.xpath("//link[@rel='shortcut icon']/@t-att-href")[0])
