"""练习 3：用 Enum 定义状态。"""

try:
    from solution import Enrollment, EnrollmentStatus
except ImportError:  # pragma: no cover - package import fallback
    from .solution import Enrollment, EnrollmentStatus


__all__ = ["EnrollmentStatus", "Enrollment"]


if __name__ == "__main__":
    enrollment = Enrollment("小北", "Python 程序设计")
    print(f"初始状态: {enrollment.status.value}")
    enrollment.approve()
    print(f"审核后: {enrollment.status.value}")
    enrollment.complete()
    print(f"完成后: {enrollment.status.value}")
