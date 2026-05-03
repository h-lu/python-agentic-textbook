"""练习 5：实现带状态转换的 Enrollment dataclass。"""

try:
    from solution import Enrollment, EnrollmentStatus
except ImportError:  # pragma: no cover - package import fallback
    from .solution import Enrollment, EnrollmentStatus


__all__ = ["EnrollmentStatus", "Enrollment"]


if __name__ == "__main__":
    enrollment = Enrollment(student_id="S001", course_id="CS101")
    print(f"初始状态: {enrollment.status.value}")
    enrollment.approve("teacher1")
    print(f"审核后: {enrollment.status.value}")
    enrollment.complete(95.5)
    print(f"完成后: {enrollment.status.value}")
