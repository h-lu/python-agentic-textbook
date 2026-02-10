# Week 09：文本处理——从混乱中提取秩序

> "Some people, when confronted with a problem, think 'I know, I'll use regular expressions.' Now they have two problems."
> — Jamie Zawinski

2026年，大语言模型每天处理着数以亿计的文本请求。从 ChatGPT 到 Claude，这些 AI 的"眼睛"本质上就是复杂的文本处理算法——它们需要解析用户的输入、提取关键信息、理解上下文。但有趣的是，当 AI 帮你写代码时，它生成的往往也是文本：日志文件、配置文件、数据报表。

根据 GitHub Octoverse 报告，Python 已成为日志分析管道的核心语言，而 JSON 格式日志可将分析效率提高 60-80%。当你学会从混乱的文本中提取秩序，你就掌握了与 AI 协作的底层能力——不是被动地接受 AI 的输出，而是主动地处理、验证、转化它们。

本周，你将学会 Python 的文本处理利器：从基础的字符串方法到强大的正则表达式。

---

## 前情提要

上周你给 PyHelper 穿上了测试的铠甲——用 pytest 为 `storage.py` 和 `records.py` 编写了自动化测试。现在你可以放心地重构代码，因为测试会在你犯错时及时提醒。

但小北发现了一个新问题："我的学习笔记越记越多，想找某天的笔记得翻半天。能不能让 PyHelper 帮我搜索？"

"比如搜所有包含'Python'的笔记？"阿码问。

"对，还有按日期范围过滤，比如只看 2026 年 2 月的笔记。"

老潘正好路过："这需要文本处理能力。字符串不只是存储文本，还能拆分、查找、匹配模式。这周你们将学习 Python 的字符串方法和正则表达式——让程序从混乱的文本中提取秩序。"

---

## 学习目标

完成本周学习后，你将能够：
1. 熟练使用 Python 字符串方法进行文本清洗和提取
2. 理解正则表达式的基本语法，能用 `re` 模块进行模式匹配
3. 使用 `split` 和 `join` 处理结构化文本数据
4. 识别和处理文本处理中的边界情况（空字符串、特殊字符、编码问题）
5. 为 PyHelper 添加搜索和过滤学习笔记的功能

---

<!--
贯穿案例设计：日志分析器（Log Analyzer）
- 第 1 节：字符串方法入门 → 从简单的日志行提取时间戳和日志级别
- 第 2 节：split/join 处理结构化文本 → 拆分 CSV 格式的日志，重组输出
- 第 3 节：正则表达式基础 → 用模式匹配复杂的日志格式
- 第 4 节：re 模块实战 → 提取 IP 地址、邮箱等结构化信息
- 第 5 节：边界情况与错误处理 → 处理乱码、空行、格式不规范的日志
- 最终成果：一个能解析、搜索、过滤日志文件的 Log Analyzer，读者可以分析自己的程序日志

案例演进路线：
1. 硬编码解析 → 2. 字符串方法提取 → 3. split/join 重组 → 4. 正则匹配复杂模式 → 5. 完整的日志分析工具
-->

<!--
认知负荷预算：
- 本周新概念（5 个，预算上限 5 个）：
  1. 字符串方法（strip/split/join/find/replace 等）
  2. 正则表达式基础语法
  3. re 模块（search/match/findall/group）
  4. 原始字符串（r"..."）
  5. 边界用例思维（空字符串、特殊字符、编码）
- 结论：✅ 在预算内

回顾桥设计（至少 2 个，目标引用前 3 周的概念）：
- [函数定义]（来自 week_03）：贯穿案例中，每个解析功能封装为独立函数
- [列表/字典]（来自 week_04）：解析结果用列表存储，结构化数据用字典表示
- [文件读写]（来自 week_05）：日志从文件读取，分析结果写入新文件
- [异常处理]（来自 week_06）：处理格式错误的日志行、编码问题
- [pytest 断言]（来自 week_08）：为文本解析函数编写测试，验证边界情况

角色出场规划：
- 小北（第 1 节）：在处理用户输入时遇到空格问题，引出 strip() 方法
- 阿码（第 3 节）：质疑"为什么要学正则，字符串方法不够吗？"引出正则的价值
- 老潘（第 5 节）：分享工作中处理日志的实战经验，强调边界情况的重要性

AI 小专栏规划：
- AI 小专栏 #1（放在第 2 节之后）：
  - 主题：AI 辅助文本处理工具——从 ChatGPT 到专门的文本处理 AI
  - 连接点：与第 2 节"split/join 处理结构化文本"呼应，讨论 AI 时代文本处理工具的发展
  - 建议搜索词："AI text processing tools 2026", "LLM data extraction 2026"

- AI 小专栏 #2（放在第 4 节之后）：
  - 主题：用 AI 生成和调试正则表达式——Prompt 工程在模式匹配中的应用
  - 连接点：与第 4 节"re 模块实战"呼应，讨论如何用 AI 辅助编写复杂正则
  - 建议搜索词："AI regex generator 2026", "ChatGPT regular expression debugging 2026"

PyHelper 本周推进：
- 上周状态：PyHelper 已有多模块结构和 pytest 测试覆盖
- 本周改进：添加搜索和过滤功能
  1. `search_notes(keyword)` - 按关键词搜索笔记内容
  2. `filter_by_date(start_date, end_date)` - 按日期范围过滤
  3. `extract_tags()` - 从笔记中提取标签（如 #Python #学习）
- 涉及的本周概念：字符串方法（find/in）、正则表达式（提取标签）、边界处理（空搜索词）
- 建议示例文件：examples/pyhelper/text_utils.py（新增模块）
-->

## 1. 字符串不只是文字

小北接到了一个任务：分析服务器日志。日志文件里每一行都长这样：

```
[2026-02-09 14:32:01] ERROR: 数据库连接超时
```

她需要从中提取时间戳、日志级别和具体信息。小北想了想，用上周学的索引切片试试：

```python
log_line = "[2026-02-09 14:32:01] ERROR: 数据库连接超时"

timestamp = log_line[1:20]      # 提取 "2026-02-09 14:32:01"
level = log_line[22:27]         # 提取 "ERROR"
message = log_line[29:]         # 提取 "数据库连接超时"

print(f"时间: {timestamp}")
print(f"级别: {level}")
print(f"消息: {message}")
```

注意到这里用的 **f-string**（Week 01 学的内容）——在字符串前加 `f`，用 `{}` 嵌入变量。这比用 `+` 拼接字符串清晰多了。

运行一下，好像能工作。但小北很快发现了问题——如果日志级别是 `INFO` 而不是 `ERROR`，字符位置就变了：

