# Week 10 作业：JSON 与数据交换

## 作业说明

本周你将学会如何让数据"流动"起来——用 JSON 格式存储和交换数据。你将从基础的 JSON 读写开始，逐步掌握序列化、反序列化，最终实现一个支持导入导出的数据管理工具。

**提交方式**：将代码提交到你的 Git 仓库，运行测试确保通过，完成 Pull Request。

**参考实现**：如果你遇到困难，可以参考 `starter_code/solution.py` 中的示例代码。

---

## 基础作业（必做）

### 练习 1：JSON 基础读写

**目标**：掌握 `json` 模块的基本用法，能读写 JSON 文件。

创建文件 `practice1_json_basics.py`，完成以下功能：

1. **写入 JSON 文件**：创建一个包含学生信息的字典，写入 `student.json`
   - 字段：name（字符串）、age（整数）、grades（列表）、is_active（布尔值）

2. **读取 JSON 文件**：从 `student.json` 读取数据，打印每个字段的类型

3. **处理嵌套结构**：创建一个包含多门课程成绩的字典，写入 `courses.json`
   ```python
   {
       "student": "小北",
       "courses": [
           {"name": "Python", "score": 90},
           {"name": "数学", "score": 85}
       ]
   }
   ```

4. **美化输出**：使用 `indent` 参数让 JSON 文件更易读，使用 `ensure_ascii=False` 正确处理中文

**输入示例**：
```
（无输入，程序自动生成数据）
```

**输出示例**：
```
写入 student.json 成功
读取 student.json:
  name: 小北 (类型: <class 'str'>)
  age: 20 (类型: <class 'int'>)
  grades: [85, 90, 78] (类型: <class 'list'>)
  is_active: True (类型: <class 'bool'>)

写入 courses.json 成功
读取 courses.json:
  学生: 小北
  课程数: 2
```

**要求**：
- 使用 `json.dump()` 和 `json.load()` 处理文件
- 使用 `json.dumps()` 和 `json.loads()` 处理字符串（至少演示一次）
- 所有 JSON 文件使用 UTF-8 编码
- 文件操作使用 `with` 语句

**常见错误**：
- 忘记指定 `encoding='utf-8'` 导致中文乱码
- 混淆 `dump`（写文件）和 `dumps`（转字符串）
- 忘记 `ensure_ascii=False` 导致中文被转义成 `\uXXXX`

---

### 练习 2：数据导入导出工具

**目标**：实现一个支持多种格式的数据导入导出工具。

创建文件 `practice2_data_exchange.py`，实现以下函数：

```python
import json
from pathlib import Path


def export_data(data, filepath, format="json"):
    """导出数据到文件

    Args:
        data: 要导出的数据（字典或列表）
        filepath: 输出文件路径
        format: 导出格式，支持 "json" 或 "txt"

    Returns:
        bool: 导出是否成功
    """
    pass


def import_data(filepath):
    """从 JSON 文件导入数据

    Args:
        filepath: JSON 文件路径

    Returns:
        解析后的数据，如果失败返回 None
    """
    pass


def convert_format(input_path, output_path, output_format):
    """转换文件格式

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        output_format: 目标格式

    Returns:
        bool: 转换是否成功
    """
    pass
```

**功能要求**：

1. **export_data 函数**：
   - 支持导出为 JSON 格式（使用 `json.dump`）
   - 支持导出为 TXT 格式（简单文本，每行一个键值对）
   - 如果目录不存在，自动创建（使用 `Path.mkdir`）
   - 返回布尔值表示成功或失败

2. **import_data 函数**：
   - 只支持导入 JSON 格式
   - 处理文件不存在的情况（返回 None，不抛出异常）
   - 处理 JSON 格式错误（返回 None，打印错误信息）
   - 验证导入的数据是否为字典或列表

3. **convert_format 函数**：
   - 读取 JSON 文件，转换为另一种格式导出
   - 支持 `json` → `txt` 的转换

**测试数据**：
```python
test_data = {
    "title": "Python 学习笔记",
    "author": "小北",
    "tags": ["Python", "JSON", "学习"],
    "content": "JSON 是一种轻量级的数据交换格式"
}
```

**验证方法**：
```bash
python3 practice2_data_exchange.py
```

**常见错误**：
- 导出时不处理目录不存在的情况
- 导入时不验证文件是否存在
- 导入时不处理 JSON 解析错误
- 忘记关闭文件（没有用 `with` 语句）

---

### 练习 3：序列化与反序列化

**目标**：理解序列化的概念，能处理自定义数据类型。

创建文件 `practice3_serialization.py`，完成以下功能：

