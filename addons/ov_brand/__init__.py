from . import controllers, models
from .rebrand import forget_database, patch_code_translations

patch_code_translations()


def uninstall_hook(env):
    forget_database(env.cr.dbname)
