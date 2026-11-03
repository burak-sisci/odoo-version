"""Run Odoo module tests on a fresh database and summarise the result.

Creates (or recreates) a test database without demo data, installs the given
modules with tests enabled, and reads the log. When the modules need ov_brand,
it is installed first without tests: it removes the publisher's online service
modules, and Odoo skips the post_install tests of a run that removed modules.
The given modules it brought along are then updated with tests.

On Windows, Odoo 20.0's filestore garbage collection cannot delete files in test
set-up/teardown; those errors are reported separately and do not fail the run
(the reference result is the Linux CI). The full log is kept under OV_HOME/logs/tests/.

External requests (T2.7): Odoo runs through tools/netguard.py, which records the
name lookups of outside hosts (installation, scheduled jobs, tests, any library)
next to the log. The log adds the requests the test framework blocked (Python)
and answered itself (browser). They are listed; when ov_brand is installed, a
request to the publisher's domains fails the run.

Usage: python tools/run_tests.py MODULE[,MODULE...] [--tags TAGS] [--db NAME] [--with-demo] [--reuse] [-v]
  --tags       --test-tags value (default: /MODULE for each module)
  --db         database name (default: ov_test_<first module>)
  --with-demo  load demo data (tests should not depend on it)
  --reuse      keep the existing test database and update (-u) instead of installing
  -v           print the traceback of each real problem (CI)
"""
import argparse
import ast
import json
import os
import re
import stat
import subprocess
import sys
from urllib.parse import urlsplit

from netguard import is_publisher
from pg import OV_HOME, ROOT

PYTHON = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
ODOO_BIN = ROOT / "upstream" / "odoo" / "odoo-bin"
NETGUARD = ROOT / "tools" / "netguard.py"
CONF = ROOT / "odoo.conf"
LOG_DIR = OV_HOME / "logs" / "tests"
FILESTORE = OV_HOME / "odoo-data" / "filestore"
TEST_HTTP_PORT = "8079"
# Removes modules at the end of its installation (T2.3). Odoo then reloads the
# registry, and the post_install tests of that run never start.
PREINSTALL = "ov_brand"

LOG_LINE = re.compile(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d+ \d+ (\w+) \S+ (\S+): (.*)$")
TEST_PROBLEM = re.compile(r"^(ERROR|FAIL): (.+)$")
SUMMARY = re.compile(r"(\d+) failed, (\d+) error\(s\) of (\d+) tests when loading database")
# Odoo 20.0 on Windows: the filestore garbage collection run by the test classes
# (setUpClass/tearDownClass) cannot unlink files (T1.2 finding). The leftover
# .__gc files then trip `assert not path.endswith(GC_FILE_SUFFIX)`.
WINDOWS_GC_FRAME = "_gc_file_store_unsafe"
WINDOWS_GC_ERRORS = ("assert not path.endswith(GC_FILE_SUFFIX)", "PermissionError")
# External requests the test framework blocked (Python) or answered itself (browser)
BLOCKED_REQUEST = re.compile(r"Blocking un-mocked external HTTP request \S+ (\S+)")
BROWSER_REQUEST = re.compile(r"External chrome request during tests: (?:returning 404 for|Return empty file for) (\S+)")


def odoo(*args, log, record):
    cmd = [str(PYTHON), str(NETGUARD), str(record), str(ODOO_BIN), *args]
    with open(log, "w", encoding="utf-8") as fh:
        return subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, check=False).returncode


def own_closure(modules):
    """Return the modules and their dependencies among our modules (addons/)."""
    todo, seen = list(modules), set()
    while todo:
        name = todo.pop()
        manifest = ROOT / "addons" / name / "__manifest__.py"
        if name in seen or not manifest.exists():
            continue
        seen.add(name)
        todo += ast.literal_eval(manifest.read_text(encoding="utf-8")).get("depends", [])
    return seen


def make_filestore_writable(db):
    """Odoo stores attachments read-only (0o444). On Windows that sets the
    read-only attribute, and dropping the database then fails on the filestore."""
    for path in (FILESTORE / db).rglob("*"):
        if path.is_file():
            path.chmod(stat.S_IREAD | stat.S_IWRITE)


def parse(log):
    """Return (summary or None, [(kind, test, text)], other error lines, [(source, url)])."""
    problems, other_errors, summary, requests = [], [], None, []
    current = None
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
        match = LOG_LINE.match(line)
        if not match:
            if current:
                current[2].append(line)
            continue
        current = None
        level, _logger, message = match.groups()
        if request := BLOCKED_REQUEST.search(message):
            requests.append(("python, blocked by the tests", request.group(1)))
        elif request := BROWSER_REQUEST.search(message):
            requests.append(("browser", request.group(1)))
        elif found := SUMMARY.search(message):
            summary = tuple(int(n) for n in found.groups())
        elif level in ("ERROR", "CRITICAL") and (problem := TEST_PROBLEM.match(message)):
            current = (problem.group(1), problem.group(2), [])
            problems.append(current)
        elif level in ("ERROR", "CRITICAL"):
            other_errors.append(line)
    problems = [(kind, test, "\n".join(text)) for kind, test, text in problems]
    return summary, problems, other_errors, requests