1. **日期对象的序列化**：
   ```python
   import datetime

   event = {
       "name": "Python 考试",
       "date": datetime.date(2026, 3, 15),  # 日期对象不能直接序列化
       "created_at": datetime.datetime.now()
   }
   ```
   - 编写自定义序列化函数，将日期转为 ISO 格式字符串
   - 使用 `default` 参数序列化上述数据

2. **日期对象的反序列化**：
   - 编写自定义反序列化函数，将 ISO 格式字符串转回日期对象
   - 使用 `object_hook` 参数恢复日期类型

3. **验证序列化前后数据一致**：
   - 序列化 `event` 字典
   - 反序列化回 Python 对象
   - 比较反序列化后的日期类型是否为 `datetime.date`

**要求**：
- 自定义序列化函数要处理 `datetime.date` 和 `datetime.datetime`
- 反序列化后要能正确恢复原始数据类型
- 添加适当的错误处理

**输出示例**：
```
原始数据:
  name: Python 考试
  date: 2026-03-15 (类型: <class 'datetime.date'>)

序列化后的 JSON:
  {"name": "Python 考试", "date": "2026-03-15", "created_at": "2026-02-09T14:30:00"}

反序列化后:
  name: Python 考试
  date: 2026-03-15 (类型: <class 'datetime.date'>)
  类型恢复正确: True
```

**常见错误**：
- 忘记处理 `datetime.datetime` 和 `datetime.date` 的区别
- 反序列化时没有正确识别日期字段
- 使用 `str()` 而不是 `isoformat()` 转换日期

---

### 练习 4：防御性数据编程

**目标**：学会处理损坏的数据和边界情况。

创建文件 `practice4_defensive_programming.py`，实现一个健壮的 JSON 数据加载器：

```python
import json
from pathlib import Path


def safe_load_json(filepath):
    """安全地加载 JSON 文件

    处理以下情况：
    1. 文件不存在
    2. 文件编码问题（尝试多种编码）
    3. JSON 格式错误
    4. 数据类型不符合预期

    Args:
        filepath: JSON 文件路径

    Returns:
        dict/list: 解析后的数据
        None: 加载失败
    """
    pass


def validate_book_data(data):
    """验证书籍数据是否符合预期格式

    预期格式：
    {
        "title": "书名"（必需，字符串）,
        "author": "作者"（必需，字符串）,
        "rating": 评分（可选，1-5 的整数）
    }

    Args:
        data: 要验证的数据

    Returns:
        tuple: (是否有效, 错误信息列表)
    """
    pass


def load_books_collection(filepath):
    """加载书籍集合

    从 JSON 文件加载书籍列表，过滤掉无效记录

    Args:
        filepath: JSON 文件路径

    Returns:
        list: 有效的书籍列表
    """
    pass
```

**测试场景**：

创建以下测试文件用于验证：

1. `test_valid.json`（正常数据）：
```json
[
    {"title": "Python 编程", "author": "张三", "rating": 5},
    {"title": "算法导论", "author": "李四", "rating": 4}
]
```

2. `test_broken.json`（格式错误）：
```json
[
    {"title": "Python 编程", "author": "张三"},
    {"title": "坏数据", "author": "李四"
]
```

3. `test_invalid.json`（数据类型错误）：
```json
[
    {"title": "有效书", "author": "张三", "rating": 5},
    {"title": 123, "author": "李四"},
    {"author": "缺少标题"},
    "这不是字典"
]
```

**要求**：
- `safe_load_json` 要尝试多种编码（utf-8、utf-8-sig、gbk）
- `validate_book_data` 返回详细的错误信息
- `load_books_collection` 过滤无效记录，保留有效记录
- 所有函数都不应该因为错误数据而崩溃

**输出示例**：
```
加载 test_valid.json:
  成功加载 2 本书

加载 test_broken.json:
  JSON 解析错误: Expecting ',' delimiter
  返回空列表

加载 test_invalid.json:
  第 1 项验证失败: title 必须是字符串
  第 2 项验证失败: 缺少必需字段 title
  第 3 项验证失败: 不是字典类型
  成功加载 1 本书（共 4 项）
```

**常见错误**：
- 遇到编码错误就直接返回 None，没有尝试其他编码
- 验证函数过于严格，没有处理可选字段
- 遇到第一个无效记录就停止，没有继续处理其他记录

---

## 进阶作业（可选）

### 练习 5：数据迁移工具

**目标**：实现一个简单的数据迁移工具，处理不同版本的数据格式。

假设你有一个旧版本的书单数据格式（v1），需要迁移到新格式（v2）：

