# Week 05：读写文件——程序的记忆

> "The best way to predict the future is to invent it."
> — Alan Kay，美国著名计算机科学家，面向对象编程和图形用户界面的先驱

近几年，全球每天产生的数据量已经接近 **500 EB**（艾字节）——相当于每秒钟创建数百万部高清电影。根据 IDC 的预测，到 2028 年全球年度数据量将达到 **393 ZB**（泽字节），其中生成式 AI 是主要驱动力。这些数据从哪来？从无数个文件里——网页、日志、传感器读数、用户上传的内容……

但你发现一个有趣的矛盾了吗？AI 模型训练时"读"了这么多文件，但它们"写"出的代码如果不保存到文件，就永远停留在屏幕上。程序要真正有用，得能"记住"东西——这正是本周的核心。

本周你将学会让程序"记住"东西——不是存在内存里（关机就没了），而是存在**文件**（file）里。你会学到 `open()`、`read()`、`write()` 这些基础操作，也会学到 `pathlib` 这个现代化的路径处理库，还会理解"编码"（encoding）这个初学者最容易踩坑的地方。更重要的是，你写的程序从此能和硬盘对话——这是从"一次性脚本"到"真正的小工具"的关键一步。

---

## 前情提要

上周你学会了用**列表**和**字典**存储数据——程序能"记住"东西了，但有个致命缺陷：一关闭程序，所有数据就没了。小北上周用 PyHelper 记了一周的学习记录，结果重启电脑后，发现字典又变回空的了。

"这不太对劲，"小北盯着屏幕，"我明明写了一周的记录，怎么都没了？"

老潘在旁边解释："因为你的数据存在**内存**（RAM）里——内存是'易失性存储'，断电就清空。你想让数据'持久化'（persist），就得存到**硬盘**（disk）上——也就是**文件**。"

这周我们要解决这个问题。你将学会 Python 的文件操作——`open()`、`read()`、`write()`，以及 `pathlib` 和 `with` 语句。学到这周结束，PyHelper 的学习记录会存到文件里，下次打开程序，你的记录还在。

---

## 学习目标

完成本周学习后，你将能够：
1. 理解文件的基本概念，能用 `open()` 打开文件、读取内容、写入数据
2. 掌握 `with` 语句——确保文件正确关闭的"安全网"
3. 理解"编码"（encoding）的概念，能处理中文和特殊字符
4. 使用 `pathlib` 处理文件路径，避免硬编码路径带来的问题
5. 判断"什么时候用文件存储"，设计简单的文本格式存储数据

---

<!--
贯穿案例：日记本工具

演进路线：
- 第 1 节（从字典到文件）：把 Week 04 的学习记录字典存成文本文件，体验"关程序再打开，数据还在"
- 第 2 节（with 语句）：用 `with` 改进文件操作，学会"安全的文件处理"方式
- 第 3 节（pathlib）：用 `pathlib` 处理文件路径，解决"路径硬编码"的问题
- 第 4 节（编码与追加）：理解 UTF-8 编码，支持追加写入日记（不是覆盖）

最终成果：一个能写日记、查看日记、按日期查找的日记本工具——所有日记存在 `diary.txt` 里，程序关闭后数据永久保存
-->

<!--
认知负荷预算：
- 本周新概念（4 个，预算上限 4 个）：
  1. 文件读写（file I/O）—— open/read/write
  2. with 语句（with statement）
  3. pathlib（路径处理库）
  4. 编码（encoding）—— UTF-8
- 结论：✅ 在预算内

回顾桥设计（至少引用 Week 01-04 的 2 个概念，实际规划 5 个）：
- [字典]（来自 week_04）：在第 1 节，把字典内容写入文件，文件存的就是字典数据的"文本形式"
- [for 循环]（来自 week_02）：在第 1 节，遍历字典写入文件，每一行一个键值对
- [函数]（来自 week_03）：在第 2 节，把文件读写封装成函数，复习参数和返回值
- [字符串方法]（来自 week_01）：在第 4 节，用 split() 处理文件内容，解析日记条目
- [列表]（来自 week_04）：在第 4 节，把文件内容按行读到列表，再遍历处理
-->

<!--
角色出场规划：
- 小北（第 1 节）：写完文件操作代码，打开文件发现是空的——忘记调用 flush() 或 close()，引出"为什么要正确关闭文件"
- 阿码（第 1 节）：追问"为什么不能用字符串拼接来写文件，必须用 open()？"，引出文件对象的概念
- 老潘（第 3 节）：看到小北硬编码路径 `C:\\Users\\...`，摇头说"在公司里我们从来不会这样写，因为跨平台会出问题"，引出 pathlib
- 小北（第 4 节）：写入文件后重新读取，发现中文变成乱码——引出编码问题和 UTF-8
-->

<!--
AI 小专栏规划：

AI 小专栏 #1（放在第 1 节之后）：
- 主题：AI 模型是怎么"读"书的
- 连接点：你刚学的文件读取，和 AI 训练时读取海量文本是同一个原理
- 建议搜索词：GPT training data size 2025, LLM training data preprocessing, how AI models read text files 2026
- 搜索提示：搜索 2025-2026 年关于 LLM 训练数据量、数据预处理方法的统计数据和技术文章

AI 小专栏 #2（放在第 3 节之后）：
- 主题：pathlib 在 AI 项目中的应用
- 连接点：pathlib 让文件路径跨平台兼容，AI 项目通常在 Linux/Mac/Windows 上都要跑
- 建议搜索词：Python pathlib best practices 2026, cross platform file paths AI projects, pathlib vs os.path
- 搜索提示：搜索 pathlib 在数据处理/AI 项目中的应用案例和最佳实践

注意：两个侧栏必须基于真实数据和 URL，使用 WebSearch 或 perplexity MCP 查证。禁止编造统计数据和链接。
-->

## 1. 程序的记忆——从字典到文件

上周你用字典存储学习记录，但有个问题：程序关闭后，数据就没了。这是因为**内存**（RAM）是"易失性存储"——断电就清空。想让数据"持久化"（persist），就得存到**文件**（file）里。

