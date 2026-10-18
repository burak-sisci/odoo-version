"""Port an OCA module to Odoo 20.0 under ports/oca/<repo>/<module> (D-019).

Commands:
  fetch REPO MODULE [--branch 19.0] [--commit SHA]
      copy the module from github.com/OCA/REPO into ports/oca/REPO/MODULE,
      move the manifest version to 20.0 and write PORT.md (source, license)
  upgrade PORT_DIR
      run Odoo's upgrade_code scripts newer than the source branch on the port
  diff PORT_DIR [--stat]
      show the port's changes against the source commit recorded in PORT.md

The source is cloned shallow and sparse into a temporary directory; none of
its files is executed. upgrade_code runs with the Windows fixes found in T1.2:
paths printed with forward slashes, UTF-8 files, writes limited to the port.
Manual changes are listed by hand in PORT.md.
"""
import argparse
import ast
import datetime
import importlib.util
import logging
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from pg import ROOT

PORTS = ROOT / "ports" / "oca"
VENV = ROOT / ".venv"
PYTHON = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
ODOO_ROOT = ROOT / "upstream" / "odoo"
UPGRADE_SCRIPTS = ODOO_ROOT / "odoo" / "upgrade_code"
TARGET_SERIES = "20.0"
# OCA migration rule: the first version on a new series is <series>.1.0.0. Keeping it lets
# the official OCA release, and its migration scripts, follow the port without a gap.
PORT_VERSION = f"{TARGET_SERIES}.1.0.0"
# Licenses of our policy (D-008); anything else needs a look at COMPLIANCE.md first.
LICENSES = {"AGPL-3", "LGPL-3"}
NAME_RE = re.compile(r"^[\w.-]+$")
COPY_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc")
NOTE = "PORT.md"
# PORT.md table rows read back by `upgrade` and `diff`
NOTE_FIELDS = {
    "repo": r"Kaynak depo \| https://github\.com/OCA/([\w.-]+)",
    "branch": r"Kaynak dal \| ([\w.-]+)",
    "commit": r"Kaynak commit \| ([0-9a-f]{40})",
}
NOTE_TEMPLATE = """\
# Port notu: {module}

Son güncelleme: {today}

OCA modülü `{module}`'in Odoo {target}'a taşınmış kopyası (D-019, ARCHITECTURE.md §2 "OCA port düzeni").
Teknik ad, lisans, yazarlar ve telif notları değiştirilmez. OCA resmî {target} sürümünü yayımlayınca
port silinir ve modül `vendor/oca/{repo}` altından kullanılır.

| Alan | Değer |
|---|---|
| Kaynak depo | https://github.com/OCA/{repo} |
| Kaynak dal | {branch} |
| Kaynak commit | {sha} ({date}) |
| Lisans | {license} |
| Yazarlar | {author} |

## Değişiklikler

Kaynakla farkın tamamı: `python tools/port_oca.py diff ports/oca/{repo}/{module}`

- Manifest sürümü `{old_version}` → `{new_version}`, OCA taşıma kuralı (`port_oca.py fetch`).
"""


def git(*args, cwd=None):
    cmd = ["git", "-c", "core.autocrlf=false", "-c", "core.longpaths=true", *args]
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", check=False)
    if result.returncode:
        sys.exit(f"git {' '.join(args)} failed:\n{result.stderr.strip()}")
    return result.stdout.strip()


def remove_tree(path):
    def make_writable(func, name, _exc):
        # git writes its object files read-only; Windows refuses to delete them
        os.chmod(name, stat.S_IWRITE)
        func(name)

    shutil.rmtree(path, onexc=make_writable)


def checkout(repo, branch, commit, module, dest):
    """Clone only MODULE of OCA/REPO into DEST; return (commit sha, commit date)."""
    url = f"https://github.com/OCA/{repo}.git"
    git("clone", "--quiet", "--depth", "1", "--filter=blob:none", "--sparse", "--branch", branch, url, str(dest))
    git("sparse-checkout", "set", module, cwd=dest)
    if commit:
        git("fetch", "--quiet", "--depth", "1", "--filter=blob:none", "origin", commit, cwd=dest)
        git("checkout", "--quiet", commit, cwd=dest)
    if not (dest / module / "__manifest__.py").is_file():
        sys.exit(f"{module} not found in OCA/{repo} {branch}")
    return git("rev-parse", "HEAD", cwd=dest), git("log", "-1", "--format=%cs", cwd=dest)


def read_manifest(module_dir):
    # literal_eval only parses; nothing of the fetched module is executed
    return ast.literal_eval((module_dir / "__manifest__.py").read_text(encoding="utf-8"))


def port_dir(arg):
    port = Path(arg).resolve()
    if port.parent.parent != PORTS.resolve() or not (port / "__manifest__.py").is_file():
        sys.exit(f"{arg} is not a port (expected ports/oca/<repo>/<module>)")
    if not (port / NOTE).is_file():
        sys.exit(f"{port / NOTE} missing")
    return port


