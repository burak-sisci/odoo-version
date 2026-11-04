"""Turkish translation coverage of the package modules; overlay of ov_i18n_tr (T3.6).

Upstream ships for each module a template of its translatable terms
(i18n/<module>.pot) and a Turkish translation (i18n/tr.po). The module
ov_i18n_tr adds the missing translations and corrections in
addons/ov_i18n_tr/i18n_overlay/<module>.po, read after upstream's file. A term
counts as translated when the overlay or upstream gives it a translation.

The package modules are the applications of the sales package (MVP_APPS in
.github/workflows/ci.yml) and our modules, with their dependencies and the
modules Odoo installs automatically with them.

Usage:
  python tools/po_coverage.py [report] [--modules a,b] [--min PERCENT]
      coverage per module and in total; exit code 1 under --min
  python tools/po_coverage.py missing MODULE [--limit N] [--out FILE]
      untranslated terms as JSON, keyed for `add`
  python tools/po_coverage.py add MODULE FILE.json
      add translations {key: translation} to the overlay of MODULE
  python tools/po_coverage.py lookup TEXT [--modules a,b] [--limit N]
      existing translations of the terms containing TEXT (terminology)
  python tools/po_coverage.py check
      validate the overlay files: terms of the template, placeholders, tags
  python tools/po_coverage.py sync
      copy the comments of the current templates into the overlay files
"""
import argparse
import ast
import hashlib
import itertools
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = ROOT / "upstream" / "odoo"
OVERLAY_DIR = ROOT / "addons" / "ov_i18n_tr" / "i18n_overlay"
CI = ROOT / ".github" / "workflows" / "ci.yml"
LANG = "tr"
COUNTRY = "tr"
OWN_PREFIX = "ov_"

# Attributes whose value Odoo translates inside a term (odoo.tools.translate.TRANSLATED_ATTRS)
TRANSLATED_ATTRS = {
    "string", "add-label", "help", "sum", "avg", "confirm", "placeholder", "alt", "title", "aria-label",
    "aria-keyshortcuts", "aria-placeholder", "aria-roledescription", "aria-valuetext",
    "value_label", "data-tooltip", "label", "confirm-label", "cancel-label", "confirm-title",
}
TRANSLATED_ATTRS |= {f"t-attf-{attr}" for attr in TRANSLATED_ATTRS}

PRINTF_RE = re.compile(r"%(?:\((?P<name>[^)]*)\))?[-#0+]*(?:\d+|\*)?(?:\.(?:\d+|\*))?(?P<conv>[diouxXeEfFgGcrsa%])")
BRACE_RE = re.compile(r"\{\{.*?\}\}|\{[\w.]*\}")
TAG_RE = re.compile(r"<(/?)([A-Za-z][\w:.-]*)((?:\s+[^\s=>/]+(?:\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>]+))?)*)\s*(/?)>")
UNDERLINE_RE = re.compile(r"([=\-~^\"`#*+])\1{2,}")
ATTR_RE = re.compile(r"([^\s=>/]+)(?:\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+))?")


# --- PO files ----------------------------------------------------------------

class Entry:
    __slots__ = ("comments", "flags", "msgid", "msgstr")

    def __init__(self, comments, msgid, msgstr, flags=()):
        self.comments = comments  # raw comment lines: "#. module: x", "#: code:...", "#, flag"
        self.msgid = msgid
        self.msgstr = msgstr
        self.flags = flags

    @property
    def module(self):
        for line in self.comments:
            m = re.match(r"#\.\s*modules?:\s*(\w+)", line)
            if m:
                return m.group(1)
        return None

    @property
    def references(self):
        return [ref for line in self.comments if line.startswith("#:") for ref in line[2:].split()]

    @property
    def kinds(self):
        return [line[2:].strip() for line in self.comments if line.startswith("#.") and "module" not in line]


def _unquote(text):
    return ast.literal_eval(text)


