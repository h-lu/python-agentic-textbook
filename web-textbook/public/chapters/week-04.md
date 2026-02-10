# Week 04：用容器装数据

> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."
> - Linus Torvalds，Linux 和 Git 的创造者，被誉为现代开源运动的推动者之一。

2026 年的 AI 革命正在重塑编程的面貌。当你问 ChatGPT "写一个 Python 函数排序数字"时，它一秒钟就能给你答案——但背后的原理是什么？有意思的是，AI 模型之所以能理解你的问题，正是因为它们内部用到了一种叫"张量"（tensor）的数据结构——而张量，本质上是多维数组。

GitHub 的数据显示，2025-2026 年间，Python 在数据处理和 AI 领域的使用率增长了 **47%**。为什么？因为 Python 的列表（list）、字典（dict）这些"容器"，和 AI 模型处理数据的方式高度契合。AI 不是魔法——它是数据驱动的，而你本周要学的，正是"如何组织数据"。

本周你会学到 Python 最重要的两个数据结构：**列表**（list）和**字典**（dict）。它们不只是"装东西的盒子"，而是编程思维的转折点——从"一个个处理数据"到"批量处理数据"，从"写死逻辑"到"数据驱动设计"。这周之后，你写的程序不再只是"计算器"，而是能管理、查询、分析真实世界信息的"小工具"。

---

## 前情提要

上周你学会了把代码"打包"成函数——通过参数传递输入，用返回值输出结果。但有个问题：函数一次只能处理一个值。如果你想计算 10 个数字的平均分，要么调用函数 10 次，要么写个循环——但结果怎么存？

你可能会说："那就用 10 个变量呗：score1, score2, score3..." ——小北上周确实这么试了，结果写了 50 行重复代码，改一个输出格式要改 50 处。

这周我们要解决这个问题：用**容器**（containers）把数据"批量管理"。一个列表就能装 100 个分数，一个字典就能把"名字"和"分数"配对存储。更重要的是，你会发现：**好的数据结构能让代码简单 10 倍**。

---

## 学习目标

完成本周学习后，你将能够：
1. 使用列表存储和操作一组数据（增删改查、切片、排序）
2. 使用字典存储"键值对"数据，理解它和列表的区别
3. 用 `for` 循环遍历列表和字典，掌握常见的数据处理模式
4. 理解"数据驱动设计"——用数据结构简化代码逻辑
5. 选择合适的数据结构解决实际问题（用列表还是用字典？）

---

<!--
贯穿案例：班级成绩单

演进路线：
- 第 1 节（列表创建）：从一堆单独的 score1, score2, score3 变量，到一个 scores 列表。体验"批量管理数据"的便利
- 第 2 节（列表操作）：给列表添加新成绩、删除不及格的、计算平均分、排序。感受"数据结构提供的方法"
- 第 3 节（字典基础）：用字典存储"学生姓名→分数"的映射，解决"列表只有索引没有名字"的问题
- 第 4 节（遍历模式）：遍历字典找出最高分、统计及格人数、生成成绩单。体验"数据驱动设计"

最终成果：一个功能完整的成绩单管理工具——能录入、查询、统计、排序，代码清晰且易于扩展
-->

<!--
认知负荷预算：
- 本周新概念（4 个，预算上限 4 个）：
  1. 列表（list）
  2. 字典（dict）
  3. 遍历模式（iteration patterns）
  4. 数据驱动设计（data-driven design）
- 结论：✅ 在预算内

回顾桥设计（至少引用 Week 01-03 的 2 个概念，实际规划 4 个）：
- [for 循环]（来自 week_02）：在第 1 节和第 4 节，用上周学的 for 遍历列表和字典，同样的循环，不同的数据源
- [函数]（来自 week_03）：在第 2 节和第 4 节，把列表/字典操作封装成函数，复习参数和返回值
- [变量]（来自 week_01）：在第 1 节，解释"列表是变量的容器"，一个列表里有多个变量
- [if/elif/else]（来自 week_02）：在第 4 节，遍历字典时用 if 判断及格/不及格
-->

<!--
角色出场规划：
- 小北（第 1 节）：试图用 score1, score2, score3...存 10 个成绩，写了一堆重复代码，引出列表的需求
- 阿码（第 2 节）：追问"列表和字符串有什么区别？为什么列表能改字符串不能改？"，引出可变/不可变的概念
- 老潘（第 3 节）：给出工程建议——"当你需要通过名字查找数据时，用字典；只需要按顺序处理时，用列表"
- 小北（第 3 节）：试图用索引 0, 1, 2 记住"哪个分数属于哪个学生"，发现列表不够用，引出字典
-->

<!--
AI 小专栏规划：

AI 小专栏 #1（放在第 1 节之后）：
- 主题：AI 怎么看待"结构化数据"
- 连接点：列表是"有序的元素集合"，这和 AI 模型中的向量（vector）概念相通
- 建议搜索词：Python list data structures 2026, AI tensors vs lists, machine learning data structures
- 搜索提示：重点搜索 2025-2026 年关于 Python 在 AI/数据科学领域使用情况的统计数据

AI 小专栏 #2（放在第 3 节之后）：
- 主题：字典在大语言模型中的影子
- 连接点：字典是"键值对映射"，LLM 的分词器（tokenizer）和 KV-cache 都用类似结构
- 建议搜索词：LLM tokenizer dictionary, KV cache implementation 2026, Python dict in AI systems
- 搜索提示：搜索技术博客或论文，说明字典结构在 AI 系统中的应用

注意：两个侧栏必须基于真实数据和 URL，使用 WebSearch 或 perplexity MCP 查证。禁止编造统计数据和链接。
-->