def read_note(port):
    text = (port / NOTE).read_text(encoding="utf-8")
    values = {}
    for key, pattern in NOTE_FIELDS.items():
        match = re.search(rf"^\| {pattern} ", text, re.MULTILINE)
        if not match:
            sys.exit(f"{port / NOTE}: row for {key} not found")
        values[key] = match.group(1)
    return values


def add_note_line(port, line):
    path = port / NOTE
    text = path.read_text(encoding="utf-8").rstrip("\n") + f"\n{line}\n"
    today = datetime.date.today().isoformat()
    text = re.sub(r"^Son güncelleme: .*$", f"Son güncelleme: {today}", text, count=1, flags=re.MULTILINE)
    path.write_text(text, encoding="utf-8", newline="")


def cmd_fetch(args):
    for name in (args.repo, args.module, args.branch):
        if not NAME_RE.match(name):
            sys.exit(f"invalid name: {name}")
    target = PORTS / args.repo / args.module
    if target.exists():
        sys.exit(f"{target} exists; remove it to fetch again")
    version_re = re.compile(r"""(["']version["']\s*:\s*["'])""" + re.escape(args.branch) + r"""\.[\d.]+(["'])""")
    tmp = Path(tempfile.mkdtemp(prefix="ov-port-"))
    try:
        sha, date = checkout(args.repo, args.branch, args.commit, args.module, tmp / "src")
        source = tmp / "src" / args.module
        manifest = read_manifest(source)
        license_ = manifest.get("license", "LGPL-3")
        if license_ not in LICENSES:
            sys.exit(f"license {license_} is outside our policy; check docs/COMPLIANCE.md first")
        if not manifest.get("installable", True):
            print(f"warning: {args.module} is marked not installable on {args.branch}")
        text, count = version_re.subn(rf"\g<1>{PORT_VERSION}\g<2>", (source / "__manifest__.py").read_text(encoding="utf-8"))
        if count != 1:
            sys.exit(f"manifest version does not start with {args.branch}: {manifest.get('version')}")
        shutil.copytree(source, target, ignore=COPY_IGNORE)
    finally:
        remove_tree(tmp)
    (target / "__manifest__.py").write_text(text, encoding="utf-8", newline="")
    new_version = read_manifest(target)["version"]
    (target / NOTE).write_text(NOTE_TEMPLATE.format(
        module=args.module, repo=args.repo, branch=args.branch, sha=sha, date=date,
        license=license_, author=manifest.get("author", "-"), target=TARGET_SERIES,
        old_version=manifest["version"], new_version=new_version,
        today=datetime.date.today().isoformat(),
    ), encoding="utf-8", newline="")
    print(f"copied OCA/{args.repo}@{sha[:8]} ({date}) {args.module} -> {target.relative_to(ROOT).as_posix()}")
    print(f"version {manifest['version']} -> {new_version}, license {license_}")
    print("next: python tools/port_oca.py upgrade <port>; list manual changes in PORT.md;"
          " add the port to docs/COMPLIANCE.md section 5")
    return 0


def module_index():
    """Module name -> directory, in addons path order (ARCHITECTURE.md section 2)."""
    bases = [ODOO_ROOT / "addons", ODOO_ROOT / "odoo" / "addons",
             *sorted((ROOT / "vendor" / "oca").glob("*")), *sorted(PORTS.glob("*")), ROOT / "addons"]
    index = {}
    for base in bases:
        for manifest in sorted(base.glob("*/__manifest__.py")):
            index.setdefault(manifest.parent.name, manifest.parent)
    return index


def dependencies(module):
    index, found, stack = module_index(), {}, [module]
    while stack:
        name = stack.pop()
        if name in found:
            continue
        if name not in index:
            sys.exit(f"dependency {name} is not in the addons path; vendor or port it first")
        found[name] = index[name]
        stack.extend(read_manifest(index[name]).get("depends", []))
    return found


class WarningCounter(logging.Handler):
    """Counts the warnings of the scripts: files they could not rewrite."""

    def __init__(self):
        super().__init__(logging.WARNING)
        self.count = 0

    def emit(self, record):
        self.count += 1


def load_scripts(source_branch, parse_version):
    """upgrade_code scripts newer than the source branch, plus the unversioned ones (Owl 3)."""
    scripts = []
    for path in sorted(UPGRADE_SCRIPTS.glob("*.py")):
        prefix = path.name.partition("-")[0]
        if re.fullmatch(r"\d+\.\d+", prefix) and not (
                parse_version(source_branch) < parse_version(prefix) <= parse_version(TARGET_SERIES)):
            continue
        spec = importlib.util.spec_from_file_location(f"upgrade_code_{path.stem}", path)
        script = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = script  # dataclasses look their module up
        spec.loader.exec_module(script)
        if hasattr(script, "upgrade"):  # tools_*.py are helpers
            scripts.append((path.stem, script))
    return scripts


