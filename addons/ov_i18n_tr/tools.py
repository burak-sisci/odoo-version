"""Turkish translations completing upstream's, read after its own (T3.6).

Upstream reads the translations of a module from ``<module>/i18n/<lang>.po``.
This module keeps, for each upstream module, the entries it translates in
``i18n_overlay/<module>.po``: missing translations and corrections. The file
is read right after upstream's, so its entries win, through the function
listing the translation files of a module, ``get_po_paths``:

- code terms (``_()``, ``env._()``, ``_t``): ``odoo.tools.translate``, for the
  whole process, the code translations having no database;
- record terms (views, fields, menus, actions) and module names: the same
  function, imported by name in ``ir.module.module`` and in the manifest
  reader, while this module's methods of ``ir.module.module`` load them. A
  database without this module keeps upstream's translations.
"""
import contextvars
import functools
from pathlib import Path

MODULE = 'ov_i18n_tr'
OVERLAY_DIR = Path(__file__).resolve().parent / 'i18n_overlay'
# Base language of the overlay files, as upstream names its files
OVERLAY_LANG = 'tr'

# Set while this module's ir.module.module loads the record terms of a database
loading_records = contextvars.ContextVar('ov_i18n_tr_loading_records', default=False)


def overlay_path(module_name, lang):
    """Return the path of the overlay file of ``module_name`` for ``lang``, None without one."""
    from odoo.tools.translate import get_base_langs  # noqa: PLC0415

    if OVERLAY_LANG not in get_base_langs(lang):
        return None
    path = OVERLAY_DIR / f'{module_name}.po'
    return str(path) if path.is_file() else None


def overlay_modules():
    """Return the names of the modules having an overlay file."""
    return sorted(path.stem for path in OVERLAY_DIR.glob('*.po'))


def upstream_po_paths(module_name, lang):
    """Return the paths of upstream's translation files of ``module_name``, without the overlay."""
    from odoo.tools import translate  # noqa: PLC0415

    get_po_paths = getattr(translate.get_po_paths, 'ov_i18n_tr_original', translate.get_po_paths)
    return list(get_po_paths(module_name, lang))


def _with_overlay(original, records):
    @functools.wraps(original)
    def get_po_paths(module_name, lang):
        yield from original(module_name, lang)
        if not records or loading_records.get():
            path = overlay_path(module_name, lang)
            if path:
                yield path

    get_po_paths.ov_i18n_tr_original = original
    return get_po_paths


def patch_po_paths():
    """Add the overlay file to the translation files upstream reads."""
    from odoo.modules import module  # noqa: PLC0415
    from odoo.tools import translate  # noqa: PLC0415

    from odoo.addons.base.models import ir_module  # noqa: PLC0415

    if hasattr(translate.get_po_paths, 'ov_i18n_tr_original'):
        return
    translate.get_po_paths = _with_overlay(translate.get_po_paths, records=False)
    ir_module.get_po_paths = _with_overlay(ir_module.get_po_paths, records=True)
    module.get_po_paths = _with_overlay(module.get_po_paths, records=True)
    # code translations read before the module was imported
    translate.code_translations.python_translations.clear()
    translate.code_translations.web_translations.clear()
