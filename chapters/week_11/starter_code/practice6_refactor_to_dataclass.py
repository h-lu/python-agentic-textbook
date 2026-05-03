"""练习 6：重构字典密集的项目为 dataclass。"""

try:
    from solution import (
        Book,
        calculate_value,
        find_by_isbn,
        load_books,
        save_books,
        update_stock,
    )
except ImportError:  # pragma: no cover - package import fallback
    from .solution import (
        Book,
        calculate_value,
        find_by_isbn,
        load_books,
        save_books,
        update_stock,
    )


__all__ = [
    "Book",
    "find_by_isbn",
    "update_stock",
    "calculate_value",
    "save_books",
    "load_books",
]


if __name__ == "__main__":
    books = [
        Book("Python 编程", "张三", "978-7-111-12345-6", 89.0, 10, "编程"),
        Book("算法导论", "李四", "978-7-111-23456-7", 128.0, 5, "算法"),
    ]
    print("总价值:", calculate_value(books))
