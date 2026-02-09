# Week 11 作业：dataclass 与类型提示

## 作业说明

本周你将学会如何让代码"自己说明自己"——用 dataclass 定义清晰的数据模型，用类型提示提升代码可读性。你将从基础的 dataclass 定义开始，逐步掌握字段默认值、类型提示、状态管理，最终实现一个支持数据模型和状态转换的任务追踪器。

**提交方式**：将代码提交到你的 Git 仓库，运行测试确保通过，完成 Pull Request。

**参考实现**：如果你遇到困难，可以参考 `starter_code/solution.py` 中的示例代码。

---

## 基础作业（必做）

### 练习 1：定义 Student dataclass

**目标**：掌握 `@dataclass` 装饰器的基本用法，能定义一个简单的数据类。

创建文件 `practice1_student_dataclass.py`，完成以下功能：

1. **定义 Student dataclass**：
   - 字段：name（字符串）、age（整数）、major（字符串）、gpa（浮点数）
   - gpa 应该有默认值 0.0
   - major 应该有默认值 "未定"

2. **创建 Student 实例**：
   - 创建一个只有 name 和 age 的学生（使用默认 major 和 gpa）
   - 创建一个包含所有字段的学生

3. **打印学生信息**：
   - 打印每个字段
   - 打印 dataclass 自动生成的 `__repr__` 输出

**输入示例**：
```python
# 无输入，程序自动创建数据
```

**输出示例**：
```
学生1（使用默认值）:
  姓名: 小北
  年龄: 20
  专业: 未定
  GPA: 0.0
  __repr__: Student(name='小北', age=20, major='未定', gpa=0.0)

学生2（完整字段）:
  姓名: 阿码
  年龄: 21
  专业: 计算机科学
  GPA: 3.8
  __repr__: Student(name='阿码', age=21, major='计算机科学', gpa=3.8)
```

**要求**：
- 使用 `@dataclass` 装饰器
- 为字段添加类型提示
- 为 gpa 和 major 设置默认值
- 导入正确的模块（`from dataclasses import dataclass`）

**常见错误**：
- 忘记导入 `dataclass` 模块
- 类型提示写错（如把 `str` 写成 `"str"`）
- 默认值位置错误（有默认值的字段必须放在没有默认值的字段后面）

---

### 练习 2：给函数添加类型提示

**目标**：掌握类型提示的语法，能正确标注函数参数和返回值。

创建文件 `practice2_type_hints.py`，完成以下函数的类型提示：

```python
from typing import List, Optional, Dict

def calculate_average(scores: List[int]) -> float:
    """计算平均分"""
    pass


def find_student(students: List[dict], name: str) -> Optional[dict]:
    """按姓名查找学生，找不到返回 None"""
    pass


def filter_by_major(students: List[dict], major: str) -> List[dict]:
    """筛选某个专业的学生"""
    pass


def count_by_major(students: List[dict]) -> Dict[str, int]:
    """统计每个专业的学生人数"""
    pass


def get_top_student(students: List[dict]) -> Optional[dict]:
    """获取 GPA 最高的学生，空列表返回 None"""
    pass
```

**功能要求**：

1. **calculate_average**：
   - 接收一个整数列表（成绩）
   - 返回平均分（浮点数）
   - 空列表返回 0.0

2. **find_student**：
   - 接收学生列表和姓名
   - 找到返回学生字典，找不到返回 None
   - 使用 `.get()` 访问字典，避免 KeyError

3. **filter_by_major**：
   - 接收学生列表和专业名称
   - 返回该专业的所有学生

4. **count_by_major**：
   - 接收学生列表
   - 返回字典，键是专业名，值是该专业的学生数

5. **get_top_student**：
   - 接收学生列表
   - 返回 GPA 最高的学生
   - 空列表返回 None

**测试数据**：
```python
students = [
    {"name": "小北", "major": "计算机科学", "gpa": 3.5},
    {"name": "阿码", "major": "数学", "gpa": 3.9},
    {"name": "老潘", "major": "计算机科学", "gpa": 3.2}
]
```

**验证方法**：
```bash
python3 practice2_type_hints.py
```

