from odoo import api, models
from odoo.tools.translate import TranslationImporter

from odoo.addons.ov_i18n_tr.tools import (
    MODULE,
    loading_records,
    overlay_modules,
    overlay_path,
)


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    @api.model
    def _load_module_terms(self, modules, langs, overwrite=False):
        # The overlay file of each module is read with upstream's, in the same
        # import: same rules (existing translations kept unless overwrite).
        token = loading_records.set(True)
        try:
            result = super()._load_module_terms(modules, langs, overwrite=overwrite)
        finally:
            loading_records.reset(token)
        if MODULE in modules:
            # The modules installed before this one did not read their overlay.
            # On installation, its entries replace the translations they have.
            module = self.search([('name', '=', MODULE)])
            self._load_overlay_terms(
                [name for name in overlay_modules() if name not in modules],
                langs,
                overwrite=overwrite or module.state == 'to install',
            )
        return result

    @api.model
    def _load_overlay_terms(self, modules, langs, overwrite=False):
        """Load the record terms of the overlay files of the installed ``modules``."""
        installed = self.search([('name', 'in', list(modules)), ('state', '=', 'installed')]).mapped('name')
        importer = TranslationImporter(self.env.cr, verbose=False)
        for module_name in installed:
            for lang in langs:
                path = overlay_path(module_name, lang)
                if path:
                    importer.load_file(path, lang)
        importer.save(overwrite=overwrite)

    @api.model
    def _load_non_installed_modules_manifest_terms(self, langs):
        token = loading_records.set(True)
        try:
            return super()._load_non_installed_modules_manifest_terms(langs)
        finally:
            loading_records.reset(token)
