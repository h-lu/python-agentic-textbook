"""练习 4：dataclass 与 JSON 相互转换。"""

try:
    from solution import Task
except ImportError:  # pragma: no cover - package import fallback
    from .solution import Task


__all__ = ["Task"]


if __name__ == "__main__":
    task = Task("完成 Week 11 作业", "high", tags=["Python", "dataclass"])
    print("转换为字典:", task.to_dict())
