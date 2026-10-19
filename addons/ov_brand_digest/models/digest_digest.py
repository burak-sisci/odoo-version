from odoo import api, models


class DigestDigest(models.Model):
    _inherit = 'digest.digest'

    def _compute_tips(self, company, user, tips_count=1, consumed=True):
        """No tips: they are the publisher's content, text about its product and
        images on its servers, which the mail client of the user would load."""
        return []

    @api.model
    def _ov_brand_reset_default_name(self):
        """Drop the translations of the default digest's name. They carry the
        publisher's name, and the translations of this module, loaded after
        them, do not replace existing ones."""
        digest = self.env.ref('digest.digest_digest_default', raise_if_not_found=False)
        langs = [code for code, _name in self.env['res.lang'].get_installed() if code != 'en_US']
        if digest and langs:
            digest.update_field_translations('name', dict.fromkeys(langs, False))