**v1 格式**（旧）：
```json
{
    "books": [
        {"name": "Python 编程", "writer": "张三"},
        {"name": "算法导论", "writer": "李四"}
    ],
    "version": 1
}
```

**v2 格式**（新）：
```json
{
    "books": [
        {
            "title": "Python 编程",
            "author": "张三",
            "rating": 0,
            "tags": [],
            "added_date": "2026-02-09"
        }
    ],
    "version": 2,
    "total_count": 1
}
```

创建文件 `practice5_data_migration.py`，实现：

```python
def detect_version(data):
    """检测数据版本"""
    pass


def migrate_v1_to_v2(old_data):
    """将 v1 数据迁移到 v2"""
    pass


def migrate_data(input_path, output_path):
    """主迁移函数"""
    pass
```

**要求**：
- 自动检测输入数据的版本
- 迁移时添加新字段的默认值
- 字段重命名（name → title, writer → author）
- 添加迁移时间戳
- 如果数据已经是 v2，直接返回
- 返回迁移后的数据和迁移报告（哪些字段被修改）

**提交物**：
- `practice5_data_migration.py`
- `sample_v1.json`（示例旧数据）
- `migration_report.md`（说明迁移逻辑和字段映射）

---

### 练习 6：配置管理器

**目标**：实现一个支持多种格式的配置管理器。

创建文件 `practice6_config_manager.py`，实现一个 `ConfigManager` 类：

```python
class ConfigManager:
    """配置管理器，支持 JSON 格式存储"""

    def __init__(self, config_path):
        """初始化，加载配置文件"""
        pass

    def get(self, key, default=None):
        """获取配置项"""
        pass

    def set(self, key, value):
        """设置配置项"""
        pass

    def save(self):
        """保存配置到文件"""
        pass

    def export(self, filepath, format="json"):
        """导出配置"""
        pass

    def import_config(self, filepath):
        """导入配置（合并或覆盖）"""
        pass
```

**功能要求**：
- 支持嵌套键（如 `get("database.host")`）
- 支持配置验证（某些键必须有值）
- 支持配置导入时的合并策略（覆盖 vs 合并）
- 自动备份旧配置

**使用示例**：
```python
config = ConfigManager("app_config.json")
config.set("theme", "dark")
config.set("editor.font_size", 14)
config.save()

# 导出为不同格式
config.export("backup.json", format="json")
config.export("settings.txt", format="txt")
```

---

## AI 协作练习（可选）

### 练习 7：审查 AI 生成的 JSON 处理代码

**背景**：阿码让 AI 帮他写一个"学生成绩管理器"的 JSON 处理模块。AI 生成了下面的代码。

**任务**：审查这段代码，找出问题并修复。

#### AI 生成的代码

```python
# student_manager.py （AI 生成）

import json

def load_students(filename):
    """从 JSON 文件加载学生列表"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def save_students(filename, students):
    """保存学生列表到 JSON 文件"""
    with open(filename, 'w') as f:
        json.dump(students, f)

def add_student(filename, student):
    """添加学生到文件"""
    students = load_students(filename)
    students.append(student)
    save_students(filename, students)

def find_student(filename, name):
    """按姓名查找学生"""
    students = load_students(filename)
    for student in students:
        if student['name'] == name:
            return student
    return None

# 测试代码
if __name__ == "__main__":
    student = {"name": "小北", "score": 90}
    add_student("students.json", student)
    print(find_student("students.json", "小北"))
```

#### 审查清单

请检查以下问题：

- [ ] **代码能运行吗？**
  - 提示：如果 `students.json` 文件不存在会怎样？
  - 提示：如果文件内容不是有效的 JSON 会怎样？

- [ ] **异常处理完整吗？**
  - 提示：`load_students` 如果文件不存在会怎样？
  - 提示：如果 JSON 格式错误会怎样？
  - 提示：`find_student` 如果 `name` 键不存在会怎样？

- [ ] **数据验证有吗？**
  - 提示：`add_student` 是否检查了学生数据的格式？
  - 提示：如果 `student` 不是字典会怎样？
  - 提示：如果 `student` 缺少必需字段会怎样？

- [ ] **编码处理正确吗？**
  - 提示：中文内容保存后会不会乱码？
  - 提示：Windows 和 macOS 的换行符有区别吗？

- [ ] **性能考虑了吗？**
  - 提示：`add_student` 每次都读写整个文件，有什么问题？
  - 提示：如果文件很大会怎样？

- [ ] **你能写一个让它失败的测试吗？**
  - 提示：传入一个包含中文的学生数据？
  - 提示：传入一个缺少 `name` 字段的字典？
  - 提示：在程序运行时删除数据文件？

#### 你的修复

