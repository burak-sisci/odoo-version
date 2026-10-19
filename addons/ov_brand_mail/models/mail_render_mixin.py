import re

from markupsafe import Markup

from odoo import api, models

# Logo of the publisher in upstream e-mail templates (e-invoice notifications).
# The templates are data the users can edit and reset, so the logo is removed
# from the rendered e-mails.
UPSTREAM_LOGO_FILE = 'logo_inverse_white_206px.png'
UPSTREAM_LOGO = re.compile(rf'<img\b[^>]*\bsrc="[^"]*/web/static/img/{re.escape(UPSTREAM_LOGO_FILE)}"[^>]*>')


class MailRenderMixin(models.AbstractModel):
    _inherit = 'mail.render.mixin'

    @api.model
    def _render_template(self, template_src, model, res_ids, engine='inline_template',
                         add_context=None, options=None):
        rendered = super()._render_template(
            template_src, model, res_ids, engine=engine, add_context=add_context, options=options)
        for res_id, value in rendered.items():
            if isinstance(value, str) and UPSTREAM_LOGO_FILE in value:
                cleaned = UPSTREAM_LOGO.sub('', value)
                rendered[res_id] = Markup(cleaned) if isinstance(value, Markup) else cleaned
        return rendered