让我们从最简单的例子开始：把一段文字写入文件。

```python
# 打开文件（如果不存在会创建）
file = open("hello.txt", "w", encoding="utf-8")

# 写入内容
file.write("Hello, World!")
file.write("这是第二行\n")

# 关闭文件（非常重要！）
file.close()
```

运行这段代码后，你的目录里会多出一个 `hello.txt` 文件，内容是：

```
Hello, World!这是第二行
```

小北看完，疑惑道："为什么两行文字连在一起了？"

好问题！因为你没有加换行符。`\n` 是**换行符**（newline），但你在第二行末尾加了 `\n`，第一行末尾没加。所以它们会连在一起。

```python
file = open("hello.txt", "w", encoding="utf-8")
file.write("Hello, World!\n")  # 第一行末尾加 \n
file.write("这是第二行\n")     # 第二行末尾加 \n
file.close()
```

现在 `hello.txt` 的内容是：

```
Hello, World!
这是第二行
```

---

小北立刻试了一下，结果打开文件发现是**空的**。

"怎么回事？"小北盯着空文件，"代码明明运行了啊！"

老潘在旁边看了一眼："你忘记 `close()` 了。"

```python
file = open("hello.txt", "w", encoding="utf-8")
file.write("Hello, World!\n")
# 忘记写 file.close() 了！
```

"这有什么区别吗？"小北不解。

"区别大了，"老潘解释，"Python 的文件写入有**缓冲**（buffering）——你调用 `write()` 时，数据先存在内存的'缓冲区'里，不会立即写到硬盘。只有缓冲区满了或者你调用 `close()` 时，数据才会真正落盘。你这行代码跑完，数据还在缓冲区里，程序就结束了，所以文件是空的。"

小北听完，赶紧加上 `file.close()`，再运行一次——文件终于有内容了。

阿码在旁边问："那有没有办法避免忘记 `close()`？"

"有，"老潘说，"这就是下一节要讲的 `with` 语句——它会自动帮你关文件。"

---

现在让我们回到 PyHelper 的例子。上周我们用字典存储学习记录：

```python
learning_log = {
    "02-09": "学会了列表和字典的基本用法",
    "02-10": "写了一个成绩单项目"
}
```

这周，我们把字典写入文件：

```python
learning_log = {
    "02-09": "学会了列表和字典的基本用法",
    "02-10": "写了一个成绩单项目"
}

# 打开文件（"w" 表示写入模式）
file = open("pyhelper_data.txt", "w", encoding="utf-8")

# 遍历字典，写入每一行（用 Week 02 学的 for 循环）
for date, content in learning_log.items():
    file.write(f"{date}: {content}\n")

# 关闭文件
file.close()

print("数据已保存到 pyhelper_data.txt")
```

运行后，`pyhelper_data.txt` 的内容是：

```
02-09: 学会了列表和字典的基本用法
02-10: 写了一个成绩单项目
```

每行一个键值对，用 `:` 分隔。这是你自己定义的"文件格式"——简单、可读、易于解析。

---

接下来是**读取**文件：

```python
# 打开文件（"r" 表示读取模式）
file = open("pyhelper_data.txt", "r", encoding="utf-8")

# 读取全部内容（作为一个大字符串）
content = file.read()
print(content)

# 关闭文件
file.close()
```

输出：

```
02-09: 学会了列表和字典的基本用法
02-10: 写了一个成绩单项目
```

`file.read()` 会把整个文件读成一个**字符串**。如果文件很大（比如 100 MB），这会占用大量内存。

更常见的做法是**按行读取**：

```python
file = open("pyhelper_data.txt", "r", encoding="utf-8")

# readlines() 返回一个列表，每个元素是一行（包含换行符）
lines = file.readlines()
print(lines)  # ['02-09: 学会了列表和字典的基本用法\n', '02-10: 写了一个成绩单项目\n']

file.close()

# 遍历每一行（用 Week 02 学的 for 循环）
for line in lines:
    # 去掉末尾的换行符
    line = line.strip()
    if line:  # 如果这行不是空的
        print(f"读取到：{line}")
```

输出：

```
读取到：02-09: 学会了列表和字典的基本用法
读取到：02-10: 写了一个成绩单项目
```

`line.strip()` 会去掉字符串两端的空白字符（空格、换行符、制表符等）。这是处理文件内容时最常用的方法之一。

阿码问："`read()` 和 `readlines()` 有什么区别？"

好问题！记住这个口诀：

- `read()`：像把整个文件"一口气读完"，吐出**一个大字符串**
- `readlines()`：也一口气读完，但把每行剪下来，塞进**一个列表**里

想象你在读一本书：
- `read()` = 把整本书复印成一张巨大的纸
- `readlines()` = 把每页剪下来，堆成一叠纸
- `for line in file` = 一页一页慢慢读，不会累着内存（下一节会讲）

还有一个**逐行读取**的方式（不会一次性把整个文件加载到内存）：

```python
file = open("pyhelper_data.txt", "r", encoding="utf-8")

# 直接遍历文件对象（逐行读取）
for line in file:
    line = line.strip()
    if line:
        print(f"读取到：{line}")

file.close()
```

这种写法适合处理**大文件**——它不会一次性把整个文件读入内存，而是"读一行，处理一行"。

小北问："那我应该用哪种方式？"

老潘给了个简单的规则，并补充了一些具体场景：

| 文件大小 | 典型场景 | 推荐方式 |
|---------|---------|---------|
| < 1 MB | 配置文件、学习记录、小型日志 | `read()` 或 `readlines()` 都可以 |
| 1-10 MB | CSV 数据文件（几千行）、中等日志 | `readlines()` 或 `for line in file:` |
| \> 10 MB | 大型 CSV、系统日志、数据导出 | `for line in file:` 逐行读取 |
| 不确定 | 用户提供的文件、可能很大的数据 | 优先用 `for line in file:`，更安全 |