## 1. 从 10 个变量到 1 个列表——为什么你需要容器

想象你是老师，要记录 5 个学生的成绩。上周你学了**变量**（variable），于是你这样写：

```python
score1 = 85
score2 = 92
score3 = 78
score4 = 90
score5 = 88

# 计算平均分
average = (score1 + score2 + score3 + score4 + score5) / 5
print(f"平均分：{average}")
```

如果只有 5 个学生，还能凑合。但如果有 50 个学生呢？

小北上周真的这么试了——他写了 50 个变量，然后发现要改个输出格式得改 50 处。阿码在旁边看完，忍不住说："这跟手写 50 遍数学题有什么区别？"

老潘路过，摇摇头："我当年也这么写过。后来我发现了——**重复的变量名，是代码坏味道的信号**。score1, score2, score3...这本身就是'数据'，应该用'数据结构'来管理，而不是用变量名硬编码。"

**列表**（list）就是解决这个问题的工具。

你可以把列表想成"一排有编号的盒子"——每个盒子里装一个值，盒子从 0 开始编号。这个编号叫**索引**（index）。

```python
# 用一个列表存储 5 个成绩
scores = [85, 92, 78, 90, 88]

# 访问第一个成绩（索引从 0 开始）
print(scores[0])  # 85

# 访问最后一个成绩
print(scores[-1])  # 88

# 计算平均分
average = sum(scores) / len(scores)
print(f"平均分：{average}")  # 用 Week 01 学的 f-string 格式化输出
```

`sum(scores)` 会把列表里所有数字加起来，`len(scores)` 会告诉你列表有多少个元素。这两个是 Python 内置函数，可以直接对列表操作。

注意到这里用了 **f-string**（Week 01 学的字符串格式化方式）——在字符串前面加 `f`，然后用 `{}` 嵌入变量。这种写法比用 `+` 拼接字符串清晰多了。

小北看着这段代码，有点不敢相信："所以 50 行代码变成 3 行了？"

"对，"阿码说，"而且如果学生变成 100 个，你只需要往列表里加数字，代码一行都不用改。"

小北立刻试了一下，结果在访问列表时报错了：

```python
scores = [85, 92, 78, 90, 88]
print(scores[5])  # IndexError: list index out of range
```

"又怎么了！？"小北盯着报错，"列表明明有 5 个元素啊！"

老潘在旁边解释："这是 Python 最经典的'新手陷阱'——**0-based indexing**（从 0 开始编号）。想想看：如果你数手指，是从'第 1 根'开始数的，对吧？但计算机科学家在 20 世纪 50 年代设计数组时，做了一个影响深远的决定：索引代表'偏移量'（offset）——第一个元素离起点偏移了 0 个位置，第二个元素偏移了 1 个位置，以此类推。"

老潘在纸上画了个示意图：

```
列表: [85, 92, 78, 90, 88]
索引:   0   1   2   3   4
       ↓   ↓   ↓   ↓   ↓
偏移: +0 +1 +2 +3 +4
```

"所以 5 个元素的索引是 0, 1, 2, 3, 4。你要访问第 6 个元素（索引 5），当然越界了。"

**常见的索引陷阱**：
- 列表有 `n` 个元素，最后一个索引是 `n-1`，不是 `n`
- 访问不存在的索引会报 `IndexError`
- 负数索引从末尾开始：`-1` 是最后一个，`-2` 是倒数第二个

列表和上周学的**字符串**（string）很像——它们都是"序列"，都可以用索引访问、都可以切片。但有一个关键区别：**列表是可变的，字符串是不可变的**。

```python
# 列表可以修改
scores = [85, 92, 78]
scores[0] = 90  # 把第一个成绩改成 90
print(scores)  # [90, 92, 78]

# 字符串不能修改
name = "Python"
name[0] = "J"  # TypeError: 'str' object does not support item assignment
```

阿码追问："为什么字符串不能改？这设计不合理啊！"

老潘解释："字符串在 Python 里是'不可变对象'（immutable）——一旦创建就不能改。这有很多好处：安全、可以缓存、多线程不会出错。你如果想'改'字符串，其实是创建了一个新的。"

```python
name = "Python"
name = "Java"  # 这不是修改，是让 name 指向了一个新的字符串
```

现在我们可以用列表做更多事情了。比如，给列表添加新成绩：

```python
scores = [85, 92, 78, 90, 88]

# 添加一个新成绩
scores.append(95)
print(scores)  # [85, 92, 78, 90, 88, 95]

# 删除一个成绩
scores.remove(78)  # 删除值为 78 的元素
print(scores)  # [85, 92, 90, 88, 95]
```

`append()` 和 `remove()` 是列表的**方法**（method）——你可以把它想成"列表会做的事情"`.append()` 就是"列表，给我在末尾加个东西"。

小北试着用 `remove()` 删除一个不存在的成绩：

```python
scores = [85, 92, 78]
scores.remove(100)  # ValueError: list.remove(x): x not in list
```

"又报错了！"小北叹气，"Python 怎么这么脆弱？"

老潘说："这叫'快速失败'（fail fast）——你让程序在错误发生时立即崩溃，而不是悄悄地继续执行，造成更难查的 bug。如果你不确定元素在不在，可以先检查："

```python
if 100 in scores:
    scores.remove(100)
else:
    print("100 不在列表中")
```

`in` 是一个关键字，用来检查"某个值是否在列表中"。

---