def cmd_upgrade(args):
    port = port_dir(args.port)
    if not sys.flags.utf8_mode or Path(sys.prefix).resolve() != VENV.resolve():
        # Odoo's dependencies live in the venv; the scripts read files with the default encoding.
        cmd = [str(PYTHON), "-X", "utf8", str(Path(__file__).resolve()), "upgrade", str(port)]
        return subprocess.run(cmd, check=False).returncode
    note = read_note(port)
    deps = dependencies(port.name)
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    warnings = WarningCounter()
    logging.getLogger().addHandler(warnings)
    sys.path.insert(0, str(ODOO_ROOT))
    from odoo.cli import upgrade_code  # noqa: PLC0415 (needs the venv and sys.path set above)
    from odoo.tools import parse_version  # noqa: PLC0415

    class ForwardSlashPath(type(Path())):
        """The scripts test paths with '/static/'; on Windows str(path) has backslashes."""

        def __str__(self):
            return super().__str__().replace("\\", "/")

    outside = []

    class PortFile(upgrade_code.FileAccessor):
        """Saves inside the port only, as UTF-8 with LF line ends."""

        def _save(self):
            if not self.dirty:
                return
            if not self.path.is_relative_to(port):
                # e.g. the ir.access script also rewrites the dependencies it reads
                outside.append(self.path)
            elif self._content is None:
                self.path.unlink(missing_ok=True)
            else:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                self.path.write_text(self._content, encoding="utf-8", newline="")

    upgrade_code.Path = ForwardSlashPath
    upgrade_code.FileAccessor = PortFile

    results, failed = [], False
    for name, script in load_scripts(note["branch"], parse_version):
        # One file manager per script, so each one reads the result of the previous one.
        manager = upgrade_code.FileManager([str(port.parent)])
        manager._files = {key: file for key, file in manager._files.items() if file.path.is_relative_to(port)}
        manager._modules = {module: ForwardSlashPath(path) for module, path in deps.items()}
        try:
            script.upgrade(manager)
        except Exception as exc:  # noqa: BLE001
            print(f"{name}: ERROR {type(exc).__name__}: {exc} (changes of this script not saved)")
            failed = True
            continue
        changed = sorted((file for file in manager if file.dirty), key=lambda file: str(file.path))
        for file in changed:
            file._save()
        inside = [file for file in changed if file.path.is_relative_to(port)]
        print(f"{name}: {len(inside)} file(s)")
        for file in inside:
            status = "deleted" if file.content is None else "updated"
            print(f"  {status}: {file.path.relative_to(port).as_posix()}")
        for line in manager._summary:
            print(f"  {line}")
        if inside:
            results.append(f"`{name}` {len(inside)} dosya")
    if outside:
        print(f"changes outside the port, not saved: {len(outside)}")
    if failed:
        return 1
    summary = ", ".join(results) if results else "değişiklik yok"
    if warnings.count:
        summary += f"; elle bakılacak {warnings.count} uyarı (betik çıktısı)"
    add_note_line(port, f"- Odoo `upgrade_code` betikleri, {note['branch']} sonrası ve Owl 3 (`port_oca.py upgrade`): {summary}.")
    print(f"recorded in {NOTE}: {summary}")
    return 0


def cmd_diff(args):
    port = port_dir(args.port)
    note = read_note(port)
    tmp = Path(tempfile.mkdtemp(prefix="ov-port-"))
    try:
        checkout(note["repo"], note["branch"], note["commit"], port.name, tmp / "src")
        shutil.copytree(tmp / "src" / port.name, tmp / "source" / port.name, ignore=COPY_IGNORE)
        shutil.copytree(port, tmp / "port" / port.name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", NOTE))
        cmd = ["git", "-c", "core.autocrlf=false", "--no-pager", "diff", "--no-index", "--no-prefix",
               *(["--stat"] if args.stat else []), "source", "port"]
        rc = subprocess.run(cmd, cwd=tmp, check=False).returncode
    finally:
        remove_tree(tmp)
    return 0 if rc in (0, 1) else rc  # 1: differences found


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    fetch = commands.add_parser("fetch", help="copy an OCA module into ports/oca")
    fetch.add_argument("repo")
    fetch.add_argument("module")
    fetch.add_argument("--branch", default="19.0")
    fetch.add_argument("--commit")
    upgrade = commands.add_parser("upgrade", help="run upgrade_code on a port")
    upgrade.add_argument("port")
    diff = commands.add_parser("diff", help="changes against the source commit")
    diff.add_argument("port")
    diff.add_argument("--stat", action="store_true")
    args = parser.parse_args()
    return {"fetch": cmd_fetch, "upgrade": cmd_upgrade, "diff": cmd_diff}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