```python
log_line = "[2026-02-09 14:32:02] INFO: 用户登录成功"
level = log_line[22:27]         # 提取 "INFO:" —— 多了一个冒号！
```

"这也太脆弱了吧，"小北嘟囔着，"稍微变个格式就出错。"

她需要的不是"第几个字符"，而是"方括号里的内容""方括号和冒号之间的内容"。这时候，字符串方法就派上用场了。

### 用 find 定位，用 strip 清洗

`find()` 方法可以帮你找到子串的位置：

```python
log_line = "[2026-02-09 14:32:01] ERROR: 数据库连接超时"

# 找到右方括号的位置
bracket_end = log_line.find("]")
print(bracket_end)              # 输出: 21

# 找到冒号的位置
colon_pos = log_line.find(":")
print(colon_pos)                # 输出: 28
```

`find()` 返回子串第一次出现的索引，找不到时返回 `-1`。有了位置，就可以更灵活地切片：

```python
# 提取方括号里的时间戳（不包括方括号）
timestamp = log_line[1:bracket_end]
print(timestamp)                # 输出: 2026-02-09 14:32:01

# 提取日志级别（方括号和冒号之间，去掉空格）
level = log_line[bracket_end+2:colon_pos]
print(level)                    # 输出: ERROR
```

但这里有个隐患——如果日志级别前后有空格呢？

```python
log_line = "[2026-02-09 14:32:01]  WARNING : 磁盘空间不足"
level = log_line[bracket_end+2:colon_pos]
print(f"级别: '{level}'")        # 输出: ' WARNING ' —— 前后有空格！
```

这就是 `strip()` 方法的用武之地。它去除字符串首尾的空白字符：

```python
level = level.strip()
print(f"级别: '{level}'")        # 输出: 'WARNING'
```

`strip()` 还可以去除指定的字符：

```python
"[ERROR]".strip("[]")           # 输出: 'ERROR'
"---hello---".strip("-")         # 输出: 'hello'
```

### 字符串是不可变的序列

这里有个重要细节你可能没注意：上面的代码中，`level.strip()` 并没有改变 `level` 本身，而是返回了一个新字符串。

```python
level = " WARNING "
level.strip()                   # 返回 "WARNING"，但 level 还是 " WARNING "
print(level)                    # 输出: " WARNING "

# 必须重新赋值
level = level.strip()
print(level)                    # 输出: "WARNING"
```

字符串在 Python 中是**不可变**（immutable）的——一旦创建，就不能修改。所有字符串方法都返回新字符串，而不是修改原字符串。这和列表不同：

```python
# 列表是可变的
my_list = [1, 2, 3]
my_list.append(4)               # my_list 变成了 [1, 2, 3, 4]

# 字符串是不可变的
my_str = "hello"
my_str.upper()                  # 返回 "HELLO"，但 my_str 还是 "hello"
```

这个特性让字符串更安全——你不用担心某个函数会"偷偷"修改你的字符串。但也意味着字符串拼接频繁时，要考虑性能（虽然对初学者来说，先写对更重要）。

现在小北可以写一个更健壮的解析函数了：

```python
def parse_log_line(line):
    """解析单行日志，返回字典"""
    bracket_end = line.find("]")
    colon_pos = line.find(":")

    if bracket_end == -1 or colon_pos == -1:
        return None                 # 格式不对，返回 None

    timestamp = line[1:bracket_end]
    level = line[bracket_end+2:colon_pos].strip()
    message = line[colon_pos+2:]

    return {
        "timestamp": timestamp,
        "level": level,
        "message": message
    }

# 测试
log = "[2026-02-09 14:32:01] ERROR: 数据库连接超时"
result = parse_log_line(log)
print(result)
# 输出: {'timestamp': '2026-02-09 14:32:01', 'level': 'ERROR', 'message': '数据库连接超时'}
```

这个版本比硬编码切片好多了——它能处理不同长度的日志级别，还能检查格式是否正确。但小北注意到，如果日志格式再复杂一点（比如时间戳里有方括号，或者消息里也有冒号），这个解析器还是会出错。

"有没有更强大的工具？"她问。

"有，"老潘说，"但先别急。把基础打牢，你会发现正则表达式只是另一种描述'查找模式'的方式。"

---

## 2. 拆分与重组——split 和 join 的艺术

掌握了 `find()` 和 `strip()`，你已经能处理很多文本清洗任务了。但面对结构化的数据——比如 CSV 格式的日志——逐个字符地找位置就显得笨拙。这时候，`split()` 和 `join()` 这对黄金搭档就该出场了。

阿码拿到了一份 CSV 格式的访问日志，这是运维部门导出的标准格式，长这样：

```
timestamp,ip,method,path,status
2026-02-09 14:32:01,192.168.1.1,GET,/api/users,200
2026-02-09 14:32:05,192.168.1.2,POST,/api/login,200
2026-02-09 14:32:10,192.168.1.1,GET,/api/products,404
```

他需要从每一行提取 IP 地址和状态码。阿码想了想，用 `find` 一个个找逗号的位置？那也太麻烦了。

"用 `split()`，"老潘从旁边飘过，"专门干这个的。"

### 用 split 拆，用 join 合

`split()` 方法按指定分隔符把字符串拆成列表：

```python
line = "2026-02-09 14:32:01,192.168.1.1,GET,/api/users,200"
parts = line.split(",")
print(parts)
# 输出: ['2026-02-09 14:32:01', '192.168.1.1', 'GET', '/api/users', '200']

# 提取特定字段
ip = parts[1]
status = parts[4]
print(f"IP: {ip}, 状态: {status}")
```

默认情况下，`split()` 按空白字符（空格、制表符、换行）拆分，且会合并连续的空白：

```python
"hello   world".split()         # 输出: ['hello', 'world']
"hello\tworld\npython".split()  # 输出: ['hello', 'world', 'python']
```

如果不传参数，`split()` 还会自动去除首尾的空白。这在处理用户输入时特别有用——还记得 Week 06 学的**输入校验**吗？在调用 `int()` 或 `float()` 转换之前，先用 `split()` 清理一下用户输入的空白，可以避免很多麻烦：

```python
user_input = "  192.168.1.1  "
user_input.split(",")           # 输出: ['  192.168.1.1  ']
user_input.split()              # 输出: ['192.168.1.1']
```

`split()` 还有个兄弟 `partition()`，它只拆一次，返回三元组：

```python
"key=value".partition("=")      # 输出: ('key', '=', 'value')
"key=value=extra".partition("=") # 输出: ('key', '=', 'value=extra')
```

