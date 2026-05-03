"""练习 1：定义 Student dataclass。

这个文件是给学生对照作业文件名使用的入口；完整参考实现放在
solution.py 中，这里只暴露本练习需要的 Student。
"""

try:
    from solution import Student
except ImportError:  # pragma: no cover - package import fallback
    from .solution import Student


__all__ = ["Student"]


if __name__ == "__main__":
    student1 = Student("小北", 20)
    student2 = Student("阿码", 21, "计算机科学", 3.8)
    for index, student in enumerate([student1, student2], 1):
        print(f"学生{index}: {student}")
