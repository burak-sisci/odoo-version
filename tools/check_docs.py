"""Check that the project documents are consistent with each other.

Usage: python tools/check_docs.py
Exit code 0 = consistent, 1 = errors found (the step is not done).
"""
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECISION_STATUSES = {"Geçerli", "Açık", "Ertelendi"}
MATRIX_STATUSES = {"plan", "inceleniyor", "geliştiriliyor", "test", "tamam"}
DATE_RE = re.compile(r"^Son güncelleme: (\d{4}-\d{2}-\d{2})\s*$", re.M)
TASK_RE = re.compile(r"\bT\d+\.\d+\b")
TRIGGER_RE = re.compile(r"\*\*(Karar noktası|Yeniden değerlendirme):\*\*(.*)")

errors = []


def read(rel):
    path = ROOT / rel
    if not path.exists():
        errors.append(f"{rel}: dosya yok")
        return ""
    return path.read_text(encoding="utf-8")


def parse_date(value, where):
    try:
        return datetime.date.fromisoformat(value)
    except (TypeError, ValueError):
        errors.append(f"{where}: geçersiz tarih {value!r}")
        return None


def check_state():
    try:
        state = json.loads(read("state.json") or "{}")
    except json.JSONDecodeError as e:
        errors.append(f"state.json: geçersiz JSON ({e})")
        return {}
    for key in ("last_updated", "phase", "current_task", "tasks_done",
                "blocked_on_user", "next_actions", "decisions", "docs"):
        if key not in state:
            errors.append(f"state.json: '{key}' anahtarı eksik")
    return state


def roadmap_tasks():
    text = read("ROADMAP.md")
    return dict((tid, mark) for mark, tid in re.findall(r"^- \[(.)\] (T\d+\.\d+)", text, flags=re.M))


def check_decisions(state, tasks):
    text = read("DECISIONS.md")
    blocks = re.split(r"^### ", text, flags=re.M)[1:]
    found = {}
    for block in blocks:
        m = re.match(r"(D-\d{3})", block)
        s = re.search(r"\*\*Durum:\*\*\s*(\S+)", block)
        if not m:
            continue
        if not s or s.group(1) not in DECISION_STATUSES:
            errors.append(f"DECISIONS.md: {m.group(1)} durumu geçersiz/eksik (izinli: {sorted(DECISION_STATUSES)})")
            continue
        found[m.group(1)] = s.group(1)
        triggers = TRIGGER_RE.findall(block)
        if s.group(1) == "Ertelendi" and not any(k == "Karar noktası" and TASK_RE.search(v) for k, v in triggers):
            errors.append(f"DECISIONS.md: {m.group(1)} ertelenmiş ama '**Karar noktası:** T<faz>.<sıra>' satırı yok")
        for kind, value in triggers:
            for tid in TASK_RE.findall(value):
                if tasks.get(tid) == "x":
                    errors.append(f"DECISIONS.md: {m.group(1)} '{kind}' görevi {tid} tamamlanmış; karar güncellenmeli")
    summary = dict(re.findall(r"^\| (D-\d{3}) \|[^|]*\| (\S+) \|$", text, flags=re.M))
    if summary != found:
        errors.append(f"DECISIONS.md: özet tablo ile kayıtlar uyuşmuyor ({summary} != {found})")
    in_state = {d.get("id"): d.get("status") for d in state.get("decisions", [])}
    if in_state != found:
        errors.append(f"state.json decisions ile DECISIONS.md uyuşmuyor: "
                      f"yalnız state'te={sorted(set(in_state.items()) - set(found.items()))}, "
                      f"yalnız DECISIONS'ta={sorted(set(found.items()) - set(in_state.items()))}")
    open_ids = {k for k, v in found.items() if v == "Açık"}
    if set(state.get("blocked_on_user", [])) != open_ids:
        errors.append(f"state.json blocked_on_user açık kararlarla aynı olmalı: {sorted(open_ids)}")


def check_roadmap(state, tasks):
    current = state.get("current_task")
    if current not in tasks:
        errors.append(f"state.json current_task {current!r} ROADMAP.md içinde yok")
    elif tasks[current] == "x":
        errors.append(f"state.json current_task {current} ROADMAP.md'de tamamlanmış görünüyor")
    done_roadmap = {t for t, mark in tasks.items() if mark == "x"}
    done_state = set(state.get("tasks_done", []))
    if done_roadmap != done_state:
        errors.append(f"tamamlanan görevler uyuşmuyor: yalnız ROADMAP={sorted(done_roadmap - done_state)}, "
                      f"yalnız state={sorted(done_state - done_roadmap)}")


def check_task_refs(state, tasks):
    # CHANGELOG is history: it may name tasks that were later renumbered or removed.
    for rel in ["state.json"] + [d for d in state.get("docs", []) if d.endswith(".md") and d != "CHANGELOG.md"]:
        for tid in sorted(set(TASK_RE.findall(read(rel)))):
            if tid not in tasks:
                errors.append(f"{rel}: {tid} görevine atıf var ama ROADMAP.md'de yok")


def check_dates(state):
    last = parse_date(state.get("last_updated"), "state.json last_updated")
    today = datetime.date.today()
    changelog = read("CHANGELOG.md")
    heads = re.findall(r"^## (\d{4}-\d{2}-\d{2})", changelog, flags=re.M)
    if not heads:
        errors.append("CHANGELOG.md: tarih başlığı yok")
    elif last and heads[0] != last.isoformat():
        errors.append(f"CHANGELOG.md en üst kayıt {heads[0]} != state.json last_updated {last}")
    for rel in state.get("docs", []):
        if not rel.endswith(".md"):
            continue
        m = DATE_RE.search(read(rel))
        if not m:
            errors.append(f"{rel}: 'Son güncelleme: YYYY-AA-GG' satırı yok")
            continue
        d = parse_date(m.group(1), rel)
        if d and d > today:
            errors.append(f"{rel}: tarih gelecekte ({d})")
        if d and last and d > last:
            errors.append(f"{rel}: tarih ({d}) state.json last_updated'dan ({last}) yeni")


def check_matrix():
    text = read("docs/MODULE_MATRIX.md")
    for line in text.splitlines():
        if not line.startswith("|") or line.startswith("|---") or "Durum |" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[-1] not in MATRIX_STATUSES:
            errors.append(f"MODULE_MATRIX.md: geçersiz durum {cells[-1]!r} → {cells[0]}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    state = check_state()
    tasks = roadmap_tasks()
    check_decisions(state, tasks)
    check_roadmap(state, tasks)
    check_task_refs(state, tasks)
    check_dates(state)
    check_matrix()
    if errors:
        print(f"HATA: {len(errors)} tutarsızlık bulundu")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: belgeler tutarlı")
    return 0


if __name__ == "__main__":
    sys.exit(main())