当你只需要拆成"前面"和"后面"两部分时，`partition()` 比 `split()` 更清晰。

那 `join()` 呢？它是 `split()` 的逆操作——用字符串作为"胶水"，把列表粘起来：

```python
words = ["hello", "world", "python"]
" ".join(words)                 # 输出: "hello world python"
",".join(words)                 # 输出: "hello,world,python"
"-".join(words)                 # 输出: "hello-world-python"
```

注意 `join()` 的语法有点特别——它是"胶水".join(列表)，而不是列表.join("胶水")。这看起来反直觉，但想想就明白了：字符串方法属于字符串类型，列表没有 `join` 方法。

### 实战：过滤日志

现在阿码可以写一个函数，从 CSV 日志中提取所有状态码为 404 的记录：

```python
def filter_404_logs(csv_lines):
    """从 CSV 日志中提取所有 404 错误"""
    errors = []
    for line in csv_lines:
        line = line.strip()
        if not line or line.startswith("timestamp"):
            continue                    # 跳过空行和表头

        parts = line.split(",")
        if len(parts) >= 5 and parts[4] == "404":
            errors.append({
                "time": parts[0],
                "ip": parts[1],
                "path": parts[3]
            })
    return errors

# 测试
logs = [
    "timestamp,ip,method,path,status",
    "2026-02-09 14:32:01,192.168.1.1,GET,/api/users,200",
    "2026-02-09 14:32:10,192.168.1.1,GET,/api/products,404",
    "2026-02-09 14:32:15,192.168.1.3,GET,/api/admin,404"
]

errors = filter_404_logs(logs)
for e in errors:
    print(f"{e['time']} - {e['ip']} 访问 {e['path']} 失败")
```

这段代码用到了 Week 02 学的 **for 循环**遍历列表，以及 **条件判断**（`if not line or line.startswith("timestamp")`）来跳过表头和空行。还记得吗？`continue` 让程序跳过当前循环的剩余代码，直接进入下一次迭代。

运行结果：

```
2026-02-09 14:32:10 - 192.168.1.1 访问 /api/products 失败
2026-02-09 14:32:15 - 192.168.1.3 访问 /api/admin 失败
```

阿码很满意，但他注意到一个问题：如果日志字段里包含逗号怎么办？比如路径是 `/api/search?q=hello,world`，`split(",")` 就会把它拆成两部分。

"这就是 CSV 格式的局限，"老潘说，"真实的 CSV 解析需要用专门的库（比如 `csv` 模块），它会处理引号、转义等复杂情况。但对于简单的日志分析，`split()` 已经够用了。"

阿码点点头，突然想到另一个问题："那如果我想把过滤后的结果输出成另一种格式呢？"

"用 `join()` 重组："

```python
def format_errors_for_report(errors):
    """把错误记录格式化成报告格式"""
    lines = ["时间,IP,路径"]
    for e in errors:
        line = ",".join([e["time"], e["ip"], e["path"]])
        lines.append(line)
    return "\n".join(lines)

report = format_errors_for_report(errors)
print(report)
```

输出：

```
时间,IP,路径
2026-02-09 14:32:10,192.168.1.1,/api/products
2026-02-09 14:32:15,192.168.1.3,/api/admin
```

`split()` 和 `join()` 是一对黄金搭档——一个把结构化文本拆成数据，一个把数据重组为文本。掌握了它们，你就掌握了文本处理的"拆"与"合"。

但阿码的日志分析任务还没完。第二天，他收到了另一批日志——这次不是规整的 CSV 格式，而是系统直接输出的混合文本。阿码打开文件，眉头皱了起来：

```
[2026-02-09 14:32:01] 192.168.1.1 - GET /api/users 200
[2026-02-09 14:32:05] 用户 admin@example.com 登录成功
[2026-02-09 14:32:10] 192.168.1.1 - GET /api/products 404
[2026-02-09 14:32:15] 收到来自 user@company.org 的反馈: 系统卡顿
```

"这怎么弄？"阿码挠挠头，"格式完全不统一啊——有的带 IP 和 HTTP 状态码，有的是纯文本描述，还有的包含邮箱地址。用 `split()` 根本没法处理，因为分隔符不一样，字段位置也不固定。"

他试着用 `find()` 找规律，但很快就陷入了嵌套的 `if` 判断——"如果这一行有 IP 地址，就……如果这一行有邮箱，就……"

"字符串方法不够用啊。"阿码有点沮丧。

"这时候就该正则表达式出场了，"老潘说，"它不是字符串方法的替代品，而是'描述模式'的语言——你不需要知道数据在第几个位置，只需要描述'它长什么样'。"

---

> **AI 时代小专栏：AI 辅助文本处理工具**
>
> 2026 年的文本处理领域正在经历一场变革。传统的正则表达式和字符串方法依然重要，但 AI 工具正在成为开发者的新帮手。
>
> **Firecrawl**（https://www.firecrawl.dev）是一个典型的例子——它能将任意网站转换为结构化的 Markdown 或 JSON，供大语言模型使用。你不再需要手写复杂的爬虫和解析逻辑，只需调用 API 就能获得干净的结构化数据。
>
> 在受监管的行业（金融、保险、法律），**IBM Watson Natural Language Understanding** 提供了企业级的文本分析能力，包括情感分析、实体提取和关系识别。这些工具的优势在于可解释性和合规性——比直接调用通用大模型更符合审计要求。
>
> 2026 年的趋势是**混合工作流**（OCR/API + LLM）：先用传统的文档处理 API 保证准确性，再用大语言模型进行语义理解和结构化提取。比如处理发票时，先用 OCR 提取文本，再用 LLM 理解"这是供应商名称，那是金额"。
>
> 更值得关注的是**无代码/低代码平台**（如 Unstract）的兴起——非技术用户也能通过拖拽界面构建文本提取管道。这意味着文本处理能力正在民主化。
>
> 但这不意味着你学的 `split()` 和 `join()` 过时了。恰恰相反——当 AI 返回的结果需要清洗、当混合工作流需要胶水代码、当你需要验证 AI 的输出时，这些基础工具仍然是零成本、高可控的选择。理解底层原理，才能在高层次工具面前保持清醒。
>
> 参考（访问日期：2026-02-09）：
> - https://www.firecrawl.dev
> - https://www.ovaledge.com/blog/natural-language-processing-software
> - https://brightdata.com/blog/web-data/best-data-extraction-tools

---

## 3. 当字符串方法不够用——正则表达式入门

