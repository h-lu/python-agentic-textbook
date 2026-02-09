# Week 10：数据交换的艺术——JSON 与序列化

> "Data is the new oil, but unlike oil, data is not scarce. It's abundant, and its value comes from how we refine and exchange it."
> — Clive Humby

2025 年，全球活跃着超过 2 亿个 API，预计到 2030 年将增长到 17 亿个。根据 Postman 的《2025 State of the API Report》，REST API 以 93% 的采用率稳居主导地位，而 JSON 作为 REST API 的默认数据格式，已成为现代软件世界的通用语言。更值得注意的是，Gartner 预测到 2026 年，AI 和大语言模型将驱动 API 使用量增长 30%——从 OpenAI 的 API 到 Claude 的函数调用，从微服务架构到云原生应用，JSON 是这一切的基石。

但 JSON 不仅仅是一种格式——它代表了一种思维方式：**结构化数据的可移植性**。当你的 PyHelper 学习记录能以 JSON 格式存储时，它就不再局限于一个程序——你可以把数据导入到其他工具中分析，可以分享给朋友，甚至可以作为训练数据喂给 AI。本周，你将学会如何让数据"流动"起来。

---

## 前情提要

上周你给 PyHelper 添加了搜索和过滤功能——用字符串方法查找关键词，用正则表达式提取标签，按日期范围过滤笔记。小北很满意，现在找笔记方便多了。

但阿码提出了一个新问题："如果我想把学习记录备份到云端，或者导入到 Excel 里分析怎么办？"

"现在的数据格式是自定义的文本格式，"老潘说，"不容易被其他工具识别。你需要一种通用的数据交换格式。"

"JSON？"小北想起之前见过这个词。

"对，JSON 是现代软件世界的通用语言。这周你们将学习如何用 JSON 格式存储数据，以及如何导入导出——让你的学习记录真正'流动'起来。"

---

## 学习目标

完成本周学习后，你将能够：
1. 理解 JSON 格式的结构和用途，能读写 JSON 文件
2. 掌握 Python 的 `json` 模块（`load`、`dump`、`loads`、`dumps`）
3. 理解序列化与反序列化的概念，能处理自定义数据类型
4. 设计支持导入导出的数据接口，实现数据迁移
5. 为 PyHelper 添加 JSON 格式存储和导入导出功能

---

<!--
贯穿案例设计：个人书单管理器（Book Tracker）
- 第 1 节：为什么需要 JSON → 从自定义文本格式的问题开始，引出 JSON 的价值
- 第 2 节：JSON 基础与读写 → 用 json 模块读写书单数据
- 第 3 节：序列化与反序列化 → 处理复杂数据结构（嵌套字典、列表）
- 第 4 节：导入导出功能 → 实现从 CSV/其他格式导入，导出为 JSON
- 第 5 节：数据验证与错误处理 → 处理损坏的 JSON、格式不兼容等问题
- 最终成果：一个能导入导出 JSON 格式书单数据的 Book Tracker，支持与其他工具交换数据

案例演进路线：
1. 自定义格式存储 → 2. 改用 JSON 格式 → 3. 处理嵌套数据结构 → 4. 实现导入导出 → 5. 完整的数据交换工具
-->

<!--
认知负荷预算：
- 本周新概念（5 个，预算上限 5 个）：
  1. JSON 格式语法（对象、数组、键值对）
  2. json 模块（load/dump/loads/dumps）
  3. 序列化（Serialization）与反序列化（Deserialization）
  4. 数据契约/Schema（数据结构的约定）
  5. 数据迁移（导入导出的设计思路）
- 结论：✅ 在预算内

回顾桥设计（至少 2 个，目标引用前 3 周的概念）：
- [文件读写]（来自 week_05）：在第 2 节，用 with open() 配合 json.load/dump 读写文件
- [异常处理]（来自 week_06）：在第 5 节，用 try/except 处理 JSONDecodeError 等解析错误
- [模块化]（来自 week_07）：贯穿案例中，数据读写逻辑封装为独立模块
- [pytest]（来自 week_08）：为 JSON 解析函数编写测试，验证边界情况
- [字符串处理]（来自 week_09）：在导入导出时处理文本编码、格式转换

角色出场规划：
- 小北（第 1 节）：尝试手动解析自定义格式时出错，引出 JSON 的必要性
- 阿码（第 3 节）：追问"为什么不用 pickle？"引出不同序列化方案的对比
- 老潘（第 5 节）：分享工作中数据迁移的实战经验，强调数据验证的重要性
- 小北（第 4 节）：在实现导入功能时遇到编码问题，引出编码处理
- 阿码（第 2 节）：质疑"JSON 和 Python 字典看起来一样，有什么区别？"
- 老潘（第 2 节）：解释 JSON 的跨语言特性，强调通用格式的价值

AI 小专栏规划：
- AI 小专栏 #1（放在第 2 节之后）：
  - 主题：AI 工具如何辅助处理 JSON 数据——从代码生成到数据验证
  - 连接点：与第 2 节"JSON 基础与读写"呼应，讨论 AI 时代 JSON 处理工具的发展
  - 建议搜索词："AI JSON processing tools 2026", "LLM structured data extraction 2026"

- AI 小专栏 #2（放在第 4 节之后）：
  - 主题：API 数据交互与 AI 应用——JSON 在 AI 工作流中的核心地位
  - 连接点：与第 4 节"导入导出功能"呼应，讨论现代 API 如何使用 JSON 交换数据
  - 建议搜索词："OpenAI API JSON format 2026", "REST API JSON usage statistics 2026"

