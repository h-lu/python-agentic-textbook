# Week 02：让程序做选择

> "The computer is incredibly fast, accurate, and stupid. Man is incredibly slow, inaccurate, and brilliant. The marriage of the two is a force beyond calculation."
> — Leo Cherne, 经济学家与政策顾问

2026 年初，DeepMind 发布的 AlphaGeometry 在国际数学奥林匹克竞赛中达到了银牌水平——它能自动完成几何证明题的推导步骤。更早的 AlphaGo 早就在围棋这种"纯决策"游戏上击败了人类冠军。这些系统有一个共同点：它们的核心是"做选择"——根据不同的情况采取不同的策略。本周，你将赋予 Python 程序做选择的能力。这不只是写几个 `if` 语句，而是让程序从"死板地执行命令"进化为"能根据情况灵活应对"的智能体。

---

## 前情提要

上周你学会了让程序说话、记东西、和用户聊天。你的名片生成器已经可以交互式地收集信息并漂亮地输出了。但有一个问题：程序还不会"做选择"——不管用户输入什么，它都会照单全收，然后按固定流程输出。如果用户输入年龄为 -5 呢？如果邮箱格式明显不对呢？程序目前没有能力判断和处理这些情况。本周，我们就要解决这个问题。

---

## 学习目标

完成本周学习后，你将能够：

1. 使用 `if`/`elif`/`else` 语句让程序根据条件执行不同代码块
2. 编写布尔表达式，理解比较运算符和逻辑运算符
3. 使用 `for` 循环重复执行指定次数的任务
4. 使用 `while` 循环在条件满足时持续执行
5. 用 `range()` 函数生成数字序列
6. 理解 Python 的缩进规则，避免缩进错误
7. 使用 `break` 和 `continue` 控制循环流程（延伸）

---

<!--
贯穿案例：猜数字游戏

演进路线：
- 第 1 节（if/elif/else）：单次判断版——用户猜一次，程序只告诉"大了""小了""猜对了"
- 第 2 节（while 循环）：让用户反复猜，直到猜中为止
- 第 3 节（for 循环 + range）：限制猜测次数（如最多 5 次），增加游戏紧张感
- 第 4 节（布尔表达式 + 逻辑运算）：增加游戏难度选择（简单/中等/困难），影响数字范围

最终成果：一个完整的猜数字游戏，有难度选择、次数限制、胜负判定
-->

<!--
认知负荷预算：
- 本周新概念（4 个，预算上限 4 个）：
  1. 条件判断（if/elif/else）
  2. 布尔表达式（比较运算符 + 逻辑运算符）
  3. for 循环
  4. while 循环
- 延伸概念（不计入预算，作为延伸）：
  - range 函数（for 循环的工具）
  - break/continue 语句（控制流程）
- 结论：✅ 在预算内

回顾桥设计（至少引用 Week 01 的 2 个概念）：
- [print]（来自 week_01）：在第 1 节，用 print 输出"大了""小了"的提示
- [input]（来自 week_01）：在第 1 节，用 input 获取用户猜测的数字
- [变量]（来自 week_01）：在第 2 节，用变量记录是否猜中的状态
- [f-string]（来自 week_01）：在第 3 节，用 f-string 显示剩余次数
- [int() 转换]（来自 week_01 的延伸内容）：在第 1 节，将 input() 返回的字符串转为整数
-->

<!--
角色出场规划：
- 小北（第 1 节）：写 if guess == secret 时忘记写冒号，引出语法错误
- 小北（第 2 节）：写 while 循环时忘记更新变量，导致无限循环
- 阿码（第 3 节）：追问"range(5) 为什么是从 0 开始不是 1？"，引出左闭右开区间
- 老潘（第 4 节）：给出工程建议——"布尔表达式太复杂时，用变量给它起个名字"

总出场次数：4 次（3 个不同角色），满足每章至少 2 次的要求
-->

<!--
AI 小专栏规划：

专栏 #1（放在第 1 节之后）：
- 主题：AI 怎样"做选择"？
- 连接点：与第 1 节的条件判断呼应——AI 内部也是无数个 if/else 分支
- 建议搜索词："AI decision trees 2026", "machine learning conditional logic 2026"

