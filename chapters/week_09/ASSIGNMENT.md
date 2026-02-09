# Week 09 作业：文本处理与正则表达式——从混乱中提取秩序

## 作业说明

本周你将掌握 Python 的文本处理能力：从基础的字符串方法（strip、split、join、find）到强大的正则表达式。你将学会从混乱的日志文件中提取结构化信息，处理各种边界情况，并为 PyHelper 添加搜索和过滤功能。

**提交方式**：将代码提交到你的 Git 仓库，运行测试确保通过，完成 Pull Request。

**参考实现**：如果你遇到困难，可以参考 `starter_code/solution.py` 中的示例代码。

---

## 基础作业（必做）

### 练习 1：字符串方法练习——清洗和提取

**目标**：熟练使用字符串方法进行文本清洗和信息提取。

**任务**：

`starter_code/log_parser.py` 提供了一个基础的日志解析器框架。你需要完成以下函数：

1. **`clean_log_line(line)`**：清洗日志行
   - 去除首尾空白字符
   - 去除行尾的换行符（`\n`、 `\r\n`）
   - 如果行是空字符串，返回 `None`
   - 如果行以 `#` 开头（注释行），返回 `None`

2. **`extract_timestamp(line)`**：从日志行提取时间戳
   - 日志格式：`[2026-02-09 14:32:01] ERROR: 数据库连接超时`
   - 使用 `find()` 定位方括号位置
   - 返回方括号内的内容（如 `2026-02-09 14:32:01`）
   - 如果格式不正确，返回 `None`

3. **`extract_level(line)`**：从日志行提取日志级别
   - 提取方括号和冒号之间的内容（如 `ERROR`、`INFO`、`WARNING`）
   - 使用 `strip()` 去除前后空格
   - 转换为大写

**输入/输出示例**：

```python
# 测试 clean_log_line
clean_log_line("  [2026-02-09 14:32:01] ERROR: 超时  \n")
# 返回: "[2026-02-09 14:32:01] ERROR: 超时"

clean_log_line("   ")           # 返回: None
clean_log_line("# 这是注释")    # 返回: None

# 测试 extract_timestamp
extract_timestamp("[2026-02-09 14:32:01] ERROR: 超时")
# 返回: "2026-02-09 14:32:01"

extract_timestamp("没有方括号的行")
# 返回: None

# 测试 extract_level
extract_level("[2026-02-09 14:32:01]  warning : 磁盘不足")
# 返回: "WARNING"
```

**验证方法**：
```bash
pytest chapters/week_09/tests/test_log_parser.py::test_clean_log_line -v
pytest chapters/week_09/tests/test_log_parser.py::test_extract_timestamp -v
pytest chapters/week_09/tests/test_log_parser.py::test_extract_level -v
```

**常见错误**：
- 忘记 `strip()` 去除首尾空格，导致比较失败
- 用索引硬编码切片位置，无法处理不同长度的日志级别
- 忘记检查 `find()` 返回 `-1`（未找到）的情况
- 字符串不可变，忘记重新赋值（如 `line.strip()` 但没有 `line = line.strip()`）

---

### 练习 2：split 和 join 练习——处理 CSV 格式数据

**目标**：掌握 `split()` 和 `join()` 方法处理结构化文本数据。

**任务**：

完成 `starter_code/csv_handler.py` 中的以下函数：

1. **`parse_csv_line(line)`**：解析单行 CSV 数据
   - 输入：`"2026-02-09 14:32:01,192.168.1.1,GET,/api/users,200"`
   - 使用 `split(",")` 拆分为列表
   - 返回包含字段的字典：`{"time": ..., "ip": ..., "method": ..., "path": ..., "status": ...}`
   - 如果字段数量不对（不是 5 个），返回 `None`

2. **`filter_by_status(lines, status_code)`**：过滤指定状态码的记录
   - 输入：CSV 行列表和要过滤的状态码（如 `"404"`）
   - 返回所有匹配状态码的记录列表
   - 跳过表头行（以 `timestamp` 开头）