PyHelper 本周推进：
- 上周状态：PyHelper 已支持搜索和过滤功能，数据存储为自定义文本格式
- 本周改进：
  1. 数据文件从自定义文本格式升级为 JSON 格式
  2. 添加 export_notes(format) 函数 - 支持导出为 JSON/CSV
  3. 添加 import_notes(file_path) 函数 - 支持从 JSON 文件导入
  4. 添加数据版本兼容性处理（处理旧格式数据迁移）
- 涉及的本周概念：JSON 序列化、数据契约、导入导出设计、异常处理（JSONDecodeError）
- 建议示例文件：examples/pyhelper/storage_json.py（重构 storage 模块）
-->

## 1. 当自定义格式成为枷锁

小北想把自己在 PyHelper 里的学习记录分享给阿码。她打开数据文件，里面是这样的：

```
2026-02-01|学习了 JSON 格式，原来它是 JavaScript 的对象表示法
2026-02-02|练习了 json.dumps 和 json.loads，dumps 是把对象变成字符串
2026-02-03|阿码问我：JSON 和字典有什么区别？
```

"简单明了，"小北想，"每行一条记录，用竖线分隔日期和内容。"

她写了个函数来读取这个文件：

```python
def load_notes_old_format(filepath):
    """读取旧格式的学习记录"""
    notes = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 2:
                notes.append({
                    "date": parts[0],
                    "content": parts[1]
                })
    return notes
```

这代码用了 `with open()` 和 **with 语句**自动管理文件关闭，用 **for 循环**遍历每一行，`split("|")` 按竖线拆分——这些都是你熟悉的工具。看起来没问题，直到阿码收到了一条包含竖线的笔记：

```
2026-02-04|学习了 split 方法，它按分隔符拆分字符串，比如 "a|b|c".split("|")
```

小北的解析器傻眼了。`split("|")` 会把这行拆成 4 个部分，而不是 2 个。她的代码以为 `len(parts) == 2`，直接跳过了这条记录。

"等等，这条笔记怎么没导进来？"阿码问。

小北检查了半天才发现问题。她试着修复："那我改用更特殊的分隔符，比如 `|||`？"

"如果笔记内容里也有 `|||` 呢？"阿码反问。

"那……我转义一下？把内容里的 `|` 换成 `\|`？"

"那你得写转义和解转义的代码。而且如果笔记里本来就有 `\|` 呢？"

小北沉默了。她意识到自己在走一条不归路——**自定义格式就像打地鼠，解决一个 edge case，冒出两个新的**。数据本身在变化，而她的格式却僵化地假设数据"应该长什么样"——这正是数据驱动设计的反面。

更麻烦的是，阿码想把这些记录导入到 Excel 里分析。Excel 不认识小北的"竖线分隔格式"，它认识的是 CSV、JSON 这些**标准格式**。

"我是不是在重复造轮子？"小北问老潘。

老潘点点头："自定义格式适合临时脚本，但一旦涉及数据交换——给别人用、给别的程序用、甚至给三个月后的你自己用——你就需要一种**通用的、有标准库支持的、被广泛认可**的格式。"

"JSON？"

"JSON。"

---

## 2. JSON——数据的通用语言

小北第一次看 JSON 文件时，有种似曾相识的感觉：

```json
{
    "date": "2026-02-01",
    "content": "学习了 JSON 格式",
    "tags": ["Python", "JSON", "学习笔记"],
    "rating": 5
}
```

"这不就是 Python 字典吗？"她心想。大括号、键值对、冒号分隔——简直一模一样。

阿码也发现了这一点："JSON 和字典看起来一样，有什么区别？"

老潘正好路过："好问题。它们看起来像，但本质不同。"

### JSON 是文本，字典是内存对象

**JSON**（JavaScript Object Notation）是一种**文本格式**——它本质上是字符串，遵循特定的语法规则。你可以用任何文本编辑器打开 JSON 文件，可以把它复制粘贴到聊天窗口，可以把它存进数据库的文本字段。

**Python 字典**是**内存中的数据结构**——它只在程序运行时存在，有特定的方法（如 `.keys()`、`.get()`），不能被直接"传输"到其他程序。

把字典变成 JSON 字符串，这个过程叫**序列化**（serialization）。把 JSON 字符串变回字典，叫**反序列化**（deserialization）。

Python 标准库提供了 `json` 模块来处理这一切：

```python
import json

# Python 字典
note = {
    "date": "2026-02-01",
    "content": "学习了 JSON 格式",
    "tags": ["Python", "JSON"],
    "rating": 5
}

# 序列化：字典 → JSON 字符串
json_str = json.dumps(note)
print(json_str)
# 输出: {"date": "2026-02-01", "content": "学习了 JSON 格式", "tags": ["Python", "JSON"], "rating": 5}

print(type(json_str))  # <class 'str'> —— 是字符串！
```

注意 `json.dumps()` 返回的是**字符串**，不是字典。现在你可以把这个字符串写入文件、发送到网络、或者存进数据库。

### JSON 的跨语言特性

"那为什么不用 Python 自己的格式？"阿码追问，"比如直接把字典用 `str()` 转成字符串？"

老潘笑了："你听说过世界语（Esperanto）吗？"

小北和阿码摇摇头。

"世界语是人工创造的语言，专门为了让不同国家的人能交流。它不属于任何一个国家，但所有人都学它。"老潘接着说，"JSON 就是编程世界语——它不属于 Python，不属于 JavaScript，不属于任何语言。它是一种'中立'的数据格式，让所有程序都能对话。"

阿码眼睛一亮："所以 Python 写的程序、JavaScript 写的网页、R 语言做数据分析——它们都用 JSON 交流？"