专栏 #2（放在第 3 节之后）：
- 主题：AI 代码补全的原理
- 连接点：与第 3 节的循环和迭代呼应——AI 模型通过无数次迭代训练
- 建议搜索词："GitHub Copilot code completion mechanism 2026", "AI code generation training process 2026"
-->

## 1. 如果这样，那就那样

到目前为止，你的程序是"一条路走到黑"的——从第一行执行到最后一行，不管中间发生了什么。这就像一个只会说"是"的人，不管你问什么都点头。

真实世界不是这样的。你会根据情况做决定：如果下雨就带伞，如果饿了就吃饭，如果困了就睡觉。程序也需要这种能力。

Python 里做决定的语句叫 `if`（如果）。来看最简单的例子：

```python
age = int(input("请输入你的年龄："))

if age >= 18:
    print("你已经成年了")
```

这还是上周你用过的 `input 函数`和 `print 函数`——`input` 获取用户输入，`print` 输出信息到屏幕。区别在于，现在加上了 `if` 语句，程序可以根据输入内容"做选择"了。

`age >= 18` 是一个**条件**（condition）。如果这个条件为真（True），就执行缩进的代码块；如果为假（False），就跳过。

小北照着教材敲完代码，自信满满地按下回车——然后 Python 用红色大字教育了他：

```
SyntaxError: invalid syntax
```

"等等，我哪里写错了？"小北盯着屏幕，反复检查了三遍，甚至数了空格数量。

你发现问题了吗？他写的是：

```python
if age >= 18
    print("你已经成年了")
```

漏掉了冒号 `:`。在 Python 里，`if` 语句的末尾必须有冒号——这是 Python 在说"我要开始说条件了"，就像讲故事前先清清嗓子。没有冒号，Python 就不知道你接下来要说啥。

现在来完善一下，加上"否则"的情况：

```python
age = int(input("请输入你的年龄："))

if age >= 18:
    print("你已经成年了")
else:
    print("你还未成年")
```

`else`（否则）处理条件不满足的情况。注意 `else` 后面也有冒号，而且它不需要条件——因为 `else` 就是"否则"的意思，就像一个不会追问"为什么"的听话孩子。

如果你想判断多种情况呢？用 `elif`（else if 的缩写）：

```python
score = int(input("请输入你的考试分数："))

if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

`elif` 让你可以连续判断多个条件。Python 会从上到下检查，遇到第一个为真的条件就执行对应的代码块，然后跳过剩余的所有判断。

这里有个重要细节：这些判断是有**顺序**的。如果你把 `score >= 60` 放在最前面，那么 85 分也会被判定为"及格"，因为它满足第一个条件，后面就不检查了。

现在把这些知识应用到我们的贯穿案例上——猜数字游戏的最简版本：

```python
secret = 42
guess = int(input("猜一个数字（1-100）："))

if guess == secret:
    print("恭喜你，猜对了！")
elif guess < secret:
    print("太小了")
else:
    print("太大了")
```

运行一次，猜一个数字，程序告诉你结果。但只能猜一次，这太没意思了。能不能让用户反复猜，直到猜中为止？这就是下一节的内容。

> **AI 时代小专栏：AI 怎样"做选择"？**
>
> 你刚写的 `if/elif/else` 语句，本质上是在"做决策"。有意思的是，世界上最先进的 AI 系统——从你手机里的语音助手到自动驾驶汽车——内部也是无数个这样的条件判断在层层嵌套。
>
> 机器学习里有一个经典算法叫**决策树**（decision tree），它的结构就像一个巨大的 `if/elif/else` 嵌套组合。想象一下"Guess Who?"游戏：你通过一系列"是/否"问题（"他戴眼镜吗？""她的头发是深色的吗？"）来缩小猜测范围。决策树就是这个原理——通过成千上万个 `IF 特征 A > 阈值 THEN 预测类别 X` 的判断，最终得出结果。
>
> 2026 年，决策树仍然是十大最重要的机器学习算法之一，广泛用于医疗诊断、欺诈检测、推荐系统等领域。你今天学的条件判断逻辑，就是理解这些 AI 系统的基础。当然，现代 AI 的决策树不是人手写的，而是通过数据"训练"出来的——但核心思想和你写的 `if score >= 90: print("优秀")` 并没有本质区别。
>
> 参考（访问日期：2026-02-08）：
> - https://medium.com/@brentwash35/understanding-decision-trees-the-machine-learning-algorithm-that-thinks-like-you-do-4e20a18b7172
> - https://estha.ai/blog/everything-you-need-to-know-about-if-then-logic-applications-from-basics-to-advanced-use-cases/
> - https://shiftmag.dev/how-guess-who-logic-shapes-ai-decision-trees-and-predictive-ml-5874/

## 2. 让它一直猜，直到猜中

上一节的猜数字游戏有个尴尬的问题：用户只能猜一次。如果没猜中，程序就结束了，用户得重新运行才能再猜。这体验很糟糕——就像考试只给你一次机会，考完直接离场。

我们希望程序"一直问，直到猜中为止"。这就是**循环**（loop）的概念。

Python 里最简单的循环是 `while`（当……的时候）：

```python
secret = 42