请修复上述问题，提交：
1. 修复后的 `student_manager_fixed.py`
2. 一个简短的 `ai_review.md`，说明你发现了哪些问题，以及你是如何修复的

**提示**：
- 添加适当的异常处理（FileNotFoundError、JSONDecodeError）
- 指定文件编码为 UTF-8
- 添加数据验证逻辑
- 考虑使用 `.get()` 而不是 `[]` 访问字典键
- 思考如何优化频繁读写的性能问题（至少要在文档中说明）

---

## 验证与提交

### 自测清单

在提交前，请确认：

- [ ] 练习 1 完成：`practice1_json_basics.py` 能正确读写 JSON 文件
- [ ] 练习 2 完成：`practice2_data_exchange.py` 的导入导出功能正常
- [ ] 练习 3 完成：`practice3_serialization.py` 能正确处理日期序列化
- [ ] 练习 4 完成：`practice4_defensive_programming.py` 能处理各种错误情况
- [ ] 运行 `python3 -m pytest chapters/week_10/tests -q` 通过所有测试
- [ ] 代码已提交到 Git，至少有 2 次提交（draft + verify）

### Git 提交规范

```bash
# 第一次提交（草稿）
git add chapters/week_10/practice*.py
git commit -m "draft week_10: 完成 JSON 基础读写和导入导出"

# 第二次提交（验证）
git add chapters/week_10/practice*.py
git add chapters/week_10/test_*.json
git commit -m "verify week_10: 完成防御性编程，所有测试通过"

# 推送到远端
git push origin week_10
```

### Pull Request 描述模板

```markdown
## Week 10 作业完成情况

### 已完成的练习
- [x] 练习 1：JSON 基础读写
- [x] 练习 2：数据导入导出工具
- [x] 练习 3：序列化与反序列化
- [x] 练习 4：防御性数据编程

### 进阶练习（可选）
- [ ] 练习 5：数据迁移工具
- [ ] 练习 6：配置管理器

### AI 协作练习（可选）
- [ ] 练习 7：审查 AI 生成的代码

### 自测结果
- 运行 `python3 -m pytest chapters/week_10/tests -q`：通过 / 失败
- JSON 文件读写测试：通过 / 失败
- 异常处理测试：通过 / 失败

### 遇到的困难
（记录你遇到的问题和解决方法）

### 请 Review 的重点
（特别希望 reviewer 关注的地方，如异常处理逻辑）
```

---

## 常见问题 FAQ

**Q1: `json.load()` 和 `json.loads()` 有什么区别？**

A:
- `json.load(f)`：从文件对象读取 JSON 数据
- `json.loads(s)`：从字符串解析 JSON 数据

记忆技巧：带 `s` 的是处理字符串（string），不带 `s` 的是处理文件。

**Q2: 为什么我的中文显示成了 `\uXXXX`？**

A: 默认情况下 `json.dumps()` 会把非 ASCII 字符转义。添加 `ensure_ascii=False` 参数：
```python
json.dumps(data, ensure_ascii=False)
```

**Q3: 如何处理日期对象的序列化？**

A: 使用 `default` 参数提供自定义序列化函数：
```python
def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f"无法序列化 {type(obj)}")

json.dumps(data, default=serialize_datetime)
```

**Q4: 导入 JSON 文件时怎么知道文件编码？**

A: 通常 JSON 文件使用 UTF-8 编码。如果遇到编码错误，可以尝试多种编码：
```python
for encoding in ['utf-8', 'utf-8-sig', 'gbk']:
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return json.load(f)
    except UnicodeDecodeError:
        continue
```

**Q5: 什么是 `JSONDecodeError`，怎么处理？**

A: `JSONDecodeError` 表示 JSON 格式不正确（如缺少括号、逗号位置错误等）。应该捕获它并给出友好的错误提示：
```python
try:
    data = json.load(f)
except json.JSONDecodeError as e:
    print(f"JSON 格式错误: {e}")
    return None
```

---

## 挑战自我

如果你想进一步挑战自己，可以尝试：

1. **Schema 验证**：使用 `jsonschema` 库（需要安装）验证 JSON 数据是否符合预定义的 schema
2. **增量保存**：实现一个只保存修改部分的 JSON 存储系统，避免每次读写整个文件
3. **JSON Lines 格式**：学习并支持 JSON Lines 格式（每行一个 JSON 对象，适合大文件）
4. **API 数据获取**：使用 `urllib` 或 `requests` 库从真实 API 获取 JSON 数据并处理

---

祝你学习愉快！JSON 是现代数据交换的通用语言，掌握它你就掌握了与任何系统对话的能力。