"对。你的 Python 程序把数据存成 JSON，你朋友的 JavaScript 网页能直接读。公司的数据团队用 R 处理这个 JSON，手机 App 用 Swift 也能解析。JSON 让数据不再被任何语言'绑架'。"

小北若有所思："所以学 JSON 不是学 Python 特性，是学整个软件世界的通用格式？"

"正是。学会它，你就掌握了与任何系统交换数据的钥匙。"

### JSON 语法速查

JSON 的语法和 Python 字典很像，但有几点关键区别：

| 特性 | Python 字典 | JSON |
|------|------------|------|
| 键 | 可以是任何不可变类型（数字、元组等） | 必须是**双引号字符串** |
| 字符串 | 单引号或双引号都行 | 必须是**双引号** |
| 布尔值 | `True`, `False` | `true`, `false`（小写） |
| 空值 | `None` | `null` |
| 尾随逗号 | 允许 | 不允许 |

小北试着写一个合法的 JSON：

```json
{
    "title": "Python 学习笔记",
    "count": 42,
    "active": true,
    "tags": ["编程", "Python", "学习"],
    "metadata": {
        "author": "小北",
        "version": 1.0
    }
}
```

注意：
- 所有键都用双引号包裹
- 字符串用双引号，不能用单引号
- `true` 和 `false` 是小写
- 最后一个元素后面不能有逗号（尾随逗号）

如果你试图用 Python 的 `json` 模块解析一个格式错误的 JSON，它会报错：

```python
import json

# 错误的 JSON：用了单引号
bad_json = "{'key': 'value'}"

try:
    data = json.loads(bad_json)
except json.JSONDecodeError as e:
    print(f"解析失败: {e}")
    # 输出: 解析失败: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

这就是 JSON 的"严格"之处——它不像 Python 那么宽容，但正是这种严格保证了跨语言的一致性。

现在小北可以把学习记录存成 JSON 格式了：

```python
import json

notes = [
    {"date": "2026-02-01", "content": "学习了 JSON", "rating": 5},
    {"date": "2026-02-02", "content": "练习了序列化", "rating": 4}
]

# 写入 JSON 文件
with open("notes.json", "w", encoding="utf-8") as f:
    json.dump(notes, f)
```

注意这里用的是 `json.dump()`（没有 s），它直接把数据写入文件对象。与之对应的 `json.load()` 从文件读取 JSON：

```python
# 从 JSON 文件读取
with open("notes.json", "r", encoding="utf-8") as f:
    loaded_notes = json.load(f)

print(loaded_notes)
# [{'date': '2026-02-01', 'content': '学习了 JSON', 'rating': 5}, ...]
```

小北松了口气。再也不用自己处理分隔符、转义、edge case 了——`json` 模块帮她搞定了一切。

---

> **AI 时代小专栏：AI 工具如何辅助处理 JSON 数据**
>
> 2026 年，AI 工具正在重塑 JSON 数据的处理方式。从结构化数据提取到 Schema 验证，AI 的能力已经超越了简单的代码生成。
>
> **LLM 的结构化输出能力**：OpenAI 的 GPT-4 在 Structured Outputs 模式下对 JSON Schema 的合规性达到了 **100%**。相比之下，LLM 对 JSON 的解析准确率（98-100%）显著高于 YAML（89-94%）。这意味着在 AI 工作流中，JSON 正成为首选的数据交换格式。
>
> **AI 驱动的数据提取工具**：
> - **Firecrawl**：开发者优先的结构化数据平台，能将任意网站转换为 LLM-ready 的 JSON/Markdown 格式
> - **Oxylabs AI Studio**：低代码 AI 数据提取工具，支持用自然语言描述数据需求，自动输出结构化 JSON
> - **Monkt**：文档到结构化数据转换器，支持批量处理和图像理解，适合处理复杂文档
>
> **实际应用场景**：你可以让 AI 从一段非结构化的课程描述中提取出 `{"course_name": "...", "time": "...", "instructor": "..."}` 这样的 JSON，直接用于程序处理。这种能力正在改变数据录入、文档处理和 API 开发的工作流。
>
> 但记住，AI 生成的 JSON 处理代码仍然需要你的审查。理解 `json.dumps()` 和 `json.loads()` 的底层行为，才能在 AI 辅助下保持清醒。基础工具永远不会过时——它们是你评估 AI 输出的基准。
>
> 参考（访问日期：2026-02-09）：
> - [LLMs for Structured Data: The Workforce Shift in 2026](https://www.ruh.ai/blogs/llms-for-structured-data-workforce-shift-2026)
> - [Slashdot - AI Tools for JSON](https://slashdot.org/software/ai-tools/for-json/)

---

## 3. 序列化——让对象"可传输"

学会了 JSON 的基础读写，小北开始处理更复杂的数据。她的书单数据越来越丰富——一本书不仅有标题和作者，还有阅读笔记、标签、评分——而且笔记本身是一个列表：

```python
book = {
    "title": "Python 编程：从入门到实践",
    "author": "Eric Matthes",
    "rating": 5,
    "tags": ["Python", "编程入门", "实践"],
    "notes": [
        {"date": "2026-02-01", "content": "第 1 章介绍了变量和字符串"},
        {"date": "2026-02-03", "content": "第 3 章的函数部分很有启发"}
    ],
    "finished": False
}
```

"这种嵌套结构能存成 JSON 吗？"小北有点担心。

"试试就知道了，"阿码说。

```python
import json

