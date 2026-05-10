"""Minimal PyHelper-style CLI used by the Week 14 release deliverable."""

from __future__ import annotations


def format_note(title: str, body: str = "") -> str:
    title = title.strip()
    body = body.strip()
    if not title:
        raise ValueError("title must not be blank")
    return f"# {title}\n\n{body}" if body else f"# {title}"


def main(argv: list[str] | None = None) -> int:
    argv = argv or []
    if not argv:
        print("pyhelper: use `pyhelper note <title>`")
        return 0
    if argv[0] == "note" and len(argv) >= 2:
        print(format_note(argv[1]))
        return 0
    print("unknown command")
    return 1
