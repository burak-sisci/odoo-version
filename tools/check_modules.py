"""Check our own Odoo modules against the project rules.

Rules (CLAUDE.md; D-007, D-014, D-016):
- technical name starts with `ov_`;
- manifest: license AGPL-3 (own code) or LGPL-3 (derived from LGPL code),
  version 20.0.x.y.z, AUTHOR among the authors, no `description` key (Odoo
  shows the README instead);
- no "Odoo" or the working name in the texts users see: manifest name and
  summary, README.rst;
- README.rst: Odoo renders the module description as reStructuredText;
- tests/ with at least one test_*.py, i18n/tr.po.

Code-level checks are pylint-odoo's (.pylintrc). OCA ports keep their own
names, licenses and authors (D-019) and are not checked here.

Usage: python tools/check_modules.py [MODULE_DIR...]   (default: every module in addons/)
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADDONS = ROOT / "addons"
PREFIX = "ov_"
# Manifest author of our modules. An assumption until the user decides (USER_TASKS K12);
# .pylintrc (manifest-required-authors) repeats it.
AUTHOR = "burak-sisci"
LICENSES = {"AGPL-3", "LGPL-3"}
VERSION_RE = re.compile(r"^20\.0\.\d+\.\d+\.\d+$")
# "Odoo" as a product name, which also catches the working name odoo-version (D-007, D-014).
BRAND_RE = re.compile(r"odoo", re.IGNORECASE)
README_FILES = ("README.rst", "README.md", "README.txt", "README")


def modules():
    if not ADDONS.is_dir():
        return []
    return sorted(p for p in ADDONS.iterdir() if (p / "__manifest__.py").is_file())


def check(module):
    problems = []
    name = module.name
    try:
        manifest = ast.literal_eval((module / "__manifest__.py").read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError) as exc:
        return [f"__manifest__.py cannot be read: {exc}"]

    if not name.startswith(PREFIX):
        problems.append(f"technical name must start with {PREFIX!r} (D-014)")
    if manifest.get("license") not in LICENSES:
        problems.append(f"license {manifest.get('license')!r}: use AGPL-3, or LGPL-3 for code derived from LGPL code (D-016)")
    if not VERSION_RE.match(str(manifest.get("version", ""))):
        problems.append(f"version {manifest.get('version')!r} must be 20.0.x.y.z")
    authors = [a.strip() for a in str(manifest.get("author", "")).split(",")]
    if AUTHOR not in authors:
        problems.append(f"author {manifest.get('author')!r} must include {AUTHOR!r}")
    if "description" in manifest:
        problems.append("no `description` key: Odoo shows the README as the description")
    for key in ("name", "summary"):
        if BRAND_RE.search(str(manifest.get(key, ""))):
            problems.append(f"manifest {key} mentions Odoo (D-007)")

    readmes = [module / f for f in README_FILES if (module / f).is_file()]
    if not (module / "README.rst").is_file():
        problems.append("README.rst missing: it is the module description, rendered as reStructuredText")
    for readme in readmes:
        if BRAND_RE.search(readme.read_text(encoding="utf-8")):
            problems.append(f"{readme.name} mentions Odoo (D-007); users see it as the module description")

    if not list((module / "tests").glob("test_*.py")):
        problems.append("tests/test_*.py missing")
    if not (module / "i18n" / "tr.po").is_file():
        problems.append("i18n/tr.po missing")
    return problems


def main():
    targets = [Path(arg).resolve() for arg in sys.argv[1:]] or modules()
    failed = 0
    for module in targets:
        for problem in check(module):
            print(f"{module.name}: {problem}")
            failed += 1
    if failed:
        print(f"modules: {failed} problem(s)")
        return 1
    print(f"modules: {len(targets)} checked, OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