while True:
    guess = int(input("猜一个数字（1-100）："))

    if guess == secret:
        print("恭喜你，猜对了！")
        break
    elif guess < secret:
        print("太小了，再试一次")
    else:
        print("太大了，再试一次")
```

`while True` 的意思是"永远重复"。字面看像是个糟糕的主意——程序岂不是要跑到天荒地老？别急，`break` 语句会"跳出循环"——当用户猜对时，程序就会退出循环，结束运行。就像紧急出口，平时用不上，关键时刻救命。

小北兴奋地写下了这段代码，运行后猜对了数字——程序打印了"恭喜你"，但还没等他高兴完，屏幕上又出现了"猜一个数字"的提示。

"怎么回事？我明明写了 `break` 啊？"小北盯着屏幕，有点慌。

我们来帮他看看问题：

```python
if guess == secret:
    print("恭喜你，猜对了！")
# 小北忘记写 break 了！
```

原来如此。小北太激动，写完 `print` 就忘了 `break`。没有 `break`，循环就会一直执行下去，变成一个**无限循环**（infinite loop）。如果遇到这种情况，按 `Ctrl + C` 可以强制停止程序。

`while` 循环的另一种常见写法是带条件：

```python
secret = 42
guess = 0  # 初始化为一个不等于 secret 的值

while guess != secret:
    guess = int(input("猜一个数字（1-100）："))

    if guess < secret:
        print("太小了")
    elif guess > secret:
        print("太大了")

print("恭喜你，猜对了！")
```

这里的条件是 `guess != secret`（猜的不等于答案）。只要这个条件为真，循环就继续；一旦猜中（条件变为假），循环结束。

现在你的猜数字游戏已经能反复猜测了。但还有一个问题：有些玩家可能会猜几十次才猜中，这让游戏失去了挑战性。能不能限制猜测次数？比如最多 5 次。这需要用到另一种循环——`for` 循环。

## 3. 数到几就停

上一节的 `while` 循环有个问题：你永远不知道用户要猜多少次。运气好的人 3 次就猜中，运气不好的人可能猜 20 次。如果你想"让游戏更刺激一点"——比如最多只能猜 5 次——就需要一种新的工具。

这就是 `for` 循环的用武之地。`while` 说"一直做，直到条件不满足"，`for` 说"做 N 次，然后就停"。两种循环看似相似，但适用于完全不同的场景。

`for` 循环需要一个"计数器"，Python 里通常用 `range()` 函数来生成数字序列：

```python
for i in range(5):
    print(f"第 {i + 1} 次循环")
```

输出：

```
第 1 次循环
第 2 次循环
第 3 次循环
第 4 次循环
第 5 次循环
```

阿码在旁边看了一眼，突然举手："等等，`range(5)` 产生的是 0, 1, 2, 3, 4，不是 1, 2, 3, 4, 5？这有点反直觉啊。"

确实如此。`range(5)` 生成的是从 0 开始、到 5 结束（但不包括 5）的整数序列。这叫"左闭右开"区间——数学上写成 `[0, 5)`。

第一次见到这玩意儿，你可能会觉得"为什么不从 1 开始？计数不都是从 1 开始的吗？"——这是非常正常的反应。日常生活中我们确实从 1 开始数，但编程世界里从 0 开始是传统（数组索引、列表下标都是从 0 开始的）。而且这样有个好处：`range(5)` 就是"循环 5 次"，很直观。

现在来给猜数字游戏加上次数限制：

```python
secret = 42
max_attempts = 5