**输出示例**：
```
平均分: 3.533333333333333

查找"阿码": {'name': '阿码', 'major': '数学', 'gpa': 3.9}
查找"不存在": None

计算机科学专业的学生: [{'name': '小北', ...}, {'name': '老潘', ...}]

专业统计: {'计算机科学': 2, '数学': 1}

GPA 最高的学生: {'name': '阿码', 'major': '数学', 'gpa': 3.9}
```

**常见错误**：
- 类型提示语法错误（如 `list[int]` 写成 `List[int]`，但 Python 3.9+ 两种都支持）
- 忘记导入 `typing` 模块的 `List`、`Optional`、`Dict`
- 没有处理空列表的情况
- 使用 `[]` 访问字典而不是 `.get()`

---

### 练习 3：用 Enum 定义状态

**目标**：掌握 `Enum` 的用法，能用它定义有限的状态集合。

创建文件 `practice3_enum_status.py`，完成以下功能：

1. **定义 EnrollmentStatus 枚举**：
   ```python
   from enum import Enum

   class EnrollmentStatus(Enum):
       """选课状态"""
       PENDING = "待审核"
       APPROVED = "已通过"
       REJECTED = "已拒绝"
       COMPLETED = "已完成"
   ```

2. **定义 Enrollment dataclass**：
   ```python
   @dataclass
   class Enrollment:
       """选课记录"""
       student_name: str
       course_name: str
       status: EnrollmentStatus = EnrollmentStatus.PENDING
   ```

3. **实现状态转换方法**：
   ```python
   def approve(self):
       """审核通过"""
       pass

   def reject(self):
       """审核拒绝"""
       pass

   def complete(self):
       """标记为已完成"""
       pass
   ```

**状态转换规则**：
- PENDING → APPROVED（审核通过）
- PENDING → REJECTED（审核拒绝）
- APPROVED → COMPLETED（完成课程）
- COMPLETED 不能转换到其他状态
- REJECTED 不能转换到其他状态

**验证方法**：
```python
# 创建一个待审核的选课记录
enrollment = Enrollment("小北", "Python 程序设计")
print(f"初始状态: {enrollment.status.value}")

# 审核通过
enrollment.approve()
print(f"审核后: {enrollment.status.value}")

# 完成课程
enrollment.complete()
print(f"完成后: {enrollment.status.value}")

# 尝试非法转换（应该抛出异常）
try:
    enrollment.approve()
    print("错误：已完成的课程不应能再次审核")
except ValueError as e:
    print(f"正确阻止了非法转换: {e}")
```

**输出示例**：
```
初始状态: 待审核
审核后: 已通过
完成后: 已完成
正确阻止了非法转换: 已完成的课程不能再次审核
```

**常见错误**：
- 忘记导入 `Enum`
- 状态转换没有检查当前状态
- 抛出异常时没有给出清晰的错误信息
- 访问枚举值时忘记用 `.value`

---

### 练习 4：dataclass 与 JSON 相互转换

**目标**：掌握 dataclass 与 JSON 的相互转换，理解 `asdict()` 和 `from_dict()` 的用法。

创建文件 `practice4_json_conversion.py`，完成以下功能：

1. **定义 Task dataclass**：
   ```python
   from dataclasses import dataclass, asdict
   from typing import List
   import json

   @dataclass
   class Task:
       """任务"""
       title: str
       priority: str
       completed: bool = False
       tags: List[str] = None

       def __post_init__(self):
           """初始化后处理，设置 tags 默认值"""
           if self.tags is None:
               self.tags = []
   ```

2. **实现转换方法**：
   ```python
   def to_dict(self) -> dict:
       """转换为字典"""
       pass

   @classmethod
   def from_dict(cls, data: dict) -> "Task":
       """从字典创建 Task"""
       pass

   def to_json(self, filepath: str) -> None:
       """保存为 JSON 文件"""
       pass

   @classmethod
   def from_json(cls, filepath: str) -> "Task":
       """从 JSON 文件加载"""
       pass
   ```

**功能要求**：

1. **to_dict**：
   - 使用 `asdict()` 函数
   - 返回字典

2. **from_dict**：
   - 接收字典参数
   - 处理字段缺失的情况（使用 `.get()` 设置默认值）
   - 返回新的 Task 实例

3. **to_json**：
   - 调用 `to_dict()` 转换为字典
   - 使用 `json.dump()` 保存
   - 使用 `ensure_ascii=False` 处理中文