def read_po(path):
    """Return (header lines, [Entry]) of a PO file; obsolete entries are dropped."""
    if not path.is_file():
        return [], []
    entries = []
    header = []
    block = []
    for line in path.read_text(encoding="utf-8").splitlines() + [""]:
        if line.strip():
            block.append(line)
            continue
        if not block:
            continue
        comments, msgid, msgstr, plural = [], [], [], False
        target = None
        for raw in block:
            if raw.startswith("#~"):
                comments = None
                break
            if raw.startswith("#"):
                comments.append(raw)
            elif raw.startswith("msgctxt"):
                target = None
            elif raw.startswith("msgid_plural"):
                plural = True
                target = None
            elif raw.startswith("msgid "):
                target = msgid
                target.append(_unquote(raw[6:]))
            elif raw.startswith("msgstr[0]"):
                target = msgstr
                target.append(_unquote(raw[9:].strip()))
            elif raw.startswith("msgstr["):
                target = None
            elif raw.startswith("msgstr "):
                target = msgstr
                target.append(_unquote(raw[7:]))
            elif raw.startswith('"') and target is not None:
                target.append(_unquote(raw))
        block = []
        if comments is None or plural:
            continue
        msgid, msgstr = "".join(msgid), "".join(msgstr)
        if not msgid:
            header = comments
            continue
        flags = tuple(f.strip() for line in comments if line.startswith("#,") for f in line[2:].split(","))
        entries.append(Entry(comments, msgid, msgstr, flags))
    return header, entries


