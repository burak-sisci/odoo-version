from odoo import models

from odoo.addons.ov_brand.rebrand import rebrand_html
from odoo.addons.ov_brand.tools import get_brand_name


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def _set_value_from_template(self, template_fname, composer_fname=False):
        """Rebrand the template texts the composer copies without rendering them
        (mass mailing, batch comments). They are rendered when sent, as texts
        of the composer."""
        value = super()._set_value_from_template(template_fname, composer_fname)
        if isinstance(value, str) and value:
            rebranded = rebrand_html(value, get_brand_name(self.env), self.template_id.env.lang or self.env.lang)
            if rebranded != value:
                self[composer_fname or template_fname] = value = rebranded
        return value