4. **from_json**：
   - 使用 `json.load()` 读取
   - 调用 `from_dict()` 创建实例
   - 处理文件不存在的情况

**测试数据**：
```python
task = Task(
    title="完成 Week 11 作业",
    priority="high",
    tags=["Python", "dataclass"]
)

# 转换为字典
task_dict = task.to_dict()
print("转换为字典:", task_dict)

# 保存为 JSON
task.to_json("task.json")
print("已保存到 task.json")

# 从 JSON 加载
loaded_task = Task.from_json("task.json")
print("从 JSON 加载:", loaded_task)
```

**输出示例**：
```
转换为字典: {'title': '完成 Week 11 作业', 'priority': 'high', 'completed': False, 'tags': ['Python', 'dataclass']}
已保存到 task.json
从 JSON 加载: Task(title='完成 Week 11 作业', priority='high', completed=False, tags=['Python', 'dataclass'])
```

**要求**：
- 正确使用 `asdict()` 函数
- 处理字段缺失的情况
- JSON 文件使用 UTF-8 编码
- 添加适当的错误处理

**常见错误**：
- 忘记使用 `field(default_factory=list)` 处理可变默认值（或用 `__post_init__`）
- `from_dict` 没有处理字段缺失
- 忘记设置 `ensure_ascii=False`
- 没有处理文件不存在的情况

---

## 进阶作业（可选）

### 练习 5：实现带状态转换的 Enrollment dataclass

**目标**：综合运用 dataclass、Enum 和状态管理，实现一个完整的选课系统。

创建文件 `practice5_enrollment_system.py`，实现以下功能：

1. **定义完整的 Enrollment dataclass**：
   ```python
   from dataclasses import dataclass, field
   from datetime import date
   from typing import Optional

   @dataclass
   class Enrollment:
       """选课记录"""
       student_id: str
       course_id: str
       status: EnrollmentStatus = EnrollmentStatus.PENDING
       enrolled_date: date = field(default_factory=date.today)
       approved_date: Optional[date] = None
       completed_date: Optional[date] = None
       notes: str = ""

       def approve(self, reviewer: str) -> None:
           """审核通过"""
           pass

       def reject(self, reviewer: str, reason: str) -> None:
           """审核拒绝"""
           pass

       def complete(self, grade: float) -> None:
           """完成课程"""
           pass

       def can_approve(self) -> bool:
           """检查是否可以审核通过"""
           pass

       def can_reject(self) -> bool:
           """检查是否可以拒绝"""
           pass

       def can_complete(self) -> bool:
           """检查是否可以完成"""
           pass
   ```

2. **状态转换规则**：
   - PENDING → APPROVED：记录审核人和审核日期
   - PENDING → REJECTED：记录审核人、拒绝原因和日期
   - APPROVED → COMPLETED：记录完成日期和成绩
   - 其他转换都是非法的

3. **转换方法要求**：
   - `approve`：检查当前状态，设置状态为 APPROVED，记录审核日期
   - `reject`：检查当前状态，设置状态为 REJECTED，记录审核日期和原因
   - `complete`：检查当前状态，设置状态为 COMPLETED，记录完成日期和成绩
   - 所有非法转换都抛出 `ValueError` 并给出清晰错误信息

4. **辅助方法**：
   - `can_approve`：返回是否可以审核通过（状态是 PENDING）
   - `can_reject`：返回是否可以拒绝（状态是 PENDING）
   - `can_complete`：返回是否可以完成（状态是 APPROVED）

**测试场景**：
```python
# 创建选课记录
enrollment = Enrollment("S001", "CS101")
print(f"初始状态: {enrollment.status.value}")

# 审核通过
enrollment.approve("teacher1")
print(f"审核后: {enrollment.status.value}, 审核日期: {enrollment.approved_date}")

# 完成课程
enrollment.complete(95.5)
print(f"完成后: {enrollment.status.value}, 完成日期: {enrollment.completed_date}")

# 尝试非法转换
try:
    enrollment.approve("teacher2")
    print("错误：不应允许重复审核")
except ValueError as e:
    print(f"正确阻止: {e}")
```

