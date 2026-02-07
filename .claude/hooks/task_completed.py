#!/usr/bin/env python3
"""Hook: TaskCompleted — validate the current week when a task is marked done."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

# hooks live at .claude/hooks/ — add scripts/ to path for _common.
_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

from _common import python_for_repo, read_current_week  # noqa: E402


def _parse_week_from_task_subject(task_subject: str | None) -> str | None:
    if not task_subject:
        return None
    m = re.search(r"\[\s*week_(\d{1,2})\s*\]", task_subject, flags=re.IGNORECASE)
    if not m:
        return None
    return f"week_{int(m.group(1)):02d}"


def main() -> int:
    root = _REPO_ROOT
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"[TaskCompleted hook] invalid JSON on stdin: {e}", file=sys.stderr)
        return 2

    week = _parse_week_from_task_subject(payload.get("task_subject"))
    if not week:
        week = read_current_week(root)
    if not week:
        print(
            "[TaskCompleted hook] cannot determine target week. "
            "Use task subject prefix like '[week_XX] ...' or set chapters/current_week.txt.",
            file=sys.stderr,
        )
        return 2

    python = python_for_repo(root)
    cmd = [python, str(root / "scripts" / "validate_week.py"), "--week", week, "--mode", "task"]
    print(f"[TaskCompleted hook] running: {' '.join(cmd)}", file=sys.stderr)
    proc = subprocess.run(cmd, cwd=root, text=True, capture_output=True)
    if proc.returncode != 0:
        print("─" * 60, file=sys.stderr)
        if proc.stdout:
            print(proc.stdout.rstrip(), file=sys.stderr)
        if proc.stderr:
            print(proc.stderr.rstrip(), file=sys.stderr)
        print("─" * 60, file=sys.stderr)
        print(f"[TaskCompleted hook] validation FAILED for {week}.", file=sys.stderr)
    else:
        print(f"[TaskCompleted hook] validation OK for {week}.", file=sys.stderr)
    return 0 if proc.returncode == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
