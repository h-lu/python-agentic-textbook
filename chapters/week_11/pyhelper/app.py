"""Week 11 PyHelper: dataclass models."""

try:
    from .models import Note, StudyPlan
except ImportError:
    from models import Note, StudyPlan


def main() -> None:
    note = Note("2026-05-11", "用 dataclass 表达学习笔记", ["dataclass"])
    plan = StudyPlan("完成 PyHelper 数据建模", ["Note", "StudyPlan"], 2.5)
    print(note.to_dict())
    print(plan.summary())


if __name__ == "__main__":
    main()