**输出示例**：
```
初始状态: 待审核
审核后: 已通过, 审核日期: 2026-02-09
完成后: 已完成, 完成日期: 2026-02-09
正确阻止: 已完成的课程不能再次审核
```

**要求**：
- 状态转换逻辑完整且正确
- 所有非法转换都能被阻止
- 错误信息清晰明确
- 使用类型提示
- 可选字段使用 `Optional`

---

### 练习 6：重构字典密集的项目为 dataclass

**目标**：理解何时需要重构，能将字典密集的代码重构为 dataclass。

假设你有以下基于字典的代码（旧代码）：

```python
# 旧代码：纯字典版本
books = [
    {
        "title": "Python 编程",
        "author": "张三",
        "isbn": "978-7-111-12345-6",
        "price": 89.0,
        "stock": 10,
        "category": "编程"
    },
    {
        "title": "算法导论",
        "author": "李四",
        "isbn": "978-7-111-23456-7",
        "price": 128.0,
        "stock": 5,
        "category": "算法"
    }
]

def find_by_isbn(books, isbn):
    """按 ISBN 查找书籍"""
    for book in books:
        if book["isbn"] == isbn:
            return book
    return None

def update_stock(books, isbn, quantity):
    """更新库存"""
    book = find_by_isbn(books, isbn)
    if book:
        book["stock"] += quantity
    return book

def calculate_value(books):
    """计算总价值"""
    total = 0
    for book in books:
        total += book["price"] * book["stock"]
    return total
```

创建文件 `practice6_refactor_to_dataclass.py`，完成重构：

1. **定义 Book dataclass**：
   - 包含所有字段（title, author, isbn, price, stock, category）
   - 添加类型提示
   - 为可选字段设置默认值

2. **重构所有函数**：
   - 将函数签名从 `books: list[dict]` 改为 `books: list[Book]`
   - 将函数返回类型从 `dict | None` 改为 `Book | None`
   - 使用属性访问（`book.isbn`）代替字典访问（`book["isbn"]`）

3. **添加 JSON 支持**：
   - 实现 `to_dict()` 和 `from_dict()` 方法
   - 实现 `to_json()` 和 `from_json()` 类方法

4. **添加辅助方法**：
   - `is_available()`：检查是否有库存
   - `get_value()`：计算这本书的总价值（price * stock）

5. **对比重构前后的差异**：
   - 在注释中说明重构带来的改进
   - 至少列出 3 个改进点

**测试场景**：
```python
# 创建书籍列表
books = [
    Book("Python 编程", "张三", "978-7-111-12345-6", 89.0, 10, "编程"),
    Book("算法导论", "李四", "978-7-111-23456-7", 128.0, 5, "算法")
]

# 查找书籍
book = find_by_isbn(books, "978-7-111-12345-6")
print(f"找到书籍: {book.title}, 库存: {book.stock}")

# 更新库存
update_stock(books, "978-7-111-12345-6", -2)
print(f"更新后库存: {book.stock}")

# 计算总价值
total = calculate_value(books)
print(f"总价值: {total}")

# 保存到 JSON
save_books(books, "books.json")
print("已保存到 books.json")

# 从 JSON 加载
loaded_books = load_books("books.json")
print(f"加载了 {len(loaded_books)} 本书")
```

**要求**：
- dataclass 设计合理
- 类型提示完整
- 所有函数都有类型提示
- JSON 转换正确
- 在注释中说明重构带来的改进（至少 3 点）

---

## AI 协作练习（可选）

### 练习 7：审查 AI 生成的 dataclass 代码

**背景**：阿码让 AI 帮他写一个"图书馆借阅系统"的 dataclass 模型。AI 生成了下面的代码。

**任务**：审查这段代码，找出问题并修复。

#### AI 生成的代码