# 嵌套字典 + 列表，照样能序列化
json_str = json.dumps(book)
print(json_str)
```

输出：

```json
{"title": "Python 编程：从入门到实践", "author": "Eric Matthes", "rating": 5, "tags": ["Python", "编程入门", "实践"], "notes": [{"date": "2026-02-01", "content": "第 1 章介绍了变量和字符串"}, {"date": "2026-02-03", "content": "第 3 章的函数部分很有启发"}], "finished": false}
```

完美。JSON 天生支持嵌套结构——对象里可以有数组，数组里可以有对象，想套多深套多深。

但小北注意到一个问题：输出全部挤在一行，太难读了。

### 美化输出

`json.dumps()` 有个 `indent` 参数，可以让输出格式化：

```python
# indent=2 表示用 2 个空格缩进
pretty_json = json.dumps(book, indent=2, ensure_ascii=False)
print(pretty_json)
```

输出：

```json
{
  "title": "Python 编程：从入门到实践",
  "author": "Eric Matthes",
  "rating": 5,
  "tags": [
    "Python",
    "编程入门",
    "实践"
  ],
  "notes": [
    {
      "date": "2026-02-01",
      "content": "第 1 章介绍了变量和字符串"
    },
    {
      "date": "2026-02-03",
      "content": "第 3 章的函数部分很有启发"
    }
  ],
  "finished": false
}
```

`ensure_ascii=False` 是另一个常用参数——它让中文字符原样输出，而不是被转义成 `\uXXXX` 形式。

### 为什么不用 pickle？

阿码突然问："我查资料时看到有人说用 `pickle` 也能序列化，而且似乎更简单？"

老潘听到后走过来："`pickle` 确实能序列化 Python 对象，但它有几个致命问题。"

`pickle` 是 Python 特有的序列化格式，它能序列化几乎任何 Python 对象——包括自定义类的实例。但代价是：

1. **只支持 Python**：别的语言读不了 pickle 文件
2. **安全性问题**：加载不可信的 pickle 文件可能执行恶意代码
3. **版本兼容性**：Python 版本升级后，旧 pickle 文件可能读不了

"那什么时候用 pickle？"阿码问。

"临时缓存、进程间通信——只在 Python 内部用，且不涉及安全敏感场景时。"老潘说，"但凡涉及数据交换、长期存储、跨语言协作，JSON 是更安全的选择。"

小北点点头："所以 JSON 是'通用货币'，pickle 是'内部代金券'？"

"比喻得不错，"老潘笑了，"JSON 是黄金，pickle 是超市积分卡。"

### 序列化的边界

小北发现，并非所有东西都能序列化成 JSON：

```python
import datetime

book_with_date = {
    "title": "某本书",
    "added_date": datetime.date(2026, 2, 9)  # 日期对象
}

json.dumps(book_with_date)
# TypeError: Object of type date is not JSON serializable
```

报错很清晰：日期对象不是 JSON 可序列化的。JSON 标准只支持：

- 字符串（string）
- 数字（number）
- 布尔值（true/false）
- null
- 数组（array）
- 对象（object）

日期、自定义对象、集合（set）……这些都不在 JSON 标准里。

解决办法是**自定义序列化逻辑**：

```python
import json
import datetime

def serialize_book(obj):
    """自定义序列化函数"""
    if isinstance(obj, datetime.date):
        return obj.isoformat()  # 转成 "2026-02-09" 字符串
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

book_with_date = {
    "title": "某本书",
    "added_date": datetime.date(2026, 2, 9)
}

json_str = json.dumps(book_with_date, default=serialize_book)
print(json_str)
# 输出: {"title": "某本书", "added_date": "2026-02-09"}
```

`default` 参数接收一个函数，当 `json.dumps()` 遇到无法序列化的对象时，会调用这个函数。你的函数负责把对象转成 JSON 支持的基本类型。

反过来，反序列化时怎么把字符串 `"2026-02-09"` 变回日期对象？可以用 `object_hook`：

```python
def deserialize_book(dct):
    """自定义反序列化函数"""
    if "added_date" in dct:
        dct["added_date"] = datetime.date.fromisoformat(dct["added_date"])
    return dct

book = json.loads(json_str, object_hook=deserialize_book)
print(book["added_date"])  # 2026-02-09（日期对象，不是字符串）
```

这样，你就能在 JSON 的局限性和 Python 的灵活性之间找到平衡。

---

## 4. 数据的自由流动——导入与导出

序列化解决了"数据怎么存"的问题，但数据的价值在于流动。小北的书单管理器现在能存 JSON 了，但她想要更多："我想把豆瓣的书单导入进来，也想把我们的书单导出给别的程序用。"

这就是**数据导入导出**——让你的程序成为数据流动的枢纽，而不是孤岛。

### 设计导入导出接口

老潘建议："先设计接口，再写实现。导入导出是数据契约（data contract）——你和外部世界达成的协议。"

小北定义了两个函数：

```python
import json
from pathlib import Path

def export_books(books, filepath, format="json"):
    """导出书单到文件

    Args:
        books: 书单列表，每个元素是字典
        filepath: 输出文件路径
        format: 导出格式，支持 "json" 或 "csv"
    """
    filepath = Path(filepath)

    if format == "json":
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(books, f, indent=2, ensure_ascii=False)
    elif format == "csv":
        # CSV 导出（简化版，只导出基本字段）
        import csv
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            if books:
                writer = csv.DictWriter(f, fieldnames=["title", "author", "rating"])
                writer.writeheader()
                writer.writerows(books)
    else:
        raise ValueError(f"不支持的格式: {format}")

    print(f"已导出 {len(books)} 本书到 {filepath}")