3. **`format_as_table(records)`**：将记录列表格式化为表格字符串
   - 使用 `join()` 方法
   - 输出格式：
     ```
     时间                  | IP           | 路径
     ----------------------|--------------|----------------
     2026-02-09 14:32:01   | 192.168.1.1  | /api/users
     ```

**输入/输出示例**：

```python
# 测试 parse_csv_line
parse_csv_line("2026-02-09 14:32:01,192.168.1.1,GET,/api/users,200")
# 返回: {
#     "time": "2026-02-09 14:32:01",
#     "ip": "192.168.1.1",
#     "method": "GET",
#     "path": "/api/users",
#     "status": "200"
# }

parse_csv_line("字段不够")  # 返回: None

# 测试 filter_by_status
lines = [
    "timestamp,ip,method,path,status",
    "2026-02-09 14:32:01,192.168.1.1,GET,/api/users,200",
    "2026-02-09 14:32:10,192.168.1.1,GET,/api/products,404",
]
filter_by_status(lines, "404")
# 返回: [{"time": "2026-02-09 14:32:10", "ip": "192.168.1.1", ...}]
```

**验证方法**：
```bash
pytest chapters/week_09/tests/test_csv_handler.py -v
```

**常见错误**：
- `split(",")` 和 `split()` 混淆——后者按任意空白拆分
- 忘记跳过表头行，把表头也当成数据处理
- `join()` 语法写反（应该是 `"|".join(list)`，不是 `list.join("|")`）
- 处理空行时返回空字符串而不是跳过

---

### 练习 3：正则表达式基础——匹配邮箱、IP 地址

**目标**：理解正则表达式基本语法，能用 `re` 模块进行模式匹配。

**任务**：

完成 `starter_code/pattern_matcher.py` 中的以下函数：

1. **`find_ip_addresses(text)`**：找出文本中所有的 IP 地址
   - IP 格式：`xxx.xxx.xxx.xxx`，每个 `xxx` 是 1-3 位数字
   - 使用 `re.findall()`
   - 返回所有匹配的 IP 地址列表

2. **`find_emails(text)`**：找出文本中所有的邮箱地址
   - 简化版邮箱格式：`用户名@域名.后缀`
   - 用户名可以包含字母、数字、下划线、点、减号
   - 使用 `re.findall()`

3. **`is_valid_phone(phone)`**：验证是否为合法的中国手机号
   - 格式：以 1 开头，第二位是 3-9，共 11 位数字
   - 使用 `re.match()` 或 `re.search()`
   - 返回布尔值

**输入/输出示例**：

```python
# 测试 find_ip_addresses
text = "服务器 192.168.1.1 和 10.0.0.1 通信"
find_ip_addresses(text)
# 返回: ["192.168.1.1", "10.0.0.1"]

# 测试 find_emails
text = "联系 admin@example.com 或 support@company.org.cn"
find_emails(text)
# 返回: ["admin@example.com", "support@company.org.cn"]

# 测试 is_valid_phone
is_valid_phone("13812345678")   # 返回: True
is_valid_phone("1381234567")    # 返回: False（10位）
is_valid_phone("11812345678")   # 返回: False（第二位是1）
is_valid_phone("23812345678")   # 返回: False（不以1开头）
```

**提示**：
- IP 正则：`r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"`
- 邮箱正则（简化版）：`r"[\w.-]+@[\w.-]+\.\w+"`
- 手机号正则：`r"^1[3-9]\d{9}$"`

**验证方法**：
```bash
pytest chapters/week_09/tests/test_pattern_matcher.py -v
```

**常见错误**：
- 忘记在正则字符串前加 `r`（原始字符串），导致 `\d` 被当成转义字符
- 用 `re.match()` 时忘记它只从开头匹配，应该用 `re.search()`
- 忘记 `findall()` 返回的是列表，直接对结果用 `.group()`
- 正则写得太严格（如邮箱不允许点号）或太宽松（如 IP 匹配 999.999.999.999）

---

### 练习 4：日志分析器扩展——添加新功能

**目标**：综合运用字符串方法和正则表达式，为日志分析器添加实用功能。

