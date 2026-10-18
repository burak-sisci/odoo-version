"""Run Odoo module tests on a fresh database and summarise the result.

Creates (or recreates) a test database without demo data, installs the given
modules with tests enabled, and reads the log. On Windows, Odoo 20.0's
filestore garbage collection cannot delete files in test set-up/teardown; those
errors are reported separately and do not fail the run (the reference result
is the Linux CI). The full log is kept under OV_HOME/logs/tests/.

Usage: python tools/run_tests.py MODULE[,MODULE...] [--tags TAGS] [--db NAME] [--with-demo] [--reuse] [-v]
  --tags       --test-tags value (default: /MODULE for each module)
  --db         database name (default: ov_test_<first module>)
  --with-demo  load demo data (tests should not depend on it)
  --reuse      keep the existing test database and update (-u) instead of installing
  -v           print the traceback of each real problem (CI)
"""
import argparse
import os
import re
import subprocess
import sys

from pg import OV_HOME, ROOT

PYTHON = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
ODOO_BIN = ROOT / "upstream" / "odoo" / "odoo-bin"
CONF = ROOT / "odoo.conf"
LOG_DIR = OV_HOME / "logs" / "tests"
TEST_HTTP_PORT = "8079"

LOG_LINE = re.compile(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d+ \d+ (\w+) \S+ (\S+): (.*)$")
TEST_PROBLEM = re.compile(r"^(ERROR|FAIL): (.+)$")
SUMMARY = re.compile(r"(\d+) failed, (\d+) error\(s\) of (\d+) tests when loading database")
# Odoo 20.0 on Windows: the filestore garbage collection run by the test classes
# (setUpClass/tearDownClass) cannot unlink files (T1.2 finding). The leftover
# .__gc files then trip `assert not path.endswith(GC_FILE_SUFFIX)`.
WINDOWS_GC_FRAME = "_gc_file_store_unsafe"
WINDOWS_GC_ERRORS = ("assert not path.endswith(GC_FILE_SUFFIX)", "PermissionError")


def odoo(*args, log):
    cmd = [str(PYTHON), str(ODOO_BIN), *args]
    with open(log, "w", encoding="utf-8") as fh:
        return subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, check=False).returncode


def parse(log):
    """Return (summary or None, [(kind, test, text)], other error lines)."""
    problems, other_errors, summary = [], [], None
    current = None
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
        match = LOG_LINE.match(line)
        if not match:
            if current:
                current[2].append(line)
            continue
        current = None
        level, _logger, message = match.groups()
        if found := SUMMARY.search(message):
            summary = tuple(int(n) for n in found.groups())
        elif level in ("ERROR", "CRITICAL") and (problem := TEST_PROBLEM.match(message)):
            current = (problem.group(1), problem.group(2), [])
            problems.append(current)
        elif level in ("ERROR", "CRITICAL"):
            other_errors.append(line)
    return summary, [(kind, test, "\n".join(text)) for kind, test, text in problems], other_errors


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

    if not args.reuse:
        init = ["db", "-c", str(CONF), "init", db, "--force"] + (["--with-demo"] if args.with_demo else [])
        if odoo(*init, log=log):
            sys.exit(f"could not create database {db}; see {log}")
    # Tests start Odoo's HTTP server; a port of its own lets them run next to the dev server.
    rc = odoo("-c", str(CONF), "-d", db, "-u" if args.reuse else "-i", ",".join(modules), "--test-enable",
              "--test-tags", tags, "--http-port", TEST_HTTP_PORT, "--stop-after-init", log=log)

    summary, problems, other_errors = parse(log)
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
    unexplained = failed + errors - len(known)
    if unexplained > 0:
        print(f"RESULT: FAILED ({unexplained})")
        return 1
    print("RESULT: OK" + (" (Windows gc errors only)" if known else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
