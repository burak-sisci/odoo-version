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
PLAN = "PLAN.md"
USER_TASKS = "USER_TASKS.md"
DECISION_STATUSES = {"Geçerli", "Açık", "Ertelendi"}
MATRIX_STATUSES = {"plan", "inceleniyor", "geliştiriliyor", "test", "tamam"}
# Task categories (D-021): K = user, B = together, C = Claude.
CATEGORIES = ("K", "B", "C")
USER_CATEGORIES = {"K", "B"}
DATE_RE = re.compile(r"^Son güncelleme: (\d{4}-\d{2}-\d{2})\s*$", re.M)
TASK_RE = re.compile(r"\bT\d+\.\d+\b")
TRIGGER_RE = re.compile(r"\*\*(Karar noktası|Yeniden değerlendirme):\*\*(.*)")
PLAN_TASK_RE = re.compile(r"^- \[(.)\] (T\d+\.\d+) (.*)$", re.M)
CATEGORY_RE = re.compile(r"· (\S+)(?: — .*)?$")
PHASE_RE = re.compile(r"^### (F\d+) — .*`\[(.)\]`\s*$", re.M)
DASH_RE = re.compile(r"^\| (F\d+) \|(?:[^|]*\|){3} `\[(.)\]` \| (\d+)/(\d+) \| (\d+) · (\d+) · (\d+) \|$", re.M)
TOTAL_RE = re.compile(r"^\*\*Toplam:\*\* (\d+)/(\d+) görev · Kullanıcı (\d+) · Birlikte (\d+) · Claude (\d+)\s*$", re.M)
CURRENT_RE = re.compile(r"^\*\*Şu anki görev:\*\* (T\d+\.\d+)", re.M)
USER_TASK_RE = re.compile(r"^- \[(.)\] (T\d+\.\d+)\b", re.M)
ACTION_DEF_RE = re.compile(r"^- \[.\] (K\d+)\b", re.M)
ACTION_REF_RE = re.compile(r"\bK\d+\b")

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


def plan_tasks():
    """Return ({task id: mark}, {task id: category}) from the PLAN task lines."""
    tasks, categories = {}, {}
    for mark, tid, rest in PLAN_TASK_RE.findall(read(PLAN)):
        if tid in tasks:
            errors.append(f"{PLAN}: {tid} birden fazla görev satırında")
        tasks[tid] = mark
        m = CATEGORY_RE.search(rest)
        if not m or m.group(1) not in CATEGORIES:
            errors.append(f"{PLAN}: {tid} kategorisi geçersiz/eksik (izinli: {list(CATEGORIES)})")
            continue
        categories[tid] = m.group(1)
    return tasks, categories


def phase_of(tid):
    return "F" + tid[1:].split(".")[0]


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


def check_plan(state, tasks):
    current = state.get("current_task")
    if current not in tasks:
        errors.append(f"state.json current_task {current!r} {PLAN} içinde yok")
    elif tasks[current] == "x":
        errors.append(f"state.json current_task {current} {PLAN}'de tamamlanmış görünüyor")
    elif state.get("phase", {}).get("id") != phase_of(current):
        errors.append(f"state.json phase.id {state.get('phase', {}).get('id')!r} != current_task fazı {phase_of(current)}")
    done_plan = {t for t, mark in tasks.items() if mark == "x"}
    done_state = set(state.get("tasks_done", []))
    if done_plan != done_state:
        errors.append(f"tamamlanan görevler uyuşmuyor: yalnız {PLAN}={sorted(done_plan - done_state)}, "
                      f"yalnız state={sorted(done_state - done_plan)}")


def category_counts(tids, categories):
    return tuple(sum(1 for t in tids if categories.get(t) == c) for c in CATEGORIES)


