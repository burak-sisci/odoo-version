from psycopg2.extras import Json

from odoo import api, models
from odoo.tools import SQL
from odoo.tools.translate import TranslationImporter

from odoo.addons.ov_i18n_tr.tools import (
    MODULE,
    loading_records,
    overlay_modules,
    overlay_path,
    upstream_po_paths,
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
        upstream = TranslationImporter(self.env.cr, verbose=False)
        for module_name in installed:
            for lang in langs:
                path = overlay_path(module_name, lang)
                if path:
                    importer.load_file(path, lang)
                    if overwrite:
                        for upstream_path in upstream_po_paths(module_name, lang):
                            upstream.load_file(upstream_path, lang)
        if overwrite:
            # before the import, which empties the importer
            self._overwrite_upstream_terms(importer, upstream)
        importer.save(overwrite=overwrite)

    @api.model
    def _overwrite_upstream_terms(self, overlay, upstream):
        """Correct the record translations still holding upstream's value.

        Even with ``overwrite``, the import keeps the translations of the
        records the customer may change (noupdate), such as currencies: the
        language is loaded before this module is installed, so upstream's
        mistranslation would stay. A translation is replaced only while it is
        upstream's: one changed by the customer is kept.
        """
        self.env.flush_all()
        for model_name, fields in overlay.model_translations.items():
            model = self.env[model_name]
            for field_name, records in fields.items():
                field = model._fields.get(field_name)
                if not field or not field.store or not field.translate or callable(field.translate):
                    continue
                upstream_records = upstream.model_translations.get(model_name, {}).get(field_name, {})
                for xmlid, values in records.items():
                    record = self.env.ref(xmlid, raise_if_not_found=False)
                    if record is None or record._name != model_name:
                        continue
                    self.env.cr.execute(
                        SQL('SELECT %s FROM %s WHERE id = %s',
                            SQL.identifier(field_name), SQL.identifier(model._table), record.id),
                    )
                    current = self.env.cr.fetchone()[0] or {}
                    changes = {
                        lang: value
                        for lang, value in values.items()
                        if current.get(lang) != value
                        and current.get(lang) == upstream_records.get(xmlid, {}).get(lang)
                    }
                    if changes:
                        self.env.cr.execute(SQL(
                            'UPDATE %s SET %s = %s || %s::jsonb WHERE id = %s',
                            SQL.identifier(model._table), SQL.identifier(field_name),
                            SQL.identifier(field_name), Json(changes), record.id,
                        ))
                        record.invalidate_recordset([field_name])

    @api.model
    def _load_non_installed_modules_manifest_terms(self, langs):
        token = loading_records.set(True)
        try:
            return super()._load_non_installed_modules_manifest_terms(langs)
        finally:
            loading_records.reset(token)