```python
# library_system.py （AI 生成）

from dataclasses import dataclass
from enum import Enum
from typing import List

class BookStatus(Enum):
    """书籍状态"""
    AVAILABLE = "可借"
    BORROWED = "已借出"
    LOST = "丢失"
    DAMAGED = "损坏"

@dataclass
class Book:
    """书籍"""
    title: str
    author: str
    isbn: str
    status: BookStatus = BookStatus.AVAILABLE
    borrower_id: str = None
    due_date: str = None

    def borrow(self, borrower_id: str, days: int):
        """借书"""
        if self.status == BookStatus.AVAILABLE:
            self.status = BookStatus.BORROWED
            self.borrower_id = borrower_id
            from datetime import datetime, timedelta
            self.due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        else:
            print("书已被借出")

    def return_book(self):
        """还书"""
        self.status = BookStatus.AVAILABLE
        self.borrower_id = None
        self.due_date = None

    def mark_lost(self):
        """标记为丢失"""
        self.status = BookStatus.LOST

@dataclass
class Library:
    """图书馆"""
    books: List[Book] = []

    def find_by_isbn(self, isbn: str):
        """按 ISBN 查找书籍"""
        for book in self.books:
            if book["isbn"] == isbn:  # 这里有个问题
                return book
        return None

    def borrow_book(self, isbn: str, borrower_id: str, days: int = 30):
        """借书"""
        book = self.find_by_isbn(isbn)
        if book:
            book.borrow(borrower_id, days)
            return True
        return False

    def return_book(self, isbn: str):
        """还书"""
        book = self.find_by_isbn(isbn)
        if book:
            book.return_book()
            return True
        return False
```

#### 审查清单

请检查以下问题：

- [ ] **代码能运行吗？**
  - 提示：`Library.find_by_isbn()` 中用 `book["isbn"]` 访问 dataclass 字段对吗？
  - 提示：`borrower_id: str = None` 这样的默认值类型提示正确吗？

- [ ] **类型提示完整吗？**
  - 提示：`borrower_id: str = None` 和 `due_date: str = None` 的类型提示有什么问题？
  - 提示：函数返回值缺少类型提示吗？

- [ ] **状态转换逻辑完整吗？**
  - 提示：已丢失的书还能借吗？已借出的书能标记为损坏吗？
  - 提示：还书时需要检查当前状态吗？

- [ ] **错误处理完善吗？**
  - 提示：`borrow()` 方法打印"书已被借出"就够了吗？应该抛出异常吗？
  - 提示：找不到书时返回 `None`，调用方记得检查吗？

- [ ] **dataclass 设计合理吗？**
  - 提示：`books: List[Book] = []` 这样的可变默认值有问题吗？
  - 提示：是否应该使用 `field(default_factory=list)`？

- [ ] **你能写一个让它失败的测试吗？**
  - 提示：尝试借一本已经丢失的书？
  - 提示：尝试归还一本没有被借出的书？
  - 提示：创建多个 Library 实例，它们会共享同一个 books 列表吗？

#### 你的修复

请修复上述问题，提交：
1. 修复后的 `library_system_fixed.py`
2. 一个简短的 `ai_review.md`，说明你发现了哪些问题，以及你是如何修复的

**提示**：
- `borrower_id` 和 `due_date` 应该用 `Optional[str]` 而不是 `str = None`
- 访问 dataclass 字段用 `.` 而不是 `[]`
- 可变默认值要用 `field(default_factory=list)`
- 状态转换应该检查当前状态并抛出 `ValueError`
- 所有函数都应该添加返回值类型提示

---

## 验证与提交

### 自测清单

在提交前，请确认：

- [ ] 练习 1 完成：`practice1_student_dataclass.py` 能正确定义和使用 dataclass
- [ ] 练习 2 完成：`practice2_type_hints.py` 的类型提示正确且完整
- [ ] 练习 3 完成：`practice3_enum_status.py` 能正确定义 Enum 和状态转换
- [ ] 练习 4 完成：`practice4_json_conversion.py` 能正确转换 dataclass 和 JSON
- [ ] 运行 `python3 -m pytest chapters/week_11/tests -q` 通过所有测试
- [ ] 代码已提交到 Git，至少有 2 次提交（draft + verify）

### Git 提交规范

```bash
# 第一次提交（草稿）
git add chapters/week_11/practice*.py
git commit -m "draft week_11: 完成 dataclass 基础和类型提示练习"

# 第二次提交（验证）
git add chapters/week_11/practice*.py
git commit -m "verify week_11: 完成状态管理和 JSON 转换，所有测试通过"

# 推送到远端
git push origin week_11
```

### Pull Request 描述模板