def import_books(filepath):
    """从文件导入书单

    Args:
        filepath: JSON 文件路径

    Returns:
        书单列表
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        books = json.load(f)

    # 简单的数据验证
    if not isinstance(books, list):
        raise ValueError("JSON 根元素必须是数组")

    print(f"已导入 {len(books)} 本书")
    return books
```

注意 `export_books()` 的设计：用 `pathlib.Path` 处理路径（这样无论 Windows 还是 macOS 都能正确工作），用异常处理捕获文件不存在的情况，docstring 清晰地说明参数和返回值——这些都是你在前面几周逐渐养成的工程习惯。

### 处理编码问题

小北在测试导入功能时遇到了一个奇怪的问题：

```python
# 尝试导入一个从 Windows 系统生成的 JSON
books = import_books("books_from_windows.json")
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc0 in position 123
```

"又是编码问题，"小北叹了口气——她在 Week 09 处理日志时就遇到过这种报错，没想到又来了。

但这次她学聪明了：

```python
def import_books_robust(filepath):
    """更健壮的导入函数，自动处理编码"""
    filepath = Path(filepath)

    # 尝试多种编码
    encodings = ["utf-8", "utf-8-sig", "gbk", "latin-1"]

    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                content = f.read()
            print(f"成功用 {enc} 编码读取")
            break
        except UnicodeDecodeError:
            continue
    else:
        raise UnicodeDecodeError(f"无法解码文件，尝试了: {encodings}")

    # 解析 JSON
    books = json.loads(content)
    return books
```

`utf-8-sig` 是 Windows 记事本保存 UTF-8 时可能带上的 BOM（字节顺序标记）——这是她在 Week 09 处理文本文件时学到的技巧。

### 数据版本兼容性

阿码提出了一个更深的问题："如果我们的程序升级了，数据结构变了，旧版本保存的 JSON 还能读吗？"

这是个好问题。假设 v1 的书单长这样：

```json
{"title": "某本书", "author": "某人"}
```

v2 增加了 `rating` 字段：

```json
{"title": "某本书", "author": "某人", "rating": 5}
```

用 v2 的程序读 v1 的数据，会报错吗？

```python
book = {"title": "某本书", "author": "某人"}
print(book.get("rating", 0))  # 输出 0，不会报错
```

用 `.get()` 而不是 `[]` 访问字典键，是处理版本兼容性的常用技巧。`.get()` 在键不存在时返回默认值（或你指定的值），而不是抛出 `KeyError`。

更完善的方案是显式的**数据迁移**：

```python
def migrate_book_data(book, from_version=1):
    """将旧版本数据迁移到最新版本"""
    if from_version < 2:
        # v1 → v2：添加 rating 字段，默认为 0
        book.setdefault("rating", 0)

    if from_version < 3:
        # v2 → v3：添加 tags 字段，默认为空列表
        book.setdefault("tags", [])

    return book

# 在导入时调用
books = import_books("old_books.json")
books = [migrate_book_data(b, from_version=1) for b in books]
```

这就是**防御性数据编程**——不仅考虑"正常情况"，还要考虑"数据来自三个月前的旧版本"的情况。

---

> **AI 时代小专栏：API 数据交互与 AI 应用**
>
> JSON 是现代 API 的通用语言，而 API 是 AI 应用的基石。2026 年，JSON 在 AI 工作流中的地位愈发重要——OpenAI 的 ChatGPT 已拥有 **2.5 亿月活用户**，超过 **90% 的财富 500 强公司**集成了 OpenAI API，累计 API 调用量达 **1.2 万亿次**。
>
> **AI API 的 JSON 格式**：OpenAI、Claude、Gemini 等大模型 API 都使用 JSON 进行请求和响应。一个典型的 OpenAI API 响应结构如下：
> ```json
> {
>   "id": "chatcmpl-xxx",
>   "object": "chat.completion",
>   "created": 1683130927,
>   "model": "gpt-4",
>   "choices": [{
>     "index": 0,
>     "message": {
>       "role": "assistant",
>       "content": "Response text here"
>     },
>     "finish_reason": "stop"
>   }],
>   "usage": {
>     "prompt_tokens": 10,
>     "completion_tokens": 16,
>     "total_tokens": 26
>   }
> }
> ```
> 理解这种 JSON 结构，是调用任何 AI API 的前提。
>
> **Function Calling 与结构化输出**：现代 LLM 支持 "function calling"——模型可以输出结构化的 JSON，供你的程序解析执行。比如让模型分析一段文本，返回 `{"sentiment": "positive", "confidence": 0.95}` 这样的 JSON。这种能力正在改变人机交互的方式。
>
> **Azure OpenAI 的监控指标**：在生产环境中，API 的 JSON 响应还包含关键的性能指标，如 `ActiveTokens`（活跃令牌数）、`GeneratedTokens`（生成令牌数）等，用于监控和优化成本。
>
> 根据 Postman 2025 报告，89% 的开发者现在在日常工作中使用生成式 AI，而 71% 的互联网流量已经是 API 调用。掌握 JSON，就是掌握了与这个 AI 驱动世界对话的语法——你刚学的 `json.load()` 和 `json.dump()`，正是理解这些 API 响应的基础。
>
> 参考（访问日期：2026-02-09）：
> - [OpenAI Usage Statistics 2026](https://fueler.io/blog/openai-usage-revenue-valuation-growth-statistics)
> - [Azure OpenAI Monitoring Reference](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/monitor-openai-reference)
> - [OpenAI API Response Structure](https://www.swiftorial.com/tutorials/artificial_intelligence/openai_api/core_concepts/response_structure/)

---

## 5. 防御性数据编程

导入导出功能写好了，但小北想测试一下"如果 JSON 文件坏了会怎样"。

她故意创建一个损坏的 JSON 文件：

```json
[
  {"title": "书 1", "author": "作者 1"},
  {"title": "书 2", "author": "作者 2"
]
```

注意第二本书缺少右大括号。然后她运行导入：

```python
books = import_books("broken.json")
# json.JSONDecodeError: Expecting ',' delimiter: line 4 column 1 (char 67)
```

程序崩溃了。这在 Week 06 学过——需要**异常处理**。

### 捕获 JSONDecodeError

```python
import json
from pathlib import Path

def safe_import_books(filepath):
    """安全地导入书单，处理各种错误情况"""
    filepath = Path(filepath)

    # 检查文件是否存在
    if not filepath.exists():
        print(f"错误: 文件 {filepath} 不存在")
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            books = json.load(f)
    except json.JSONDecodeError as e:
        print(f"错误: JSON 格式不正确 - {e}")
        return []
    except UnicodeDecodeError as e:
        print(f"错误: 文件编码问题 - {e}")
        return []
    except Exception as e:
        print(f"错误: 未知错误 - {e}")
        return []

    # 验证数据结构
    if not isinstance(books, list):
        print("错误: JSON 根元素必须是数组")
        return []

    # 过滤掉无效的记录
    valid_books = []
    for i, book in enumerate(books):
        if not isinstance(book, dict):
            print(f"警告: 第 {i} 项不是字典，已跳过")
            continue
        if "title" not in book:
            print(f"警告: 第 {i} 项缺少 title 字段，已跳过")
            continue
        valid_books.append(book)

    print(f"成功导入 {len(valid_books)} 本书（共 {len(books)} 项）")
    return valid_books
```

这个函数展示了**防御性编程**的几个层次：

1. **前置检查**：文件是否存在？——这是 **输入校验**的第一步，在使用数据前先验证其合法性
2. **异常捕获**：用 try/except 捕获特定的 JSON 解析错误和 **异常类型**
3. **数据验证**：解析成功后，验证数据结构是否符合预期
4. **优雅降级**：遇到问题时返回空列表（或部分有效数据），而不是崩溃

这里用的是你在 Week 06 见过的 **EAFP 风格**（先尝试再道歉），而不是 **LBYL**（先看再跳）。与其在解析前检查一堆条件，不如直接尝试解析，失败了再捕获异常处理——这让代码更简洁，而且通常更快（因为只有出错时才有额外开销）。

### Schema 验证的概念

老潘看到小北的代码，点了点头："不错，但你这种验证是'硬编码'的。如果字段变多了，验证代码会很长。"

"那怎么办？"

"工程上常用 **Schema 验证**。Schema 是数据结构的'说明书'——你先定义好数据应该长什么样，然后用工具自动验证。"

Python 有 `jsonschema` 库可以做这件事（需要安装）：

```python
# 定义 Schema（数据契约）
book_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["title", "author"],
        "properties": {
            "title": {"type": "string"},
            "author": {"type": "string"},
            "rating": {"type": "integer", "minimum": 1, "maximum": 5}
        }
    }
}

# 验证数据（需要安装 jsonschema: pip install jsonschema）
from jsonschema import validate, ValidationError

try:
    validate(instance=books, schema=book_schema)
    print("数据验证通过")
except ValidationError as e:
    print(f"数据验证失败: {e.message}")
```

Schema 的好处是**声明式**——你把规则写成配置，而不是代码。这让验证逻辑更清晰，也更容易维护。

"在实际项目中，"老潘说，"我们通常在数据入口处做 Schema 验证——API 接收请求时、导入文件时。这样脏数据进不来，后面的代码就可以假设数据是干净的。"

### 老潘的数据迁移实战经验

老潘分享了一个故事，声音里带着一丝后怕：

"我刚工作时，接手过一个数据迁移任务。看起来很简单——把用户表从旧系统导出来，导入到新系统。我写了脚本，在测试环境跑了一遍，没问题。上线前我还沾沾自喜，觉得这任务太轻松了。"

"结果呢？"小北好奇地问。

"结果上线第一天，客服电话被打爆了。"老潘摇摇头，"第一个用户打进来的电话我现在还记得。他说：'我生日是 5 月 15 号，你们系统怎么显示我是 1970 年出生的？我今年才 25 岁！'"

"怎么回事？"小北倒吸一口凉气。

"旧系统里，生日字段有两种格式：一种是完整的 '1990-05-15'，另一种是 '05/15'（默认当年，因为系统主要面向年轻用户）。我的导入脚本没考虑到第二种情况，就把 '05/15' 当成无效日期，填了默认值 1970-01-01。"

阿码问："后来怎么解决的？"

"那个周末我加班了两天。写了一个更智能的解析器，处理各种可能的日期格式——'05/15'、'5-15'、'0515'……甚至还有用户手打成 '五月十五' 的。然后重新导入所有 15 万条用户数据，给受影响的 873 个用户发道歉邮件，每人送了一张 50 元的代金券。"

"成本不低啊。"阿码说。

"成本高的是公司的信誉。"老潘苦笑，"从那以后，我做数据迁移的第一步就是分析真实数据——采样一千条记录，统计格式分布，找 edge case，而不是假设数据'应该长什么样'。"

他顿了顿，眼神变得严肃："**永远不要信任外部数据**。无论它来自文件、API 还是数据库，都有可能出乎你的意料。验证、验证、再验证。这不是多余的工作，这是保命的工作。"

---

## PyHelper 进度

上周你给 PyHelper 加上了搜索和过滤功能。这周，让它的数据真正"流动"起来。

### 从自定义格式升级到 JSON

PyHelper 原来的数据文件是自定义文本格式，这周升级为 JSON。好处是显而易见的——数据可以被其他工具读取，也可以手动编辑。

```python
# pyhelper/storage.py
import json
from pathlib import Path

DATA_FILE = Path.home() / ".pyhelper" / "notes.json"


def save_notes(notes):
    """保存笔记到 JSON 文件"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


