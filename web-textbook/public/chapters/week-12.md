# Week 12：像专业人士一样写命令行工具

> "The best programs are the ones written so that they can be read and understood by humans, not just executed by machines."
> — Brian Kernighan

2025-2026 年，命令行工具（CLI）正在经历一场复兴。GitHub 上 stars 过万的 CLI 项目如 `eza`（现代 ls 替代品）、`zellij`（终端工作区管理器）、`gitui`（Git TUI 工具）等，都是纯命令行界面但体验极佳的工具。这种复兴背后有两个驱动力：一是 DevOps 和云原生技术的普及（服务器上只能用命令行），二是 AI 编程助手让写 CLI 工具的门槛大幅降低——你不再需要记忆 argparse 的所有 API，让 AI 生成骨架，你专注于业务逻辑即可。

更重要的趋势是 **"CLI as API"** 的理念——命令行工具不只是给人用的，也是脚本和其他程序调用的接口。2025 年的 [CobraConf（命令行工具开发者大会）](https://www.cobraconf.com/)讨论最多的主题之一就是"如何设计既适合人类交互、又适合程序调用的 CLI"。退出码、标准输出、JSON 模式、子命令设计——这些你即将学习的概念，正是专业 CLI 工具的标志。

从 Week 01 你写下第一个 `print("Hello")` 到现在，你已经走了很远。现在，让 PyHelper 变成一个真正的命令行工具——像 `git`、`docker`、`pytest` 那样，通过命令行参数和子命令与世界交互。

---

## 前情提要

上周小北给 PyHelper 加上了 dataclass 数据模型和类型提示——代码变得清晰多了，IDE 能自动补全，状态转换也有了规则。阿码很满意："现在代码自己说明自己，不用翻来翻去猜字段名了。"

但老潘发现了一个问题："你们每次运行 PyHelper 还得改代码调用函数。能不能像 `git status` 那样，在命令行里敲 `pyhelper add` 就添加笔记？"

小北眼睛一亮："对啊！我一直在想这个问题。Git 那样的命令行工具是怎么写的？"

"这就是本周的主题，"老潘说，"argparse——Python 标准库的命令行解析器。学会它，你就能写出真正的 CLI 工具。"

---

## 学习目标

完成本周学习后，你将能够：
1. 理解 argparse 的基本用法，能解析位置参数和可选参数
2. 掌握子命令的设计，能实现类似 `git add` / `git commit` 的多命令结构
3. 理解退出码的概念，能用 `sys.exit()` 返回正确的状态
4. 掌握 logging 的基础用法，能用日志记录程序运行信息
5. 为 PyHelper 实现完整的 CLI 界面（add/list/search/export/stats 子命令）

---

<!--
贯穿案例设计：todo-cli —— 命令行待办事项工具

为什么选这个案例：
- 紧扣 argparse 主题（命令行参数解析）
- 与 PyHelper 的学习笔记场景区分开（避免重复）
- 足够简单但不幼稚：支持 add/list/done/delete/stats 子命令
- 能自然演示：位置参数、可选参数、子命令、互斥参数、退出码

案例演进路线：
- 第 1 节：最简单的 add 命令（一个位置参数）→ 能添加单个待办事项
- 第 2 节：list 命令加可选参数（过滤状态）→ 支持 --all/--pending/--done 参数
- 第 3 节：重构为子命令架构 → add/list/done/delete 统一入口
- 第 4 节：加 done/delete 子命令 + 退出码 → 支持标记完成和删除，返回正确的退出码
- 第 5 节：stats 子命令 + logging → 统计功能 + 日志记录

最终成果：一个功能完整的 todo-cli 工具，支持：
- `todo add "买牛奶"` → 添加待办
- `todo list --pending` → 列出未完成
- `todo done 1` → 标记第 1 项完成
- `todo delete 1` → 删除第 1 项
- `todo stats` → 显示统计信息
- 日志记录到文件
- 退出码：成功返回 0，失败返回 1

认知负荷预算：
- 本周新概念（4 个，预算上限 4 个）：
  1. argparse（命令行参数解析）
  2. 子命令（subcommands）
  3. 退出码（exit codes）
  4. logging（日志记录）
- 结论：✅ 在预算内

回顾桥设计（至少 3 个，目标引用前 4 周的概念）：
- [异常处理]（来自 week_06）：在第 2 节，处理命令行参数解析错误
- [import 与模块]（来自 week_07）：在第 3 节，从 argparse 模块导入 ArgumentParser
- [pytest 断言]（来自 week_08）：在第 4 节，测试 CLI 的退出码
- [JSON 读写]（来自 week_10）：在第 5 节，stats 子命令导出 JSON 格式统计
- [dataclass]（来自 week_11）：贯穿全程，用 dataclass 定义 Todo 模型
- [类型提示]（来自 week_11）：贯穿全程，CLI 函数添加类型提示

角色出场规划：
- 小北（第 1 节）：用 `sys.argv` 手写解析，发现太麻烦，引出 argparse
- 阿码（第 2 节）：追问"为什么一定要用双横线 --all？"引出参数规范
- 老潘（第 3 节）：分享 Git 子命令的设计哲学，讲解子命令架构
- 小北（第 4 节）：忘记返回退出码，导致脚本调用失败，引出退出码的重要性
- 阿码（第 5 节）：质疑"为什么不用 print？"引出 logging 和 print 的区别

AI 小专栏规划：
- AI 小专栏 #1（放在第 2 节之后）：
  - 主题：AI 辅助生成 CLI 代码——argparse 样板代码的自动化
  - 连接点：与第 2 节"可选参数"呼应，讨论 AI 工具如何辅助生成 argparse 代码
  - 建议搜索词："AI generate argparse code 2026", "GitHub Copilot CLI tool generation 2026"

- AI 小专栏 #2（放在第 4 节之后）：
  - 主题：退出码与脚本自动化——AI 时代 DevOps 的基础
  - 连接点：与第 4 节"退出码"呼应，讨论退出码在 CI/CD 和脚本自动化中的重要性
  - 建议搜索词："exit codes CI/CD automation 2026", "bash script error handling 2026"

PyHelper 本周推进：
- 上周状态：PyHelper 已有 dataclass 数据模型和 JSON 序列化，但仍需在代码中调用函数
- 本周改进：
  1. 用 argparse 创建主入口 `pyhelper_cli.py`
  2. 实现子命令：add/list/search/export/stats
  3. 添加 --verbose 参数控制日志级别
  4. 返回正确的退出码（成功 0，失败 1）
  5. 用 logging 记录操作日志到文件
- 涉及的本周概念：argparse、子命令、退出码、logging
- 建议示例文件：examples/pyhelper/cli.py（新增 CLI 入口）
-->

## 1. 从脚本到工具——你的第一个 argparse 程序

小北的 Task Tracker 运行得不错，但她每次要添加任务都得改代码：

```python
# 每次运行都要改这里
task = Task("完成 Week 12 作业", "high")
save_task("task.json", task)
```

"这太麻烦了，"她想，"能不能像 `git add .` 那样，在命令行里敲 `task add '写作业'` 就添加任务？"

阿码在旁边说："我记得 Week 01 学过 `sys.argv` ——你可以从命令行读取参数啊。"

```python
# examples/01_argv_before.py
import sys

if len(sys.argv) < 2:
    print("用法：python task.py <任务标题>")
    sys.exit(1)

title = sys.argv[1]
print(f"添加任务：{title}")
```

注意到 `f"添加任务：{title}"` 了吗？这是 Week 01 学过的 **f-string**——在字符串中嵌入变量。命令行工具的输出几乎都用 f-string，因为你需要把用户输入的值显示出来。

运行：

```bash
python task.py "写作业"
# 输出：添加任务：写作业
```

看起来不错，但问题很快就来了。老潘看到小北的代码，摇摇头："你这个只能添加任务。如果我想加优先级呢？比如 `task.py '写作业' --priority high`。"

小北想了想："那我就得去解析 `sys.argv[2]` 和 `sys.argv[3]`……如果参数顺序变了怎么办？如果用户没传优先级呢？"

"对，"老潘说，"`sys.argv` 是原始字符串列表，你得手写解析逻辑——检查参数个数、类型、顺序、默认值……这东西写多了会疯。"

"那怎么办？"

"Python 标准库有个专门的工具：`argparse`。"

### argparse：命令行参数解析器

argparse 是 Python 标准库的一部分，专门用来解析命令行参数。先看一个最简单的例子：

```python
# examples/01_argparse_first.py
import argparse

# 创建解析器
parser = argparse.ArgumentParser(description="任务管理工具")

# 添加位置参数（必需）
parser.add_argument("title", help="任务标题")

# 解析参数
args = parser.parse_args()

print(f"添加任务：{args.title}")
```

运行：

```bash
python task.py "写作业"
# 输出：添加任务：写作业

python task.py
# 输出：usage: task.py [-h] title
#       error: the following arguments are required: title
```

注意到了吗？argparse 自动帮你做了几件事：
1. **生成帮助信息**：`-h` / `--help` 自动生成
2. **验证必需参数**：如果你不传 `title`，它会报错
3. **友好的错误提示**：告诉你缺少什么参数

"这比手写 `sys.argv` 好多了，"小北满意地说，"而且不用自己写帮助文档。"

```bash
python task.py --help
# 输出：
# usage: task.py [-h] title
#
# positional arguments:
#   title       任务标题
#
# optional arguments:
#   -h, --help  show this help message and exit
```

### 位置参数 vs 可选参数

argparse 有两种参数：**位置参数**（positional）和**可选参数**（optional）。

位置参数：必须按顺序提供，比如 `git add <file>` 中的 `<file>`。

```python
parser.add_argument("title", help="任务标题")
```

可选参数：用 `-` 或 `--` 开头，比如 `git commit -m "message"` 中的 `-m`。

```python
parser.add_argument("--priority", help="任务优先级", default="medium")
```

完整例子：

```python
# examples/01_positional_optional.py
import argparse

parser = argparse.ArgumentParser(description="任务管理工具")

# 位置参数（必需）
parser.add_argument("title", help="任务标题")

# 可选参数
parser.add_argument("--priority", help="任务优先级", choices=["low", "medium", "high"], default="medium")

args = parser.parse_args()

print(f"添加任务：{args.title}")
print(f"优先级：{args.priority}")
```

还记得 Week 03 学过的 **函数分解** 吗？每个子命令的逻辑应该封装成独立的函数，这样代码更清晰、更容易测试。你很快会在第 3 节看到如何把子命令路由到函数。

运行：

```bash
python task.py "写作业"
# 输出：添加任务：写作业
#       优先级：medium

python task.py "写作业" --priority high
# 输出：添加任务：写作业
#       优先级：high

python task.py "写作业" --priority ultra
# 输出：error: argument --priority: invalid choice: 'ultra' (choose from 'low', 'medium', 'high')
```

注意到 `choices` 参数了吗？它限制优先级只能是 `low`/`medium`/`high` —— 如果用户输入其他值，argparse 会报错。这就是 Week 06 学过的**输入校验**，只不过这次在命令行层面完成。

### argparse 的三个魔法：自动完成的事情

老潘掰着指头数 argparse 自动帮你做的事：

**第一，自动生成帮助信息**。你写了 `help="任务标题"`，argparse 自动生成 `--help` 文档。不用自己写大段的帮助文本。

**第二，自动类型转换**。你可以指定参数类型，argparse 自动转换：

```python
parser.add_argument("count", type=int, help="数量")

args = parser.parse_args()
print(args.count * 2)  # count 是 int 类型，可以直接运算
```

如果用户输入非数字，argparse 会报错：`error: argument count: invalid int value: 'abc'`。

**第三，自动验证参数**。`choices`、`required`、`nargs` 等参数让 argparse 自动验证输入合法性，不用你写 `if` 语句检查。

"所以 argparse 的核心价值，"老潘总结道，"是让你不用写重复的解析代码——这些'样板代码' argparse 都帮你做了。"

小北恍然大悟："就像 Week 11 学的 dataclass 自动生成 `__init__` 一样，argparse 自动生成参数解析代码。"

"对，Python 哲学就是'不要重复自己'（DRY）。"

---

## 2. 让命令更灵活——可选参数与默认值

小北的任务添加工具可以加优先级了，但她很快想到一个新问题："我有时候想添加任务，有时候想列出任务，有时候想标记完成——这些功能怎么整合？"

阿码在旁边说："Git 是怎么做的？`git add`、`git commit`、`git status`……每个都是不同的子命令。"

"对，子命令！"老潘说，"但先别急——我们先把单一命令的功能做完整，加上可选参数和默认值。子命令是第 3 节的事。"

### 为什么有些参数有两种写法？-p 和 --priority

小北注意到一个现象：命令行工具的参数好像都有"两种写法"。

```bash
git commit -m "fix bug"
git commit --message "fix bug"
```

"为什么要重复设计？"她问，"直接用一种不就行了？"

老潘笑了笑："这是用户体验的智慧——短选项让你敲得快，长选项让你看得懂。"

argparse 可以同时定义这两种形式：

```python
# examples/02_short_long_options.py
import argparse

parser = argparse.ArgumentParser(description="任务管理工具")

# 同时定义短选项和长选项
parser.add_argument("-p", "--priority", help="任务优先级", choices=["low", "medium", "high"], default="medium")

parser.add_argument("-t", "--tags", help="任务标签（多个用逗号分隔）", default="")

parser.add_argument("title", help="任务标题")

args = parser.parse_args()

print(f"添加任务：{args.title}")
print(f"优先级：{args.priority}")
print(f"标签：{args.tags}")
```

三种用法，完全等价：

```bash
# 短选项——敲起来快
python task.py "写作业" -p high -t "Python,作业"

# 长选项——可读性强
python task.py "写作业" --priority high --tags "Python,作业"

# 混用——也行
python task.py "写作业" -p high --tags "Python,作业"
```

"为什么要同时提供两种？"小北问。

老潘解释："短选项适合**交互式使用**——你敲命令时 `-p high` 比 `--priority high` 快。长选项适合**脚本**——三个月后看脚本，`--priority high` 一眼就明白是什么意思。"

阿码点点头："就像 Git 的 `-m` 和 `--message`，都是一回事。"

### 互斥参数——"这个和那个不能同时用"

小北想加一个功能：列出任务时，可以按状态过滤（`--all` / `--pending` / `--done`），但这些参数不能同时用——你不能说"列出所有已完成任务"，这不是自相矛盾吗？

```python
# examples/02_mutually_exclusive.py
import argparse

parser = argparse.ArgumentParser(description="任务列表工具")

# 创建互斥组
group = parser.add_mutually_exclusive_group()

group.add_argument("--all", action="store_true", help="显示所有任务")
group.add_argument("--pending", action="store_true", help="只显示未完成任务")
group.add_argument("--done", action="store_true", help="只显示已完成任务")

args = parser.parse_args()

if args.all:
    print("列出所有任务")
elif args.pending:
    print("列出来完成任务")
elif args.done:
    print("列出已完成任务")
else:
    print("列出所有任务（默认）")
```

注意到 `action="store_true"` 了吗？这是一个特殊的 action —— 它不需要参数值，只要参数存在就是 `True`，不存在就是 `False`。

运行：

```bash
python task.py --all
# 输出：列出所有任务

python task.py --pending
# 输出：列出来完成任务

python task.py --all --pending
# 输出：error: argument --pending: not allowed with argument --all
```

argparse 自动检测互斥参数冲突——如果用户同时用 `--all` 和 `--pending`，它会报错。这又是 Week 06 学过的**输入校验**，在命令行层面完成。

> **AI 时代小专栏：AI 辅助生成 CLI 代码——argparse 样板代码的自动化**
>
> argparse 的样板代码（add_argument、参数类型、help 文本）很适合 AI 生成。2026 年，AI 编程助手（GitHub Copilot、Cursor、Claude Code）在 CLI 工具开发上已经成为主流——因为 argparse 的 API 很规则，AI 很容易学会。
>
> 现实案例：GitHub 社区有开发者分享"用 Copilot CLI 在 80 分钟内构建项目健康检查工具"的经验——AI 帮助快速生成 argparse 骨架代码，开发者专注于业务逻辑。[2025 年的一项实战案例](https://dev.to/srijan-x/building-devpulse-a-project-health-checker-in-80-minutes-with-github-copilot-cli-2gh6)显示，用 AI 辅助开发 CLI 工具可以将编码时间缩短 60% 以上。
>
> 2026 年还出现了专门的 CLI 编码工具：Claude Code、Aider、OpenCode、Gemini CLI 等，它们都"终端优先"——直接在命令行里和 AI 对话来修改代码。Addy Osmani 在他的[2026 年 LLM 编码工作流](https://medium.com/@addyosmani/my-llm-coding-workflow-going-into-2026-52fe1681325e)中专门提到，AI 代理为命令行使用设计是关键趋势。
>
> 但 AI 也有盲区：它很难帮你"设计"命令行接口。比如：
> - 什么时候用位置参数，什么时候用可选参数？
> - 什么时候用短选项，什么时候用长选项？
> - 什么时候用互斥组，什么时候用子命令？
>
> 这些是**设计决策**，需要你自己判断。AI 可以帮你生成代码，但决策得你来。
>
> 实践建议：
> - 让 AI 生成 argparse 的"骨架"（add_argument 调用）
> - 你自己审核参数设计（命名、顺序、是否必需）
> - 用 Week 08 学的 pytest 测试 CLI 的各种参数组合
> - 记得让 AI 生成帮助文档，然后手动优化（AI 生成的 help 文本通常很生硬）
>
> 所以 argparse 在 AI 时代变得更"容易写"——但设计一个好的 CLI 仍然需要你的判断。你刚学的位置参数、可选参数、互斥组，正是你需要自己"设计决策"的地方。
>
> 参考（访问日期：2026-02-09）：
> - [About GitHub Copilot CLI](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
> - [Building DevPulse with Copilot CLI](https://dev.to/srijan-x/building-devpulse-a-project-health-checker-in-80-minutes-with-github-copilot-cli-2gh6)
> - [Top 5 CLI coding agents in 2026](https://pinggy.io/blog/top_cli_based_ai_coding_agents/)
> - [Best AI Coding Assistants 2026](https://replit.com/discover/best-ai-coding-assistant)
> - [My LLM coding workflow going into 2026](https://medium.com/@addyosmani/my-llm-coding-workflow-going-into-2026-52fe1681325e)

### 参数的默认值

你已经见过 `default="medium"` 这样的默认值。但如果用户根本没传某个参数，argparse 会用 `default` 的值；如果用户传了，就用用户传的值。

```python
# 优先级默认是 medium
parser.add_argument("--priority", choices=["low", "medium", "high"], default="medium")

# 用户没传，用默认
python task.py "写作业"
# args.priority = "medium"

# 用户传了，用用户的
python task.py "写作业" --priority high
# args.priority = "high"
```

这和 Week 11 学的 dataclass 字段默认值是一样的思路——给一个合理的默认值，让用户不用每次都指定。

"那如果我想让参数是必需的呢？"小北问，"比如任务标题必须传。"

"位置参数默认就是必需的，"老潘说，"如果你想让可选参数也变成必需的，加 `required=True`。"

```python
# 这个参数虽然用 -- 开头，但必须传
parser.add_argument("--title", required=True, help="任务标题（必需）")
```

"为什么要这样？"阿码问，"既然是必需的，为什么不直接用位置参数？"

"好问题，"老潘说，"有时候你想让参数名更明确。比如 `docker run --image ubuntu` —— `image` 用 `--image` 比 `docker run ubuntu` 更清楚。"

小北点点头："所以位置参数适合'省略参数名更简洁'的场景，可选参数适合'参数名更重要'的场景。"

---

## 3. 子命令架构——像 Git 一样组织功能

小北的工具现在可以添加任务、列出任务了，但她发现代码越来越乱：

```python
# 所有逻辑都在一个文件里，越来越长
if args.command == "add":
    # 添加任务的代码
    # ...
elif args.command == "list":
    # 列出任务的代码
    # ...
elif args.command == "done":
    # 标记完成的代码
    # ...
```

"这不对，"她想，"Git 肯定不是这么写的。`git add` 和 `git commit` 一定是分开的。"

老潘点头："对——这就是**子命令**（subcommands）。Git 把功能拆成不同的子命令，每个子命令有自己的参数和逻辑。"

### 用 subparsers 创建子命令

argparse 的 `add_subparsers()` 可以创建子命令结构：

```python
# examples/03_subcommands.py
import argparse

# 创建主解析器
parser = argparse.ArgumentParser(description="任务管理工具")
subparsers = parser.add_subparsers(dest="command", help="可用命令")

# 添加 'add' 子命令
add_parser = subparsers.add_parser("add", help="添加新任务")
add_parser.add_argument("title", help="任务标题")
add_parser.add_argument("--priority", choices=["low", "medium", "high"], default="medium")

# 添加 'list' 子命令
list_parser = subparsers.add_parser("list", help="列出任务")
list_parser.add_argument("--all", action="store_true", help="显示所有任务")
list_parser.add_argument("--pending", action="store_true", help="只显示未完成任务")

# 添加 'done' 子命令
done_parser = subparsers.add_parser("done", help="标记任务为完成")
done_parser.add_argument("id", type=int, help="任务 ID")

# 解析参数
args = parser.parse_args()

# 根据子命令执行不同逻辑
if args.command == "add":
    print(f"添加任务：{args.title}，优先级：{args.priority}")
elif args.command == "list":
    if args.all:
        print("列出所有任务")
    elif args.pending:
        print("列出来完成任务")
    else:
        print("列出所有任务（默认）")
elif args.command == "done":
    print(f"标记任务 {args.id} 为完成")
elif args.command is None:
    # 没有传子命令，显示帮助
    parser.print_help()
```

这个 `if-elif` 结构是不是很眼熟？它和 Week 02 学过的 **while 循环** 的控制流类似——根据不同的条件执行不同的代码块。只不过子命令用 `if-elif` 做一次性判断，而 while 循环用 `if` 做重复判断。

运行：

```bash
# 不传子命令，显示帮助
python todo.py
# 输出：usage: todo.py [-h] {add,list,done} ...
#       positional arguments:
#         {add,list,done}  可用命令

# 添加任务
python todo.py add "写作业" --priority high
# 输出：添加任务：写作业，优先级：high

# 列出任务
python todo.py list --pending
# 输出：列出来完成任务

# 标记完成
python todo.py done 1
# 输出：标记任务 1 为完成
```

注意到 `dest="command"` 了吗？它告诉 argparse "把用户输入的子命令名存到 `args.command` 变量里"。你可以用 `if args.command == "add"` 判断用户想用哪个子命令。

### 子命令的设计哲学

老潘看着代码，满意地点点头："这才是专业 CLI 工具的样子。每个子命令职责单一，参数清晰。"

他画了一张子命令的设计原则图：

```
git add <file>      → 添加文件到暂存区（位置参数：file）
git commit -m "msg"  → 提交更改（可选参数：-m）
git status          → 查看状态（无参数）

todo add "title"    → 添加任务
todo list --pending → 列出未完成任务
todo done 1         → 标记完成（位置参数：id）
```

"好的子命令设计有三个原则，"老潘说：

**第一，动词命名**。子命令用动词（`add`、`list`、`done`），不是名词（`task`、`item`）。因为用户在做动作——"添加任务"、"列出任务"、"标记完成"。

**第二，参数符合直觉**。`add` 的位置参数是任务标题（必需），`list` 的参数是过滤选项（可选），`done` 的位置参数是任务 ID（必需）。这些符合用户的"心理模型"。

**第三，帮助文档清晰**。每个子命令都有自己的 help 文本，用户可以单独查看：

```bash
python todo.py add --help
# 输出：
# usage: todo.py add [-h] [--priority {low,medium,high}] title
#
# positional arguments:
#   title       任务标题
#
# optional arguments:
#   -h, --help  show this help message and exit
#   --priority  任务优先级
```

阿码试了一下，眼睛一亮："这样我可以单独查看每个子命令的帮助，不用记那么多参数了。"

"对，这就是专业 CLI 工具的标志——用户不需要记住所有参数，工具会告诉他。"

### 把子命令路由到函数

小北看着代码里的 `if args.command == "add"` 逻辑，觉得可以更干净：

```python
# examples/03_subcommands_functions.py
import argparse

def cmd_add(args):
    """添加任务"""
    print(f"添加任务：{args.title}，优先级：{args.priority}")
    return 0  # 成功返回 0

def cmd_list(args):
    """列出任务"""
    if args.all:
        print("列出所有任务")
    elif args.pending:
        print("列出来完成任务")
    else:
        print("列出所有任务（默认）")

def cmd_done(args):
    """标记任务完成"""
    print(f"标记任务 {args.id} 为完成")

# 创建解析器
parser = argparse.ArgumentParser(description="任务管理工具")
subparsers = parser.add_subparsers(dest="command", help="可用命令")

# 添加子命令
add_parser = subparsers.add_parser("add", help="添加新任务")
add_parser.add_argument("title", help="任务标题")
add_parser.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
add_parser.set_defaults(func=cmd_add)  # 设置处理函数

list_parser = subparsers.add_parser("list", help="列出任务")
list_parser.add_argument("--all", action="store_true")
list_parser.add_argument("--pending", action="store_true")
list_parser.set_defaults(func=cmd_list)

done_parser = subparsers.add_parser("done", help="标记任务为完成")
done_parser.add_argument("id", type=int)
done_parser.set_defaults(func=cmd_done)

# 解析并调用
args = parser.parse_args()
if args.command:
    args.func(args)  # 调用对应的函数
else:
    parser.print_help()
```

注意到 `add_parser.set_defaults(func=cmd_add)` 了吗？它告诉 argparse "如果用户用 `add` 子命令，就把 `cmd_add` 函数赋值给 `args.func`"。最后你只需要 `args.func(args)` 就能调用正确的函数。

"这比 `if args.command == "add"` 干净多了，"小北满意地说。

"对，而且每个子命令的逻辑都独立封装在函数里，"老潘补充道，"方便测试和维护。"

---

## 4. 退出码——告诉调用者"成功还是失败"

小北的 todo-cli 工具运行得不错，直到有一天，她写了个自动化脚本：

```bash
#!/bin/bash
# 添加任务，如果成功就打印提示

python todo.py add "写作业"
if [ $? -eq 0 ]; then
    echo "任务添加成功"
else
    echo "任务添加失败"
fi
```

运行脚本，一切看起来正常：

```bash
$ ./my_script.sh
添加任务：写作业
任务添加成功
```

但有一天，她故意传了一个空标题：

```bash
$ python todo.py add ""
错误：任务标题不能为空
```

然后在脚本里运行：

```bash
$ ./my_script.sh
错误：任务标题不能为空
任务添加成功  # ← 等等，这不对！
```

"什么？！"小北盯着屏幕，"明明报错了，为什么脚本还说'任务添加成功'？"

她查了一下 `$?` 的值——居然是 `0`。

"这不对啊，"她想，"失败应该是非 0 才对。"

她跑去问老潘。老潘看了一眼她的代码，笑了笑："你的工具根本没有返回**退出码**（exit code）。默认情况下，Python 程序总是返回 0——就算你报错退出了，退出码还是 0。脚本根本不知道你'失败'了。"

"那怎么告诉它'我失败了'？"

"`sys.exit()`——这就是今天的主角。"

### 退出码的约定

Unix/Linux 系统有一个约定：**退出码 0 表示成功，非 0 表示失败**。

```python
# examples/04_exit_codes.py
import sys
import argparse

parser = argparse.ArgumentParser(description="任务管理工具")
parser.add_argument("title", help="任务标题")
args = parser.parse_args()

# 模拟添加任务的逻辑
if not args.title.strip():
    print("错误：任务标题不能为空", file=sys.stderr)
    sys.exit(1)  # 返回非 0 退出码表示失败

print(f"添加任务：{args.title}")
sys.exit(0)  # 返回 0 退出码表示成功
```

还记得 Week 07 学过的 **包结构** 吗？当你的 CLI 工具变得复杂时，你可以把不同子命令放到不同的模块里（`commands/add.py`、`commands/list.py`），然后在一个主入口文件中导入它们。这让大型 CLI 工具的结构更清晰。

注意到 `file=sys.stderr` 了吗？错误消息应该输出到**标准错误流**（stderr），而不是标准输出流（stdout）。这样脚本可以分别捕获正常输出和错误消息。

运行：

```bash
python todo.py "写作业"
echo $?
# 输出：0

python todo.py ""
echo $?
# 输出：1
```

现在脚本可以正确判断了：

```bash
#!/bin/bash
python todo.py "写作业"
if [ $? -eq 0 ]; then
    echo "任务添加成功"
else
    echo "任务添加失败"
fi
```

### 常见退出码约定

虽然你可以用任何非 0 值表示失败，但有一些常见的约定：

| 退出码 | 含义 | 示例场景 |
|--------|------|----------|
| 0 | 成功 | 命令正常执行完毕 |
| 1 | 一般性错误 | 参数错误、文件不存在 |
| 2 | 误用 shell 命令 | 参数太多或太少 |
| 126 | 命令无法执行 | 没有执行权限 |
| 127 | 命令未找到 | 敲错了命令名 |
| 130 | 被 Ctrl+C 中断 | 用户主动终止 |
| 其他 | 应用特定错误 | 自定义错误类型 |

"不要过度设计退出码，"老潘提醒道，"大多数情况下，0 表示成功，1 表示失败就够了。除非你有非常明确的区分需求（比如'文件不存在'用 2，'权限不足'用 3），否则不要搞太多退出码。"

小北想起自己之前写过一个工具，用了 10 多种退出码，结果后来自己也记不住哪个数字对应什么错误。"好吧，我会保持简单。"

### 在子命令中使用退出码

结合第 3 节的子命令架构，每个子命令可以返回不同的退出码：

```python
# examples/04_exit_codes_subcommands.py
import sys
import argparse

def cmd_add(args):
    """添加任务"""
    if not args.title.strip():
        print("错误：任务标题不能为空", file=sys.stderr)
        return 1  # 返回失败退出码
    print(f"添加任务：{args.title}")
    return 0  # 返回成功退出码

def cmd_done(args):
    """标记任务完成"""
    # 模拟：如果任务 ID 不存在
    if args.id < 1 or args.id > 100:
        print(f"错误：任务 ID {args.id} 不存在", file=sys.stderr)
        return 1
    print(f"标记任务 {args.id} 为完成")
    return 0

# 创建解析器
parser = argparse.ArgumentParser(description="任务管理工具")
subparsers = parser.add_subparsers(dest="command", help="可用命令")

add_parser = subparsers.add_parser("add", help="添加新任务")
add_parser.add_argument("title", help="任务标题")
add_parser.set_defaults(func=cmd_add)

done_parser = subparsers.add_parser("done", help="标记任务为完成")
done_parser.add_argument("id", type=int)
done_parser.set_defaults(func=cmd_done)

# 解析并调用
args = parser.parse_args()
if args.command:
    exit_code = args.func(args)
    sys.exit(exit_code)
else:
    parser.print_help()
    sys.exit(1)
```

注意到每个命令函数都返回退出码（0 或 1），最后用 `sys.exit(exit_code)` 统一退出。这样每个子命令都可以独立判断成功或失败。

还记得 Week 07 学过的 **`__name__` 守卫** 吗？在实际的 CLI 工具中，你需要在主入口文件加上：

```python
if __name__ == "__main__":
    main()
```

这确保了当你直接运行 `python todo_cli.py` 时才会执行 argparse 逻辑，而当其他模块 `import todo_cli` 时不会自动执行。这是 Python 模块化的基础。

### 测试退出码

Week 08 你学过 pytest，现在可以测试 CLI 的退出码：

```python
# tests/test_cli_exit_codes.py
import pytest
import subprocess

def test_add_success():
    """测试成功添加任务"""
    result = subprocess.run(
        ["python", "todo.py", "add", "写作业"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0  # 退出码应该是 0
    assert "添加任务" in result.stdout

def test_add_empty_title():
    """测试空标题应该失败"""
    result = subprocess.run(
        ["python", "todo.py", "add", ""],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1  # 退出码应该是 1
    assert "错误" in result.stderr

def test_done_invalid_id():
    """测试无效 ID 应该失败"""
    result = subprocess.run(
        ["python", "todo.py", "done", "999"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "不存在" in result.stderr
```

`subprocess.run()` 可以在测试中运行 CLI 工具并捕获退出码、标准输出和错误输出。这和 Week 08 学的**TDD 循环**一样——你先定义"什么算成功/失败"，再写测试验证，最后实现确保测试通过。

> **AI 时代小专栏：退出码与脚本自动化——AI 时代 DevOps 的基础**
>
> 退出码看起来是个小细节，但在自动化脚本和 CI/CD（持续集成/持续部署）流水线中至关重要。如果 CLI 工具不返回正确的退出码，自动化脚本无法判断"这步是否成功"，整个流水线就会失控。
>
> Unix/Linux 系统有一个约定：每个命令返回退出码，0 表示成功，非 0 表示失败。Bash 脚本用 `$?` 获取上一个命令的退出码，CI/CD 工具（Jenkins、GitHub Actions、GitLab CI）都依赖退出码来判断流水线步骤是否成功。[Bash 自动化的 DevOps 路线图](https://medium.com/@sainath.814/devops-roadmap-part-18-bash-scripting-shell-automation-variables-loops-functions-235b85a2f00e)强调，退出码是简化流程和增强管道可靠性的核心机制。
>
> 现实案例：从 Bash 到 GitHub Actions 的自动化演进中，退出码是错误处理的核心。[一个实战案例](https://infosecwriteups.com/from-bash-to-github-actions-automating-cicd-for-a-real-world-saas-project-d89b251cd371)显示，正确的退出码设计可以让 CI/CD 流水线在失败时立即停止，避免浪费资源。甚至测试工具（如 Playwright）也依赖退出码来报告测试结果——[GitHub 上有专门的讨论](https://github.com/microsoft/playwright/issues/14109)如何为不同的测试失败定义不同的退出码。
>
> 更重要的是，**退出码是脚本和 AI 工具的"共同协议"**。当你写出 `sys.exit(1)` 时，AI 工具（如 GitHub Actions 的 AI 助手）能理解"这里失败了"，可以自动触发重试或回滚。但如果你忘记返回退出码，AI 也无能为力。[Linux 和 Jenkins 的退出码实践](https://www.linkedin.com/pulse/linux-jenkins-understanding-exit-codes-smarter-prem-raj-vulli-6a1lc)指出，退出码是人和 AI 的共同语言——理解这个协议，才能让自动化工具真正为你服务。
>
> 实践建议：
> - 每个 CLI 命令都应该返回明确的退出码（0 成功，1 失败）
> - 错误消息输出到 `stderr`（`print(..., file=sys.stderr)`）
> - 用 pytest + subprocess 测试退出码（就像你本周学的那样）
> - 在 CI/CD 流水线中，确保"失败就停止"（`set -e` in Bash）
>
> 所以退出码不是老古董——它是 AI 时代自动化脚本和 DevOps 的基础设施。你刚学的 `sys.exit(0)` 和 `sys.exit(1)`，正是让脚本和 AI 工具"理解"你的程序是否成功的关键。
>
> 参考（访问日期：2026-02-09）：
> - [DevOps Roadmap: Bash Scripting & Shell Automation](https://medium.com/@sainath.814/devops-roadmap-part-18-bash-scripting-shell-automation-variables-loops-functions-235b85a2f00e)
> - [Error handling in bash](https://notifox.com/blog/bash-error-handling)
> - [List of exit status codes in Linux](https://medium.com/@himanshurahangdale153/list-of-exit-status-codes-in-linux-f4f00c46c9e0)
> - [Linux and Jenkins: Understanding Exit Codes for Smarter CI/CD](https://www.linkedin.com/pulse/linux-jenkins-understanding-exit-codes-smarter-prem-raj-vulli-6a1lc)
> - [From Bash to GitHub Actions: Automating CI/CD](https://infosecwriteups.com/from-bash-to-github-actions-automating-cicd-for-a-real-world-saas-project-d89b251cd371)
> - [Define different exit codes for CI/CD - Playwright issue](https://github.com/microsoft/playwright/issues/14109)

---

## 5. 日志记录——让程序"说话"到文件

小北的 todo-cli 工具已经能添加任务、列出任务、标记完成了。但有一天，她发现了一个问题：用户说"昨天我添加了一个任务，但今天不见了"，但小北不知道发生了什么——没有记录，无法追踪。

"你需要**日志**（logging），"老潘说，"把程序的运行信息记录到文件里，这样出问题时可以追溯。"

阿码在旁边说："那我用 `print()` 不就行了？"

```python
print("添加任务：写作业")
```

老潘摇摇头："`print` 就像在路边大喊——声音很大，但风一吹就没了。`logging` 才像写日记——记下来，以后还能翻。"

他打了个比方："想象你在做菜。`print` 就像你边做边喊'我现在加盐了'——当时能听见，但过后没人记得你加了多少。`logging` 就像你拿个小本子记下来'14:30 加盐 3 克'——三个月后还能翻出来对照。"

"而且，"老潘继续说，"`print` 分不清轻重缓急。但 `logging` 知道哪些是闲话（DEBUG），哪些是正事（INFO），哪些是警告（WARNING），哪些是出错了（ERROR）。"

### logging vs print

具体来说，logging 和 print 的区别是：

| 维度 | print | logging |
|------|-------|---------|
| 目标 | 输出到终端（stdout） | 输出到文件、终端、网络等 |
| 级别 | 无 | DEBUG/INFO/WARNING/ERROR/CRITICAL |
| 时间戳 | 无 | 自动添加 |
| 格式化 | 需手动拼接 | 自动格式化 |
| 生产环境 | 不适合 | 专为生产设计 |

先看一个简单的 logging 例子：

```python
# examples/05_logging_first.py
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="todo.log"
)

# 使用日志
logging.info("添加任务：写作业")
logging.warning("任务标题为空")
logging.error("任务 ID 999 不存在")
```

运行后，`todo.log` 文件内容：

```
2026-02-09 14:30:15,123 - INFO - 添加任务：写作业
2026-02-09 14:30:16,456 - WARNING - 任务标题为空
2026-02-09 14:30:17,789 - ERROR - 任务 ID 999 不存在
```

注意到时间戳自动添加了吗？logging 模块会记录每条日志的时间、级别和消息——这在排查问题时非常有用。

### 日志级别

logging 有 5 个级别，从低到高：

| 级别 | 数值 | 何时使用 | 示例 |
|------|------|----------|------|
| DEBUG | 10 | 调试信息 | `变量 x 的值是 5` |
| INFO | 20 | 正常运行信息 | `添加任务：写作业` |
| WARNING | 30 | 警告（但不影响运行） | `任务标题为空，使用默认值` |
| ERROR | 40 | 错误（影响部分功能） | `任务 ID 不存在` |
| CRITICAL | 50 | 严重错误（程序无法继续） | `数据库连接失败，程序退出` |

日志级别的意义是**过滤**——你可以设置 `level=logging.WARNING`，这样只有 WARNING 及以上的日志会被记录，DEBUG 和 INFO 会被忽略。

```python
# 只记录 WARNING 及以上
logging.basicConfig(level=logging.WARNING)

logging.debug("这是调试信息")  # 不会记录
logging.info("这是正常信息")   # 不会记录
logging.warning("这是警告")    # 会记录
logging.error("这是错误")      # 会记录
```

"为什么要过滤？"小北问。

"生产环境中，DEBUG 和 INFO 日志太多了，"老潘说，"你只关心'出了什么问题'，所以只记录 WARNING 和 ERROR。但开发时，你可以设置 `level=logging.DEBUG`，看到所有日志。"

### 在 CLI 工具中使用 logging

把 logging 集成到 todo-cli 中：

```python
# examples/05_logging_cli.py
import argparse
import logging
import sys

# 配置日志（全局）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="todo.log"
)

# 创建 logger
logger = logging.getLogger(__name__)

def cmd_add(args):
    """添加任务"""
    logger.info(f"尝试添加任务：{args.title}")

    if not args.title.strip():
        logger.warning("任务标题为空")
        print("错误：任务标题不能为空", file=sys.stderr)
        return 1

    # 模拟添加任务的逻辑
    logger.info(f"任务添加成功：{args.title}")
    print(f"添加任务：{args.title}")
    return 0

def cmd_list(args):
    """列出任务"""
    logger.info("列出任务")
    print("列出所有任务")
    return 0

# 创建解析器
parser = argparse.ArgumentParser(description="任务管理工具")
subparsers = parser.add_subparsers(dest="command", help="可用命令")

add_parser = subparsers.add_parser("add", help="添加新任务")
add_parser.add_argument("title", help="任务标题")
add_parser.set_defaults(func=cmd_add)

list_parser = subparsers.add_parser("list", help="列出任务")
list_parser.set_defaults(func=cmd_list)

# 添加 --verbose 参数控制日志级别
parser.add_argument("--verbose", action="store_true", help="显示详细日志")

# 解析
args = parser.parse_args()

# 如果 --verbose，调整日志级别
if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    logger.debug("verbose 模式已启用")

if args.command:
    exit_code = args.func(args)
    sys.exit(exit_code)
else:
    parser.print_help()
    sys.exit(1)
```

注意到 `--verbose` 参数了吗？用户可以控制日志详细程度：

```bash
# 正常模式（INFO 级别）
python todo.py add "写作业"

# 详细模式（DEBUG 级别）
python todo.py --verbose add "写作业"
```

`todo.log` 文件会记录所有操作：

```
2026-02-09 14:30:15,123 - __main__ - INFO - 尝试添加任务：写作业
2026-02-09 14:30:15,124 - __main__ - INFO - 任务添加成功：写作业
2026-02-09 14:30:16,456 - __main__ - INFO - 列出任务
```

### logging 的最佳实践

老潘分享了几条 logging 的最佳实践：

**第一，不要用 logging 记录敏感信息**。密码、令牌、个人隐私等不要记录到日志，因为日志文件可能被其他用户或工具读取。

**第二，用合适的日志级别**。DEBUG 开发时用，INFO 记录正常操作，WARNING 记录"不致命的问题"，ERROR 记录"功能失败"，CRITICAL 记录"程序无法继续"。

**第三，日志消息要清晰**。不要写 `logging.info("出错了")`，要写 `logging.info(f"任务 {task_id} 添加失败：{reason}")` —— 三个月后看日志你还能明白发生了什么。

**第四，生产环境不要用 DEBUG 级别**。DEBUG 日志太多了，会影响性能和磁盘空间。生产环境通常用 INFO 或 WARNING。

阿码问："那如果我想把日志同时输出到文件和终端呢？"

"需要用 `logging.Handler`，"老潘说，"一个 Handler 写文件，一个 Handler 写终端。但这个有点复杂，你先用 `basicConfig` 够用了。等有需求再学高级用法。"

小北满意地点点头："现在我的工具有日志了，出问题可以追溯。"

---

## PyHelper 进度

上周你给 PyHelper 加上了 dataclass 数据模型和类型提示。这周，让 PyHelper 变成一个真正的 CLI 工具——像 `git`、`docker` 那样，通过命令行交互。

### 从"调用函数"到"命令行工具"

之前 PyHelper 的使用方式是这样的：

```python
# 旧方式：在代码里调用
from pyhelper.core import add_note, list_notes

note = add_note("今天学了 argparse")
list_notes()
```

现在，PyHelper 变成 CLI 工具：

```bash
# 新方式：通过命令行
pyhelper add "今天学了 argparse"
pyhelper list --pending
pyhelper search "argparse"
pyhelper export --format json
pyhelper stats
```

### argparse 主入口

创建 `cli.py` 作为 CLI 入口：

```python
# examples/pyhelper/cli.py
import argparse
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

# 导入核心功能
from core import Note, NoteStatus, add_note, list_notes, search_notes, export_notes
from storage import load_notes, save_notes

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="pyhelper.log"
)
logger = logging.getLogger(__name__)

# 数据文件路径
DATA_FILE = Path.home() / ".pyhelper" / "notes.json"

def cmd_add(args):
    """添加学习笔记"""
    logger.info(f"添加笔记：{args.content}")

    # 加载现有笔记
    notes = load_notes(DATA_FILE)

    # 创建新笔记
    note = Note(
        id=datetime.now().strftime('%Y%m%d-%H%M%S'),
        content=args.content,
        tags=args.tags.split(",") if args.tags else [],
        status=NoteStatus.DRAFT
    )

    # 保存
    notes.append(note)
    save_notes(DATA_FILE, notes)

    print(f"✓ 笔记已添加：{note.id}")
    return 0

def cmd_list(args):
    """列出笔记"""
    logger.info("列出笔记")

    notes = load_notes(DATA_FILE)

    # 过滤
    if args.pending:
        notes = [n for n in notes if n.status == NoteStatus.DRAFT]
    elif args.published:
        notes = [n for n in notes if n.status == NoteStatus.PUBLISHED]

    # 显示
    for note in notes:
        status_icon = "✓" if note.status == NoteStatus.PUBLISHED else "○"
        print(f"{status_icon} [{note.id}] {note.content[:50]}...")

    print(f"\n共 {len(notes)} 条笔记")
    return 0

def cmd_search(args):
    """搜索笔记"""
    logger.info(f"搜索笔记：{args.keyword}")

    notes = load_notes(DATA_FILE)
    results = search_notes(notes, args.keyword)

    print(f"找到 {len(results)} 条匹配笔记：")
    for note in results:
        print(f"  - {note.content[:50]}...")

    return 0

def cmd_export(args):
    """导出笔记"""
    logger.info(f"导出笔记：{args.format}")

    notes = load_notes(DATA_FILE)
    export_notes(notes, args.output, args.format)

    print(f"✓ 已导出到 {args.output}")
    return 0

def cmd_stats(args):
    """显示统计信息"""
    logger.info("生成统计")

    notes = load_notes(DATA_FILE)

    total = len(notes)
    draft = len([n for n in notes if n.status == NoteStatus.DRAFT])
    published = len([n for n in notes if n.status == NoteStatus.PUBLISHED])
    archived = len([n for n in notes if n.status == NoteStatus.ARCHIVED])

    print("PyHelper 统计")
    print("=" * 30)
    print(f"总笔记数：{total}")
    print(f"  - 草稿：{draft}")
    print(f"  - 已发布：{published}")
    print(f"  - 已归档：{archived}")

    if args.json:
        import json
        stats = {
            "total": total,
            "draft": draft,
            "published": published,
            "archived": archived
        }
        print("\nJSON 格式：")
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    return 0

def main():
    """主入口"""
    parser = argparse.ArgumentParser(description="PyHelper - 命令行学习助手")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # add 子命令
    add_parser = subparsers.add_parser("add", help="添加学习笔记")
    add_parser.add_argument("content", help="笔记内容")
    add_parser.add_argument("--tags", help="标签（逗号分隔）")
    add_parser.set_defaults(func=cmd_add)

    # list 子命令
    list_parser = subparsers.add_parser("list", help="列出笔记")
    group = list_parser.add_mutually_exclusive_group()
    group.add_argument("--pending", action="store_true", help="只显示草稿")
    group.add_argument("--published", action="store_true", help="只显示已发布")
    list_parser.set_defaults(func=cmd_list)

    # search 子命令
    search_parser = subparsers.add_parser("search", help="搜索笔记")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.set_defaults(func=cmd_search)

    # export 子命令
    export_parser = subparsers.add_parser("export", help="导出笔记")
    export_parser.add_argument("--output", "-o", default="backup.json", help="输出文件")
    export_parser.add_argument("--format", choices=["json", "csv"], default="json", help="导出格式")
    export_parser.set_defaults(func=cmd_export)

    # stats 子命令
    stats_parser = subparsers.add_parser("stats", help="统计信息")
    stats_parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    stats_parser.set_defaults(func=cmd_stats)

    # 全局参数
    parser.add_argument("--verbose", action="store_true", help="详细日志")

    # 解析
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("verbose 模式已启用")

    # 执行
    if args.command:
        # 确保数据目录存在
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        exit_code = args.func(args)
        sys.exit(exit_code)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 安装为系统命令

如果想直接敲 `pyhelper add` 而不是 `python cli.py add`，可以创建一个入口脚本：

```bash
# 创建 ~/.local/bin/pyhelper
cat > ~/.local/bin/pyhelper << 'EOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, "/path/to/pyhelper")
from cli import main
sys.exit(main())
EOF

# 添加执行权限
chmod +x ~/.local/bin/pyhelper

# 确保 ~/.local/bin 在 PATH 中
export PATH="$HOME/.local/bin:$PATH"
```

现在可以直接用：

```bash
pyhelper add "今天学了 argparse"
pyhelper list --pending
pyhelper stats --json
```

老潘看到这个工具，满意地点点头："这才是专业 CLI 工具的样子——子命令清晰、参数合理、有日志、有退出码。"

小北也很满意："现在 PyHelper 不只是个 Python 脚本，而是一个真正的命令行工具了！"

---

## Git 本周要点

本周必会命令：
- `git status` —— 查看当前状态
- `git diff` —— 查看具体修改内容
- `git add -A` —— 添加所有修改
- `git commit -m "message"` —— 提交修改
- `git log --oneline -n 10` —— 查看最近 10 次提交

常见坑：
- **参数顺序错误**：argparse 的位置参数必须按顺序传，`python todo.py "写作业"` 不能写成 `python todo.py --priority high "写作业"`
- **退出码忘记返回**：如果不用 `sys.exit()`，Python 默认返回 0（即使出错了）
- **日志级别设置不当**：生产环境用 `DEBUG` 级别会产生大量日志，影响性能
- **stderr vs stdout**：错误消息应该输出到 `stderr`（`print(..., file=sys.stderr)`），而不是 `stdout`

Pull Request (PR)：
- 本周延续 PR 流程：分支 → 多次提交 → push → PR → review → merge
- PR 描述模板：
  ```markdown
  ## 本周做了什么
  - 学习了 argparse 的基本用法
  - 实现了子命令架构（add/list/done/delete/stats）
  - 理解了退出码的概念
  - 掌握了 logging 的基础用法
  - 为 PyHelper 实现了完整的 CLI 界面

  ## 自测
  - [ ] 运行 `python3 -m pytest chapters/week_12/tests -q` 通过
  - [ ] todo-cli 所有子命令能正常工作
  - [ ] 退出码测试通过
  - [ ] PyHelper CLI 能正常运行

  ## 待 review
  请重点检查 argparse 参数设计和退出码处理
  ```

---

## 本周小结（供下周参考）

"我有个感悟，"小北合上电脑，"这周学的不是'怎么写 argparse'，而是'怎么设计工具'。"

老潘抬头看她："怎么说？"

"你看，"小北翻开笔记，"`add` 的位置参数是任务标题（必需），`list` 的参数是过滤选项（可选）——这些都是'设计决策'，不是技术细节。我以前只会写代码，现在学会了'思考用户怎么用'。"

阿码在旁边补充："而且退出码和 logging 也是——不是'怎么写'，而是'怎么负责任'。退出码是对调用者负责，logging是对未来的自己负责。"

老潘笑了："恭喜你们，从'写代码的人'进化成'设计工具的人'了。"

本周你完成了从"脚本"到"命令行工具"的跃迁——学会了用 argparse 解析命令行参数，用子命令架构组织功能，用退出码告诉调用者执行结果，用 logging 记录程序运行信息。这些不只是技术技能，更是**工程思维的体现**——你在设计"别人（包括未来的你）如何使用你的程序"。

还记得 Week 01 你写下第一个 `print("Hello")` 吗？那时的程序只能"自说自话"，没有交互。Week 02 你学了 `input()`，可以和用户对话，但得在代码里调用函数。现在，你的工具可以通过命令行参数和子命令与世界交互——像 `git`、`docker`、`pytest` 那样，成为其他脚本和工具可以调用的"组件"。

小北感叹："原来 CLI 工具不只是'命令行界面'，更是'程序的接口设计'——就像 API 设计，只不过是用命令行而不是 HTTP。"

下周我们将进入 Week 13：Agentic 团队工作流——学习用 agent team 模式协作，用 review checklist 审查代码，用失败驱动迭代改进。CLI 工具提供了"命令行界面"，agent team 将提供"协作工作流"——你将从"单兵作战"进入"团队协作"的模拟环境。

---

## Definition of Done（学生自测清单）

完成本周学习后，请确认你能做到以下事情：

**核心技能**：你能用 `argparse.ArgumentParser()` 创建命令行解析器，能用 `add_argument()` 添加位置参数和可选参数；能用 `add_subparsers()` 创建子命令架构；能用 `sys.exit()` 返回正确的退出码；能用 `logging` 模块记录日志。

**编程哲学**：你理解**专业 CLI 工具的设计原则**——参数符合直觉、帮助文档清晰、错误消息友好、日志可追溯。你知道**退出码**在自动化脚本中的重要性——0 表示成功，非 0 表示失败。

**实践能力**：你能设计和实现一个多子命令的 CLI 工具（类似 Git）；能为每个子命令设置合适的参数和默认值；能用 pytest + subprocess 测试 CLI 的退出码；能为 PyHelper 实现完整的 CLI 界面。

**工程习惯**：你至少提交了 2 次 Git（draft + verify），并且运行 `python3 -m pytest chapters/week_12/tests -q` 通过了所有测试。

---

**如果你想验证自己的掌握程度**，试着回答这些问题：

- argparse 和手写 `sys.argv` 解析有什么区别？
- 什么时候用位置参数，什么时候用可选参数？
- 子命令架构有什么优势？如何用 argparse 实现？
- 退出码是什么？为什么它对自动化脚本很重要？
- logging 和 print 的区别是什么？什么时候用 logging？
- 如何用 pytest 测试 CLI 工具的退出码？

如果你能自信地回答这些问题，说明你已经掌握了本周的核心内容。

---

<!--
章节结构骨架（供 chapter-writer 参考）：

1. 章首导入（引言格言 + 时代脉搏）——由 prose-polisher 填写
2. 前情提要——由 chapter-writer 根据上周小结填写
3. 学习目标——已完成
4. 贯穿案例设计说明（HTML 注释）——已完成
5. 认知负荷 + 回顾桥 + 角色出场规划（HTML 注释）——已完成
6. AI 小专栏规划（HTML 注释）——已完成
7. 第 1 节：从脚本到工具——你的第一个 argparse 程序——由 chapter-writer 撰写
8. 第 2 节：让命令更灵活——可选参数与默认值——由 chapter-writer 撰写
9. AI 小专栏 #1——由 prose-polisher 填写（放在第 2 节之后）
10. 第 3 节：子命令架构——像 Git 一样组织功能——由 chapter-writer 撰写
11. 第 4 节：退出码——告诉调用者"成功还是失败"——由 chapter-writer 撰写
12. AI 小专栏 #2——由 prose-polisher 填写（放在第 4 节之后）
13. 第 5 节：日志记录——让程序"说话"到文件——由 chapter-writer 撰写
14. PyHelper 进度——由 chapter-writer 撰写
15. Git 本周要点——已完成
16. 本周小结（供下周参考）——由 chapter-writer 填写
17. Definition of Done——已完成
-->
