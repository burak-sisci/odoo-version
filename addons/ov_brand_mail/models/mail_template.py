from odoo import api, models

from odoo.addons.ov_brand.rebrand import rebrand_html
from odoo.addons.ov_brand.tools import get_brand_name


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    @api.model
    def _render_template(self, template_src, model, res_ids, engine='inline_template',
                         add_context=None, options=None):
        """Rebrand the subject and body of the templates (T2.6) before rendering
        them. Their texts are data; the texts of the composer, which the user
        writes, are not changed."""
        if engine != 'qweb_view' and isinstance(template_src, str):
            template_src = rebrand_html(template_src, get_brand_name(self.env), self.env.lang)
        return super()._render_template(
            template_src, model, res_ids, engine=engine, add_context=add_context, options=options)
