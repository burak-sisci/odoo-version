"""Create the skeleton of a new module of ours in addons/.

The skeleton follows the project rules checked by tools/check_modules.py:
manifest (license, author, version 20.0.1.0.0), README.rst, models/,
security/ir.access.csv, i18n/tr.po and a first test.

Usage: python tools/new_module.py ov_NAME [--title TITLE] [--summary TEXT] [--depends base,...] [--license LGPL-3]
  --title    manifest name (default: from the technical name)
  --summary  one-line manifest summary
  --depends  comma-separated dependencies (default: base)
  --license  AGPL-3 (default, our own code) or LGPL-3 (derived from LGPL code, D-016)
"""
import argparse
import re
import sys

from check_modules import ADDONS, AUTHOR, LICENSES, PREFIX

NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def manifest(name, title, summary, depends, license_):
    deps = "".join(f"        {dep!r},\n" for dep in depends)
    return (
        "{\n"
        f"    'name': {title!r},\n"
        "    'version': '20.0.1.0.0',\n"
        f"    'summary': {summary!r},\n"
        f"    'author': {AUTHOR!r},\n"
        f"    'license': {license_!r},\n"
        "    'depends': [\n"
        f"{deps}"
        "    ],\n"
        "    'data': [\n"
        "        'security/ir.access.csv',\n"
        "    ],\n"
        "}\n"
    )


def readme(title, summary):
    return (
        f"{'=' * len(title)}\n{title}\n{'=' * len(title)}\n\n"
        f"{summary}\n\n"
        ".. Bu metin Uygulamalar ekranında modülün açıklaması olarak görünür (reStructuredText).\n"
        "   Modülün ne yaptığını, nasıl kurulduğunu ve kullanıldığını Türkçe anlat.\n"
    )


def translation(name):
    return (
        f"# Turkish translation of the {name} module.\n"
        "#\n"
        'msgid ""\n'
        'msgstr ""\n'
        f'"Project-Id-Version: {name} 20.0\\n"\n'
        '"Report-Msgid-Bugs-To: \\n"\n'
        '"Last-Translator: \\n"\n'
        '"Language-Team: \\n"\n'
        '"Language: tr\\n"\n'
        '"MIME-Version: 1.0\\n"\n'
        '"Content-Type: text/plain; charset=UTF-8\\n"\n'
        '"Content-Transfer-Encoding: \\n"\n'
        '"Plural-Forms: nplurals=2; plural=n != 1;\\n"\n'
    )


def first_test(name):
    cls = "Test" + "".join(part.capitalize() for part in name.split("_"))
    return (
        "from odoo.tests import TransactionCase, tagged\n"
        "\n"
        "\n"
        "@tagged('post_install', '-at_install')\n"
        f"class {cls}(TransactionCase):\n"
        "\n"
        "    def test_module_installed(self):\n"
        f"        module = self.env['ir.module.module'].search([('name', '=', {name!r})])\n"
        "        self.assertEqual(module.state, 'installed')\n"
    )


def files(name, title, summary, depends, license_):
    return {
        "__init__.py": "from . import models\n",
        "__manifest__.py": manifest(name, title, summary, depends, license_),
        "README.rst": readme(title, summary),
        "models/__init__.py": "",
        "security/ir.access.csv": "id,name,model_id,group_id/id,operation,domain\n",
        "i18n/tr.po": translation(name),
        "tests/__init__.py": f"from . import test_{name}\n",
        f"tests/test_{name}.py": first_test(name),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("name")
    parser.add_argument("--title")
    parser.add_argument("--summary", default="")
    parser.add_argument("--depends", default="base")
    parser.add_argument("--license", default="AGPL-3", choices=sorted(LICENSES))
    args = parser.parse_args()
    if not (NAME_RE.match(args.name) and args.name.startswith(PREFIX)):
        sys.exit(f"technical name must be lowercase snake_case and start with {PREFIX!r}")
    target = ADDONS / args.name
    if target.exists():
        sys.exit(f"{target} already exists")
    title = args.title or args.name.removeprefix(PREFIX).replace("_", " ").title()
    summary = args.summary or title
    depends = [dep.strip() for dep in args.depends.split(",") if dep.strip()]
    for rel, content in files(args.name, title, summary, depends, args.license).items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    print(f"created {target}")
    print(f"next: python tools/run_tests.py {args.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
