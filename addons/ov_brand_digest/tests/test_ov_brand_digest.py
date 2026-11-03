from lxml import html

from odoo.tests import TransactionCase, new_test_user, tagged

from odoo.addons.ov_brand.tests.test_powered_by import powered_by_lines
from odoo.addons.ov_brand.tools import DEFAULT_BRAND_NAME, POWERED_BY_PARAM


@tagged('post_install', '-at_install')
class TestOvBrandDigest(TransactionCase):

    def test_default_digest_name(self):
        self.assertEqual(self.env.ref('digest.digest_digest_default').name, 'Your Periodic Digest')

    def test_default_digest_name_translations(self):
        self.env['res.lang']._activate_lang('tr_TR')
        digest = self.env.ref('digest.digest_digest_default')
        digest.update_field_translations('name', {'tr_TR': 'Fictional Publisher Digest'})
        self.env['digest.digest']._ov_brand_reset_default_name()
        self.assertEqual(digest.with_context(lang='tr_TR').name, 'Your Periodic Digest')

    def _send(self, name):
        user = new_test_user(self.env, f'ov_digest_{len(name)}', email='digest@example.com')
        digest = self.env['digest.digest'].create({
            'name': name,
            'user_ids': [(4, user.id)],
            'kpi_res_users_connected': True,
        })
        digest._action_send_to_user(user)
        mail = self.env['mail.mail'].sudo().search([('subject', 'like', name)])
        self.assertEqual(len(mail), 1)
        for text in ('odoo.com', 'odoocdn.com', 'Sent by', 'Odoo Mobile'):
            self.assertNotIn(text, mail.body_html)
        self.assertIn(f'/digest/{digest.id}/unsubscribe?token=', mail.body_html)
        # No tip was shown to the user
        self.assertFalse(self.env['digest.tip'].search_count([('user_ids', 'in', user.ids)]))
        return mail.body_html

    def test_digest_mail(self):
        self.assertTrue(self.env['digest.tip'].search_count([]))
        # "Powered by" and the product name under the company name, without a link (K17)
        body = self._send('Fictional Digest')
        self.assertEqual(powered_by_lines(body), [f'Powered by {DEFAULT_BRAND_NAME}'])
        self.assertFalse(html.fromstring(body).xpath(f"//a[contains(., '{DEFAULT_BRAND_NAME}')]"))
        # Hidden in the settings
        self.env['ir.config_parameter'].sudo().set_bool(POWERED_BY_PARAM, False)
        body = self._send('Fictional Second Digest')
        self.assertNotIn('Powered by', body)