**任务**：

在 `starter_code/log_analyzer.py` 中完成以下功能：

1. **`extract_urls(text)`**：从文本中提取所有 URL
   - 简化版 URL 格式：`http://...` 或 `https://...`
   - 使用正则表达式
   - 返回 URL 列表

2. **`analyze_error_types(log_lines)`**：分析错误日志，按错误类型统计
   - 输入：日志行列表
   - 提取每行的日志级别（ERROR、WARNING、INFO 等）
   - 返回字典：`{"ERROR": 5, "WARNING": 3, "INFO": 10}`

3. **`find_slow_queries(log_lines, threshold_ms)`**：找出慢查询日志
   - 假设慢查询日志格式：`[时间] SLOW: 查询耗时 150ms - SELECT ...`
   - 提取耗时数字，与阈值比较
   - 返回超过阈值的查询列表

**输入/输出示例**：

```python
# 测试 extract_urls
text = "访问 https://example.com 或 http://test.org/path"
extract_urls(text)
# 返回: ["https://example.com", "http://test.org/path"]

# 测试 analyze_error_types
logs = [
    "[2026-02-09 14:32:01] ERROR: 连接失败",
    "[2026-02-09 14:32:02] WARNING: 内存不足",
    "[2026-02-09 14:32:03] ERROR: 超时",
]
analyze_error_types(logs)
# 返回: {"ERROR": 2, "WARNING": 1}

# 测试 find_slow_queries
logs = [
    "[2026-02-09 14:32:01] SLOW: 查询耗时 150ms - SELECT * FROM users",
    "[2026-02-09 14:32:02] SLOW: 查询耗时 50ms - SELECT * FROM posts",
]
find_slow_queries(logs, 100)
# 返回: [{"time": "2026-02-09 14:32:01", "duration": 150, "query": "SELECT * FROM users"}]
```

**验证方法**：
```bash
pytest chapters/week_09/tests/test_log_analyzer.py -v
```

**常见错误**：
- 正则表达式贪婪匹配导致结果过多（用 `.*?` 非贪婪版本）
- 忘记处理日志格式不匹配的情况
- 提取数字时忘记转换为 `int`
- 没有处理空输入或空列表的情况

---

## 进阶作业（选做）

### 挑战 1：实现 URL 参数提取器

**目标**：编写更复杂的正则模式，提取 URL 中的查询参数。

**任务**：

完成 `starter_code/url_parser.py` 中的函数：

1. **`parse_query_params(url)`**：解析 URL 查询参数
   - 输入：`"https://example.com/search?q=python&page=1&sort=desc"`
   - 返回字典：`{"q": "python", "page": "1", "sort": "desc"}`

2. **`parse_path_params(url)`**：解析 RESTful 路径参数
   - 输入：`"/api/users/123/posts/456"`
   - 返回列表：`["users", "123", "posts", "456"]`

3. **`reconstruct_url(base, params)`**：根据基础 URL 和参数字典重建 URL
   - 输入：`"https://api.example.com/search"`, `{"q": "python", "page": "2"}`
   - 返回：`"https://api.example.com/search?q=python&page=2"`

**输入/输出示例**：

```python
parse_query_params("https://example.com/search?q=python&page=1")
# 返回: {"q": "python", "page": "1"}

parse_query_params("https://example.com/")  # 没有参数
# 返回: {}

parse_path_params("/api/users/123/posts/456")
# 返回: ["api", "users", "123", "posts", "456"]

reconstruct_url("https://api.example.com/search", {"q": "python"})
# 返回: "https://api.example.com/search?q=python"
```

**提示**：
- 查询参数正则：`r"[?&](\w+)=(\w+)"`
- 考虑使用 `re.findall()` 配合分组
- 处理 URL 编码（如 `%20` 转换为空格）是加分项

---

### 挑战 2：处理编码问题和异常边界

**目标**：学会处理文本处理中的编码问题和边界情况。

**任务**：

完成 `starter_code/safe_reader.py` 中的函数：

