"""Copy Odoo's AI agent skills from the pinned upstream into .claude/skills/.

The skills are upstream files (LGPL-3, Odoo S.A.) and are copied verbatim;
they are never edited here. Project rules that take precedence over them are
in CLAUDE.md. Run again whenever the upstream commit moves.

Usage: python tools/sync_skills.py [--check]
  --check  exit 1 if .claude/skills/ differs from upstream (for CI)
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = ROOT / "upstream" / "odoo"
SOURCE = UPSTREAM / "skills"
TARGET = ROOT / ".claude" / "skills"
# Our own files next to the copies: the provenance note and the license text.
LOCAL_FILES = {"SOURCE.md", "LICENSE"}

SOURCE_NOTE = """# Kaynak

Bu klasördeki rehberler Odoo Community deposunun `skills/` klasörünün değiştirilmemiş kopyasıdır.

- Kaynak: https://github.com/odoo/odoo, dal 20.0, commit `{commit}`
- Telif: Odoo S.A. Lisans: LGPL-3 (`LICENSE`, upstream deposundan kopya).
- Elle düzenlenmez. Upstream commit'i ilerleyince `python tools/sync_skills.py` ile yeniden kopyalanır.
- Proje kurallarıyla çelişkide `CLAUDE.md` önce gelir.
"""


def lf(path):
    # The upstream checkout may use CRLF on Windows (core.autocrlf); this repository stores LF.
    return path.read_bytes().replace(b"\r\n", b"\n")


def upstream_files():
    return sorted(p.relative_to(SOURCE) for p in SOURCE.rglob("*") if p.is_file())


def local_files():
    if not TARGET.exists():
        return []
    return sorted(p.relative_to(TARGET) for p in TARGET.rglob("*")
                  if p.is_file() and str(p.relative_to(TARGET)) not in LOCAL_FILES)


def upstream_commit():
    return subprocess.run(["git", "-C", str(UPSTREAM), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()


def differences():
    diffs = []
    wanted, present = upstream_files(), local_files()
    diffs += [f"missing: {p}" for p in wanted if p not in present]
    diffs += [f"extra: {p}" for p in present if p not in wanted]
    diffs += [f"changed: {p}" for p in wanted if p in present and lf(SOURCE / p) != lf(TARGET / p)]
    license_copy = TARGET / "LICENSE"
    if not license_copy.exists() or lf(UPSTREAM / "LICENSE") != lf(license_copy):
        diffs.append("changed: LICENSE")
    note = TARGET / "SOURCE.md"
    if not note.exists() or note.read_text(encoding="utf-8") != SOURCE_NOTE.format(commit=upstream_commit()):
        diffs.append("changed: SOURCE.md (upstream commit)")
    return diffs


def sync():
    if TARGET.exists():
        shutil.rmtree(TARGET)
    for rel in upstream_files():
        (TARGET / rel).parent.mkdir(parents=True, exist_ok=True)
        (TARGET / rel).write_bytes(lf(SOURCE / rel))
    (TARGET / "LICENSE").write_bytes(lf(UPSTREAM / "LICENSE"))
    (TARGET / "SOURCE.md").write_text(SOURCE_NOTE.format(commit=upstream_commit()), encoding="utf-8", newline="\n")
    print(f"copied {len(upstream_files())} files to {TARGET}")


def main():
    if not SOURCE.is_dir():
        sys.exit(f"no upstream skills at {SOURCE}; initialise the submodule first")
    if "--check" in sys.argv[1:]:
        diffs = differences()
        print("\n".join(diffs) or "skills: in sync with upstream")
        return 1 if diffs else 0
    sync()
    return 0


if __name__ == "__main__":
    sys.exit(main())