for attempt in range(max_attempts):
    guess = int(input(f"第 {attempt + 1} 次猜测（1-100）："))

    if guess == secret:
        print("恭喜你，猜对了！")
        break
    elif guess < secret:
        print("太小了")
    else:
        print("太大了")

    # 剩余次数提示
    remaining = max_attempts - attempt - 1
    if remaining > 0:
        print(f"你还有 {remaining} 次机会")
else:
    # 注意这个 else 和 for 对齐，不是和 if 对齐
    print(f"很遗憾，{max_attempts} 次都没猜中。答案是 {secret}")
```

这里有个容易混淆的新东西：`for` 循环后面的 `else`。这个 `else` 会在循环"正常结束"时执行——也就是说，如果没有被 `break` 打断，循环跑完了所有次数，就会执行 `else` 里的代码。

"等一下，`else` 不是配合 `if` 用的吗？怎么会和 `for` 配合？"——这也是很多新手的疑问。Python 的设计确实有点特别：`for...else` 的意思是"跑完所有循环都没成功，就执行 else"。如果你中途 `break` 跳出了，`else` 就不会执行。

现在你的游戏有次数限制了。但还可以做得更好：让用户选择难度。简单模式数字范围是 1-50，中等模式 1-100，困难模式 1-200。这需要用到更复杂的条件判断。

> **AI 时代小专栏：AI 代码补全的原理**
>
> 你刚写的 `for` 循环，本质上是在"重复做一件事直到达到目标"。有意思的是，这和 AI 模型的训练过程惊人地相似。
>
> GitHub Copilot 这样的 AI 编程助手，能够在你敲代码时自动补全剩余部分。它的"智能"从哪里来？答案是通过**数万次迭代训练**。训练过程大致是这样：给模型一个代码片段，让它预测下一行；对比预测结果和真实代码；计算误差；调整模型参数；然后——再来一次。这个"预测→对比→调整→再预测"的循环，可能会重复数十亿次，就像一个巨大的 `for` 循环在不断地优化模型。
>
> 到 2026 年，GitHub Copilot 的自动补全已经相当成熟，通常一次建议 1-3 行代码。它不贪心，不像某些竞品那样一次生成整个函数——因为它知道，太长的建议反而容易出错。这种"保守但可靠"的策略，和你写的 `for attempt in range(5)` 思路一致：控制节奏，一步步来。
>
> 参考（访问日期：2026-02-08）：
> - https://trendminds.in/github-copilot-master-guide-2026-the-ultimate-ai-coding-handbook/
> - https://research.aimultiple.com/large-language-model-training/
> - https://medium.com/@addyosmani/my-llm-coding-workflow-going-into-2026-52fe1681325e

## 4. 当条件变得复杂

现在来给游戏加难度选择。用户输入 1（简单）、2（中等）、3（困难），程序根据选择设置不同的数字范围。这听起来很简单，但写代码时会发现一个问题：怎么检查"用户输入的是 1、2 或 3 之外的无效值"？

```python
print("选择难度：")
print("1. 简单（1-50）")
print("2. 中等（1-100）")
print("3. 困难（1-200）")

difficulty = int(input("请输入难度（1-3）："))

if difficulty == 1:
    secret = 42  # 简单模式，答案固定
    max_num = 50
elif difficulty == 2:
    secret = 87
    max_num = 100
elif difficulty == 3:
    secret = 156
    max_num = 200
else:
    print("无效的难度选择，默认使用中等模式")
    secret = 87
    max_num = 100
```

这看起来没问题。但如果你想让用户输入英文 "easy"/"medium"/"hard" 呢？或者你想检查"用户输入的是数字且在 1-3 之间"呢？这就需要更复杂的条件判断。

Python 支持**逻辑运算符**（logical operators），可以把多个条件组合起来：

```python
difficulty = input("请输入难度（1-3）：")

# 检查是否为数字且在范围内
if difficulty.isdigit() and (1 <= int(difficulty) <= 3):
    difficulty = int(difficulty)
else:
    print("无效输入，请输入 1、2 或 3")
    difficulty = 2  # 默认中等