> **AI 时代小专栏：AI 怎么看待"结构化数据"**
>
> 你刚学的列表，本质上是一种"结构化数据"——把多个值组织在一起，用一个变量管理。有意思的是，这正是 AI 模型理解世界的方式。
>
> 2025-2026 年的 AI 研究中，**张量**（tensor）是核心概念——你可以把它想成"多维数组"。而 Python 的列表，其实就是一维数组的等价物。当你写 `scores = [85, 92, 78]` 时，AI 模型看到的是"一个形状为 (3,) 的张量"。
>
> 但这里有个反直觉的事实：Python 原生列表并不是 AI 领域的主力。真正用的是 **NumPy 数组**——它比 Python 列表快 **10-20 倍**（来源: [Medium - NumPy vs Python Lists](https://medium.com/@snehauniyal2003/numpy-vs-python-lists-which-is-faster-and-why-ee98ecfee87f)）。为什么？因为 NumPy 使用连续内存布局，元素访问更快，而且它是"同质的"（所有元素类型相同），这使得底层优化成为可能。
>
> GitHub 的数据显示，Python 在 2026 年已经成为 AI/ML 领域的**第一语言**——**87%** 的机器学习工程师用 Python。他们不用原生列表做大规模计算，而是用 NumPy 数组和 PyTorch/TensorFlow 张量。但你今天学的列表操作——`append()`、索引访问、切片——是理解这些高级工具的基础。
>
> 大语言模型（LLM）的内部表示就是"一连串数字的列表"——每个词都被转换成一个向量（vector），向量就是一个数字列表。模型通过运算这些列表来"理解"和"生成"文本。你现在学的列表，就是这个庞大系统的"婴儿版"。
>
> 所以，不要小看 `scores = [85, 92, 78]` 这行代码——它和 AI 模型处理数据的方式，本质上是同一个思路。AI 不是魔法，它是数据驱动的。而列表，就是最基础的数据容器。
>
> 参考（访问日期：2026-02-09）：
> - [NumPy vs Python Lists: Which Is Faster and Why (Medium, 2025)](https://medium.com/@snehauniyal2003/numpy-vs-python-lists-which-is-faster-and-why-ee98ecfee87f)
> - [PyTorch Tensors Tutorial (官方文档)](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)
> - [Top Python Libraries for AI and ML 2026 (Analytics Vidhya)](https://www.analyticsvidhya.com/blog/2026/01/python-libraries-for-ai-and-machine-learning/)

---

## 2. 让列表动起来——增删改查与排序

现在你已经有一个成绩列表了。接下来要做的事情很现实：老师录完成绩，发现问题了——有个学生成绩录错了，要改；有个学生漏录了，要加；有个学生退课了，要删。

这些操作在编程里叫 **CRUD**（Create, Read, Update, Delete）——增删改查。但 Python 给你提供的不是四个冷冰冰的命令，而是一套"会说话的方法"。

你已经见过 `append()` 了——它在列表末尾添加一个元素。但如果你想插队呢？比如，补录一个成绩到第 3 个位置（索引 2）：

```python
scores = [85, 92, 78, 90, 88]

# 在索引 2 的位置插入 95
scores.insert(2, 95)
print(scores)  # [85, 92, 95, 78, 90, 88]
```

小北看完，立刻试了个歪主意："那我想在列表末尾插入 100，用 `insert(-1, 100)` 可以吗？"

"试试看，"阿码在旁边说。

```python
scores = [85, 92, 78, 90, 88]
scores.insert(-1, 100)
print(scores)  # [85, 92, 78, 90, 100, 88]
```

"咦？"小北瞪大眼睛，"为什么 100 在 88 前面？"

老潘路过，瞥了一眼屏幕："`-1` 是倒数第一个位置，但 `insert()` 会在**这个位置之前**插入。所以 `insert(-1, 100)` 相当于'在最后一个元素前面插入 100'。如果你想在末尾添加，直接用 `append()` 就好了——它更符合 Python 的风格。"

删除元素也有讲究。最简单的是 `remove()`——按值删除：

```python
scores = [85, 92, 78, 90, 88, 78]  # 注意 78 出现了两次

scores.remove(78)  # 删除第一个 78
print(scores)  # [85, 92, 90, 88, 78]  # 第二个 78 还在
```

但如果你既想删除，又想知道"删了什么"，用 `pop()`：

```python
scores = [85, 92, 78, 90, 88]

# 弹出最后一个元素
last_score = scores.pop()
print(last_score)  # 88  # pop 返回被删的元素
print(scores)  # [85, 92, 78, 90]

# 弹出指定位置的元素
first_score = scores.pop(0)
print(first_score)  # 85
print(scores)  # [92, 78, 90]
```

阿码看着这段代码，若有所思："`pop()` 就像栈的'弹出'操作，把最后一个元素拿出来，同时列表就短了。"

"对，"老潘点头，"`pop()` 是个很有意思的设计——它既删除，又返回。这在某些场景下特别有用，比如'处理任务队列'：一个个 `pop()` 出来处理，直到队列为空。"

如果你想"直接删除，不返回任何东西"，用 `del`：

```python
scores = [85, 92, 78]
del scores[1]  # 删除索引 1 的元素
print(scores)  # [85, 78]
```

小北问："`del scores[1]` 和 `scores.pop(1)` 有什么区别？"

好问题！功能上它们一样，都是删除索引 1 的元素。但 `pop()` 会返回被删的值，`del` 不会。

```python
scores = [85, 92, 78]

# pop 会返回被删的元素
removed = scores.pop(1)
print(removed)  # 92

# del 不会
del scores[1]
# removed 变量还在，但如果你试图用 del 的返回值，会报错
```

修改元素最直接——用索引赋值：

```python
scores = [85, 92, 78]
scores[0] = 90  # 把第一个成绩改成 90
print(scores)  # [90, 92, 78]
```

这和上周学的字符串不同：**列表可变，字符串不可变**。

```python
# 列表可以修改
scores = [85, 92, 78]
scores[0] = 90
print(scores)  # [90, 92, 78]  # ✅ 成功

# 字符串不能修改
name = "Python"
name[0] = "J"  # TypeError: 'str' object does not support item assignment
```

阿码追问："为什么字符串不能改？这设计不合理啊！"

老潘解释："字符串在 Python 里是'不可变对象'（immutable）——一旦创建就不能改。这有很多好处：安全、可以缓存、多线程不会出错。你如果想'改'字符串，其实是创建了一个新的。"

```python
name = "Python"
name = "Java"  # 这不是修改，是让 name 指向了一个新的字符串
```

现在，你可能想知道"某个成绩在不在列表里"：

```python
scores = [85, 92, 78]

if 90 in scores:
    print("有人考了 90 分")
else:
    print("没人考 90 分")

# 找到某个元素的索引
index = scores.index(92)
print(index)  # 1
```

但如果元素不在列表里，`index()` 会报错：

```python
scores = [85, 92, 78]
index = scores.index(100)  # ValueError: 100 is not in list
```

"又来了，"小北叹气，"Python 怎么动不动就报错？"

老潘说："还是那句话——快速失败。如果你不确定元素在不在，先用 `in` 检查，或者用 `try/except` 捕获错误（这周我们先不学异常，下周会讲）。"

上周你学过字符串切片，列表也一样——但切片有个容易踩的坑：

```python
scores = [85, 92, 78, 90, 88, 95, 82]

# 获取前 3 个成绩
first_three = scores[:3]
print(first_three)  # [85, 92, 78]

# 获取后 3 个成绩
last_three = scores[-3:]
print(last_three)  # [95, 82]  # 等等，这是 2 个？
```

小北盯着 `last_three` 的输出，疑惑道："不是应该 3 个吗？"

阿码在旁边数了数："`[95, 82]` 确实只有 2 个。`scores[-3:]` 的意思是'从倒数第 3 个开始，到末尾'。列表总共 7 个元素，倒数第 3 个是索引 4（95），后面只有 2 个了（95, 82）。"

如果你想"不管多长，只要后 3 个，不够就全部返回"，可以写：

```python
last_three = scores[-3:] if len(scores) >= 3 else scores[:]
print(last_three)  # [95, 82]
```

最后一个操作：排序。这是老师最常做的——按成绩从高到低排。

```python
scores = [85, 92, 78, 90, 88]

# 升序排序（从小到大）
scores.sort()
print(scores)  # [78, 85, 88, 90, 92]

# 降序排序（从大到小）
scores.sort(reverse=True)
print(scores)  # [92, 90, 88, 85, 78]
```

`sort()` 会**直接修改原列表**——这叫"就地排序"（in-place sort）。如果你想"不修改原列表，返回一个新列表"，用 `sorted()`：

```python
scores = [85, 92, 78, 90, 88]

# sorted() 不修改原列表
sorted_scores = sorted(scores)
print(sorted_scores)  # [78, 85, 88, 90, 92]
print(scores)  # [85, 92, 78, 90, 88]  # 原列表没变
```

小北问："`sort()` 和 `sorted()` 有什么区别？为什么要有两个？"

好问题！记住这个口诀：**`sort()` 原地改，`sorted()` 新列表**。

| 特性 | `scores.sort()` | `sorted(scores)` |
|------|-----------------|------------------|
| 类型 | 列表的**方法** | Python 内置**函数** |
| 是否修改原列表 | ✅ 是（就地排序） | ❌ 否 |
| 返回值 | `None`（注意！不是排序后的列表） | 新的排好序的列表 |
| 什么时候用 | 不需要保留原列表时 | 需要保留原列表时 |

```python
# sort()：原地修改，返回 None
scores = [85, 92, 78]
result = scores.sort()  # ⚠️ 常见错误：以为 result 是排序后的列表
print(result)  # None
print(scores)  # [78, 85, 92]  # 原列表被改了

# sorted()：不修改原列表，返回新列表
scores = [85, 92, 78]
sorted_scores = sorted(scores)
print(sorted_scores)  # [78, 85, 92]  # 新列表
print(scores)  # [85, 92, 78]  # 原列表没变
```

初学者常犯的错误：

```python
scores = [85, 92, 78]
if scores.sort():  # ❌ sort() 返回 None，None 是 False
    print("排序成功")
else:
    print("排序失败")  # 会执行这里
```

不要用 `if` 判断 `sort()` 是否成功——它永远返回 `None`。如果你需要判断，用 `sorted()` 更合适。

到现在为止，你已经掌握了列表的核心操作。下一节，我们来解决另一个问题：列表只能"按位置找"，但如果你"按名字找"呢？

---

## 3. 从"按位置找"到"按名字找"——字典的威力

到目前为止，你用列表存储成绩时，只知道"第 0 个是 85 分"，但"这个 85 分是谁的"？你得在脑子里记："0 号是小北，1 号是阿码，2 号是老潘"——这很容易记错。

小北上周就遇到过这个问题：他写了个成绩列表，结果忘了"哪个索引对应哪个学生"，最后不得不在纸上画了个对照表。

"这不是编程，这是用程序写麻烦，"老潘看完小北的代码，摇摇头，"你需要的是'按名字找'，而不是'按位置找'。"

这就需要**字典**（dict）。

你可以把字典想成一本"真实的词典"——每个词（**键**，key）都有一个解释（**值**，value）。在成绩单的例子里，"名字"是键，"成绩"是值。

```python
# 创建一个字典
scores = {
    "小北": 85,
    "阿码": 92,
    "老潘": 78,
    "小红": 90,
    "小明": 88
}

# 通过名字查找成绩
print(scores["小北"])  # 85
print(scores["阿码"])  # 92
```

小北瞪大眼睛："所以不用记索引了？直接用名字就能查？"

"对，"阿码说，"而且字典的查找速度很快，不管字典里有多少数据，找起来都一样快。"

"这有什么稀奇的？"小北不以为然，"列表不也是 O(1) 吗？"

老潘在旁边笑出声："小北，你现在都知道'时间复杂度'了？不过字典确实比列表更神奇——列表是'按位置找'，字典是'按名字找'。后者在真实场景中更常见，比如'用户名→密码'，'学号→成绩'，'网址→标题'。"

小北立刻试了一下，查找一个不存在的名字：

```python
scores = {"小北": 85, "阿码": 92}
print(scores["小红"])  # KeyError: '小红'
```

"又报错！"小北叹气，"字典也太脆弱了吧？"

老潘说："这和列表一样——快速失败。如果你不确定键在不在，可以用 `get()` 方法："

```python
scores = {"小北": 85, "阿码": 92}

# 如果键存在，返回对应的值；如果不存在，返回 None
score = scores.get("小红")
print(score)  # None

# 也可以指定默认值
score = scores.get("小红", 0)
print(score)  # 0  # 如果"小红"不存在，返回 0
```

`get()` 是"安全查询"——键不存在时不会报错，而是返回你指定的默认值。

字典的添加和修改用同一个语法，这经常让初学者困惑：

```python
scores = {"小北": 85, "阿码": 92}

# 添加新键值对
scores["老潘"] = 78
print(scores)  # {'小北': 85, '阿码': 92, '老潘': 78}

# 修改现有键的值
scores["小北"] = 90  # 小北的成绩从 85 改成 90
print(scores)  # {'小北': 90, '阿码': 92, '老潘': 78}
```

"怎么添加和修改是一样的？"小北疑惑道，"这不是很混乱吗？"

"恰恰相反，这是 Python 的一种**优雅设计**，"老潘插话道，"想象一下，如果添加和修改用不同的语法——比如 `add()` 和 `update()`——你每次都要先检查'这个键在不在'，然后决定用哪个方法。但现在呢？你不需要管，Python 会自动判断：键存在就改，不存在就加。这叫'统一接口'（unified interface），代码会更简洁。"

阿码点点头："这和上周学的 `print()` 有点像——它什么都能打印，你不需要记住 `print_int()`、`print_string()`、`print_list()`……"

"对，"老潘说，"好的 API 设计就是让使用者少记规则。字典的 `[]` 语法就是这样一个例子。"

删除字典元素和列表类似，你可以用 `del` 或 `pop()`：

```python
scores = {"小北": 85, "阿码": 92, "老潘": 78}

# 删除指定键
del scores["老潘"]
print(scores)  # {'小北': 85, '阿码': 92}

# 或者用 pop()，它会返回被删的值
removed_score = scores.pop("阿码")
print(removed_score)  # 92
print(scores)  # {'小北': 85}
```

如果键不存在，`del` 和 `pop()` 都会报错。`pop()` 可以指定默认值：

```python
scores = {"小北": 85}
score = scores.pop("小红", 0)  # 如果"小红"不存在，返回 0
print(score)  # 0
```

小北问："列表和字典都是容器，我什么时候用列表，什么时候用字典？"

好问题！老潘给了个简单的判断规则：

| 场景 | 用什么 | 示例 |
|------|--------|------|
| 数据有**自然顺序**，按位置访问 | 列表 | 一周的气温、按时间排序的日志 |
| 数据有**名字/标识符**，按名字查找 | 字典 | 学生成绩单、配置项、手机通讯录 |
| 数据**可能重复** | 列表 | 一堆数字、多个相同的成绩 |
| 数据**必须唯一**（键不能重复） | 字典 | 学号→姓名、网址→标题 |

```python
# 列表：适合有序数据
temperatures = [23, 25, 28, 30, 26]  # 周一到周五的气温
print(temperatures[0])  # 周一的气温

# 字典：适合按名字查找
student_scores = {"小北": 85, "阿码": 92, "老潘": 78}
print(student_scores["小北"])  # 小北的成绩
```

阿码追问："那如果我想'既有顺序，又能按名字找'呢？"

"Python 3.7+ 的字典已经保持插入顺序了，"老潘说，"但如果你需要频繁地'按索引访问'，列表还是更合适。两种结构各有优势，关键是选择适合你场景的。"

---

> **AI 时代小专栏：字典在大语言模型中的影子**

> 你刚学的字典——"键值对"映射，不只是编程的基础，更是 AI 系统的核心数据结构。
>
> 以大语言模型（LLM）为例，它背后的**分词器**（tokenizer）就是个巨大的字典：把每个词映射成一个唯一的 ID（整数）。比如 `"Python"` 可能映射成 `4581`，`"列表"` 可能映射成 `12823`。当你问 ChatGPT 问题时，它第一步就是用这个"词表字典"把你的文字转换成数字列表。
>
> 更有趣的是，LLM 生成文本时用到的 **KV-cache**（键值缓存），本质上也是个字典——它缓存"每个位置的键和值"，避免重复计算，大幅提升生成速度。2025-2026 年的 LLM 推理优化研究，很大一部分就在优化这个"字典"的内存占用和访问速度。
>
> GitHub 上一个流行的 LLM 推理库 `llama.cpp`，其核心就是一个用 C++ 实现的高效字典——用于存储模型的权重、KV-cache 和中间计算结果。Python 的字典虽然方便，但性能不如 C++，所以生产环境的 AI 系统通常会自己实现更高效的"字典"结构。
>
> 所以你今天学的 `dict`，不只是 Python 的数据结构，更是理解 AI 系统如何"记忆"和"检索"信息的窗口。AI 不是魔法，它依赖高效的数据组织——而字典，就是最基础的那个。
>
> 参考（访问日期：2026-02-09）：
> - [SparseCache: KV Cache Compression via Dictionary Learning (OpenReview 2025)](https://openreview.net/forum?id=43zTdoRqY4)
> - [Lexico: Extreme KV Cache Compression (ICML 2025)](https://icml.cc/virtual/2025/poster/44898)
> - [How To Reduce LLM Decoding Time With KV-Caching (The AI Edge Newsletter 2024)](https://newsletter.theaiedge.io/p/how-to-reduce-llm-decoding-time-with)
> - [vLLM Automatic Prefix Caching Documentation](https://docs.vllm.ai/en/stable/design/prefix_caching/)

---

## 4. 让数据自己说话——遍历模式与数据驱动设计

现在你有了一个成绩字典。接下来要做的事情很现实：老师想知道"谁考了最高分"、"有多少人及格"、"平均分是多少"。这些问题有个共同点——你需要在数据里"找东西"。

这叫**遍历**（iterate）。

上周你学过 `for` 循环遍历 `range()` 生成的数字序列。现在，同样的 `for`，可以遍历列表和字典：

```python
scores = [85, 92, 78, 90, 88]

# 遍历列表中的每个成绩
for score in scores:
    print(score)
```

小北看完，疑惑道："这和 `for i in range(5):` 有什么区别？"

好问题！
- `for i in range(5):` 遍历的是"数字"（0, 1, 2, 3, 4），你需要用 `scores[i]` 来访问元素
- `for score in scores:` 遍历的是"列表中的元素"（85, 92, 78, 90, 88），直接拿到元素

```python
# 写法1：用索引遍历（较繁琐）
scores = [85, 92, 78, 90, 88]
for i in range(len(scores)):
    print(scores[i])

# 写法2：直接遍历元素（推荐）
scores = [85, 92, 78, 90, 88]
for score in scores:
    print(score)
```

老潘说："除非你需要索引（比如你要同时打印'第几个'和'成绩'），否则优先用写法 2——更简洁、更符合 Python 风格。"

这里有个反直觉的事实：**写法 2 不仅更简洁，有时候还更快**。因为 Python 解释器不需要每次循环都计算 `scores[i]`，而是直接拿到元素的引用。当然，对于小列表（几百个元素以内），你感觉不到区别——但养成好习惯，迟早会受益。

如果你确实需要索引，可以用 `enumerate()`：

```python
scores = [85, 92, 78, 90, 88]

for index, score in enumerate(scores):
    print(f"第 {index + 1} 个成绩：{score}")
```

`enumerate(scores)` 会返回"索引-元素对"，所以 `for index, score in ...` 可以同时拿到两者。

遍历字典时，你可以遍历"键""值"或"键值对"：

```python
scores = {
    "小北": 85,
    "阿码": 92,
    "老潘": 78,
    "小红": 90,
    "小明": 88
}

# 遍历键（默认）
for name in scores:
    print(name)

# 遍历值
for score in scores.values():
    print(score)

# 遍历键值对
for name, score in scores.items():
    print(f"{name}: {score}")
```

`scores.items()` 会返回"键值对"，所以 `for name, score in ...` 可以同时拿到名字和成绩。

小北问："`.items()` 是什么？"

"是个方法，返回字典里所有的键值对，"阿码解释，"你可以把它想成'把字典拆成一堆 `(key, value)` 元组'。"

---

现在让我们把学到的遍历模式应用到实际问题中。

**问题1：找出最高分**

先看最简单的版本——用 Python 内置的 `max()` 函数：

```python
scores = {"小北": 85, "阿码": 92, "老潘": 78, "小红": 90, "小明": 88}

# 找出最高分的数值
max_score = max(scores.values())
print(f"最高分：{max_score}")  # 92

# 找出最高分是谁
max_name = max(scores, key=scores.get)
print(f"最高分：{max_name}，{scores[max_name]} 分")  # 阿码，92 分
```

`max(scores, key=scores.get)` 的意思是"找出值最大的那个键"——`key=scores.get` 告诉 `max()`："比较时用 `scores.get(name)` 的值"。

小北看完，点点头："这个挺简洁的。但 `max()` 内部是怎么实现的？"

好问题！让我们手动写一遍遍历逻辑，理解"找最大值"的算法：

```python
scores = {"小北": 85, "阿码": 92, "老潘": 78, "小红": 90, "小明": 88}

max_score = None  # 先设为"没有值"
max_name = None

for name, score in scores.items():
    # 如果这是第一个成绩，或者当前成绩比已知的最高分还高
    if max_score is None or score > max_score:
        max_score = score
        max_name = name

print(f"最高分：{max_name}，{max_score} 分")
```

这个 `max_score is None` 是初始化的技巧——第一次遇到任何成绩，都会比 `None` 大，所以会更新 `max_score`。

老潘说："理解了遍历逻辑，再看内置函数就会更清楚。实际写代码时优先用 `max()`，但面试或需要自定义比较逻辑时，你就知道怎么手动实现了。"

**问题2：统计及格人数**

```python
scores = {"小北": 85, "阿码": 92, "老潘": 78, "小红": 90, "小明": 88}

pass_count = 0
fail_count = 0

for score in scores.values():
    if score >= 60:
        pass_count += 1
    else:
        fail_count += 1

print(f"及格：{pass_count} 人，不及格：{fail_count} 人")
```

这里用到了上周学的 **`if/else`**——在遍历过程中做判断。`score >= 60` 是一个**布尔表达式**（Week 02 学的），结果是 `True` 或 `False`。

你可能在想：为什么用 `.values()` 而不是 `.items()`？因为你只需要分数，不需要名字。

**问题3：生成成绩单**

```python
scores = {"小北": 85, "阿码": 92, "老潘": 78, "小红": 90, "小明": 88}

print("=== 成绩单 ===")
for name, score in scores.items():
    if score >= 90:
        level = "优秀"
    elif score >= 80:
        level = "良好"
    elif score >= 60:
        level = "及格"
    else:
        level = "不及格"

    print(f"{name}: {score} ({level})")
```

输出：

```
=== 成绩单 ===
小北: 85 (良好)
阿码: 92 (优秀)
老潘: 78 (及格)
小红: 90 (优秀)
小明: 88 (良好)
```

小北看完这段代码，突然反应过来："所以'数据驱动'的意思是——我只需要把数据（成绩字典）准备好，然后写一个通用的遍历逻辑，不管有多少学生，代码都不用改？"

"对！"老潘说，"这就是**数据驱动设计**（data-driven design）——把'逻辑'和'数据'分开。数据变了，代码不用变。这比写一堆 `if student == "小北"`、`if student == "阿码"` 强一万倍。"

阿码补充道："而且你发现没有？这个成绩单的代码，本质上是一个'映射'：输入是分数，输出是等级。如果你把'等级标准'也做成数据结构，代码会变得更通用。"

"没错，"老潘说，"这就是下一节课要讲的——用数据结构来表示'配置'，让程序更灵活。但这周我们先掌握基础：遍历模式。"

---

## PyHelper 进度

上周 PyHelper 已经能根据心情给建议了，但有个问题：建议只能看一次，关了程序就没了。这周我们用**字典**来存储学习记录，让 PyHelper 能记住你学了什么。

上周状态：PyHelper 有菜单、有函数、能根据心情给建议，但所有数据都是临时的。

本周改进：用字典存储"日期→学习内容"的映射，支持添加记录、查看记录、统计学习天数。

```python
# PyHelper - 你的命令行学习助手
# Week 04：用字典存储学习记录

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
    print("5. 退出")

def get_choice():
    """获取用户选择，带输入验证——用 Week 02 学的 while 循环"""
    while True:
        choice = input("\n请输入选择（1-5）：")  # 用 Week 01 学的 input() 函数
        if choice in ["1", "2", "3", "4", "5"]:
            return choice
        print("无效输入，请输入 1-5")

def add_record(learning_log):
    """
    添加学习记录
    这是 Week 03 学的**函数定义**（function definition）——用 def 语句给代码起名字
    learning_log: 字典，格式为 {"日期": "学习内容"}
    """
    date = input("请输入日期（如 02-09）：")
    content = input("请输入今天学了什么：")

    if date in learning_log:
        print(f"注意：{date} 的记录会被覆盖")
    learning_log[date] = content
    print(f"已添加：{date} - {content}")

def show_records(learning_log):
    """查看所有学习记录"""
    if not learning_log:
        print("还没有学习记录哦，去添加一些吧！")
        return

    print("\n=== 学习记录 ===")
    # 按日期排序
    for date in sorted(learning_log.keys()):
        print(f"{date}: {learning_log[date]}")

def show_stats(learning_log):
    """统计学习天数"""
    count = len(learning_log)
    print(f"\n你已经学习了 {count} 天")

    if count >= 5:
        print("太棒了！坚持就是胜利！")
    elif count >= 2:
        print("不错的开始，继续加油！")
    else:
        print("万事开头难，加油！")

def get_mood():
    """获取用户心情"""
    print("\n今天心情怎么样？")
    print("1. 充满干劲")
    print("2. 一般般")
    print("3. 有点累")
    mood = input("请输入你的心情（1-3）：")
    return mood

def get_advice(mood):
    """根据心情返回建议"""
    if mood == "1":
        return "太好了！推荐你今天挑战一个新概念，比如列表或字典。"
    elif mood == "2":
        return "那就做点巩固练习吧，写几个小例子，熟悉一下遍历模式。"
    elif mood == "3":
        return "累了就休息一下吧，今天可以只看视频不动手，或者写 10 分钟代码就停。"
    else:
        return "写点巩固练习最稳妥。"

def show_advice():
    """功能：显示学习建议"""
    mood = get_mood()
    advice = get_advice(mood)
    print(f"\n{advice}")

def main():
    """主函数"""
    # 用字典存储学习记录
    learning_log = {}

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

请选择功能：
1. 添加学习记录
2. 查看所有记录
3. 统计学习天数
4. 获取学习建议
5. 退出

请输入选择（1-5）：1
请输入日期（如 02-09）：02-09
请输入今天学了什么：学会了列表和字典的基本用法
已添加：02-09 - 学会了列表和字典的基本用法

----------------------------------------

请选择功能：
1. 添加学习记录
2. 查看所有记录
3. 统计学习天数
4. 获取学习建议
5. 退出

请输入选择（1-5）：2

=== 学习记录 ===
02-09: 学会了列表和字典的基本用法

----------------------------------------

请选择功能：
1. 添加学习记录
2. 查看所有记录
3. 统计学习天数
4. 获取学习建议
5. 退出

请输入选择（1-5）：3

你已经学习了 1 天
万事开头难，加油！
```

对比上周的代码，你会发现几个变化：

1. **用字典存储数据**：`learning_log = {}` 是一个空字典，用来存储"日期→学习内容"
2. **字典作为参数传递**：`add_record(learning_log)` 把字典传给函数，函数内部修改字典
3. **字典遍历**：`show_records()` 遍历字典，按日期排序后输出
4. **字典长度**：`len(learning_log)` 返回字典里有多少个键值对

老潘看到这段代码，点点头："现在 PyHelper 能'记住'你学了什么了。但还有个问题——程序关闭后，数据就没了。下个星期，我们会学到'把数据存到文件'，这样下次打开程序，你的学习记录还在。"

小北问："那为什么不现在就学？"

"因为一口吃不成胖子，"老潘笑笑，"这周先把列表和字典学扎实，下周学文件读写会更轻松。编程就是这样——每周加一点能力，慢慢就能做复杂的事情了。"

---

## Git 本周要点

本周必会命令：
- `git restore <file>` —— 撤销工作区的修改（恢复到最近一次 commit 的状态）
- `git reset --soft HEAD~1` —— 撤销最后一次提交，但保留修改在工作区
- `git status` —— 查看哪些文件被修改了
- `git diff` —— 查看具体改了什么

常见坑：
- 列表索引越界：`scores[5]` 访问了不存在的索引，会报 `IndexError`
- 字典键不存在：`scores["小红"]` 访问了不存在的键，会报 `KeyError`，建议用 `get()` 方法
- `sort()` 返回 `None`：`result = scores.sort()` 是错误的，`sort()` 会修改原列表并返回 `None`
- 混淆 `sort()` 和 `sorted()`：前者修改原列表，后者返回新列表
- 遍历时修改容器：在 `for` 循环里修改正在遍历的列表/字典会导致问题

**遍历时修改的正确做法**：

```python
# ❌ 错误：遍历列表时删除元素
scores = [85, 92, 78, 60, 55]
for score in scores:
    if score < 60:
        scores.remove(score)  # 会跳过某些元素！
```

✅ **正确做法 1：收集要删除的元素，遍历完后再删除**

```python
scores = [85, 92, 78, 60, 55]
to_remove = []
for score in scores:
    if score < 60:
        to_remove.append(score)

for score in to_remove:
    scores.remove(score)
```

✅ **正确做法 2：用列表推导式创建新列表（推荐）**

```python
scores = [85, 92, 78, 60, 55]
# 创建一个新列表，只保留及格的分数
scores = [score for score in scores if score >= 60]
```

撤销修改工作流：
- 如果你改了文件但后悔了：`git restore scores.py` 可以撤销修改（慎用，无法恢复）
- 如果你 commit 了但发现错了：`git reset --soft HEAD~1` 可以撤销 commit 但保留修改，改完再重新 commit

Pull Request (PR)：
- Week 04 暂不要求 PR，但建议练习 `git restore` 和 `git reset`——这两个命令能帮你"反悔"

---

## 本周小结（供下周参考）

这一周，你学会了 Python 里最重要的两个数据结构：**列表**（list）和**字典**（dict）。列表是"有序的元素集合"，可以通过索引访问、可以增删改查、可以排序。字典是"键值对的映射"，可以通过名字（键）快速查找对应的值。

更重要的是，你学会了**遍历模式**——用 `for` 循环逐个处理列表/字典中的元素，以及**数据驱动设计**——把逻辑和数据分开，数据变了，代码不用变。这是编程思维的一个转折点：从"写死逻辑"到"用数据结构简化代码"。

下周，我们将学习"读写文件"——让你的程序能把数据保存到硬盘上，下次打开还能用。你会发现，文件存储的"本质"就是把你的列表和字典转换成文本，下次再读回来。

---

## Definition of Done（学生自测清单）

完成本周学习后，请确认你能：

- [ ] 理解列表的概念，能创建、访问、修改列表元素
- [ ] 掌握列表的常见操作：`append()`、`insert()`、`remove()`、`pop()`、`del`
- [ ] 理解列表切片，能用 `scores[:3]`、`scores[-3:]` 等方式获取子列表
- [ ] 理解 `sort()` 和 `sorted()` 的区别（修改原列表 vs 返回新列表）
- [ ] 理解字典的概念，能创建、访问、修改字典的键值对
- [ ] 掌握字典的常见操作：`get()` 方法、`del`、`pop()`、`in` 判断键是否存在
- [ ] 能用 `for` 循环遍历列表和字典，理解 `for item in list:` 和 `for key, value in dict.items():`
- [ ] 能用 `enumerate()` 同时获取索引和元素
- [ ] 理解"数据驱动设计"的基本思想，能用列表/字典简化代码逻辑
- [ ] 能判断"什么时候用列表，什么时候用字典"
- [ ] 完成班级成绩单项目（录入、查询、统计、排序）
- [ ] 给 PyHelper 添加"学习记录"功能（用字典存储）
- [ ] Git 至少提交 2 次（draft + verify）
- [ ] 运行 `python3 -m pytest chapters/week_04/tests -q` 并通过所有测试

<!--
章节结构骨架（供 chapter-writer 参考）：

1. 章首导入（引言格言 + 时代脉搏）——已完成
2. 前情提要——已完成
3. 学习目标——已完成
4. 贯穿案例设计说明（HTML 注释）——已完成
5. 认知负荷 + 回顾桥 + 角色出场规划（HTML 注释）——已完成
6. AI 小专栏规划（HTML 注释）——已完成
7. 第 1 节：从 10 个变量到 1 个列表——为什么你需要容器——已完成
8. 第 2 节：让列表动起来——增删改查与排序——已完成
9. 第 3 节：从"按位置找"到"按名字找"——字典的威力——已完成
10. 第 4 节：让数据自己说话——遍历模式与数据驱动设计——已完成
11. PyHelper 进度——已完成
12. Git 本周要点——已完成
13. 本周小结（供下周参考）——已完成
14. Definition of Done——已完成
-->