1. **`safe_read_file(file_path, encoding='utf-8')`**：安全读取文件
   - 尝试用指定编码读取
   - 如果失败，依次尝试 `gbk`、`latin-1`
   - 如果都失败，用 `errors='replace'` 读取
   - 返回文件内容

2. **`read_logs_with_fallback(file_path)`**：读取日志文件，处理各种边界情况
   - 跳过空行和注释行
   - 记录解析失败的行号
   - 返回成功解析的记录列表和错误列表

3. **`normalize_whitespace(text)`**：规范化空白字符
   - 将所有制表符、换行符、多个连续空格替换为单个空格
   - 去除首尾空白
   - 返回规范化后的文本

**输入/输出示例**：

```python
# 测试 normalize_whitespace
normalize_whitespace("  hello   world\t\n  python  ")
# 返回: "hello world python"

# safe_read_file 应该能处理不同编码的文件
# read_logs_with_fallback 返回 (records, errors) 元组
```

**提示**：
- 使用 `try/except UnicodeDecodeError` 处理编码问题
- 使用 `re.sub(r"\s+", " ", text)` 规范化空白
- 考虑使用 `enumerate()` 记录行号

---

## AI 协作练习（可选）

**背景**：阿码想用 AI 工具帮他写一个提取手机号和身份证号的正则表达式。AI 生成了下面的代码，但老潘提醒他："AI 生成的正则一定要验证，它可能会漏掉边界情况。"

### AI 生成的代码

```python
# ai_generated_patterns.py （AI 生成）

import re

def extract_phones(text):
    """提取手机号"""
    pattern = r"1\d{10}"
    return re.findall(pattern, text)

def extract_id_cards(text):
    """提取身份证号"""
    pattern = r"\d{17}[\dXx]"
    return re.findall(pattern, text)

def extract_dates(text):
    """提取日期（格式：YYYY-MM-DD）"""
    pattern = r"\d{4}-\d{2}-\d{2}"
    return re.findall(pattern, text)
```

### 审查清单

请仔细审查这段 AI 生成的代码：

- [ ] **正则表达式是否正确？**
  - 手机号正则 `1\d{10}` 是否太宽松？（会匹配 12 开头的"手机号"吗？）
  - 身份证号正则会匹配 19 位数字吗？
  - 日期正则会匹配 `2026-99-99` 这种无效日期吗？

- [ ] **边界情况是否处理？**
  - 如果输入是空字符串，会返回什么？
  - 如果输入是 `None`，会抛出异常吗？
  - 连续的数字会被当成一个还是多个匹配？

- [ ] **能否写出让它失败的测试？**
  - 写一个测试，证明手机号正则的问题
  - 写一个测试，证明身份证号正则的问题
  - 写一个测试，证明日期正则的问题

- [ ] **是否有改进空间？**
  - 能否提取带区号的座机号？
  - 能否区分 15 位和 18 位身份证号？
  - 能否同时支持 `YYYY-MM-DD` 和 `YYYY/MM/DD` 格式？

### 你的任务

1. **找出至少 3 个问题**：列出你发现的问题，说明为什么它们是问题

2. **编写测试用例**：为 AI 的代码编写测试，证明问题存在

3. **修复并改进**：基于 AI 的代码，写出更好的版本

4. **撰写审查报告**：创建 `ai_review_report.md`，包含：
   - AI 生成代码的优点
   - 发现的问题清单（附测试用例）
   - 你的改进版本（附改进说明）
   - 对 "AI 生成正则 vs 人工编写正则" 的思考

**提示**：
- 中国大陆手机号第二位是 3-9，不是任意数字
- 身份证号最后一位是校验位，有特定算法
- 日期正则如果不限制范围，会匹配 `9999-99-99`

---

## 验证与提交

### 自测清单

在提交前，请确认：