```

这里用到了 `and`（且）运算符：两边的条件都为真，整个表达式才为真。

另外两个逻辑运算符是 `or`（或）和 `not`（非）：

```python
# or：只要有一个为真，整个表达式就为真
if age < 18 or age > 65:
    print("你可以享受优惠票价")

# not：取反
if not (difficulty == 1 or difficulty == 2 or difficulty == 3):
    print("无效的难度选择")
```

老潘在旁边看了一眼代码，摇摇头："`not (difficulty == 1 or difficulty == 2 or difficulty == 3)` 这行能跑，但太绕了。我当年也这么写，后来 code review 时被前辈教育了。"

他顺手改成了：

```python
if difficulty not in [1, 2, 3]:
    print("无效的难度选择")
```

"可读性第一。等号写多了会眼花，用 `not in` 一眼就看懂在干嘛。"

老潘的建议很重要。**布尔表达式太复杂时，用变量给它起个名字**：

```python
# 之前：复杂的嵌套条件
if (difficulty == 1 and max_num == 50) or (difficulty == 2 and max_num == 100):
    ...

# 之后：清晰的变量名
is_valid_difficulty = difficulty in [1, 2, 3]
is_valid_range = max_num in [50, 100, 200]

if is_valid_difficulty and is_valid_range:
    ...
```

现在来整合所有内容，完成最终版的猜数字游戏：

```python
import random

print("=== 猜数字游戏 ===")
print("选择难度：")
print("1. 简单（1-50）")
print("2. 中等（1-100）")
print("3. 困难（1-200）")

difficulty = int(input("请输入难度（1-3）："))

if difficulty == 1:
    max_num = 50
elif difficulty == 2:
    max_num = 100
elif difficulty == 3:
    max_num = 200
else:
    print("无效选择，使用中等模式")
    max_num = 100

secret = random.randint(1, max_num)  # 随机生成答案
max_attempts = 5

print(f"\n我想好了一个 1 到 {max_num} 之间的数字，你有 {max_attempts} 次机会猜中它！")

for attempt in range(max_attempts):
    guess = int(input(f"\n第 {attempt + 1} 次猜测："))

    if guess == secret:
        print(f"恭喜！你用了 {attempt + 1} 次猜中了答案 {secret}！")
        break
    elif guess < secret:
        print("太小了")
    else:
        print("太大了")

    remaining = max_attempts - attempt - 1
    if remaining > 0:
        print(f"还有 {remaining} 次机会")
else:
    print(f"\n很遗憾，{max_attempts} 次都用完了。答案是 {secret}")
```

这个游戏已经完整了：有难度选择、次数限制、胜负判定。更重要的是，你在写这个游戏的过程中，学会了让程序"做选择"和"重复做事"——这是编程最核心的两个能力。

你可能会想："就这？不就是把几个 `if` 和 `for` 组合起来吗？"——没错，但几乎所有复杂的程序都是这样一层层搭起来的。搜索引擎的排序算法是无数个条件判断，操作系统的任务调度是复杂的循环，你玩的游戏的核心逻辑也不过是你刚才写的东西的放大版。

## PyHelper 进度

上周 PyHelper 还只是一颗种子，只能打印一句鼓励的话。本周，我们用 `if`/`else` 让它变得智能一点——根据用户的心情推荐不同的学习建议。

```python
# PyHelper - 你的命令行学习助手
# Week 02：根据心情推荐建议

print("=" * 40)
print("  欢迎使用 PyHelper！")
print("=" * 40)
print()

print("今天心情怎么样？")
print("1. 充满干劲")
print("2. 一般般")
print("3. 有点累")

mood = input("\n请输入你的心情（1-3）：")

if mood == "1":
    print("\n太好了！推荐你今天挑战一个新概念，")
    print("比如开始学习函数或者列表。")
elif mood == "2":
    print("\n那就做点巩固练习吧，")
    print("复习上周的变量和字符串，写几个小例子。")
elif mood == "3":
    print("\n累了就休息一下吧，")
    print("今天可以只看视频不动手，或者写 10 分钟代码就停。")
else:
    print("\n输入无效？那就按'一般般'来吧，")
    print("写点巩固练习最稳妥。")

print()
print("记住：学编程是马拉松，不是百米冲刺。找到自己的节奏最重要。")
```

运行效果示例：

```
========================================
  欢迎使用 PyHelper！
========================================