def read_record(record):
    """Return the lookups recorded by tools/netguard.py, as [(source, host, stack)]."""
    if not record.exists():
        return []
    entries = [json.loads(line) for line in record.read_text(encoding="utf-8").splitlines() if line]
    return [("python", entry["host"], entry["stack"]) for entry in entries]


def report_external(record, requests, guarded, verbose):
    """Print the external requests of the run; return the number of requests
    to the publisher's domains that fail it."""
    found = [(source, urlsplit(url).hostname or url, [url]) for source, url in requests]
    found += read_record(record)
    if not found:
        print("external requests: none")
        return 0
    hosts = {}
    for source, host, _details in found:
        hosts.setdefault(host, set()).add(source)
    listed = ", ".join(f"{host} ({'; '.join(sorted(sources))})" for host, sources in sorted(hosts.items()))
    print(f"external requests: {len(hosts)} hosts: {listed}")
    publisher = [item for item in found if is_publisher(item[1])]
    if publisher:
        verdict = "" if guarded else " (not counted: ov_brand is not installed)"
        print(f"requests to the publisher's domains: {len(publisher)}{verdict}")
        for source, host, details in publisher:
            print(f"  {source}: {host}")
            if verbose:
                print("\n".join(f"    {line}" for line in details))
    return len(publisher) if guarded else 0


def is_windows_gc(text):
    return os.name == "nt" and WINDOWS_GC_FRAME in text and any(err in text for err in WINDOWS_GC_ERRORS)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("modules")
    parser.add_argument("--tags")
    parser.add_argument("--db")
    parser.add_argument("--with-demo", action="store_true")
    parser.add_argument("--reuse", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    if not CONF.exists():
        sys.exit("odoo.conf missing; run `python tools/odoo_conf.py` first")
    modules = [m.strip() for m in args.modules.split(",") if m.strip()]
    db = args.db or f"ov_test_{modules[0]}"
    tags = args.tags or ",".join(f"/{m}" for m in modules)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log = LOG_DIR / f"{db}.log"
    record = LOG_DIR / f"{db}.net.jsonl"
    record.unlink(missing_ok=True)
    guarded = PREINSTALL in own_closure(modules)

    if not args.reuse:
        if os.name == "nt":
            make_filestore_writable(db)
        init = ["db", "-c", str(CONF), "init", db, "--force"] + (["--with-demo"] if args.with_demo else [])
        if odoo(*init, log=log, record=record):
            sys.exit(f"could not create database {db}; see {log}")
    names = ",".join(modules)
    if args.reuse:
        selection = ["-u", names]
    elif guarded:
        if odoo("-c", str(CONF), "-d", db, "-i", PREINSTALL, "--stop-after-init", log=log, record=record):
            sys.exit(f"could not install {PREINSTALL}; see {log}")
        # Odoo installs the missing ones and updates those that came with it,
        # so that the tests of all of them run
        selection = ["-i", names, "-u", names]
    else:
        selection = ["-i", names]
    # Tests start Odoo's HTTP server; a port of its own lets them run next to the dev server.
    rc = odoo("-c", str(CONF), "-d", db, *selection, "--test-enable",
              "--test-tags", tags, "--http-port", TEST_HTTP_PORT, "--stop-after-init", log=log, record=record)

    summary, problems, other_errors, requests = parse(log)
    known = [p for p in problems if is_windows_gc(p[2])]
    real = [p for p in problems if p not in known]
    print(f"log: {log}")
    if summary is None:
        print(f"no test summary in the log (exit code {rc}); the run did not finish")
        for line in other_errors[-5:]:
            print(f"  {line}")
        return 1
    failed, errors, total = summary
    print(f"tests: {total}, failed: {failed}, errors: {errors}")
    if known:
        print(f"known Windows filestore gc errors (not counted, T1.2): {len(known)}")
    for kind, test, text in real:
        print(f"  {kind}: {test}")
        if args.verbose:
            print("\n".join(f"    {line}" for line in text.splitlines()))
    if other_errors:
        print(f"other ERROR log lines: {len(other_errors)} (see the log; expected ones should be muted in tests)")
    publisher = report_external(record, requests, guarded, args.verbose)
    unexplained = failed + errors - len(known)
    if unexplained > 0 or publisher:
        print(f"RESULT: FAILED ({unexplained + publisher})")
        return 1
    print("RESULT: OK" + (" (Windows gc errors only)" if known else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