- [ ] 练习 1 完成：`clean_log_line`、`extract_timestamp`、`extract_level` 函数正确实现
- [ ] 练习 2 完成：`parse_csv_line`、`filter_by_status`、`format_as_table` 函数正确实现
- [ ] 练习 3 完成：正则表达式能正确匹配 IP、邮箱、手机号
- [ ] 练习 4 完成：日志分析器扩展功能正常工作
- [ ] 运行 `python3 -m pytest chapters/week_09/tests -q` 通过所有测试
- [ ] 进阶练习（如完成）：URL 参数提取器能正确处理各种格式
- [ ] 进阶练习（如完成）：编码问题处理函数能安全读取不同编码的文件
- [ ] 代码已提交到 Git，至少有 2 次提交（draft + verify）

### Git 提交规范

```bash
# 第一次提交（草稿）
git add chapters/week_09/starter_code/log_parser.py
git commit -m "draft week_09: 完成字符串方法练习"

# 第二次提交（验证）
git add chapters/week_09/starter_code/pattern_matcher.py
git commit -m "verify week_09: 添加正则表达式功能"

# 推送到远端
git push origin week_09
```

### Pull Request 描述模板

```markdown
## Week 09 作业完成情况

### 已完成的练习
- [x] 练习 1：字符串方法练习（清洗和提取）
- [x] 练习 2：split 和 join 练习（处理 CSV 格式数据）
- [x] 练习 3：正则表达式基础（匹配邮箱、IP 地址）
- [x] 练习 4：日志分析器扩展（添加新功能）

### 进阶练习（可选）
- [ ] 挑战 1：URL 参数提取器
- [ ] 挑战 2：处理编码问题和异常边界

### AI 协作练习（可选）
- [ ] 审查 AI 生成的正则表达式

### 自测结果
- 运行 `python3 -m pytest chapters/week_09/tests -q`：通过 / 失败
- 发现的边界情况：（列出你处理的特殊输入）

### 遇到的困难
（记录你遇到的问题和解决方法）

### 请 Review 的重点
（特别希望 reviewer 关注的地方，如正则表达式的准确性）
```

---

## 常见问题 FAQ

**Q1: `split()` 和 `partition()` 有什么区别？什么时候用哪个？**

A: `split()` 按分隔符拆分所有部分，返回列表；`partition()` 只拆一次，返回三元组 `(before, separator, after)`。当你只需要分成"前面"和"后面"两部分时，`partition()` 更清晰。

**Q2: 正则表达式前面的 `r` 是什么意思？**

A: `r"..."` 表示原始字符串（raw string），里面的反斜杠不会被当作转义字符。写正则时永远用原始字符串，否则 `\d` 会被解释成特殊字符而不是"匹配数字"。

**Q3: `re.search()` 和 `re.match()` 有什么区别？**

A: `re.match()` 只从字符串开头匹配；`re.search()` 扫描整个字符串，返回第一个匹配。大多数情况下用 `re.search()`。

**Q4: 正则表达式中的 `.`、`*`、`+`、`?` 分别匹配什么？**

A:
- `.` 匹配任意单个字符（除换行）
- `*` 前面的内容出现 0 次或多次
- `+` 前面的内容出现 1 次或多次
- `?` 前面的内容出现 0 次或 1 次

**Q5: 处理用户输入的文本时，应该考虑哪些边界情况？**

A:
- 空字符串或仅包含空白的字符串
- 特殊字符（换行符、制表符、Unicode 字符）
- 超长输入
- 编码问题（特别是中文）
- 格式不规范的输入

**Q6: AI 生成的正则可以直接用吗？**

A: 不建议直接复制。应该：1) 让 AI 解释每一部分的作用；2) 在 regex101.com 上用真实数据测试；3) 补充边界情况测试；4) 理解后再使用。

---

## 挑战自我

如果你想进一步挑战自己，可以尝试：

1. **HTML 解析**：用正则表达式提取 HTML 中的标签和属性（注意：真实项目应该用 BeautifulSoup）
2. **日志聚合器**：读取多个日志文件，按时间顺序合并输出
3. **正则性能测试**：比较 `re.search()` 和字符串方法的性能差异
4. **PyHelper 增强**：为 PyHelper 添加更多文本处理功能（如标签云、关键词统计）

---

祝你学习愉快！文本处理是编程的核心技能之一，掌握后你会发现自己能处理的数据类型大大扩展了。