阿码盯着那堆混杂的日志，意识到一个令人沮丧的事实：字符串方法虽然好用，但有个前提——你得知道数据"长什么样"。面对这种格式完全不统一的文本，`split()` 和 `find()` 都束手无策。

"我需要从所有行中提取 IP 地址和邮箱，"阿码自言自语，"但有的行有 IP，有的没有；邮箱出现在不同位置，分隔符也不一样。"

他试着写了几行代码，很快就陷入了嵌套的 `if` 判断地狱——"如果这一行包含四个数字和三个点，就提取 IP；如果包含 @ 符号，就提取邮箱……"

"字符串方法不够用啊。"阿码有点沮丧。

"这时候就该正则表达式出场了，"老潘说，"它不是字符串方法的替代品，而是'描述模式'的语言——你不需要知道数据在第几个位置，只需要描述'它长什么样'。"

### 什么是正则表达式

**正则表达式**（Regular Expression，简称 regex 或 regexp）是一种描述文本模式的迷你语言。它让你用特殊的语法表达"我要找的东西长这样"。

比如，IP 地址的模式是"四个 0-255 的数字，用点分隔"。用正则表达式写：

```
\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}
```

看不懂？没关系，拆开来看：

- `\d` 匹配任意数字（0-9）
- `{1,3}` 表示前面的内容出现 1 到 3 次
- `\.` 匹配一个点（注意反斜杠是转义，因为点在正则里有特殊含义）

邮箱的模式更复杂："用户名@域名.后缀"。简化版正则：

```
\w+@\w+\.\w+
```

- `\w` 匹配字母、数字或下划线
- `+` 表示前面的内容出现 1 次或多次

### Python 中的正则：re 模块

Python 用 `re` 模块支持正则表达式。最常用的是 `re.search()`：

```python
import re

log_line = "[2026-02-09 14:32:01] 192.168.1.1 - GET /api/users 200"

# 搜索 IP 地址
pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
match = re.search(pattern, log_line)

if match:
    print(f"找到 IP: {match.group()}")  # 输出: 找到 IP: 192.168.1.1
else:
    print("没找到 IP")
```

注意正则表达式字符串前面的 `r`，它表示**原始字符串**（raw string）。在原始字符串里，反斜杠就是反斜杠，不会被当作转义字符：

```python
# 普通字符串：\d 会被解释成转义序列
"\d"        # 实际存储的是特殊字符，不是反斜杠加 d

# 原始字符串：\d 就是反斜杠加 d
r"\d"       # 正则表达式引擎收到 \d，知道是"匹配数字"
```

如果不加 `r`，你得写 `\\d` 才能让正则收到 `\d`，这太容易出错了。所以**写正则时永远用原始字符串**。

`re.search()` 扫描整个字符串，返回第一个匹配的位置。如果只想从开头匹配（比如验证整个字符串是否符合某个格式），用 `re.match()`：

```python
# match 只从开头匹配
re.match(r"\d+", "123abc")      # 匹配成功，返回 Match 对象
re.match(r"\d+", "abc123")      # 匹配失败，返回 None

# search 扫描整个字符串
re.search(r"\d+", "abc123")     # 匹配成功，找到 "123"
```

### 常用元字符速查

正则表达式有一套自己的"字母表"，以下是常用的：

| 元字符 | 含义 | 示例 |
|--------|------|------|
| `.` | 匹配任意字符（除换行） | `a.c` 匹配 "abc", "a1c" |
| `\d` | 匹配数字 | `\d{3}` 匹配 "123" |
| `\w` | 匹配字母/数字/下划线 | `\w+` 匹配 "hello_world" |
| `\s` | 匹配空白字符 | `\s+` 匹配空格、制表符 |
| `^` | 字符串开头 | `^Hello` 匹配以 Hello 开头 |
| `$` | 字符串结尾 | `world$` 匹配以 world 结尾 |
| `*` | 前面的内容出现 0 次或多次 | `a*` 匹配 "", "a", "aaa" |
| `+` | 前面的内容出现 1 次或多次 | `a+` 匹配 "a", "aaa" |
| `?` | 前面的内容出现 0 次或 1 次 | `colou?r` 匹配 "color", "colour" |
| `{n,m}` | 前面的内容出现 n 到 m 次 | `\d{2,4}` 匹配 "12", "123", "1234" |
| `[]` | 字符集，匹配其中任意一个 | `[aeiou]` 匹配任意元音 |
| `\|` | 或，匹配左边或右边 | `cat\|dog` 匹配 "cat" 或 "dog" |
| `()` | 分组，用于提取子串 | `(\d+)-(\d+)` 提取两个数字 |

这些元字符可以组合出复杂的模式。比如，匹配一个合法的日期格式（YYYY-MM-DD）：

```python
date_pattern = r"\d{4}-\d{2}-\d{2}"
re.search(date_pattern, "今天是 2026-02-09，天气晴")  # 匹配成功
```

阿码试着用正则提取日志中的邮箱：

```python
import re

log_line = "[2026-02-09 14:32:15] 收到来自 user@company.org 的反馈"

# 简化版邮箱正则（实际邮箱规则更复杂）
email_pattern = r"\w+@\w+\.\w+"
match = re.search(email_pattern, log_line)

if match:
    print(f"找到邮箱: {match.group()}")  # 输出: 找到邮箱: user@company.org
```

"这比用字符串方法找 '@' 再前后扩展靠谱多了，"阿码说，"但那个 `\w` 好像只能匹配字母数字，如果邮箱里有 '.' 或 '-' 呢？"

"好问题，"老潘点头，"`user.name@company.org` 用上面的正则是匹配不到的。你可以用字符集改进："

```python
# 更完善的邮箱正则（仍然简化版）
email_pattern = r"[\w.-]+@[\w.-]+\.\w+"
```

`[\w.-]` 表示"字母数字下划线，或者点，或者减号"。这样 `user.name@company.org` 和 `admin-01@sub.company.org` 都能匹配了。

"正则表达式就像一把瑞士军刀，"老潘说，"小巧但功能强大。但它也有缺点——写的时候爽，读的时候哭。所以复杂的正则一定要写注释，或者拆成多个小模式。"

---

## 4. re 模块实战——模式匹配与提取

现在你已经会写简单的正则表达式了。但 `re.search()` 只是开始，`re` 模块还有更多强大的功能。

### findall：找到所有匹配

`re.search()` 只返回第一个匹配。如果你想找到所有 IP 地址，用 `re.findall()`：

