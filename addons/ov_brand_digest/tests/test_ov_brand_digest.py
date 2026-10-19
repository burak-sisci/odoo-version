from odoo.tests import TransactionCase, new_test_user, tagged


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

    def test_digest_mail(self):
        user = new_test_user(self.env, 'ov_digest', email='digest@example.com')
        digest = self.env['digest.digest'].create({
            'name': 'Fictional Digest',
            'user_ids': [(4, user.id)],
            'kpi_res_users_connected': True,
        })
        self.assertTrue(self.env['digest.tip'].search_count([]))
        digest._action_send_to_user(user)
        mail = self.env['mail.mail'].sudo().search([('subject', 'like', 'Fictional Digest')])
        self.assertEqual(len(mail), 1)
        for text in ('odoo.com', 'odoocdn.com', 'Sent by', 'Powered by', 'Odoo Mobile'):
            self.assertNotIn(text, mail.body_html)
        self.assertIn(f'/digest/{digest.id}/unsubscribe?token=', mail.body_html)
        # No tip was shown to the user
        self.assertFalse(self.env['digest.tip'].search_count([('user_ids', 'in', user.ids)]))