def load_notes():
    """从 JSON 文件加载笔记"""
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            notes = json.load(f)

        # 简单的数据验证
        if not isinstance(notes, list):
            print("警告: 数据文件格式不正确，已重置")
            return []

        return notes

    except json.JSONDecodeError:
        print("错误: 数据文件损坏，已重置")
        return []
    except Exception as e:
        print(f"错误: 读取数据失败 - {e}")
        return []
```

注意这里的**防御性编程**：文件不存在时返回空列表，JSON 解析失败时返回空列表而不是崩溃。这样即使数据文件出了问题，PyHelper 也能继续运行，而不是一启动就报错——这是异常处理在实际项目中的典型应用。

### 添加导入导出功能

现在 PyHelper 可以导出笔记供备份或分析，也可以从文件导入：

```python
def export_notes(filepath, format="json"):
    """导出笔记到文件

    Args:
        filepath: 输出文件路径
        format: 导出格式，支持 "json" 或 "txt"
    """
    notes = load_notes()
    filepath = Path(filepath)

    if format == "json":
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(notes, f, indent=2, ensure_ascii=False)
    elif format == "txt":
        # 导出为易读的文本格式
        with open(filepath, "w", encoding="utf-8") as f:
            for note in notes:
                f.write(f"日期: {note.get('date', '未知')}\n")
                f.write(f"内容: {note.get('content', '')}\n")
                f.write("-" * 40 + "\n")
    else:
        raise ValueError(f"不支持的格式: {format}")

    print(f"已导出 {len(notes)} 条笔记到 {filepath}")