```python
import re

log_text = """
[2026-02-09 14:32:01] 192.168.1.1 - GET /api/users 200
[2026-02-09 14:32:05] 用户 admin@example.com 登录成功
[2026-02-09 14:32:10] 192.168.1.1 - GET /api/products 404
[2026-02-09 14:32:15] 192.168.1.2 - POST /api/login 200
"""

ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
ips = re.findall(ip_pattern, log_text)

print(ips)
# 输出: ['192.168.1.1', '192.168.1.1', '192.168.1.2']
```

`findall()` 返回所有非重叠匹配的列表。如果正则里有分组（括号），它会返回分组内容的元组列表：

```python
# 提取日期和时间 separately
datetime_pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})"
datetimes = re.findall(datetime_pattern, log_text)

print(datetimes)
# 输出: [('2026-02-09', '14:32:01'), ('2026-02-09', '14:32:05'), ...]
```

每个元组对应一个匹配，元组里的元素对应括号里的分组。

### 分组提取：用 () 捕获子串

分组是正则最强大的功能之一。它让你在一次匹配中提取多个相关信息。

假设你要从日志中提取 HTTP 方法和路径：

```python
log_line = "192.168.1.1 - GET /api/users?page=1 200"

# 用分组提取方法、路径、状态码
pattern = r"(\w+) (/\S+) (\d{3})"
match = re.search(pattern, log_line)

if match:
    method = match.group(1)     # 第一个分组: GET
    path = match.group(2)       # 第二个分组: /api/users?page=1
    status = match.group(3)     # 第三个分组: 200

    print(f"方法: {method}, 路径: {path}, 状态: {status}")
```

`group(0)` 或 `group()` 返回整个匹配的字符串，`group(1)`、`group(2)`... 返回对应分组的内容。

你还可以给分组起名字，让代码更易读：

```python
# 命名分组 (?P<name>...)
pattern = r"(?P<method>\w+) (?P<path>/\S+) (?P<status>\d{3})"
match = re.search(pattern, log_line)

if match:
    print(match.group("method"))   # 输出: GET
    print(match.group("path"))     # 输出: /api/users?page=1

    # 还可以拿到字典形式的结果
    print(match.groupdict())
    # 输出: {'method': 'GET', 'path': '/api/users?page=1', 'status': '200'}
```

### 实战：完整的日志分析器

现在你可以写一个功能完整的日志分析器了。为了清晰，我们把它拆成两部分：先写解析函数提取信息，再写统计函数汇总数据。

**第一步：从日志行中提取结构化信息**

```python
import re

def parse_log_entry(line):
    """从单行日志中提取 IP、方法、路径、状态码

    返回字典，如果解析失败返回 None
    """
    # 正则分解：
    # (\d{1,3}\.){3}\d{1,3}  -> IP 地址（简化版，匹配四段数字）
    # .*?                   -> 任意字符（非贪婪，尽量少匹配）
    # (\w+)                 -> HTTP 方法（GET/POST 等）
    # (/\S+)                -> 路径（以 / 开头，非空白字符）
    # (\d{3})               -> 状态码（三位数字）
    pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\w+) (/\S+) (\d{3})"

    match = re.search(pattern, line)
    if match:
        ip, method, path, status = match.groups()
        return {
            "ip": ip,
            "method": method,
            "path": path,
            "status": status
        }
    return None


# 测试解析函数
log = "192.168.1.1 - GET /api/users 200"
result = parse_log_entry(log)
print(result)
# 输出: {'ip': '192.168.1.1', 'method': 'GET', 'path': '/api/users', 'status': '200'}
```

**第二步：统计每个 IP 的访问情况**

```python
from collections import defaultdict

def analyze_logs(log_lines):
    """分析日志，统计每个 IP 的访问次数和错误数"""
    # 用 defaultdict 简化计数逻辑
    # 每个 IP 对应一个字典，记录总请求数和错误数
    ip_counter = defaultdict(lambda: {"total": 0, "errors": 0})

    for line in log_lines:
        entry = parse_log_entry(line)
        if entry:
            ip = entry["ip"]
            status = entry["status"]

            # 增加总请求数
            ip_counter[ip]["total"] += 1

            # 4xx 和 5xx 状态码算错误
            if status.startswith("4") or status.startswith("5"):
                ip_counter[ip]["errors"] += 1

    return ip_counter


# 测试完整流程
logs = [
    "192.168.1.1 - GET /api/users 200",
    "192.168.1.2 - POST /api/login 200",
    "192.168.1.1 - GET /api/products 404",
    "192.168.1.1 - DELETE /api/users/123 403",
    "192.168.1.3 - GET /api/admin 500"
]

stats = analyze_logs(logs)
for ip, data in stats.items():
    print(f"{ip}: 总请求 {data['total']}, 错误 {data['errors']}")
```

输出：

```
192.168.1.1: 总请求 3, 错误 2
192.168.1.2: 总请求 1, 错误 0
192.168.1.3: 总请求 1, 错误 1
```

这里用到了 `defaultdict`（Week 04 的内容）——当你访问一个不存在的键时，它会自动创建默认值。这让计数代码更简洁，不用每次都写 `if ip not in counter:`。

同时，这段代码也展示了 Week 04 学的**遍历模式**：用 `for ip, data in stats.items()` 遍历字典的键值对。这种遍历方式在处理结构化数据时非常常见——左边是键（IP 地址），右边是值（统计数据字典）。还记得 Week 04 我们是怎么说的吗？"数据驱动设计"——让数据结构决定程序结构。

正则表达式负责从混乱的日志中提取结构化数据，解析函数负责把文本变成字典，统计函数负责汇总分析——三层分工，各司其职。

### 替换文本：re.sub()

除了查找，正则还能替换。`re.sub()` 把所有匹配的内容替换成指定字符串：

```python
# 把日志里的 IP 地址脱敏（隐藏）
log_line = "用户 192.168.1.1 访问了 /api/users"
masked = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "***.***.***.***", log_line)
print(masked)  # 输出: 用户 ***.***.***.*** 访问了 /api/users
```

`sub()` 也支持用函数动态决定替换内容：

```python
def mask_ip(match):
    ip = match.group()
    parts = ip.split(".")
    return f"***.***.{parts[2]}.{parts[3]}"  # 只保留后两段

masked = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", mask_ip, log_line)
print(masked)  # 输出: 用户 ***.***.1.1 访问了 /api/users
```

正则表达式的强大在于它的表达能力——用短短几行模式描述，就能完成复杂的文本处理任务。但它的缺点也很明显：难写、难读、容易出错。老潘分享了一个经验：

"我有一次写了个正则来验证邮箱，结果把合法的邮箱拒了，把非法的放进来了。后来学乖了——要么用成熟的库（比如 `email-validator`），要么写简单的正则做初步过滤，再用代码做详细校验。"