今天心情怎么样？
1. 充满干劲
2. 一般般
3. 有点累

请输入你的心情（1-3）：2

那就做点巩固练习吧，
复习上周的变量和字符串，写几个小例子。

记住：学编程是马拉松，不是百米冲刺。找到自己的节奏最重要。
```

老潘看到这段代码，点点头："不错，开始有交互感了。这种根据用户输入给出不同回应的逻辑，是所有交互式程序的基础——网页的表单验证、游戏的难度选择、甚至 AI 聊天机器人，核心都是 if/else。"

下周，我们会把这些判断逻辑包装成"函数"，让代码更整洁、更可复用。

## Git 本周要点

本周必会命令：
- `git diff` —— 查看修改内容
- `git add -A` —— 添加所有修改
- `git commit -m "feat: 猜数字游戏完整版"` —— 提交更改
- `git log --oneline -n 10` —— 查看最近 10 条提交

常见坑：
- 冒号和缩进：`if`/`for`/`while` 后面要有冒号，代码块要缩进 4 个空格
- 无限循环：`while` 条件永远为真时记得用 `break` 退出
- `range(5)` 是 0-4 不是 1-5，这是新手常犯的错

提交信息规范（建议）：
- `feat:` 新功能（如 `feat: 添加难度选择`）
- `fix:` 修复 bug（如 `fix: 修复无限循环问题`）
- `polish:` 代码优化（如 `polish: 简化布尔表达式`）

Pull Request (PR)：
- Week 02 暂不要求 PR，但建议每次 commit 后 push 到远端，养成备份习惯。

## 本周小结（供下周参考）

这一周，你学会了让程序"做选择"和"重复做事"。从单次判断的 `if` 语句，到反复猜测的 `while` 循环，再到限制次数的 `for` 循环，你的猜数字游戏已经是一个完整的交互式程序了。更重要的是，你理解了布尔表达式、逻辑运算符和缩进规则——这些是所有编程语言共通的基础。

下周，我们将把这些逻辑包装成"函数"，让代码更整洁、更可复用。你会发现，函数不只是"把代码打包"，更是一种思考方式——把复杂问题拆成一个个小任务。

---

## Definition of Done（学生自测清单）

完成本周学习后，请确认你能：

- [ ] 使用 `if`/`elif`/`else` 编写包含多个分支的条件判断
- [ ] 编写布尔表达式，正确使用比较运算符（`==`, `!=`, `<`, `>`）和逻辑运算符（`and`, `or`, `not`）
- [ ] 使用 `while` 循环实现"满足条件时重复执行"
- [ ] 使用 `for` 循环配合 `range()` 实现指定次数的重复
- [ ] 理解 Python 的缩进规则，能识别和修复 `IndentationError`
- [ ] 使用 `break` 跳出循环，使用 `continue` 跳过本次循环
- [ ] 完成一个完整的猜数字游戏（有难度选择、次数限制）
- [ ] 使用 Git 提交至少 2 次（draft + verify）
- [ ] 运行 `python3 -m pytest chapters/week_02/tests -q` 并通过所有测试

<!--
章节结构骨架（供 chapter-writer 参考）：

1. 章首导入（引言格言 + 时代脉搏）——已提供
2. 前情提要——已提供
3. 学习目标——已提供
4. 第 1 节：如果这样，那就那样（if/elif/else）
   - AI 小专栏 #1（AI 怎样"做选择"？）
5. 第 2 节：让它一直猜，直到猜中（while 循环）
6. 第 3 节：数到几就停（for 循环 + range）
   - AI 小专栏 #2（AI 代码补全的原理）
7. 第 4 节：当条件变得复杂（布尔表达式 + 逻辑运算符）
8. PyHelper 进度
9. Git 本周要点
10. 本周小结（供下周参考）
11. Definition of Done

写作提示：
- 每节用猜数字游戏的演进作为主线，不要散乱地讲知识点
- 代码示例尽量用游戏的片段，让读者看到"项目在长大"
- 角色出场要自然，小北适合犯语法错误（冒号、缩进），阿码适合追问原理（range 从 0 开始）
- 回顾桥要自然融入，比如"上周你用 input 获取输入，这周我们用 int 把它转成数字"
- 每节结束时项目都是可运行的，给读者成就感
-->