def _quote_line(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"').replace("\t", "\\t").replace("\r", "\\r").replace("\n", "\\n") + '"'


def _wrap(text, width=76):
    """Split ``text`` like gettext: after newlines, then at spaces under ``width``."""
    chunks = []
    for part in re.split(r"(?<=\n)", text):
        if not part:
            continue
        while len(part) > width:
            cut = part.rfind(" ", 0, width)
            if cut <= 0:
                break
            chunks.append(part[:cut + 1])
            part = part[cut + 1:]
        chunks.append(part)
    return chunks


def format_string(keyword, text):
    chunks = _wrap(text)
    if len(chunks) <= 1 and len(text) <= 70 and "\n" not in text[:-1]:
        return [f"{keyword} {_quote_line(text)}"]
    return [f'{keyword} ""'] + [_quote_line(chunk) for chunk in chunks]


def write_overlay(module, entries):
    path = OVERLAY_DIR / f"{module}.po"
    lines = [
        f"# Turkish translations of the {module} module completing upstream's (ov_i18n_tr, T3.6).",
        f"# Read after {module}/i18n/tr.po. The comments come from {module}.pot;",
        "# edit with tools/po_coverage.py (add, sync).",
        'msgid ""',
        'msgstr ""',
        '"Project-Id-Version: ov_i18n_tr 20.0\\n"',
        '"Language: tr\\n"',
        '"MIME-Version: 1.0\\n"',
        '"Content-Type: text/plain; charset=UTF-8\\n"',
        '"Content-Transfer-Encoding: \\n"',
        '"Plural-Forms: nplurals=2; plural=n != 1;\\n"',
        "",
    ]
    for entry in entries:
        lines += entry.comments
        lines += format_string("msgid", entry.msgid)
        lines += format_string("msgstr", entry.msgstr)
        lines.append("")
    OVERLAY_DIR.mkdir(parents=True, exist_ok=True)
    path.write_bytes(("\n".join(lines).rstrip("\n") + "\n").encode("utf-8"))


def key(msgid):
    return hashlib.sha1(msgid.encode("utf-8")).hexdigest()[:10]


# --- modules -----------------------------------------------------------------

def addons_dirs():
    dirs = [UPSTREAM / "odoo" / "addons", UPSTREAM / "addons"]
    for parent in (ROOT / "vendor" / "oca", ROOT / "ports" / "oca"):
        if parent.is_dir():
            dirs += sorted(p for p in parent.iterdir() if p.is_dir())
    dirs.append(ROOT / "addons")
    return dirs


def module_dirs():
    found = {}
    for parent in addons_dirs():
        if not parent.is_dir():
            continue
        for manifest in parent.glob("*/__manifest__.py"):
            found.setdefault(manifest.parent.name, manifest.parent)
    return found


def read_manifest(path):
    return ast.literal_eval((path / "__manifest__.py").read_text(encoding="utf-8"))


def mvp_apps():
    m = re.search(r"MVP_APPS:\s*([\w,]+)", CI.read_text(encoding="utf-8"))
    return m.group(1).split(",") if m else []


def online_service_modules():
    """Modules ov_brand removes with the ones depending on them (ov_brand/tools.py)."""
    text = (ROOT / "addons" / "ov_brand" / "tools.py").read_text(encoding="utf-8")
    m = re.search(r"^ONLINE_SERVICE_MODULES = \(([^)]*)\)", text, re.M)
    return set(re.findall(r"'(\w+)'", m.group(1))) if m else set()


def package_modules():
    """Modules of a database with the package: roots, dependencies, auto-installed modules.

    Like Odoo, a module of other countries is not auto-installed; the modules
    of the publisher's online services are removed by ov_brand. The result is
    the module list of the CI database of the package (90 modules on
    2026-11-04) and our auto-installed modules.
    """
    dirs = module_dirs()
    manifests = {name: read_manifest(path) for name, path in dirs.items()}
    roots = ["base"] + mvp_apps() + sorted(n for n in dirs if n.startswith(OWN_PREFIX))
    removed_roots = online_service_modules()
    removed_cache = {}

    def removed(name):
        if name not in removed_cache:
            removed_cache[name] = False
            removed_cache[name] = name in removed_roots or any(
                removed(dep) for dep in manifests.get(name, {}).get("depends", [])
            )
        return removed_cache[name]

    installed = set()

    def add(name):
        if name in installed or name not in manifests:
            return
        installed.add(name)
        for dep in manifests[name].get("depends", []):
            add(dep)

    for name in roots:
        add(name)
    changed = True
    while changed:
        changed = False
        for name, manifest in manifests.items():
            auto = manifest.get("auto_install")
            if name in installed or not auto:
                continue
            countries = manifest.get("countries")
            if countries and COUNTRY not in countries:
                continue
            trigger = auto if isinstance(auto, list) else manifest.get("depends", [])
            if set(trigger) <= installed and not removed(name):
                add(name)
                changed = True
    return {name: dirs[name] for name in sorted(installed) if not removed(name)}


def template(name, path):
    return read_po(path / "i18n" / f"{name}.pot")[1]


def upstream_translations(path):
    values = {}
    for sub in ("i18n", "i18n_extra"):
        for entry in read_po(path / sub / f"{LANG}.po")[1]:
            if entry.msgstr:
                values[entry.msgid] = entry.msgstr
    return values


def overlay(name):
    return {entry.msgid: entry for entry in read_po(OVERLAY_DIR / f"{name}.po")[1]}


def measured_modules(selected=None):
    modules = package_modules()
    if selected:
        unknown = [m for m in selected if m not in module_dirs()]
        if unknown:
            sys.exit(f"unknown modules: {', '.join(unknown)}")
        dirs = module_dirs()
        modules = {m: dirs[m] for m in selected}
    return {n: p for n, p in modules.items() if not n.startswith(OWN_PREFIX) and (p / "i18n" / f"{n}.pot").is_file()}


# --- validation --------------------------------------------------------------

def _tags(text):
    tags = []
    for closing, name, attrs, selfclosing in TAG_RE.findall(text):
        kept = sorted(
            (attr, value) for attr, value in ATTR_RE.findall(attrs) if attr not in TRANSLATED_ATTRS
        )
        tags.append((closing, name, tuple(kept), selfclosing))
    return Counter(tags)


def problems(msgid, msgstr):
    """Return the problems of a translation: placeholders, tags, line breaks, product name."""
    found = []
    if not msgstr.strip():
        found.append("empty translation")
        return found
    src = [(m.group("name"), m.group("conv")) for m in PRINTF_RE.finditer(msgid)]
    dst = [(m.group("name"), m.group("conv")) for m in PRINTF_RE.finditer(msgstr)]
    if Counter(p for p in src if p[0] is not None) != Counter(p for p in dst if p[0] is not None):
        found.append("named placeholders differ")
    if [p for p in src if p[0] is None] != [p for p in dst if p[0] is None]:
        found.append("positional placeholders differ (count, kind or order)")
    if Counter(BRACE_RE.findall(msgid)) != Counter(BRACE_RE.findall(msgstr)):
        found.append("{placeholders} differ")
    if _tags(msgid) != _tags(msgstr):
        found.append("tags or their untranslated attributes differ")
    for edge, test in (("leading", str.startswith), ("trailing", str.endswith)):
        if test(msgid, "\n") != test(msgstr, "\n"):
            found.append(f"{edge} line break differs")
    if "Odoo" in msgstr and "Odoo" not in msgid:
        found.append("product name added")
    # reStructuredText titles (module descriptions): the underline is as long as the title
    lines = msgstr.split("\n")
    for previous, line in itertools.pairwise(lines):
        if (UNDERLINE_RE.fullmatch(line) and previous.strip() and not UNDERLINE_RE.fullmatch(previous)
                and len(line) < len(previous)):
            found.append(f"title underline shorter than {previous[:30]!r}")
    return found


# --- commands ----------------------------------------------------------------

def cmd_report(args):
    selected = args.modules.split(",") if args.modules else None
    rows = []
    for name, path in measured_modules(selected).items():
        terms = template(name, path)
        done_up = upstream_translations(path)
        extra = overlay(name)
        total = len({e.msgid for e in terms})
        done = sum(1 for msgid in {e.msgid for e in terms} if (extra.get(msgid) and extra[msgid].msgstr) or done_up.get(msgid))
        rows.append((name, done, total, len(extra)))
    rows.sort(key=lambda r: (r[1] - r[2], r[0]))
    total_done = sum(r[1] for r in rows)
    total = sum(r[2] for r in rows)
    if not args.quiet:
        print(f"{'module':28} {'translated':>11} {'%':>6} {'missing':>8} {'overlay':>8}")
        for name, done, count, extra in rows:
            pct = 100 * done / count if count else 100.0
            print(f"{name:28} {done:5}/{count:<5} {pct:6.1f} {count - done:8} {extra:8}")
    pct = 100 * total_done / total if total else 100.0
    print(f"TOTAL ({len(rows)} modules): {total_done}/{total} = {pct:.2f}%, missing {total - total_done}")
    if args.min is not None and pct < args.min:
        print(f"FAILED: coverage {pct:.2f}% is under {args.min}%")
        return 1
    return 0


def cmd_missing(args):
    dirs = module_dirs()
    if args.module not in dirs:
        sys.exit(f"unknown module {args.module}")
    path = dirs[args.module]
    done_up = upstream_translations(path)
    extra = overlay(args.module)
    out = []
    seen = set()
    for entry in template(args.module, path):
        if entry.msgid in seen or done_up.get(entry.msgid) or (entry.msgid in extra and extra[entry.msgid].msgstr):
            continue
        seen.add(entry.msgid)
        out.append({"key": key(entry.msgid), "msgid": entry.msgid, "where": entry.references[:3], "kind": entry.kinds})
    out = out[args.offset:args.offset + args.limit] if args.limit else out[args.offset:]
    text = json.dumps(out, ensure_ascii=False, indent=1)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"{len(out)} terms written to {args.out}")
    else:
        sys.stdout.buffer.write(text.encode("utf-8") + b"\n")
    return 0


