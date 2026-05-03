# Week 05 作业：持久化学习日记

## 作业概述

本周你将实现一个**学习日记工具**：把每天学到的内容写入文本文件，并在下一次运行时继续读取、搜索和统计。它延续 Week 04 的字典/列表练习，但本周的重点变成**文件持久化**。

自动测试位于 `chapters/week_05/tests/`。其中 `test_file_basics.py`、`test_pathlib.py`、`test_encoding.py` 会检查本周文件操作概念，`test_diary_app.py` 会检查一个日记本工具应具备的写入、读取、搜索和统计行为。

参考实现放在 `chapters/week_05/starter_code/solution.py`，示例程序可参考：

- `chapters/week_05/examples/05_diary_app.py`
- `chapters/week_05/examples/06_pyhelper.py`

---

## 基础作业（必做）

### 功能要求

在 `chapters/week_05/starter_code/solution.py` 中实现或完善一个学习日记/学习记录工具，至少支持以下功能：

1. **添加记录**：把一条学习内容写入文件。
2. **读取所有记录**：文件不存在时返回空列表或空字典，不崩溃。
3. **搜索记录**：按关键词筛选包含该关键词的记录。
4. **统计记录数**：能统计当前文件中有多少条有效记录。
5. **持久化保存**：关闭程序后，记录仍保存在文件中。

### 建议接口

`test_diary_app.py` 使用下面这组行为作为日记本工具的参考接口。你的实现可以直接提供这些函数，便于和测试说明保持一致：

```python
def add_diary_entry(content, filename="diary.txt"):
    """追加一条日记记录。"""

def read_all_diaries(filename="diary.txt"):
    """读取所有非空日记行，文件不存在时返回 []。"""

def search_diaries(keyword, filename="diary.txt"):
    """返回所有包含 keyword 的日记行。"""

def count_diaries(filename="diary.txt"):
    """返回日记条数。"""
```

参考实现中还保留了 PyHelper 风格的学习记录接口：

```python
def load_records(filename="records.txt"):
    """读取学习记录字典。"""

def save_records(records, filename="records.txt"):
    """保存学习记录字典。"""
```

这两组接口都围绕同一件事：用文件把学习记录保存下来。

### 文件格式

日记本建议使用每行一条记录：

```text
2026-02-09: 今天学会了文件操作
2026-02-10: with 语句会自动关闭文件
2026-02-11: pathlib 处理路径很方便
```

PyHelper 学习记录可以使用：

```text
02-09: 学会了文件操作
02-10: 写了一个持久化小工具
```

如果内容里可能出现冒号，解析时使用 `split(": ", 1)`，只分割第一个分隔符。

### 技术要求

1. 文件操作必须指定 `encoding="utf-8"`。
2. 必须使用 `with` 语句或 `pathlib.Path.read_text()` / `write_text()` 这类会自动管理文件句柄的 API。
3. 必须使用 `pathlib.Path` 处理文件路径。
4. 追加日记时使用 `"a"` 模式，避免覆盖旧记录。
5. 读取前要处理文件不存在的情况。
6. 过滤空行，避免把空白内容当作有效记录。

### 输入输出示例

添加三条日记后，文件可能长这样：

```text
2026-02-09: 今天学会了文件操作
2026-02-10: with 语句很方便
2026-02-11: UTF-8 编码避免乱码
```

搜索 `文件` 时输出：

```text
=== 搜索结果 ===
2026-02-09: 今天学会了文件操作
```

---

## 进阶作业（选做）

在基础作业之上，增加以下功能：

1. **按日期分组显示**：同一天多条记录显示在同一日期下面。
2. **关键词搜索统计**：搜索时显示匹配数量。
3. **PyHelper 持久化改进**：让 `examples/06_pyhelper.py` 的学习记录保存到 `pyhelper_data.txt`，再次启动后能加载旧记录。

---

## AI 协作练习（可选）

下面这段代码是某个 AI 工具生成的"学习记录加载功能"。请审查它：

```python
def load_from_file(filename="records.txt"):
    file = open(filename, "r")
    content = file.read()
    file.close()

    records = {}
    for line in content.split("\n"):
        date, item = line.split(": ")
        records[date] = item

    return records
```

请至少指出并修复 3 个问题：

- 文件关闭是否安全？是否应该用 `with`？
- 是否指定了 UTF-8 编码？
- 文件不存在时会怎样？
- 空行或格式错误的行会怎样？
- 内容里包含冒号时会怎样？
- 相对路径在不同运行目录下会指向哪里？

提交 `ai_review.md` 时包含：

1. 问题清单。
2. 修复后的 `load_from_file()`。
3. 你如何验证修复有效。

---

## 提交要求

在 `chapters/week_05/` 目录下提交：

```text
week_05/
├── starter_code/
│   └── solution.py          # 你的主要实现或参考实现
├── records.txt              # 可选：运行后产生的学习记录数据
├── README.md                # 可选：运行说明
└── ai_review.md             # 可选：AI 协作练习报告
```

提交前请确认：

- [ ] `python3 chapters/week_05/starter_code/solution.py` 能运行。
- [ ] 能追加至少 3 条中文记录。
- [ ] 再次读取时旧记录还在。
- [ ] 搜索关键词能返回匹配记录。
- [ ] 文件操作使用 `pathlib` 和 `encoding="utf-8"`。
- [ ] 运行 `python3 -m pytest chapters/week_05/tests -q` 通过所有测试。

---

## 常见错误与提示

### 错误 1：追加记录时覆盖了旧内容

写日记这类场景应使用 `"a"` 追加模式：

```python
from pathlib import Path

def add_diary_entry(content, filename="diary.txt"):
    path = Path(filename)
    with path.open("a", encoding="utf-8") as file:
        file.write(content + "\n")
```

### 错误 2：中文乱码

读写都显式指定 UTF-8：

```python
path.write_text("中文内容", encoding="utf-8")
text = path.read_text(encoding="utf-8")
```

### 错误 3：首次运行文件不存在

读取前先处理不存在的情况：

```python
from pathlib import Path

path = Path("records.txt")
if not path.exists():
    records = []
else:
    records = path.read_text(encoding="utf-8").splitlines()
```

### 错误 4：分隔符冲突

只分割第一个 `": "`：

```python
date, content = line.split(": ", 1)
```

---

## 学习目标检查

完成作业后，你应该能：

- [ ] 用 `open()`、`read()`、`write()` 读写文件。
- [ ] 用 `with` 自动关闭文件。
- [ ] 用 `pathlib.Path` 构造和检查路径。
- [ ] 用 UTF-8 正确处理中文和 emoji。
- [ ] 用追加模式保存持续增长的记录。
- [ ] 处理文件不存在、空行、内容分隔符等边界情况。
