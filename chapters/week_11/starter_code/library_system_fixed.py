"""练习 7：修复后的图书馆借阅系统。"""

from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum
from typing import List, Optional


class BookStatus(Enum):
    """书籍状态。"""

    AVAILABLE = "可借"
    BORROWED = "已借出"
    LOST = "丢失"
    DAMAGED = "损坏"


@dataclass
class LibraryBook:
    """图书馆藏书。"""

    title: str
    author: str
    isbn: str
    status: BookStatus = BookStatus.AVAILABLE
    borrower_id: Optional[str] = None
    due_date: Optional[str] = None

    def borrow(self, borrower_id: str, days: int = 30) -> None:
        """借书；只有可借状态可以借出。"""
        if self.status != BookStatus.AVAILABLE:
            raise ValueError(f"当前状态为{self.status.value}，不能借出")
        if not borrower_id.strip():
            raise ValueError("借阅人不能为空")
        self.status = BookStatus.BORROWED
        self.borrower_id = borrower_id
        self.due_date = (date.today() + timedelta(days=days)).isoformat()

    def return_book(self) -> None:
        """还书；只有已借出状态可以归还。"""
        if self.status != BookStatus.BORROWED:
            raise ValueError(f"当前状态为{self.status.value}，不能还书")
        self.status = BookStatus.AVAILABLE
        self.borrower_id = None
        self.due_date = None

    def mark_lost(self) -> None:
        """标记为丢失。"""
        if self.status == BookStatus.DAMAGED:
            raise ValueError("损坏图书不能再标记为丢失")
        self.status = BookStatus.LOST

    def mark_damaged(self) -> None:
        """标记为损坏。"""
        if self.status == BookStatus.BORROWED:
            raise ValueError("已借出图书归还前不能标记为损坏")
        self.status = BookStatus.DAMAGED


@dataclass
class Library:
    """图书馆。"""

    books: List[LibraryBook] = field(default_factory=list)

    def find_by_isbn(self, isbn: str) -> Optional[LibraryBook]:
        """按 ISBN 查找书籍。"""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def borrow_book(self, isbn: str, borrower_id: str, days: int = 30) -> bool:
        """借出指定图书。"""
        book = self.find_by_isbn(isbn)
        if book is None:
            return False
        book.borrow(borrower_id, days)
        return True

    def return_book(self, isbn: str) -> bool:
        """归还指定图书。"""
        book = self.find_by_isbn(isbn)
        if book is None:
            return False
        book.return_book()
        return True


Book = LibraryBook


__all__ = ["BookStatus", "LibraryBook", "Book", "Library"]