def cmd_add(args):
    dirs = module_dirs()
    if args.module not in dirs:
        sys.exit(f"unknown module {args.module}")
    given = json.loads(Path(args.file).read_text(encoding="utf-8"))
    terms = {}
    for entry in template(args.module, dirs[args.module]):
        terms.setdefault(entry.msgid, entry)
    by_key = {key(msgid): entry for msgid, entry in terms.items()}
    extra = overlay(args.module)
    failed = 0
    added = 0
    for k, msgstr in given.items():
        entry = by_key.get(k)
        if entry is None:
            print(f"{k}: no such term in {args.module}.pot")
            failed += 1
            continue
        found = problems(entry.msgid, msgstr)
        if found:
            print(f"{k}: {'; '.join(found)}\n  msgid:  {entry.msgid!r}\n  msgstr: {msgstr!r}")
            failed += 1
            continue
        extra[entry.msgid] = Entry(entry.comments, entry.msgid, msgstr)
        added += 1
    order = list(terms)
    entries = sorted(extra.values(), key=lambda e: order.index(e.msgid) if e.msgid in terms else len(order))
    write_overlay(args.module, entries)
    print(f"{args.module}: {added} added or replaced, {failed} rejected, {len(entries)} in the overlay")
    return 1 if failed else 0


def cmd_lookup(args):
    selected = args.modules.split(",") if args.modules else None
    needle = args.text.lower()
    shown = 0
    for name, path in measured_modules(selected).items():
        values = upstream_translations(path)
        values.update({m: e.msgstr for m, e in overlay(name).items() if e.msgstr})
        for msgid, msgstr in values.items():
            if needle in msgid.lower() and len(msgid) <= args.max_length:
                print(f"[{name}] {msgid!r} -> {msgstr!r}")
                shown += 1
                if shown >= args.limit:
                    return 0
    return 0