"正则不是万能的，"他说，"但在'从混乱中提取秩序'这件事上，它是最好的工具之一。"

---

> **AI 时代小专栏：用 AI 生成和调试正则表达式**
>
> 写正则表达式是个技术活。模式稍微复杂一点，人脑就很难一次性写对。这时候，AI 可以当你的助手。
>
> 市面上已经有专门的工具：**RegEx Generator**（https://regex.murfasa.com）使用 OpenAI ChatGPT API，能把自然语言描述转换成正则表达式。你只需要说"匹配中国大陆手机号"，它就能生成 `^1[3-9]\d{9}$`。
>
> **AI Regex Builder**（https://ai-reg.vercel.app）则提供了预设选项——邮箱、URL、IP 地址等常见模式一键生成。这类工具适合快速原型，但生产环境使用前需要验证。
>
> 在主流 AI 助手中，Claude（Sonnet 4.5/Opus 4.5）在正则调试和复杂模式方面表现优异，部分得益于其 200K+ 的上下文窗口——你可以把大量日志样本贴给它，让它分析模式并生成对应的正则。
>
> 但使用 AI 生成正则有三个原则：
>
> 1. **信任但验证**：永远在 regex101.com 上用真实数据测试 AI 生成的正则。AI 可能会漏掉边界情况（比如邮箱里的 '+' 号）。
> 2. **理解再使用**：不要直接复制。让 AI 解释每一部分的作用，确保你理解后再用。
> 3. **简单优先**：如果 `split()` 能搞定，就别用正则。AI 有时会过度设计。
>
> 调试工具推荐：**Regex101**（支持逐步调试）、**Debuggex**（可视化 DFA 图）、**RegExr**（鼠标悬停解释）。把 AI 生成的正则贴到这些工具里，你能看到它每一步是怎么匹配的。
>
> 记住，AI 是助手，不是替代者。当你能读懂 AI 生成的正则，并判断它是否正确时，你才真正掌握了这个工具。
>
> 参考（访问日期：2026-02-09）：
> - https://regex.murfasa.com
> - https://ai-reg.vercel.app
> - https://regex101.com
> - https://www.freecodecamp.org/news/use-chatgpt-to-build-a-regex-generator/

---

## 5. 文本处理的边界与陷阱

学会了字符串方法和正则表达式，你已经能处理大多数文本任务了。但真实世界的数据是 messy 的——编码不一致、格式错乱、包含意外字符。这一节我们来谈谈防御性编程：如何让你的文本处理代码 robust。

小北的日志分析器在处理一个文件时崩溃了。

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb0 in position 1234
```

"这是什么鬼？"她盯着报错信息，一脸茫然。

老潘过来看了一眼："编码问题。你的日志文件不是 UTF-8 编码的，可能是 GBK 或者 Latin-1。"

### 编码：文本处理的隐形炸弹

计算机存储的是二进制数字，文本需要被"编码"成字节才能存储。不同的编码方式用不同的规则把字符映射到字节。UTF-8 是目前最常用的编码，但它不是唯一的。

当 Python 用错误的编码打开文件时，就会抛出 `UnicodeDecodeError`：

```python
# 假设文件实际是 GBK 编码，但用 UTF-8 打开
with open("server.log", "r", encoding="utf-8") as f:
    content = f.read()  # 可能抛出 UnicodeDecodeError
```

解决办法是显式指定编码，或者让 Python 自动处理错误：

```python
# 方法 1：尝试不同编码
encodings = ["utf-8", "gbk", "latin-1"]
for enc in encodings:
    try:
        with open("server.log", "r", encoding=enc) as f:
            content = f.read()
        print(f"成功用 {enc} 编码读取")
        break
    except UnicodeDecodeError:
        continue

