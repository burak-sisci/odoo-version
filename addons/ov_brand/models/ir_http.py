from odoo import api, models

from odoo.addons.ov_brand.rebrand import code_sources, rebrand
from odoo.addons.ov_brand.tools import get_brand_name, get_support_url


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        session_info = super().session_info()
        session_info['ov_brand_name'] = get_brand_name(self.env)
        # Odoo points the "Help" item to odoo.com
        session_info['support_url'] = get_support_url(self.env)
        return session_info

    @api.model
    def get_frontend_session_info(self):
        session_info = super().get_frontend_session_info()
        session_info['ov_brand_name'] = get_brand_name(self.env)
        return session_info

    @api.model
    def _get_translations_for_webclient(self, modules, lang):
        """Rebrand the web client terms (T2.6), the terms without a translation
        included: the web client shows their source text."""
        translations, lang_params = super()._get_translations_for_webclient(modules, lang)
        brand = get_brand_name(self.env)
        lang = lang or self.env.context.get('lang')
        for module in modules:
            module_translations = translations.get(module) or {'messages': ()}
            messages = []
            changed = False
            for message in module_translations['messages']:
                string = rebrand(message['string'], brand, lang)
                if string != message['string']:
                    message = {'id': message['id'], 'string': string}
                    changed = True
                messages.append(message)
            translated = {message['id'] for message in messages}
            for source in code_sources(module) - translated:
                messages.append({'id': source, 'string': rebrand(source, brand, lang)})
                changed = True
            if changed:
                translations[module] = {**module_translations, 'messages': messages}
        return translations, lang_params