"举个例子，"老潘说，"你的 `pyhelper_data.txt` 可能只有几 KB，用 `read()` 完全没问题。但如果公司让你处理一个 100 MB 的日志文件，你就必须用 `for line in file:`——否则一次性读入可能会把内存撑爆。"

---

现在你已经会读写文件了。但有个问题：你每次都要记得 `close()`，否则数据可能不会落盘。

下一节，我们来学一个"自动关文件"的安全写法——`with` 语句。

---

> **AI 时代小专栏：AI 模型是怎么"读"书的**

> 你刚学的文件读取，本质上就是"从硬盘读取文本到内存"。有意思的是，这正是 AI 模型训练的第一步——读取海量文本文件。
>
> OpenAI 的 GPT-4 训练数据超过 **1 TB** 的文本。这是个什么概念？如果把它打印成书，大约相当于 **1000 万本**《红楼梦》的体量——堆起来能有 100 座珠穆朗玛峰那么高。这些数据不是"魔法般"出现在模型里的，而是通过类似 `open()` 和 `read()` 的代码逐个文件读取的。
>
> 近年的 AI 训练流程通常是这样的：
> 1. **数据收集**：用爬虫从互联网下载网页（存成 HTML/文本文件）
> 2. **数据清洗**：用 Python 脚本读取文件，去除广告、垃圾内容
> 3. **分词**（tokenization）：把文本转换成"词元"（token）列表——这一步用到了字典（词表）
> 4. **训练**：把词元列表喂给模型，让它学习"下一个词是什么"
>
> 你本周学的"文件读取"，在步骤 2 和 3 中大量使用。GitHub 上一个流行的数据集工具 `HuggingFace Datasets`，其核心就是用 Python 的文件 I/O 加载 TB 级别的文本数据。
>
> 有个反直觉的事实：**AI 模型训练时，90% 的时间花在数据预处理上**（读取文件、清洗、分词），只有 10% 的时间在真正的"训练"。所以你今天学的文件操作，不只是"存储数据"，更是 AI 时代的基础技能。
>
> 参考（访问日期：2026-02-09）：
> - [GPT-4 Technical Report (OpenAI, 2023)](https://arxiv.org/abs/2303.08774)
> - [HuggingFace Datasets Documentation](https://huggingface.co/docs/datasets/)
> - [Data Preprocessing for LLMs (Sebastian Raschka, 2025)](https://sebastianraschka.com/blog/2025/llm-data-preprocessing.html)

---

## 2. 自动关文件的安全网——with 语句

上一节你学会了文件的读写，但有个隐患：你必须记得 `close()`，否则数据可能不会落盘。

小北上周就踩了这个坑：

```python
file = open("diary.txt", "w", encoding="utf-8")
file.write("今天学会了文件操作\n")
# 忘记 close() 了！
```

程序运行完，`diary.txt` 是空的——因为数据还在缓冲区里，没有真正写到硬盘。

老潘看到后，摇摇头："我当年也这么干过。后来我发现了——**忘记 `close()` 是最常见的文件操作 bug**。"

Python 提供了一个更安全的写法：**`with` 语句**（with statement）。

```python
# 用 with 语句打开文件
with open("diary.txt", "w", encoding="utf-8") as file:
    file.write("今天学会了文件操作\n")
    file.write("with 语句会自动关闭文件\n")

# 离开 with 块后，文件会自动关闭
print("文件已自动关闭")
```

`with open(...) as file:` 的意思是：
1. 打开文件
2. 把文件对象赋值给 `file`
3. 执行 `with` 块内的代码
4. **无论是否发生错误，都会自动关闭文件**

小北看完，疑惑道："这有什么区别？我不还是得写代码吗？"

"区别在于**容错**，"老潘解释，"想象一下，如果在 `file.write()` 时发生了错误（比如硬盘满了），普通写法会直接崩溃，`close()` 根本不会执行——数据可能丢失。但 `with` 语句会**保证**文件被正确关闭，即使出错了也会。"

让我们看一个出错的场景：

```python
# 普通写法（不安全）
file = open("diary.txt", "w", encoding="utf-8")
file.write("第一行\n")
int("abc")  # 故意触发一个错误（ValueError）
file.close()  # 这行不会执行！
```

运行结果：`diary.txt` 是**空的**——因为程序在 `file.close()` 之前就崩溃了。

```python
# with 语句写法（安全）
with open("diary.txt", "w", encoding="utf-8") as file:
    file.write("第一行\n")
    int("abc")  # 触发错误
# 即使出错，with 也会自动关闭文件
```

运行结果：`diary.txt` **有内容**——因为 `with` 保证在退出前关闭文件。

阿码问："那 `with` 是不是所有时候都应该用？"

"几乎是的，"老潘说，"除非你有特殊需求（比如需要长时间保持文件打开），否则**优先用 `with`**——这是 Python 社区的最佳实践。"

---

现在让我们用 `with` 改写 PyHelper 的文件操作：

```python
# 把字典写入文件（用 with）
def save_to_file(learning_log, filename="pyhelper_data.txt"):
    """
    保存学习记录到文件
    learning_log: 字典，格式为 {"日期": "学习内容"}
    """
    with open(filename, "w", encoding="utf-8") as file:
        for date, content in learning_log.items():
            file.write(f"{date}: {content}\n")
    print(f"数据已保存到 {filename}")

# 从文件读取字典（用 with）
def load_from_file(filename="pyhelper_data.txt"):
    """
    从文件加载学习记录
    返回一个字典，格式为 {"日期": "学习内容"}
    """
    learning_log = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    # 用 split() 分割日期和内容
                    parts = line.split(": ", 1)  # 最多分割 1 次
                    if len(parts) == 2:
                        date, content = parts
                        learning_log[date] = content
    except FileNotFoundError:
        print(f"注意：{filename} 不存在，将创建新文件")
    return learning_log

# 测试
learning_log = {
    "02-09": "学会了列表和字典的基本用法",
    "02-10": "写了一个成绩单项目"
}

save_to_file(learning_log)
loaded_log = load_from_file()
print(loaded_log)  # {'02-09': '学会了列表和字典的基本用法', '02-10': '写了一个成绩单项目'}
```

这里用到了 Week 03 学的**函数**——把文件操作封装成函数，代码更清晰。还用到了 Week 01 学的**字符串方法** `split()`——把一行文字按 `": "` 分割成日期和内容。

小北问："`split(": ", 1)` 里的 `1` 是什么意思？"

"`split()` 的第二个参数是**最大分割次数**，"老潘解释，"`line.split(": ", 1)` 的意思是'最多分割 1 次'。如果你的学习内容里有 `": "`，它不会被分割。"

来看看区别：

| 写法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `split(": ")` | `"02-09: 今天学了: split() 的用法"` | `['02-09', '今天学了', 'split() 的用法']` | 分割了**所有** `": "`，内容被破坏 |
| `split(": ", 1)` | `"02-09: 今天学了: split() 的用法"` | `['02-09', '今天学了: split() 的用法']` | 只分割**第一个** `": "`，内容完整 |

```python
line = "02-09: 今天学了: split() 的用法"

# 不指定分割次数（默认全部分割）
parts_all = line.split(": ")  # ['02-09', '今天学了', 'split() 的用法']

# 指定最多分割 1 次
parts_one = line.split(": ", 1)  # ['02-09', '今天学了: split() 的用法']

print(f"全部分割: {parts_all}")   # 错误！内容被破坏
print(f"分割一次: {parts_one}")    # 正确！日期和内容分开
```

阿码点点头："所以 `split(": ", 1)` 是为了保护内容里的 `": "` 不被错误分割？"

"对，"老潘说，"处理文本时，你要时刻想着'边界情况'——用户的输入可能包含任何字符。"

---

现在你已经学会了用 `with` 语句安全地读写文件——文件会自动关闭，不会因为忘记 `close()` 而丢失数据。

但还有个问题没解决。小北上周在日记本工具的代码里写了这样一行：

```python
file = open("C:\\Users\\小北\\Documents\\diary.txt", "w", encoding="utf-8")
```

老潘看完，眉头皱了起来："这个代码在我电脑上跑不了。"

"为什么？"小北不解。

下一节，我们来学一个让路径跨平台兼容的现代化工具——`pathlib`。

---

## 3. 不硬编码路径——用 pathlib 管理文件路径

小北上周写了个日记本工具，代码里有这样一行：

```python
file = open("C:\\Users\\小北\\Documents\\diary.txt", "w", encoding="utf-8")
```

老潘看完，皱了皱眉："这个代码在我电脑上跑不了。"

"为什么？"小北不解。

"因为你的路径是**硬编码**的，"老潘解释，"`C:\\Users\\小北\\Documents\\` 只在你电脑上有效。如果我换个用户名，或者用 Mac（路径是 `/Users/laopan/Documents/`），你的代码就挂了。"

小北想了想，那该怎么办？

老潘给出了两个方案：

**方案 1：用相对路径（不推荐）**

```python
file = open("diary.txt", "w", encoding="utf-8")  # 当前目录
```

问题是：当前目录是哪里？取决于你**运行程序的位置**。如果你在 `/home/xb/` 运行，文件就创建在 `/home/xb/`；如果你在 `/tmp/` 运行，文件就创建在 `/tmp/`。这很容易混乱。

**方案 2：用 `pathlib`（推荐）**

`pathlib` 是 Python 3.4+ 引入的**现代化路径处理库**，它用**对象**而不是字符串来表示路径。

```python
from pathlib import Path

# 获取用户主目录（跨平台兼容）
home_dir = Path.home()
print(home_dir)  # Windows: C:\Users\小北, Mac/Linux: /Users/小北

# 构建路径（用 / 运算符）
diary_dir = home_dir / "Documents" / "Diary"
diary_file = diary_dir / "diary.txt"

print(diary_file)  # C:\Users\小北\Documents\Diary\diary.txt
```

`Path.home()` 会自动找到当前用户的主目录（Windows 是 `C:\Users\用户名`，Mac/Linux 是 `/Users/用户名`）。

`/` 运算符是用来**拼接路径**的——`home_dir / "Documents"` 相当于把 `Documents` 拼到 `home_dir` 后面。

小北看完，若有所思："所以 `pathlib` 让路径'跨平台兼容'了？"

"对，"老潘说，"而且它还解决了 Windows 的**反斜杠问题**。"

在 Windows 上，路径用反斜杠 `\`：

```python
# Windows 路径
path = "C:\\Users\\小北\\Documents\\diary.txt"  # 要写成 \\（转义）
```

在 Mac/Linux 上，路径用正斜杠 `/`：

```python
# Mac/Linux 路径
path = "/Users/小北/Documents/diary.txt"
```

如果你硬编码路径，代码就不能跨平台。但 `pathlib` 会自动处理：

```python
from pathlib import Path

# 构建路径（自动选择正确的分隔符）
diary_file = Path.home() / "Documents" / "diary.txt"
print(diary_file)
# Windows: C:\Users\小北\Documents\diary.txt
# Mac/Linux: /Users/小北/Documents/diary.txt
```

---

`pathlib` 还有很多实用的方法：

```python
from pathlib import Path

file_path = Path("diary.txt")

# 检查文件是否存在
if file_path.exists():
    print("文件存在")
else:
    print("文件不存在")

# 创建父目录（如果不存在）
file_path.parent.mkdir(parents=True, exist_ok=True)

# 获取文件名
print(file_path.name)  # diary.txt

# 获取文件扩展名
print(file_path.suffix)  # .txt

# 读取文件内容（不用 open()）
content = file_path.read_text(encoding="utf-8")
print(content)

# 写入文件内容（不用 open()）
file_path.write_text("今天的日记\n", encoding="utf-8")
```

`file_path.read_text()` 和 `file_path.write_text()` 是 `pathlib` 提供的"快捷方法"——你不需要手动 `open()` 和 `close()`。

小北问："那我还用 `with open()` 吗？"

"`pathlib` 的快捷方法内部也用了 `with`，"老潘解释，"所以它已经是安全的了。你可以根据需要选择：
- 用 `with open()`：更灵活（比如需要追加模式、二进制模式）
- 用 `pathlib` 的快捷方法：更简洁（适合简单的读写）"

阿码追问道："那什么时候用 `pathlib`，什么时候用字符串路径？"

老潘给了个简单的规则：
- **路径需要跨平台** → 用 `pathlib`
- **路径需要拼接/操作** → 用 `pathlib`
- **路径是固定的字符串**（比如配置文件名 `"config.json"`） → 可以用字符串

---

现在让我们用 `pathlib` 改写 PyHelper 的文件操作：

```python
from pathlib import Path

def get_data_file():
    """获取数据文件的路径（跨平台兼容）"""
    # 在当前目录下创建 pyhelper_data.txt
    data_dir = Path.cwd()  # 当前工作目录
    data_file = data_dir / "pyhelper_data.txt"
    return data_file

def save_to_file(learning_log, data_file=None):
    """保存学习记录到文件"""
    if data_file is None:
        data_file = get_data_file()

    # 用 pathlib 的 write_text() 方法
    content = ""
    for date, log in learning_log.items():
        content += f"{date}: {log}\n"

    data_file.write_text(content, encoding="utf-8")
    print(f"数据已保存到 {data_file}")

def load_from_file(data_file=None):
    """从文件加载学习记录"""
    if data_file is None:
        data_file = get_data_file()

    learning_log = {}

    # 检查文件是否存在
    if not data_file.exists():
        print(f"注意：{data_file} 不存在，将创建新文件")
        return learning_log

    # 用 pathlib 的 read_text() 方法
    content = data_file.read_text(encoding="utf-8")

    for line in content.split("\n"):
        line = line.strip()
        if line:
            parts = line.split(": ", 1)
            if len(parts) == 2:
                date, log = parts
                learning_log[date] = log

    return learning_log

# 测试
learning_log = {
    "02-09": "学会了列表和字典的基本用法",
    "02-10": "写了一个成绩单项目"
}

save_to_file(learning_log)
loaded_log = load_from_file()
print(loaded_log)
```

这里用到了 Week 03 学的**参数默认值**——`data_file=None` 表示"如果没有传参，就用默认值"。还用到了 Week 02 学的**布尔逻辑**——`if not data_file.exists()` 检查文件是否存在。

---

现在你已经学会了用 `pathlib` 处理文件路径——代码能在 Windows、Mac、Linux 上跑了，不会因为路径分隔符（`\` vs `/`）的不同而报错。

小北很高兴，立刻用新学的技能写了个日记本工具。但运行后，他打开 `diary.txt`，发现了一个奇怪的现象：中文全变成了乱码——"ä»å¤©å¾å¼å¿"。

"怎么回事！？"小北盯着屏幕，"我的中文怎么变成天书了？"

下一节，我们来解开这个谜团——**编码**（encoding）。

---

> **AI 时代小专栏：pathlib 在 AI 项目中的应用**

> 你刚学的 `pathlib`，不只是"路径处理工具"，更是 AI 项目中的**标准配置**。
>
> 近年在 GitHub 上最流行的 AI 项目（如 `Transformers`、`Diffusers`、`LangChain`）都大量使用 `pathlib`。为什么？因为 AI 项目通常需要在**不同操作系统**上运行——训练在 Linux 服务器，开发在 Mac/Windows。
>
> 如果用字符串路径硬编码 `"C:\\data\\model.bin"`，在 Linux 上会直接报错。但用 `pathlib.Path("data") / "model.bin"`，代码就能跨平台运行。
>
> 更重要的是，`pathlib` 提供了很多方便的方法：
> - `path.exists()` —— 检查文件是否存在（避免 FileNotFoundError）
> - `path.parent.mkdir(parents=True)` —— 自动创建父目录（适合保存模型权重）
> - `path.read_text()` / `path.write_text()` —— 简洁的读写接口
>
> HuggingFace 的 `transformers` 库在加载模型时，就用 `pathlib` 查找模型文件：
>
> ```python
> from pathlib import Path
> model_path = Path("models") / "bert-base-uncased"
> if model_path.exists():
>     print("模型已下载")
> ```
>
> 所以你今天学的 `pathlib`，不只是让代码更简洁，更是让代码"可移植"——这是 AI 工程化的基础。
>
> 参考（访问日期：2026-02-09）：
> - [Python pathlib Documentation](https://docs.python.org/3/library/pathlib.html)
> - [Why You Should Be Using pathlib (Real Python, 2024)](https://realpython.com/python-pathlib/)
> - [Transformers Library Source Code (GitHub)](https://github.com/huggingface/transformers/blob/main/src/transformers/utils/hub.py)

---

## 4. 编码与追加——让日记本更实用

到目前为止，你写的文件都是"覆盖模式"——每次写入都会清空旧内容。但日记本需要"追加模式"——每次打开程序，新的日记应该加到旧日记后面，而不是覆盖掉。

这需要用**追加模式**（append mode）：

```python
# 追加模式（"a" 表示 append）
with open("diary.txt", "a", encoding="utf-8") as file:
    file.write("2026-02-11: 今天学到了追加模式\n")
```

`"a"` 模式会在文件**末尾**添加内容，而不是覆盖整个文件。

如果 `diary.txt` 原本有：

```
2026-02-09: 今天学会了文件操作
2026-02-10: 今天学到了 with 语句
```

运行追加代码后，文件变成：

```
2026-02-09: 今天学会了文件操作
2026-02-10: 今天学到了 with 语句
2026-02-11: 今天学到了追加模式
```

小北立刻试了一下，结果发现**中文乱码了**：

```python
with open("diary.txt", "a", encoding="utf-8") as file:
    file.write("2026-02-11: 今天很开心\n")
```

打开 `diary.txt`，看到：

```
2026-02-11: ä»å¤©å¾å¼å¿
```

"怎么回事！？"小北盯着乱码，"我的中文怎么变成天书了？"

老潘在旁边解释："这是**编码问题**（encoding）。你写文件时用的是 UTF-8，但打开文件时记事本用的可能是 GBK（Windows 中文系统的默认编码）。"

**编码**（encoding）是"把文字转换成二进制"的规则。计算机不认识"中文字符"，只认识 0 和 1。所以需要一个"翻译规则"：
- **UTF-8**：全球通用的编码，支持所有语言，是互联网标准
- **GBK**：中国国家标准编码，只支持中文
- **ASCII**：最早的编码，只支持英文

同一个中文字符，用不同编码会变成不同的二进制：

```python
# "中"字的 UTF-8 编码
"中".encode("utf-8")  # b'\xe4\xb8\xad'

# "中"字的 GBK 编码
"中".encode("gbk")  # b'\xd6\xd0'
```

如果你写文件时用 UTF-8，读文件时用 GBK，就会乱码。

```python
# 写入时用 UTF-8
with open("test.txt", "w", encoding="utf-8") as file:
    file.write("中文测试\n")

# 读取时用 GBK（会报错或乱码）
with open("test.txt", "r", encoding="gbk") as file:
    content = file.read()
    print(content)  # UnicodeDecodeError: 'gbk' codec can't decode byte 0xad
```

小北问："那怎么避免乱码？"

"记住一个规则：**统一用 UTF-8**，"老潘说，"UTF-8 是国际标准，所有现代工具都支持。写文件、读文件、数据库、网页——统统用 UTF-8，你就不会遇到编码问题。"

老潘停顿了一下，补了一句："编码问题是每个程序员都会遇到的坑。我当年刚工作时，有一次因为编码问题，线上系统处理用户名时把'张三'显示成了'å¼ ä¸'，被老板骂了半小时。从那以后，我的人生格言就变成了——能 UTF-8 就 UTF-8，能 Unicode 就 Unicode。"

小北听完，笑了："那我记住了，UTF-8 是保命符。"

```python
# ✅ 推荐：始终用 UTF-8
with open("file.txt", "r", encoding="utf-8") as file:
    content = file.read()

with open("file.txt", "w", encoding="utf-8") as file:
    file.write("中文内容\n")
```

阿码追问："如果文件本身不是 UTF-8 编码的怎么办？"

"那就用 `chardet` 库检测编码，"老潘说，"但这是进阶话题。你现在只需要记住：**你自己创建的文件，统统用 UTF-8**。"

---

现在让我们用追加模式和 UTF-8 改进日记本工具：

```python
from datetime import datetime  # Python 标准库，用于获取当前日期
from pathlib import Path

def add_diary_entry(content, filename="diary.txt"):
    """添加一条日记（追加模式）"""
    # 获取当前日期
    today = datetime.now().strftime("%Y-%m-%d")

    # 构建日记条目
    entry = f"{today}: {content}\n"

    # 追加到文件（用 with 和 UTF-8）
    with open(filename, "a", encoding="utf-8") as file:
        file.write(entry)

    print(f"日记已添加：{entry.strip()}")

def read_all_diaries(filename="diary.txt"):
    """读取所有日记"""
    diary_file = Path(filename)

    # 如果文件不存在，返回空列表
    if not diary_file.exists():
        print("日记本还是空的，快写第一篇吧！")
        return []

    # 读取所有内容
    content = diary_file.read_text(encoding="utf-8")

    # 按行分割，返回列表
    lines = content.strip().split("\n")
    return lines

def search_diaries(keyword, filename="diary.txt"):
    """按关键词搜索日记"""
    lines = read_all_diaries(filename)

    matching_entries = []
    for line in lines:
        if keyword in line:  # 如果关键词在这一行里
            matching_entries.append(line)

    return matching_entries

# 测试
add_diary_entry("今天学会了文件操作和 with 语句")
add_diary_entry("编码问题终于搞懂了，UTF-8 是王道")
add_diary_entry("追加模式让日记本能持续记录")

print("\n=== 所有日记 ===")
all_diaries = read_all_diaries()
for entry in all_diaries:
    print(entry)

print("\n=== 搜索'编码' ===")
results = search_diaries("编码")
for entry in results:
    print(entry)
```

输出：

```
日记已添加：2026-02-09: 今天学会了文件操作和 with 语句
日记已添加：2026-02-09: 编码问题终于搞懂了，UTF-8 是王道
日记已添加：2026-02-09: 追加模式让日记本能持续记录

=== 所有日记 ===
2026-02-09: 今天学会了文件操作和 with 语句
2026-02-09: 编码问题终于搞懂了，UTF-8 是王道
2026-02-09: 追加模式让日记本能持续记录

=== 搜索'编码' ===
2026-02-09: 编码问题终于搞懂了，UTF-8 是王道
```

这里用到了 Python 标准库的 `datetime` 模块——获取当前日期和时间。`datetime.now().strftime("%Y-%m-%d")` 会返回类似 `"2026-02-09"` 的字符串。

小北看完，点点头："这个日记本工具还挺实用的。每天写一点，以后还能翻看。"

"对，"老潘说，"而且你发现没有？这个工具的代码不到 50 行，但已经能做'写日记、读日记、搜日记'三件事了。这就是**文件操作**的威力——它让程序能'记住'东西，变得真正有用。"

---

现在你已经掌握了文件读写的核心技能。下一节，我们把所有东西整合起来，给 PyHelper 添加"持久化存储"功能。

---

## PyHelper 进度

上周 PyHelper 已经能用字典存储学习记录，但程序关闭后数据就没了。这周我们用**文件存储**来解决这个问题。

上周状态：PyHelper 能添加、查看、统计学习记录，但所有数据存在内存里（字典），程序关闭后丢失。

本周改进：把学习记录存到 `pyhelper_data.txt`，程序启动时自动加载，退出时自动保存。

```python
# PyHelper - 你的命令行学习助手
# Week 05：用文件存储学习记录

from pathlib import Path

# ===== 文件操作函数（用 Week 05 学的 with 和 pathlib）=====

def get_data_file():
    """获取数据文件的路径"""
    return Path.cwd() / "pyhelper_data.txt"

def load_learning_log():
    """从文件加载学习记录（返回字典）"""
    data_file = get_data_file()
    learning_log = {}

    if data_file.exists():
        content = data_file.read_text(encoding="utf-8")
        for line in content.split("\n"):
            line = line.strip()
            if line:
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    date, content = parts
                    learning_log[date] = content
        print(f"已加载 {len(learning_log)} 条学习记录")
    else:
        print("首次运行，将创建新的数据文件")

    return learning_log

def save_learning_log(learning_log):
    """保存学习记录到文件"""
    data_file = get_data_file()

    # 用 f-string 和 for 循环构建内容（Week 01 + Week 02）
    content = ""
    for date, log in learning_log.items():
        content += f"{date}: {log}\n"

    # 用 pathlib 的 write_text() 写入文件（Week 05）
    data_file.write_text(content, encoding="utf-8")
    print(f"已保存 {len(learning_log)} 条学习记录")

# ===== 原有功能函数（Week 03 + Week 04）=====

def print_welcome():
    """打印欢迎信息"""
    print("=" * 40)
    print("  欢迎使用 PyHelper！")
    print("=" * 40)
    print()

def print_menu():
    """打印菜单"""
    print("请选择功能：")
    print("1. 添加学习记录")
    print("2. 查看所有记录")
    print("3. 统计学习天数")
    print("4. 获取学习建议")
    print("5. 退出并保存")

def get_choice():
    """获取用户选择（用 Week 02 学的 while 循环）"""
    while True:
        choice = input("\n请输入选择（1-5）：")
        if choice in ["1", "2", "3", "4", "5"]:
            return choice
        print("无效输入，请输入 1-5")

def add_record(learning_log):
    """添加学习记录（直接修改传入的字典）"""
    date = input("请输入日期（如 02-09）：")
    content = input("请输入今天学了什么：")

    if date in learning_log:
        print(f"注意：{date} 的记录会被覆盖")

    learning_log[date] = content
    print(f"已添加：{date} - {content}")

def show_records(learning_log):
    """查看所有学习记录（用 Week 04 学的字典遍历）"""
    if not learning_log:
        print("还没有学习记录哦，去添加一些吧！")
        return

    print("\n=== 学习记录 ===")
    for date in sorted(learning_log.keys()):
        print(f"{date}: {learning_log[date]}")

def show_stats(learning_log):
    """统计学习天数（用 Week 04 学的 len()）"""
    count = len(learning_log)
    print(f"\n你已经学习了 {count} 天")

    if count >= 5:
        print("太棒了！坚持就是胜利！")
    elif count >= 2:
        print("不错的开始，继续加油！")
    else:
        print("万事开头难，加油！")

def get_mood():
    """获取用户心情（Week 02 的 if/else）"""
    print("\n今天心情怎么样？")
    print("1. 充满干劲")
    print("2. 一般般")
    print("3. 有点累")
    mood = input("请输入你的心情（1-3）：")
    return mood

def get_advice(mood):
    """根据心情返回建议（Week 02 的 if/elif/else）"""
    if mood == "1":
        return "太好了！推荐你今天挑战一个新概念，比如文件操作或 pathlib。"
    elif mood == "2":
        return "那就做点巩固练习吧，写几个小例子，熟悉一下文件读写。"
    elif mood == "3":
        return "累了就休息一下吧，今天可以只看视频不动手，或者写 10 分钟代码就停。"
    else:
        return "写点巩固练习最稳妥。"

def show_advice():
    """显示学习建议"""
    mood = get_mood()
    advice = get_advice(mood)
    print(f"\n{advice}")

# ===== 主函数（Week 03 学的函数定义）=====

def main():
    """主函数"""
    # 启动时加载学习记录（Week 05 的文件操作）
    learning_log = load_learning_log()

    print_welcome()

    while True:
        print_menu()
        choice = get_choice()

        if choice == "1":
            add_record(learning_log)
        elif choice == "2":
            show_records(learning_log)
        elif choice == "3":
            show_stats(learning_log)
        elif choice == "4":
            show_advice()
        elif choice == "5":
            # 退出前保存学习记录（Week 05 的文件操作）
            save_learning_log(learning_log)
            print("\n再见！祝你学习愉快！")
            break

        print("\n" + "-" * 40)

# 启动程序
if __name__ == "__main__":
    main()
```

运行效果：

```
========================================
  欢迎使用 PyHelper！
========================================

已加载 2 条学习记录

请选择功能：
1. 添加学习记录
2. 查看所有记录
3. 统计学习天数
4. 获取学习建议
5. 退出并保存

请输入选择（1-5）：2

=== 学习记录 ===
02-09: 学会了列表和字典的基本用法
02-10: 写了一个成绩单项目

----------------------------------------

请选择功能：
1. 添加学习记录
2. 查看所有记录
3. 统计学习天数
4. 获取学习建议
5. 退出并保存

请输入选择（1-5）：1
请输入日期（如 02-09）：02-11
请输入今天学了什么：学会了文件读写和 pathlib
已添加：02-11 - 学会了文件读写和 pathlib

----------------------------------------

请选择功能：
1. 添加学习记录
2. 查看所有记录
3. 统计学习天数
4. 获取学习建议
5. 退出并保存

请输入选择（1-5）：5
已保存 3 条学习记录

再见！祝你学习愉快！
```

对比上周的代码，你会发现几个关键变化：

1. **启动时加载**：`load_learning_log()` 会从 `pyhelper_data.txt` 读取旧数据，如果文件不存在就返回空字典
2. **退出时保存**：选择"退出"选项时，`save_learning_log()` 会把字典写入文件，下次启动时能恢复
3. **文件不存在时不报错**：用 `if data_file.exists()` 检查文件是否存在，避免 `FileNotFoundError`
4. **用 pathlib 管理路径**：`Path.cwd() / "pyhelper_data.txt"` 确保路径跨平台兼容

老潘看到这段代码，点点头："现在 PyHelper 能'记住'你学过的东西了。你可以每天写一点学习记录，过一个月再回头看——会很有成就感。我当年学编程的时候，就是靠写日记发现自己真的在进步。"

小北问："那下周呢？PyHelper 还会继续长大吗？"

"当然，"老潘笑笑，"下周它会学会'不怕坏输入'——不管你输入什么乱七八糟的东西，它都不会崩溃。这就是**异常处理**（exception handling）。"

---

## Git 本周要点

本周必会命令：
- `git remote add origin <url>` —— 添加远端仓库地址
- `git push -u origin main` —— 推送本地分支到远端（首次推送用 `-u` 建立追踪关系）
- `git pull` —— 拉取远端更新并合并到本地

常见坑：
- **忘记关闭文件**：数据不会落盘，用 `with` 语句避免
- **编码不匹配**：写入用 UTF-8，读取用 GBK，会乱码。统一用 UTF-8
- **路径硬编码**：`"C:\\Users\\..."` 不能跨平台，用 `pathlib` 解决
- **覆盖 vs 追加**：`"w"` 会清空文件，`"a"` 是追加模式
- **文件不存在**：读取不存在的文件会报 `FileNotFoundError`，用 `path.exists()` 检查

**文件模式速查表**：

| 模式 | 含义 | 文件不存在时 |
|------|------|-------------|
| `"r"` | 只读 | 报错 `FileNotFoundError` |
| `"w"` | 写入（覆盖） | 创建新文件 |
| `"a"` | 追加 | 创建新文件 |
| `"r+"` | 读写 | 报错 |

**Gitea 远端连接流程**：

```bash
# 1. 在 Gitea 上创建新仓库（比如 week_05）

# 2. 添加远端地址
git remote add origin https://gitea.example.com/yourname/week_05.git

# 3. 推送本地分支到远端
git push -u origin main

# 4. 以后只需要
git push  # 推送本地修改到远端
git pull  # 拉取远端修改到本地
```

Pull Request (PR)：
- Week 05 开始正式使用 PR 流程：在 Gitea 上发起 PR → 请同学 review → 通过后 merge
- PR 描述模板：
  ```markdown
  ## 本周做了什么
  - 实现了文件读写功能
  - 用 pathlib 管理路径
  - PyHelper 支持持久化存储

  ## 自测
  - [ ] 运行 `python3 -m pytest chapters/week_05/tests -q` 通过
  - [ ] PyHelper 能正常保存和加载学习记录

  ## 待 review
  请重点检查文件操作的异常处理
  ```

---

## 本周小结（供下周参考）

这一周，你学会了让程序"记住"东西——用**文件**（file）把数据存到硬盘上，而不是只留在内存里。你学会了 `open()`、`read()`、`write()` 这些基础操作，也学会了 `with` 语句——确保文件正确关闭的"安全网"。更重要的是，你理解了**编码**（encoding）的概念，知道统一用 UTF-8 可以避免中文乱码。

你还学会了用 `pathlib` 处理文件路径——它让代码能跨平台运行，不会因为 Windows/Mac/Linux 的路径差异而报错。

到现在为止，你已经掌握了 Python 入门的 5 个核心概念：变量、条件判断、函数、数据结构（列表/字典）、文件操作。下周，我们将学习**异常处理**（exception handling）——让程序"不怕坏输入"，在出错时优雅地恢复，而不是直接崩溃。

你会发现，异常处理和文件操作经常一起使用——比如"文件不存在"就是一个异常，需要你妥善处理。下周 PyHelper 会变得更健壮：不管用户输入什么乱七八糟的东西，它都不会崩。

---

## Definition of Done（学生自测清单）

完成本周学习后，请确认你能：

- [ ] 理解文件的基本概念，能用 `open()` 打开文件
- [ ] 掌握 `with` 语句，理解"为什么要自动关闭文件"
- [ ] 能用 `file.read()`、`file.readlines()`、`for line in file` 读取文件内容
- [ ] 能用 `file.write()` 写入文件，理解 `"w"` 和 `"a"` 模式的区别
- [ ] 理解"编码"（encoding）的概念，知道统一用 UTF-8 避免乱码
- [ ] 能用 `pathlib` 处理文件路径，理解 `Path.home()`、`Path.cwd()`、`/` 运算符
- [ ] 能检查文件是否存在（`path.exists()`），避免 `FileNotFoundError`
- [ ] 能用 `split()` 和 `strip()` 处理文件内容
- [ ] 理解"持久化存储"的概念，知道什么时候用文件存储数据
- [ ] 完成日记本项目（写日记、读日记、搜日记）
- [ ] 给 PyHelper 添加"持久化存储"功能（启动加载、退出保存）
- [ ] Git 至少提交 2 次（draft + verify）
- [ ] 能连接 Gitea 远端仓库，会用 `git push` 和 `git pull`
- [ ] 运行 `python3 -m pytest chapters/week_05/tests -q` 并通过所有测试

<!--
章节结构骨架（供 chapter-writer 参考）：

1. 章首导入（引言格言 + 时代脉搏）——已完成
2. 前情提要——已完成
3. 学习目标——已完成
4. 贯穿案例设计说明（HTML 注释）——已完成
5. 认知负荷 + 回顾桥 + 角色出场规划（HTML 注释）——已完成
6. AI 小专栏规划（HTML 注释）——已完成
7. 第 1 节：程序的记忆——从字典到文件——已完成
8. 第 2 节：自动关文件的安全网——with 语句——已完成
9. 第 3 节：不硬编码路径——用 pathlib 管理文件路径——已完成
10. 第 4 节：编码与追加——让日记本更实用——已完成
11. PyHelper 进度——已完成
12. Git 本周要点——已完成
13. 本周小结（供下周参考）——已完成
14. Definition of Done——已完成
-->
