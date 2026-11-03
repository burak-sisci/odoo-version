from unittest.mock import patch

from lxml import etree, html

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged
from odoo.tools import file_open

from odoo.addons.ov_brand.rebrand import rebrand, rebrand_html
from odoo.addons.ov_brand.tests.brand_leak import (
    LANGS,
    find_leak,
    is_allowed,
    scan_arch,
)
from odoo.addons.ov_brand.tests.external_requests import ExternalRequestsMixin
from odoo.addons.ov_brand.tools import (
    BRAND_NAME_PARAM,
    DEFAULT_BRAND_NAME,
    IMG_PATH,
    get_brand_name,
)
from odoo.addons.ov_brand_mail.models.res_partner import BOT_EMAIL


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
        self.assertEqual(bot.email, BOT_EMAIL)
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

    def test_email_servers_tooltip(self):
        view = self.env.ref('base.res_config_settings_view_form')
        arch = etree.fromstring(self.env['res.config.settings'].get_view(view.id)['arch'])
        self.assertFalse(arch.xpath("//setting[@id='email_servers_setting']/@title"))

    def test_security_alert(self):
        arch = self.env.ref('mail.account_security_alert')._get_combined_arch()
        self.assertFalse([href for href in arch.xpath('//a/@href') if 'odoo.com' in href])
        self.assertIn('Two-factor Authentication', arch.xpath('//a')[-1].text)

    def test_push_icon(self):
        partner = self.env['res.partner'].create({'name': 'Fictional Customer'})
        message = self.env['mail.message'].create({
            'body': 'Hello', 'model': 'res.partner', 'res_id': partner.id,
            'author_id': False, 'message_type': 'notification',
        })
        payload = partner._notify_by_web_push_prepare_payload(message)
        self.assertEqual(payload['options']['icon'], f'{IMG_PATH}/icon_192.png')

    def test_template_rendering(self):
        template = self.env.ref('auth_totp_mail.mail_template_totp_invite')
        self.assertIn('Odoo', template.subject)
        admin = self.env.ref('base.user_admin')
        subject = template._render_field('subject', admin.ids)[admin.id]
        self.assertNotIn('Odoo', subject)
        self.assertIn(DEFAULT_BRAND_NAME, subject)
        # Texts copied unrendered by the composer
        composer = self.env['mail.compose.message'].with_context(
            default_composition_mode='mass_mail',
            default_model='res.users',
            default_res_ids=admin.ids,
            default_template_id=template.id,
        ).create({})
        self.assertNotIn('Odoo', composer.subject)
        self.assertIn(DEFAULT_BRAND_NAME, composer.subject)


@tagged('post_install', '-at_install', 'ov_brand_leak')
class TestOvBrandMailLeak(TransactionCase):
    """Brand leak test of the e-mail templates (T2.6, see ov_brand)."""

    def test_mail_templates(self):
        templates = self.env['mail.template'].with_context(active_test=False).search([])
        modules = self.env['ir.module.module'].search([
            ('name', 'in', [xmlid.split('.')[0] for xmlid in templates.get_external_id().values() if xmlid]),
        ])
        self.env['res.lang']._activate_lang('tr_TR')
        modules._update_translations(['tr_TR'])
        brand = get_brand_name(self.env)
        xmlids = templates.get_external_id()
        leaks = []
        for lang in LANGS:
            for template in templates.with_context(lang=lang):
                key = xmlids[template.id] or f'mail.template:{template.id}'
                subject = rebrand(template.subject, brand, lang)
                if find_leak(subject) and not is_allowed('mail_template', f'{key}.subject'):
                    leaks.append(f'{key}.subject ({lang}): {subject}')
                if template.body_html:
                    body = html.fragment_fromstring(rebrand_html(template.body_html, brand, lang), create_parent='div')
                    if not is_allowed('mail_template', f'{key}.body_html'):
                        leaks.extend(f'{key}.body_html ({lang}): {leak[:200]}' for leak in scan_arch(body))
        self.assertFalse(leaks, "Brand leaks:\n" + "\n".join(sorted(set(leaks))))


@tagged('post_install', '-at_install', 'ov_external')
class TestOvBrandMailExternal(ExternalRequestsMixin, TransactionCase):
    """External request test of the mail servers (T2.7, see ov_brand)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # An account connected with the credentials of the database, which were
        # then removed from the Settings
        cls.env['ir.config_parameter'].sudo().search([('key', 'in', [
            'google_gmail_client_id', 'google_gmail_client_secret',
            'microsoft_outlook_client_id', 'microsoft_outlook_client_secret',
        ])]).unlink()
        cls.server = cls.env['ir.mail_server'].create({
            'name': 'Fictional server',
            'smtp_host': 'smtp.example.com',
            'smtp_user': 'sender@example.com',
            'google_gmail_refresh_token': 'fictional-refresh-token',
            'microsoft_outlook_refresh_token': 'fictional-refresh-token',
        })

    def test_gmail_refresh_without_credentials(self):
        with self.assertRaisesRegex(UserError, 'Gmail credentials are missing'):
            self.server._generate_oauth2_string('sender@example.com', self.server.google_gmail_refresh_token)
        self.assertFalse(self.external_requests)

    def test_outlook_refresh_without_credentials(self):
        with self.assertRaisesRegex(UserError, 'Outlook credentials are missing'):
            self.server._generate_outlook_oauth2_string('sender@example.com')
        self.assertFalse(self.external_requests)