def cmd_check(args):
    dirs = module_dirs()
    errors = []
    for path in sorted(OVERLAY_DIR.glob("*.po")):
        name = path.stem
        if name not in dirs:
            errors.append(f"{path.name}: no module {name}")
            continue
        terms = {}
        for entry in template(name, dirs[name]):
            terms.setdefault(entry.msgid, entry)
        seen = set()
        for entry in read_po(path)[1]:
            label = f"{path.name}: {entry.msgid[:60]!r}"
            if entry.msgid in seen:
                errors.append(f"{label}: duplicate")
            seen.add(entry.msgid)
            source = terms.get(entry.msgid)
            if source is None:
                errors.append(f"{label}: not in {name}.pot (run `sync`)")
                continue
            if entry.comments != source.comments:
                errors.append(f"{label}: comments differ from {name}.pot (run `sync`)")
            errors += [f"{label}: {p}" for p in problems(entry.msgid, entry.msgstr)]
    for error in errors:
        print(error)
    print(f"overlay: {len(list(OVERLAY_DIR.glob('*.po')))} files, {len(errors)} problems")
    return 1 if errors else 0


def cmd_sync(args):
    dirs = module_dirs()
    for path in sorted(OVERLAY_DIR.glob("*.po")):
        name = path.stem
        terms = {}
        for entry in template(name, dirs[name]) if name in dirs else []:
            terms.setdefault(entry.msgid, entry)
        kept = []
        for entry in read_po(path)[1]:
            source = terms.get(entry.msgid)
            if source is None:
                print(f"{path.name}: dropped {entry.msgid[:60]!r} (no longer in {name}.pot)")
                continue
            kept.append(Entry(source.comments, entry.msgid, entry.msgstr))
        order = list(terms)
        kept.sort(key=lambda e: order.index(e.msgid))
        write_overlay(name, kept)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command")
    report = sub.add_parser("report")
    for p in (parser, report):
        p.add_argument("--modules", help="comma-separated modules (default: the package modules)")
        p.add_argument("--min", type=float, help="fail under this total percentage")
        p.add_argument("--quiet", action="store_true", help="total only")
    missing = sub.add_parser("missing")
    missing.add_argument("module")
    missing.add_argument("--limit", type=int, default=0)
    missing.add_argument("--offset", type=int, default=0)
    missing.add_argument("--out")
    add = sub.add_parser("add")
    add.add_argument("module")
    add.add_argument("file")
    lookup = sub.add_parser("lookup")
    lookup.add_argument("text")
    lookup.add_argument("--modules")
    lookup.add_argument("--limit", type=int, default=30)
    lookup.add_argument("--max-length", type=int, default=120)
    sub.add_parser("check")
    sub.add_parser("sync")
    args = parser.parse_args()
    command = {
        None: cmd_report, "report": cmd_report, "missing": cmd_missing, "add": cmd_add,
        "lookup": cmd_lookup, "check": cmd_check, "sync": cmd_sync,
    }[args.command]
    return command(args)


if __name__ == "__main__":
    sys.exit(main())