# 方法 2：忽略或替换无法解码的字符
with open("server.log", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()  # 跳过无法解码的字符

with open("server.log", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()  # 用 � 替换无法解码的字符
```

`errors="ignore"` 和 `errors="replace"` 是处理"脏数据"的常用策略。前者直接丢弃问题字符，后者用占位符标记问题位置。

### 空字符串和空白字符

另一个常见陷阱是空字符串和空白字符的处理：

```python
# 陷阱 1：空字符串
"".split(",")           # 输出: [''] —— 不是空列表！
"a,b,".split(",")       # 输出: ['a', 'b', ''] —— 末尾有空字符串

# 陷阱 2：split() 的默认行为 vs 指定分隔符
"   a   b   ".split()    # 输出: ['a', 'b'] —— 自动去空白，合并连续空格
"   a   b   ".split(" ")  # 输出: ['', '', '', 'a', '', '', 'b', '', '', ''] —— 意外！

# 陷阱 3：各种空白字符
"hello\n".strip()       # 去掉换行符
"hello\t".strip()       # 去掉制表符
"hello ".strip()        # 去掉空格
"hello\r\n".strip()     # 去掉 Windows 换行符
```

注意陷阱 2：`split()` 不传参数时会自动处理各种空白（空格、制表符、换行），并合并连续的空白。但 `split(" ")` 指定了空格作为分隔符后，它就"较真"了——每个空格都分割，包括开头和连续的空格，结果产生一堆空字符串。这是初学者最常踩的坑之一。小北就曾经困惑过："明明都是 split，为什么结果完全不一样？"

处理文件时，空行是另一个常见问题：

```python
def safe_parse_logs(file_path):
    """安全地解析日志文件，处理各种边界情况"""
    results = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # 跳过空行
                if not line:
                    continue

                # 跳过注释行（假设以 # 开头）
                if line.startswith("#"):
                    continue

                # 解析逻辑
                parsed = parse_log_line(line)
                if parsed:
                    results.append(parsed)
                else:
                    print(f"警告: 第 {line_num} 行格式不正确，已跳过")

    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 不存在")
    except Exception as e:
        print(f"错误: 读取文件时发生异常 - {e}")

    return results
```

这个函数展示了防御性编程的几个要点：
1. 用 `strip()` 去除首尾空白
2. 显式检查空行和注释行
3. 对解析失败的情况做优雅处理（打印警告，不中断程序）
4. 用 try/except 捕获各种异常（Week 06 的内容）

### 正则表达式的贪婪陷阱

正则表达式默认是"贪婪"的——它会尽可能多地匹配。这常常导致出人意料的结果：

```python
import re

html = "<div>内容1</div><div>内容2</div>"

# 贪婪匹配：.* 会尽可能多匹配
pattern = r"<div>.*</div>"
match = re.search(pattern, html)
print(match.group())  # 输出: <div>内容1</div><div>内容2</div>
```

等等——你可能预期只匹配到第一个 `</div>`，但结果却把整个字符串都吞了！这就是贪婪的"陷阱"：`*` 和 `+` 会尽可能多地吃掉字符，直到最后一个能满足模式的位置。

再看一个更反直觉的例子：

```python
# 你想提取引号里的内容
text = '她说"你好"，然后我说"再见"'
pattern = r'".*"'
match = re.search(pattern, text)
print(match.group())  # 输出: "你好"，然后我说"再见"
# 而不是你预期的: "你好"
```

正则把第一个 `"` 和最后一个 `"` 之间的所有内容都匹配了——包括中间那句"然后我说"。

解决办法是用**非贪婪匹配**：在量词后面加个 `?`，让它"见好就收"：

```python
# 非贪婪匹配：.*? 尽可能少匹配
pattern = r"<div>.*?</div>"
match = re.search(pattern, html)
print(match.group())  # 输出: <div>内容1</div>

# 引号例子也用非贪婪
pattern = r'".*?"'
match = re.search(pattern, text)
print(match.group())  # 输出: "你好"
```

`.*?`、`+?`、`{n,m}?` 是非贪婪版本，它们在能匹配的前提下，尽可能少地消耗字符。处理 HTML 或嵌套结构时，非贪婪匹配往往更符合预期。

小北看到这里恍然大悟："原来 `?` 在正则里有两种完全不同的意思——在 `\w?` 里表示'出现 0 次或 1 次'，在 `.*?` 里表示'非贪婪'！"

"没错，"老潘说，"这正是正则表达式让人头疼的地方——同样的符号在不同上下文有不同含义。但记住这个贪婪 vs 非贪婪的区别，能帮你避免 80% 的正则意外。"

### 老潘的实战经验

老潘看着小北的代码，分享了一个故事：

"我年轻时处理过一个日志系统，当时没考虑编码问题。有一天，一个用户的文件名包含日文，整个系统崩了。更惨的是，崩溃发生在凌晨，没有值班人员，等我们发现时，积压了几十万条日志没处理。

"从那以后，我处理任何文本都遵循三条原则：

1. **显式指定编码**：永远不写 `open(filename)`，而是 `open(filename, encoding='utf-8')`。
2. **不信任输入**：用户给的任何文本都可能为空、包含特殊字符、或者格式不对。做校验，做兜底。
3. **测试边界情况**：空字符串、超长字符串、特殊字符、不同编码——这些都要在测试里覆盖（Week 08 学的 pytest 派上用场了）。"

小北点点头，把这几条记在了笔记本上。

文本处理的边界情况就像冰山——你看到的只是水面上的那一小部分。但只要你养成"防御性编程"的思维，就能避免大部分陷阱。记住：程序要能处理"不正常"的输入，而不只是"理想情况"。

---

## PyHelper 进度

上周你给 PyHelper 加上了测试铠甲。这周，让它拥有"搜索记忆"的能力。

小北的需求很实在：笔记越记越多，需要能快速找到想要的内容。我们用本周学的文本处理来实现三个功能：

```python
# pyhelper/text_utils.py
import re
from datetime import datetime


def search_notes(notes, keyword):
    """按关键词搜索笔记内容

    Args:
        notes: 笔记列表，每个笔记是字典，包含 'content' 和 'date'
        keyword: 搜索关键词

    Returns:
        匹配的笔记列表
    """
    if not keyword or not keyword.strip():
        return []

    keyword = keyword.lower().strip()
    results = []

    for note in notes:
        content = note.get("content", "").lower()
        if keyword in content:
            results.append(note)

    return results


def filter_by_date(notes, start_date=None, end_date=None):
    """按日期范围过滤笔记

    Args:
        notes: 笔记列表
        start_date: 开始日期，格式 'YYYY-MM-DD'
        end_date: 结束日期，格式 'YYYY-MM-DD'
    """
    results = []

    for note in notes:
        note_date = note.get("date", "")

        # 解析笔记日期
        try:
            note_dt = datetime.strptime(note_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            continue  # 跳过日期格式不对的笔记

        # 检查是否在范围内
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            if note_dt < start_dt:
                continue

        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            if note_dt > end_dt:
                continue

        results.append(note)

    return results


def extract_tags(content):
    """从笔记内容中提取 #标签

    标签格式：#单词（可以包含中文、字母、数字、下划线）
    例如：#Python #学习笔记 #week_09
    """
    if not content:
        return []

    # 正则匹配 #开头的标签
    # \w 匹配字母数字下划线，\u4e00-\u9fff 匹配中文字符
    pattern = r"#([\w\u4e00-\u9fff]+)"
    tags = re.findall(pattern, content)

    return tags


def format_note_summary(note):
    """格式化笔记摘要，用于列表显示"""
    date = note.get("date", "未知日期")
    content = note.get("content", "")

    # 截取前 50 个字符作为摘要
    summary = content[:50] + "..." if len(content) > 50 else content

    # 提取标签
    tags = extract_tags(content)
    tag_str = " ".join([f"#{t}" for t in tags]) if tags else ""

    return f"[{date}] {summary} {tag_str}"
```

这三个函数展示了本周知识的综合运用：

1. **`search_notes`**：用字符串的 `lower()` 和 `in` 操作实现大小写不敏感的搜索。注意边界检查——如果关键词是空字符串，直接返回空列表。

2. **`filter_by_date`**：结合字符串解析（`strptime`）和条件过滤。用 try/except 处理日期格式错误，这是 Week 06 学的异常处理。

3. **`extract_tags`**：用正则表达式提取 `#标签`。这里的正则是 `[\w\u4e00-\u9fff]+`，匹配字母数字下划线以及中文字符，让 `#Python` 和 `#学习` 都能被正确识别。

现在你可以在 `main.py` 里添加搜索菜单了：

```python
def search_menu(notes):
    """搜索功能菜单"""
    print("\n=== 搜索笔记 ===")
    print("1. 按关键词搜索")
    print("2. 按日期范围过滤")
    print("3. 查看所有标签")

    choice = input("请选择: ").strip()

    if choice == "1":
        keyword = input("输入关键词: ")
        results = search_notes(notes, keyword)
        print(f"\n找到 {len(results)} 条笔记:")
        for note in results:
            print(format_note_summary(note))

    elif choice == "2":
        start = input("开始日期 (YYYY-MM-DD，留空不限制): ").strip()
        end = input("结束日期 (YYYY-MM-DD，留空不限制): ").strip()
        results = filter_by_date(notes, start or None, end or None)
        print(f"\n找到 {len(results)} 条笔记:")
        for note in results:
            print(format_note_summary(note))

    elif choice == "3":
        all_tags = []
        for note in notes:
            all_tags.extend(extract_tags(note.get("content", "")))
        unique_tags = sorted(set(all_tags))
        print(f"\n所有标签: {', '.join(['#' + t for t in unique_tags])}")
```

PyHelper 现在不仅能记录学习笔记，还能帮你从海量笔记中找到想要的内容。这就是文本处理的力量——从混乱中提取秩序。

**如何把这些功能整合进 PyHelper？**

如果你跟着本书一路写过来，你的 PyHelper 应该已经有这些文件了：

```
pyhelper/
├── __init__.py
├── main.py          # 主菜单和交互逻辑
├── storage.py       # 文件读写（JSON 格式）
├── records.py       # 笔记的增删改查
└── text_utils.py    # 本周新增：文本处理工具
```

第一步，把上面的 `text_utils.py` 保存到 `pyhelper/` 目录。第二步，在 `main.py` 里导入这些函数：

```python
from text_utils import search_notes, filter_by_date, extract_tags, format_note_summary
```

第三步，把 `search_menu()` 函数添加到 `main.py`，然后在主菜单里加一个选项：

```python
def main():
    notes = load_notes()  # 从 storage.py 加载

    while True:
        print("\n=== PyHelper 学习助手 ===")
        print("1. 添加笔记")
        print("2. 查看所有笔记")
        print("3. 搜索笔记")      # 新增
        print("4. 退出")

        choice = input("请选择: ").strip()

        if choice == "1":
            # ... 添加笔记逻辑
        elif choice == "2":
            # ... 查看笔记逻辑
        elif choice == "3":
            search_menu(notes)   # 调用本周新增的搜索菜单
        elif choice == "4":
            break
```

现在运行 `python -m pyhelper.main`，选择 "3" 就能体验搜索功能了。试试搜索 "Python" 或按日期范围过滤，看看你的学习记录。

---

## Git 本周要点

本周必会命令：
- `git status` —— 查看当前状态
- `git diff` —— 查看具体修改内容
- `git add -A` —— 添加所有修改
- `git commit -m "message"` —— 提交修改
- `git log --oneline -n 10` —— 查看最近 10 次提交

常见坑：
- **编码问题提交**：处理文本文件时注意编码一致性，建议统一使用 UTF-8
- **换行符问题**：Windows (CRLF) 和 Unix (LF) 换行符混用会导致 diff 混乱，建议配置 `.gitattributes`
- **大文本文件**：日志文件、数据文件不要提交到 Git，用 `.gitignore` 排除

文本处理相关 `.gitignore` 模板：
```
*.log
*.csv
data/
*.txt
!requirements.txt
```

Pull Request (PR)：
- 本周延续 PR 流程：分支 → 多次提交 → push → PR → review → merge
- PR 描述模板：
  ```markdown
  ## 本周做了什么
  - 学习了 Python 字符串方法（strip/split/join/find/replace）
  - 掌握了正则表达式基础和 re 模块使用
  - 完成了 Log Analyzer 贯穿案例
  - 为 PyHelper 添加了搜索和过滤功能

  ## 自测
  - [ ] 运行 `python3 -m pytest chapters/week_09/tests -q` 通过
  - [ ] Log Analyzer 能正确解析示例日志
  - [ ] PyHelper 搜索功能正常工作

  ## 待 review
  请重点检查正则表达式的边界情况处理
  ```

---

## 本周小结（供下周参考）

本周你学会了 Python 的文本处理能力——从基础的字符串方法（strip、split、join、find）到强大的正则表达式。你掌握了用 `re` 模块进行模式匹配和分组提取，也学会了识别文本处理中的边界情况（空字符串、特殊字符、编码问题）。现在你的 Log Analyzer 可以从混乱的日志中提取结构化信息，PyHelper 也拥有了搜索和过滤学习笔记的能力。

下周我们将进入 Week 10：数据序列化——学习 JSON 和 YAML 格式，让你的程序能够与现代 API 和数据文件无缝交互，支持数据的导入导出。

---

## Definition of Done（学生自测清单）

完成本周学习后，请确认你能做到以下事情：

**核心技能**：你能熟练使用字符串方法处理文本（strip 清洗、split/join 拆分重组、find/replace 查找替换）；能编写基本的正则表达式进行模式匹配；能使用 `re.search()`、`re.findall()` 和分组提取信息；能识别并处理文本处理中的边界情况。

**编程哲学**：你理解**文本处理**在编程中的核心地位——从日志分析到数据清洗，从用户输入验证到信息提取。你知道字符串方法和正则表达式各自的优势和适用场景（简单操作用字符串方法，复杂模式用正则）。

**实践能力**：你能编写函数解析结构化文本；能为常见模式（邮箱、IP、日期）编写正则表达式；能处理"脏数据"中的异常情况；能为 PyHelper 添加实用的搜索过滤功能。

**工程习惯**：你至少提交了 2 次 Git（draft + verify），并且运行 `python3 -m pytest chapters/week_09/tests -q` 通过了所有测试。

---

**如果你想验证自己的掌握程度**，试着回答这些问题：

- `split()` 和 `partition()` 有什么区别？什么时候用哪个？
- 正则表达式中的 `.`、`*`、`+`、`?` 分别匹配什么？
- `re.search()` 和 `re.match()` 的区别是什么？
- 为什么正则表达式字符串前面要加 `r`（如 `r"\d+"`）？
- 处理用户输入的文本时，应该考虑哪些边界情况？

如果你能自信地回答这些问题，说明你已经掌握了本周的核心内容。

---

<!--
章节结构骨架（供 chapter-writer 参考）：

1. 章首导入（引言格言 + 时代脉搏）——已完成
2. 前情提要——已完成
3. 学习目标——已完成
4. 贯穿案例设计说明（HTML 注释）——已完成
5. 认知负荷 + 回顾桥 + 角色出场规划（HTML 注释）——已完成
6. AI 小专栏规划（HTML 注释）——已完成
7. 第 1 节：字符串不只是文字——已完成
8. 第 2 节：拆分与重组——已完成
9. AI 小专栏 #1——已完成（放在第 2 节之后）
10. 第 3 节：当字符串方法不够用——已完成
11. 第 4 节：re 模块实战——已完成
12. AI 小专栏 #2——已完成（放在第 4 节之后）
13. 第 5 节：文本处理的边界与陷阱——已完成
14. PyHelper 进度——已完成
15. Git 本周要点——已完成
16. 本周小结（供下周参考）——已完成
17. Definition of Done——已完成
-->
