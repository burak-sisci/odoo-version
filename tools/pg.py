"""Manage the local development PostgreSQL cluster (no admin rights needed).

The server binaries are the portable EnterpriseDB zip, unpacked under OV_HOME
(default: %LOCALAPPDATA%/odoo-version). The cluster runs under the current
user account and listens on localhost only. Credentials live in the
repository's .env file, which is never committed.

Usage: python tools/pg.py init|start|stop|status
"""
import os
import secrets
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
OV_HOME = Path(os.environ.get("OV_HOME") or Path(os.environ.get("LOCALAPPDATA", Path.home())) / "odoo-version")
BIN = OV_HOME / "pgsql" / "bin"
DATA = OV_HOME / "pgdata"
LOG = OV_HOME / "pglog" / "postgres.log"
PORT = "5432"
ODOO_ROLE = "odoo"


def exe(name):
    return str(BIN / (name + (".exe" if os.name == "nt" else "")))


def read_env():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    return env


def write_env(values):
    env = read_env()
    lines = ENV_FILE.read_text(encoding="utf-8").splitlines() if ENV_FILE.exists() else []
    lines += [f"{k}={v}" for k, v in values.items() if k not in env]
    ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(*args, **kwargs):
    return subprocess.run([str(a) for a in args], check=True, **kwargs)


def init():
    if DATA.exists():
        sys.exit(f"cluster already exists: {DATA}")
    env = read_env()
    super_pw = env.get("PG_SUPERUSER_PASSWORD") or secrets.token_urlsafe(24)
    odoo_pw = env.get("PGPASSWORD") or secrets.token_urlsafe(24)
    write_env({"PGHOST": "localhost", "PGPORT": PORT, "PGUSER": ODOO_ROLE,
               "PGPASSWORD": odoo_pw, "PG_SUPERUSER_PASSWORD": super_pw})
    with tempfile.TemporaryDirectory() as tmp:
        pwfile = Path(tmp) / "pw"
        pwfile.write_text(super_pw, encoding="utf-8")
        run(exe("initdb"), "-D", DATA, "-U", "postgres", "--pwfile", pwfile, "-E", "UTF8",
            "--locale-provider=builtin", "--builtin-locale=C.UTF-8", "--locale=C",
            "--auth=scram-sha-256")
    conf = DATA / "postgresql.conf"
    conf.write_text(conf.read_text(encoding="utf-8")
                    + f"\nlisten_addresses = 'localhost'\nport = {PORT}\n", encoding="utf-8")
    start()
    sql = f"CREATE ROLE {ODOO_ROLE} LOGIN CREATEDB PASSWORD '{odoo_pw}';"
    run(exe("psql"), "-h", "localhost", "-p", PORT, "-U", "postgres", "-d", "postgres", "-v", "ON_ERROR_STOP=1",
        "-c", sql, env={**os.environ, "PGPASSWORD": super_pw})
    print(f"cluster ready: {DATA}; role '{ODOO_ROLE}' created; credentials in .env")


def start():
    LOG.parent.mkdir(parents=True, exist_ok=True)
    out = LOG.with_name("pg_ctl.out")
    # The server must not inherit our stdout/stderr handles: a caller that waits
    # for its output pipe to close (shells, CI steps) would otherwise hang until
    # the server stops. Detach it from our console as well.
    flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    with open(out, "w", encoding="utf-8") as fh:
        code = subprocess.run([exe("pg_ctl"), "-D", str(DATA), "-l", str(LOG), "-w", "start"],
                              stdin=subprocess.DEVNULL, stdout=fh, stderr=subprocess.STDOUT,
                              creationflags=flags).returncode
    print(out.read_text(encoding="utf-8").strip())
    if code:
        sys.exit(f"pg_ctl start failed ({code}); see {LOG}")


def stop():
    run(exe("pg_ctl"), "-D", DATA, "-w", "stop")


def status():
    return subprocess.run([exe("pg_ctl"), "-D", str(DATA), "status"]).returncode


def main():
    commands = {"init": init, "start": start, "stop": stop, "status": status}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        sys.exit(__doc__)
    return commands[sys.argv[1]]() or 0


if __name__ == "__main__":
    sys.exit(main())