def import_notes(filepath):
    """从 JSON 文件导入笔记

    如果笔记已存在（相同日期和内容），则跳过
    """
    filepath = Path(filepath)

    if not filepath.exists():
        print(f"错误: 文件不存在 - {filepath}")
        return 0

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            new_notes = json.load(f)

        if not isinstance(new_notes, list):
            print("错误: 文件格式不正确")
            return 0

        existing_notes = load_notes()
        existing_keys = {
            (n.get("date"), n.get("content")) for n in existing_notes
        }

        added = 0
        for note in new_notes:
            key = (note.get("date"), note.get("content"))
            if key not in existing_keys:
                existing_notes.append(note)
                existing_keys.add(key)
                added += 1

        save_notes(existing_notes)
        print(f"成功导入 {added} 条新笔记（跳过 {len(new_notes) - added} 条重复）")
        return added

    except json.JSONDecodeError as e:
        print(f"错误: JSON 格式不正确 - {e}")
        return 0
    except Exception as e:
        print(f"错误: 导入失败 - {e}")
        return 0
```

导入功能做了**去重处理**——如果笔记已存在（相同日期和内容），则跳过。这在合并多个设备的数据时特别有用。

### 数据版本兼容性处理

小北问："如果 PyHelper 未来升级了数据结构，需要处理旧版本的数据怎么办？比如现在添加了标签功能，旧数据没有 tags 字段？"

这是个好问题。数据版本升级是所有长期维护的程序都会遇到的问题。

**场景：从 v1 升级到 v2**

假设 v1 的笔记只有日期和内容：

```python
# 旧版本数据（v1）存储在 notes.json
[
    {"date": "2026-02-01", "content": "学习了 JSON"},
    {"date": "2026-02-02", "content": "练习了 json.dumps"}
]
```

v2 版本添加了标签和创建时间：

```python
# 新版本数据（v2）的理想格式
{
    "date": "2026-02-01",
    "content": "学习了 JSON",
    "tags": ["Python", "JSON"],
    "created_at": "2026-02-01T10:30:00"
}
```

如果不做迁移，直接用 v2 的代码读取 v1 的数据，会出现什么情况？

```python
# v2 的代码尝试访问 tags
for note in load_notes():
    print(note["tags"])  # KeyError: 'tags'
```

程序崩溃了。**数据迁移函数**负责填补这个差距：

```python
def migrate_note(note, target_version=2):
    """将旧版本笔记迁移到最新版本

    Args:
        note: 笔记字典
        target_version: 目标版本号

    Returns:
        迁移后的笔记
    """
    # v1 → v2: 添加 tags 字段
    if "tags" not in note:
        note["tags"] = []  # 空列表，用户后续可以添加

    # v1 → v2: 添加 created_at 字段
    if "created_at" not in note:
        # 用日期字段作为后备，或者设为当前时间
        note["created_at"] = note.get("date", "")

    return note


def load_notes_with_migration():
    """加载笔记，自动迁移旧版本数据"""
    notes = load_notes()

    # 迁移所有笔记
    migrated = [migrate_note(n.copy()) for n in notes]  # 用 .copy() 避免修改原数据

    # 如果有任何笔记被迁移了，自动保存新版本
    if any(n != m for n, m in zip(notes, migrated)):
        save_notes(migrated)
        print(f"已自动迁移 {len(migrated)} 条笔记到最新版本")

    return migrated
