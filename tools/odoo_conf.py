"""Write the local odoo.conf from deploy/odoo.conf.example.

Placeholders are filled with the repository and OV_HOME paths and with the
database credentials in .env (created by `python tools/pg.py init`). A master
password for the database manager is generated into .env on first use.
odoo.conf and .env are never committed.

Usage: python tools/odoo_conf.py [--force]
"""
import secrets
import sys

from pg import OV_HOME, ROOT, read_env, write_env

TEMPLATE = ROOT / "deploy" / "odoo.conf.example"
TARGET = ROOT / "odoo.conf"
REQUIRED = ("PGHOST", "PGPORT", "PGUSER", "PGPASSWORD")


def main():
    if TARGET.exists() and "--force" not in sys.argv[1:]:
        sys.exit(f"{TARGET} exists; use --force to overwrite it")
    missing = [key for key in REQUIRED if not read_env().get(key)]
    if missing:
        sys.exit(f"missing in .env: {', '.join(missing)}; run `python tools/pg.py init` first")
    if not read_env().get("ODOO_ADMIN_PASSWD"):
        write_env({"ODOO_ADMIN_PASSWD": secrets.token_urlsafe(24)})
    values = {**read_env(), "root": ROOT.as_posix(), "ov_home": OV_HOME.as_posix()}
    TARGET.write_text(TEMPLATE.read_text(encoding="utf-8").format_map(values), encoding="utf-8")
    print(f"written: {TARGET}")


if __name__ == "__main__":
    main()