```markdown
## Week 11 作业完成情况

### 已完成的练习
- [x] 练习 1：定义 Student dataclass
- [x] 练习 2：给函数添加类型提示
- [x] 练习 3：用 Enum 定义状态
- [x] 练习 4：dataclass 与 JSON 相互转换

### 进阶练习（可选）
- [ ] 练习 5：实现带状态转换的 Enrollment dataclass
- [ ] 练习 6：重构字典密集的项目为 dataclass

### AI 协作练习（可选）
- [ ] 练习 7：审查 AI 生成的 dataclass 代码

### 自测结果
- 运行 `python3 -m pytest chapters/week_11/tests -q`：通过 / 失败
- dataclass 定义测试：通过 / 失败
- 状态转换测试：通过 / 失败
- JSON 转换测试：通过 / 失败

### 遇到的困难
（记录你遇到的问题和解决方法）

### 请 Review 的重点
（特别希望 reviewer 关注的地方，如状态转换逻辑、类型提示完整性）
```

---

## 常见问题 FAQ

**Q1: dataclass 和普通类有什么区别？**

A: dataclass 是 Python 官方提供的"最小封装"数据类：
- **自动生成方法**：`__init__`、`__repr__`、`__eq__` 等
- **主要用于存储数据**：不是完整的 OOP，不适合复杂业务逻辑
- **减少样板代码**：1 行装饰器代替 15+ 行手写代码

什么时候用 dataclass？当你需要"存数据"而不是"做复杂逻辑"时。

**Q2: 类型提示会强制检查吗？**

A: 不会。Python 3.5+ 的类型提示只是"提示"：
- **运行时不检查**：传错类型不会报错（除非运行时触发实际错误）
- **给工具看**：IDE、mypy、AI 工具会利用类型提示
- **渐进采用**：可以选择性地添加，不影响运行

如果你想强制检查类型，需要用 `mypy` 这样的静态类型检查工具：
```bash
pip install mypy
mypy your_file.py
```

**Q3: 为什么不能写 `tags: List[str] = []`？**

A: 这是 Python 的"可变默认值陷阱"：
```python
# 错误：所有实例共享同一个列表
@dataclass
class Task:
    tags: List[str] = []  # 不要这样写

# 正确：每个实例有独立的列表
from dataclasses import field

@dataclass
class Task:
    tags: List[str] = field(default_factory=list)  # 正确
```

或者用 `__post_init__`：
```python
@dataclass
class Task:
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
```

**Q4: `Optional[str]` 和 `str = None` 有什么区别？**

A: 从运行角度看没区别，但从类型提示角度有区别：
```python
# 不推荐：类型提示和实际默认值不一致
def func(name: str = None) -> str:  # 类型提示说"必是 str"，但默认值是 None
    pass

# 推荐：类型提示明确说明"可能是 None"
from typing import Optional

def func(name: Optional[str] = None) -> Optional[str]:  # 明确"可能是 str 或 None"
    pass
```

`Optional[str]` 是 `Union[str, None]` 的简写，表示"这个值可能是 str 或 None"。

**Q5: 如何处理 dataclass 中的日期字段？**

A: 使用 `field(default_factory=...)`：
```python
from dataclasses import dataclass, field
from datetime import date

@dataclass
class Enrollment:
    enrolled_date: date = field(default_factory=date.today)  # 注意：不要加括号
    completed_date: Optional[date] = None
```

**注意**：`default_factory=date.today`（不加括号），而不是 `default_factory=date.today()`（加括号）。
- 不加括号：传递函数对象，每次创建实例时调用
- 加括号：立即调用，所有实例共享同一个日期

---

## 挑战自我

如果你想进一步挑战自己，可以尝试：

1. **嵌套 dataclass**：实现一个包含多层嵌套的数据模型（如 `Library` 包含多个 `Bookshelf`，每个 `Bookshelf` 包含多个 `Book`）
2. **不可变 dataclass**：使用 `@dataclass(frozen=True)` 创建不可变的数据类
3. **slots**：使用 `@dataclass(slots=True)` 优化内存占用（Python 3.10+）
4. **dataclass 验证**：使用 `__post_init__` 添加字段验证逻辑
5. **mypy 集成**：安装并运行 `mypy` 检查你的代码类型提示是否正确

---

祝你学习愉快！dataclass 和类型提示是 AI 时代编写高质量 Python 代码的基础，掌握它们你就掌握了让代码"自己说明自己"的能力。