```

注意这里用了 `n.copy()`——**不要直接修改原始数据**，而是创建副本后再修改。这样可以在迁移出错时保留原始数据，方便调试。

小北试了一下：她手动创建了一个 v1 格式的 notes.json，然后运行 `load_notes_with_migration()`。程序自动检测到旧格式数据，添加了 `tags` 和 `created_at` 字段，并保存了新版本。第二次运行时，因为数据已经是最新版本，就没有重复迁移。

"这就对了，"老潘说，"数据迁移应该对用户透明——他们不需要知道背后发生了什么，只需要打开程序，数据就在那里，而且是最新格式的。"

现在 PyHelper 的数据可以：
- 用 JSON 格式存储，方便手动编辑
- 导出为 JSON 或文本格式，方便备份和分享
- 从 JSON 文件导入，支持去重
- 自动处理版本升级

这就是**数据的可移植性**——你的学习记录不再被锁定在某个程序里，它可以流动、可以被分享、可以被其他工具处理。

---

## Git 本周要点

本周必会命令：
- `git status` —— 查看当前状态
- `git diff` —— 查看具体修改内容
- `git add -A` —— 添加所有修改
- `git commit -m "message"` —— 提交修改
- `git log --oneline -n 10` —— 查看最近 10 次提交

常见坑：
- **JSON 文件换行**：Windows (CRLF) 和 Unix (LF) 换行符可能导致 JSON 解析差异
- **编码问题**：JSON 标准推荐 UTF-8，但处理外部数据时要考虑其他编码
- **大 JSON 文件**：数据文件不要提交到 Git，用 `.gitignore` 排除
- **数据文件版本冲突**：多人协作时数据文件容易产生冲突，建议用 `.gitignore` 排除

数据相关 `.gitignore` 模板：
```
*.json
*.csv
*.log
data/
!example_data.json  # 保留示例数据
```

Pull Request (PR)：
- 本周延续 PR 流程：分支 → 多次提交 → push → PR → review → merge
- PR 描述模板：
  ```markdown
  ## 本周做了什么
  - 学习了 JSON 格式和 Python json 模块
  - 理解了序列化与反序列化的概念
  - 实现了 Book Tracker 的导入导出功能
  - 为 PyHelper 添加了 JSON 格式存储和数据迁移功能

  ## 自测
  - [ ] 运行 `python3 -m pytest chapters/week_10/tests -q` 通过
  - [ ] Book Tracker 能正确导入导出 JSON
  - [ ] PyHelper 数据迁移功能正常工作

  ## 待 review
  请重点检查 JSON 异常处理和数据验证逻辑
  ```

---

## 本周小结（供下周参考）

本周你完成了从"自给自足"到"互联互通"的跃迁——学会了让数据在程序之间自由流动。你掌握了 JSON 这种通用数据格式，理解了序列化与反序列化的本质（内存对象 ↔ 文本字符串），能够设计支持导入导出的数据接口。更重要的是，你学会了防御性数据编程——如何处理损坏的数据、格式不兼容、编码问题等边界情况。

还记得 Week 05 你第一次把数据写入文件时，用的是自定义的竖线分隔格式吗？那时的数据只能被你自己的程序读取。现在，你的 Book Tracker 可以导出 JSON 给 Excel 分析，PyHelper 的学习记录可以备份到云端并在其他设备恢复——数据不再是孤岛，而是可以流动、可以分享、可以被其他工具处理的资产。

下周我们将进入 Week 11：数据建模——学习用 dataclass 定义清晰的数据结构，为更复杂的应用打下基础。JSON 让你"能存储"数据，dataclass 将帮你"更好地组织"数据。

---

## Definition of Done（学生自测清单）

完成本周学习后，请确认你能做到以下事情：

**核心技能**：你能理解 JSON 格式的结构（对象、数组、键值对），能用 `json.load()` 和 `json.dump()` 读写 JSON 文件；能用 `json.loads()` 和 `json.dumps()` 处理字符串形式的 JSON 数据；能处理嵌套的 JSON 数据结构（字典套列表、列表套字典）。

**编程哲学**：你理解**序列化**（serialization）的价值——让内存中的数据结构可以保存到文件、传输到网络、被其他程序读取。你知道 JSON 为什么是"通用语言"（跨平台、跨语言、人类可读），以及什么时候该用 JSON、什么时候该用其他格式。

**实践能力**：你能设计支持导入导出的数据接口；能处理 JSON 解析中的常见错误（`JSONDecodeError`、编码问题、格式不兼容）；能为 PyHelper 实现 JSON 格式存储和数据迁移功能。

**工程习惯**：你至少提交了 2 次 Git（draft + verify），并且运行 `python3 -m pytest chapters/week_10/tests -q` 通过了所有测试。

---

**如果你想验证自己的掌握程度**，试着回答这些问题：

- JSON 和 Python 字典有什么相似之处？有什么区别？
- `json.load()` 和 `json.loads()` 有什么区别？什么时候用哪个？
- 什么是序列化？什么是反序列化？为什么需要它们？
- 如果 JSON 文件损坏了（比如缺少一个右括号），你的程序应该怎么处理？
- 设计一个数据导入功能时，应该考虑哪些边界情况？

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
7. 第 1 节：当自定义格式成为枷锁——已完成
8. 第 2 节：JSON——数据的通用语言——已完成
9. AI 小专栏 #1——已完成（放在第 2 节之后，已用研究缓存数据增强）
10. 第 3 节：序列化——让对象"可传输"——已完成
11. 第 4 节：数据的自由流动——导入与导出——已完成
12. AI 小专栏 #2——已完成（放在第 4 节之后，已用研究缓存数据增强）
13. 第 5 节：防御性数据编程——已完成
14. PyHelper 进度——已完成
15. Git 本周要点——已完成
16. 本周小结（供下周参考）——已完成
17. Definition of Done——已完成
-->