def check_dashboard(state, tasks, categories):
    # The progress dashboard is maintained by hand; it must agree with the task lines.
    text = read(PLAN)
    by_phase = {}
    for tid, mark in tasks.items():
        by_phase.setdefault(phase_of(tid), []).append(mark)
    headers = dict(PHASE_RE.findall(text))
    dash = {f: (mark, int(d), int(t), (int(k), int(b), int(c)))
            for f, mark, d, t, k, b, c in DASH_RE.findall(text)}
    for phase in sorted(set(headers) | set(dash) | set(by_phase), key=lambda f: int(f[1:])):
        marks = by_phase.get(phase, [])
        if not marks:
            errors.append(f"{PLAN}: {phase} fazında görev yok")
            continue
        if all(m == "x" for m in marks):
            allowed = {"x"}
        elif any(m in "x~" for m in marks):
            allowed = {"~"}
        else:
            allowed = {" ", "!"}
        if headers.get(phase) not in allowed:
            errors.append(f"{PLAN}: {phase} başlık işareti {headers.get(phase)!r}, beklenen {sorted(allowed)}")
        if phase not in dash:
            errors.append(f"{PLAN}: {phase} panoda yok")
            continue
        mark, done, total, cats = dash[phase]
        if mark not in allowed:
            errors.append(f"{PLAN}: panoda {phase} işareti {mark!r}, beklenen {sorted(allowed)}")
        if (done, total) != (marks.count("x"), len(marks)):
            errors.append(f"{PLAN}: panoda {phase} {done}/{total}, görevlere göre {marks.count('x')}/{len(marks)}")
        expected_cats = category_counts([t for t in tasks if phase_of(t) == phase], categories)
        if cats != expected_cats:
            errors.append(f"{PLAN}: panoda {phase} K · B · C = {cats}, görevlere göre {expected_cats}")
    m = TOTAL_RE.search(text)
    expected = (sum(1 for v in tasks.values() if v == "x"), len(tasks)) + category_counts(tasks, categories)
    if not m:
        errors.append(f"{PLAN}: '**Toplam:** n/m görev · Kullanıcı k · Birlikte b · Claude c' satırı yok")
    elif tuple(int(g) for g in m.groups()) != expected:
        errors.append(f"{PLAN}: toplam satırı {tuple(int(g) for g in m.groups())}, görevlere göre {expected}")
    m = CURRENT_RE.search(text)
    if not m or m.group(1) != state.get("current_task"):
        errors.append(f"{PLAN}: '**Şu anki görev:**' satırı state.json current_task ile aynı olmalı")


def check_user_tasks(state, tasks, categories):
    # USER_TASKS.md lists every K and B task with the same mark as PLAN, and defines the K actions.
    text = read(USER_TASKS)
    listed = {}
    for mark, tid in USER_TASK_RE.findall(text):
        if tid in listed:
            errors.append(f"{USER_TASKS}: {tid} birden fazla kez listelenmiş")
        listed[tid] = mark
    expected = {t for t, c in categories.items() if c in USER_CATEGORIES}
    if set(listed) != expected:
        errors.append(f"{USER_TASKS}: K/B görevleri PLAN ile uyuşmuyor: eksik={sorted(expected - set(listed))}, "
                      f"fazla={sorted(set(listed) - expected)}")
    for tid, mark in listed.items():
        if tid in tasks and tasks[tid] != mark:
            errors.append(f"{USER_TASKS}: {tid} işareti {mark!r}, {PLAN}'da {tasks[tid]!r}")
    defined = ACTION_DEF_RE.findall(text)
    for kid in sorted({k for k in defined if defined.count(k) > 1}):
        errors.append(f"{USER_TASKS}: {kid} birden fazla kez tanımlı")
    for rel in ["state.json"] + [d for d in state.get("docs", []) if d.endswith(".md") and d != "CHANGELOG.md"]:
        for kid in sorted(set(ACTION_REF_RE.findall(read(rel))) - set(defined)):
            errors.append(f"{rel}: {kid} kullanıcı eylemine atıf var ama {USER_TASKS}'da tanımlı değil")


def check_task_refs(state, tasks):
    # CHANGELOG is history: it may name tasks that were later renumbered or removed.
    for rel in ["state.json"] + [d for d in state.get("docs", []) if d.endswith(".md") and d != "CHANGELOG.md"]:
        for tid in sorted(set(TASK_RE.findall(read(rel)))):
            if tid not in tasks:
                errors.append(f"{rel}: {tid} görevine atıf var ama {PLAN}'da yok")


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
    tasks, categories = plan_tasks()
    check_decisions(state, tasks)
    check_plan(state, tasks)
    check_dashboard(state, tasks, categories)
    check_user_tasks(state, tasks, categories)
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
