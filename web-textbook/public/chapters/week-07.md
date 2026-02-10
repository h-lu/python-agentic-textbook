# Week 07：把代码拆开——模块化与项目结构

> "Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."
> — Antoine de Saint-Exupéry

2026 年，AI 代码生成工具正在经历一场"架构转向"。早期的 AI 编程助手擅长生成单文件脚本——你给个需求，它给你几百行代码，能跑，但当你想要扩展功能时，问题就来了：代码散落各处、重复逻辑到处都是、改一处影响三处。

业界开始意识到：**AI 能快速生成代码，但设计的瓶颈在架构**。2026 年的多项报告指出，AI 代码生成工具正在从"代码补全"转向"架构优先的协作开发者"。企业不再满足于 AI 生成"能跑的代码"，而是要求它生成"可维护、可扩展、结构清晰的代码"。

这正好印证了软件工程领域几十年的共识：**模块化**（modularization）不是可选技巧，而是大规模软件开发的必修课。Google、Facebook 等巨头公司的代码库能够支撑数十万开发者同时协作，靠的不是每个人都写超快的代码，而是清晰的模块边界和项目结构。

这周你将学会把"一坨代码"拆成"模块化项目"——用 `import` 借用别人的工具，把自己的代码拆成多个文件，用 `__name__` 守卫让模块既能导入也能运行，最后设计一个清晰的项目目录结构。

---

## 前情提要

上周你给 PyHelper 穿上了"防弹衣"——用 `try/except` 捕获各种异常，让程序不再因为一个错误的输入就崩溃。小北很高兴，PyHelper 现在能稳稳地处理各种坏输入了。

但当他打开 `pyhelper.py` 这个文件时，新的焦虑出现了。

"1500 行……"小北盯着编辑器右侧的滚动条，"这个文件也太长了吧？我想找个函数都要滚半天。"

老潘凑过来看了一眼，摇摇头："这还不是最糟的。想象一下，如果我想复用'输入校验'的函数到另一个项目，怎么办？"

"复制粘贴？"小北试探性地问。

"复制粘贴是下策，"老潘说，"更好的方式是把代码拆成多个模块——每个文件各司其职，需要的时候 `import` 进来。"

这周我们来解决这个问题。你将学会**模块化**（modularization）——把一个巨大的单文件项目，拆成结构清晰的多模块项目。这不仅能提高代码的可维护性，还能让代码在项目之间复用。

---

## 学习目标

完成本周学习后，你将能够：
1. 理解模块的概念，掌握 `import` 语句的多种用法
2. 能把单文件代码拆分成多模块，理解 `__name__ == "__main__"` 的作用
3. 掌握 Python 的包结构和 `__init__.py` 的作用
4. 理解重构的概念，能把大函数拆成小模块
5. 能设计清晰的项目目录结构，让代码易于维护

---

## 1. 单文件项目的困境

小北的 PyHelper 现在有 1500 多行代码，全部挤在一个文件里。每次他想找某个函数，都要在编辑器里滚半天，或者用 `Ctrl+F` 搜索。

"这个文件太长了……"小北叹了口气，"我想改个菜单项，结果找了十分钟才找到 `print_menu` 函数在哪儿。"

阿码在旁边探头看了看，惊呼道："哇，这比我想象中还要糟糕。如果我是你，我宁愿重写也不想在这堆代码里找东西。"

小北瞪了他一眼："说得轻巧，你帮忙找？"

阿码凑近屏幕，假装认真找了三秒，然后直起身："算了，我觉得还是重写比较快。"

两人相视一笑——虽然问题很严肃，但偶尔自嘲一下也能缓解焦虑。

老潘走过来，瞥了一眼屏幕，摇头道："这个文件能跑，但维护起来是噩梦。"

"维护？"小北不解。

"对，**维护**（maintenance）——就是修改、扩展、修复 bug，"老潘说，"想象一下，如果你想在三个月后给 PyHelper 加一个新功能，你还能记得每个函数在文件的第几行吗？"

小北摇摇头："肯定记不住。"

"这就对了，"老潘说，"单文件项目在开始时很方便——所有东西都在一个地方，容易理解。但随着代码增长，问题就来了：想找个函数要翻半天；'输入校验'的函数没法用到其他项目；两个人同时改同一个文件时冲突会很麻烦；测试某个功能时可能会影响其他功能。"

阿码举手："那我们应该怎么办？把代码拆成多个文件？"

"对，"老潘点头，"这就是**模块化**（modularization）的核心思想——把大文件拆成小模块，每个模块负责一件事。"

---

### Week 03 的回顾：函数是模块化的第一步

还记得 Week 03 你写的**函数**（function）吗？当时你把"重复的代码"封装成了函数，比如：

```python
def print_menu():
    """打印菜单"""
    print("请选择功能：")
    print("1. 添加学习记录")
    print("2. 查看所有记录")
    print("3. 统计学习天数")
    print("4. 获取学习建议")
    print("5. 退出并保存")
```

函数本身就是一种"模块化"——它把一段代码打包，给个名字，需要的时候调用。

"对啊，"小北恍然大悟，"函数就是把代码'分块'——我在 Week 03 已经在用模块化了？"

"没错，"老潘点头，"函数是'代码块级别'的模块化。这周我们要做的是'文件级别'的模块化——把函数分块成多个文件。"

"哦！"小北若有所思，"所以模块化是'层层递进'的：先把代码分块成函数，再把函数分块成文件。"

"完美的总结！"老潘笑了。

**建议示例文件**：`01_single_file_mess.py`

---

### 为什么单文件难以维护

假设你的 PyHelper 有这些功能：

| 功能 | 函数 | 代码行数 |
|------|------|---------|
| 菜单相关 | `print_menu`, `get_choice` | ~50 行 |
| 文件操作 | `load_learning_log`, `save_learning_log` | ~80 行 |
| 输入校验 | `get_date`, `get_content`, `get_positive_integer` | ~100 行 |
| 业务逻辑 | `add_record`, `show_records`, `show_stats` | ~200 行 |
| 鼓励语 | `get_mood`, `get_advice` | ~50 行 |

如果所有这些都在一个文件里，代码会非常混乱。

"想象一下，"老潘说，"你想改'输入校验'的逻辑，结果不小心改了'文件操作'的代码——这就叫'耦合度过高'。"

"耦合度？"小北疑惑。

"**耦合**（coupling）——不同部分之间的依赖关系，"老潘解释道，"耦合度高，意味着'改 A 会影响 B'；耦合度低，意味着'改 A 不影响 B'。好的设计应该追求'低耦合、高内聚'。"

"高内聚？"阿码追问。

"**内聚**（cohesion）——一个模块内部的相关性，"老潘说，"高内聚意味着'这个模块里的东西都是相关的一类事情'。比如'输入校验'模块里应该只有输入校验的函数，不应该有'文件操作'的代码。"

小北若有所思："所以我们应该把'相关的事情'放到同一个文件里？"

"完美的总结！"老潘点头，"这就是模块化的第一步——**按功能分组**。"

---

现在，你已经理解了为什么要模块化。下一节，我们来学习如何"借用别人的工具"——用 `import` 语句使用标准库模块。

---

## 2. 借用别人的工具——import 基础

在开始拆分自己的代码之前，先来看看 Python 的**标准库**（standard library）——这是 Python 自带的"工具箱"，里面装满了现成的模块，你可以直接拿来用。

阿码第一次看到 `import` 语句时，很疑惑：

"为什么要写 `import math`？为什么不直接把 `math` 模块的代码写在当前文件里？"

"因为**重复造轮子是浪费**，"老潘说，"Python 标准库里有成百上千个模块，每个都是经过测试、优化的代码。你没必要自己写一遍。"

---

### 为什么要用 import

想象一下，如果每次你想计算平方根，都要自己写一遍这个算法：

```python
def sqrt(n):
    """计算平方根（牛顿迭代法）"""
    if n < 0:
        raise ValueError("不能计算负数的平方根")
    if n == 0:
        return 0
    x = n
    for _ in range(100):
        x = (x + n / x) / 2
    return x

# 使用
result = sqrt(16)
print(result)  # 输出: 4.0
```

这太麻烦了！Python 的 `math` 模块已经提供了 `sqrt` 函数：

```python
import math

result = math.sqrt(16)
print(result)  # 输出: 4.0
```

"哦！"小北惊讶道，"这就简单多了！"

"对，"老潘说，"`import` 就是'借用别人的工具'——你不需要知道 `math.sqrt` 内部是怎么实现的，你只需要知道'怎么用'。"

---

### import 的基本语法

Python 有几种 `import` 的写法，每种都有自己的用途。

#### 写法 1：import module

这是最基础的写法——导入整个模块。

```python
import math

result = math.sqrt(16)
print(f"平方根：{result}")

pi = math.pi
print(f"圆周率：{pi}")
```

使用时需要加模块名前缀（`math.sqrt`、`math.pi`）。

"为什么要加前缀？"小北问，"不能直接写 `sqrt(16)` 吗？那样更短啊。"

"因为**避免命名冲突**，"老潘说，"想象一下，如果 `math` 模块有一个 `log` 函数，你自己的代码也有一个 `log` 函数——如果不加前缀，Python 就不知道你想用哪个。"

小北若有所思："就像两个人都叫'小明'，你叫'小明'时，他们不知道你在叫谁。"

"完美的类比！"老潘笑了，"所以加模块名前缀就像说'数学班的小明'和'英语班的小明'，不会混淆。"

**建议示例文件**：`02_import_module.py`

---

#### 写法 2：from module import name

如果你只想用模块里的某几个功能，可以用 `from ... import ...`：

```python
from math import sqrt, pi

# 直接使用，不需要加前缀
result = sqrt(16)
print(f"平方根：{result}")
print(f"圆周率：{pi}")
```

"这样更简洁！"小北高兴道。

"但要注意命名冲突，"老潘提醒，"如果你自己的代码也有一个 `pi` 变量，就会覆盖导入的 `pi`。"

```python
from math import pi

pi = 3.14  # 覆盖了导入的 pi
print(pi)  # 输出: 3.14（不是 math.pi 的精确值）
```

**建议示例文件**：`03_from_import.py`

---

#### 写法 3：import module as alias

如果你想给模块起个简短的名字，可以用 `as`：

```python
import math as m

result = m.sqrt(16)
print(f"平方根：{result}")
```

这在模块名字很长时特别有用，比如：

```python
import matplotlib.pyplot as plt  # 数据可视化库
plt.plot([1, 2, 3], [4, 5, 6])
plt.show()
```

**建议示例文件**：`04_import_alias.py`

---

### 常用的标准库模块

Python 标准库有数百个模块，这里列出几个你最常用的：

| 模块 | 功能 | 示例函数/常量 |
|------|------|-------------|
| `math` | 数学函数 | `sqrt()`, `sin()`, `cos()`, `pi` |
| `random` | 随机数 | `random()`, `choice()`, `shuffle()` |
| `datetime` | 日期时间 | `datetime.now()`, `timedelta` |
| `pathlib` | 路径处理 | `Path()`, `read_text()`, `write_text()` |
| `json` | JSON 数据 | `loads()`, `dumps()` |
| `re` | 正则表达式 | `search()`, `findall()`, `sub()` |

阿码好奇地问："这么多模块，怎么记住？"

"不需要全部记住，"老潘笑笑，"记住最常用的（`math`、`random`、`datetime`、`pathlib`），其他的用到再查。"

---

### Week 04 的回顾：用 random 操作字典

还记得 Week 04 你用**字典**（dict）存储键值对数据吗？当时你学了如何用"人名→分数"这样的映射关系。

现在，结合刚学的 `import random`，你可以做一个"随机抽问器"：

```python
import random

students = ["小北", "阿码", "老潘", "小红", "小明"]
scores = {
    "小北": 85,
    "阿码": 90,
    "老潘": 88,
    "小红": 92,
    "小明": 87
}

# 随机抽取一个学生
lucky_student = random.choice(students)
lucky_score = scores[lucky_student]

print(f"幸运同学：{lucky_student}")
print(f"他的分数：{lucky_score}")
```

`random.choice` 会从列表中随机选一个元素——你刚从 `random` 模块"借来"了这个功能，配合 Week 04 的字典，用几行代码就做出了一个实用工具。

"哦！"小北恍然大悟，"原来模块是这样用的——把别人的工具和自己的数据结合起来！"

**建议示例文件**：`05_random_dict.py`

---

### 为什么要"不要重复造轮子"

老潘看到一个同学在写自己的"排序算法"，摇头道："为什么要自己写排序？Python 的 `sorted()` 已经做了。"

"但我想学习排序算法的原理啊！"那个同学说。

"学习可以，但工程上不要，"老潘说，"标准库的代码经过了无数人的测试和优化，比你自己写的更可靠、更高效。"

他给了一个简单的规则：

**如果标准库已经有了，就用它；如果没有，再考虑自己写或用第三方库。"

"那第三方库呢？"阿码问，"比如 `requests`、`numpy` 这些？"

"第三方库也能用 `import` 导入，"老潘说，"但需要先用 `pip` 安装。这个我们后面会讲。现在先用好标准库。"

**建议示例文件**：`06_standard_library_demo.py`

---

现在，你已经学会了如何使用 `import` 借用别人的工具。下一节，我们来学习如何**拆分自己的代码**——把一个单文件项目变成多模块项目。

---

## 3. 拆分自己的模块

"我该从哪儿开始？"小北盯着自己那1500行的 `pyhelper.py`，"从哪一行下手啊？"

"别盯着行号看，"老潘笑了，"你拆书的时候不是一页一页撕，而是按章节拆。代码也一样——**按功能分组**。"

他和阿码一起翻了一遍 PyHelper 的代码，在纸上画了个表格：

| 功能 | 函数 | 代码行数 |
|------|------|---------|
| 菜单相关 | `print_menu`, `get_choice` | ~50 行 |
| 文件操作 | `load_learning_log`, `save_learning_log` | ~80 行 |
| 输入校验 | `get_date`, `get_content`, `get_positive_integer` | ~100 行 |
| 业务逻辑 | `add_record`, `show_records`, `show_stats` | ~200 行 |
| 鼓励语 | `get_mood`, `get_advice` | ~50 行 |

"哦！"阿码拍了一下脑袋，"这就像整理衣柜——把上衣放一起、裤子放一起、袜子放一起，找的时候不用翻遍整个衣柜。"

"完美的类比！"老潘点头，"现在我们按这个拆分方案创建文件。"

他们一起分析了 PyHelper 的代码，决定这样拆分：

| 文件 | 职责 | 包含的函数 |
|------|------|-----------|
| `menu.py` | 菜单相关 | `print_menu`, `get_choice` |
| `storage.py` | 文件操作 | `load_learning_log`, `save_learning_log`, `get_data_file` |
| `input_handler.py` | 输入校验 | `get_date`, `get_content`, `get_positive_integer` |
| `encouragement.py` | 鼓励语 | `get_mood`, `get_advice` |
| `records.py` | 业务逻辑 | `add_record`, `show_records`, `show_stats` |
| `main.py` | 主入口 | `main`, `if __name__ == "__main__"` |

"哦！"小北眼睛一亮，"这样每个文件都有自己的职责，看起来清楚多了。"

---

### Step 1：创建第一个模块

小北先把"文件操作"相关的函数拆出来，创建 `storage.py`：

```python
# storage.py - 文件操作模块

from pathlib import Path

def get_data_file():
    """获取数据文件的路径"""
    return Path.cwd() / "pyhelper_data.txt"

def load_learning_log():
    """从文件加载学习记录（返回字典）"""
    data_file = get_data_file()
    learning_log = {}

    try:
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
    except Exception as e:
        print(f"加载文件时出错：{e}")
        print("将创建新的数据文件")

    return learning_log

def save_learning_log(learning_log):
    """保存学习记录到文件"""
    data_file = get_data_file()

    try:
        content = ""
        for date, log in learning_log.items():
            content += f"{date}: {log}\n"

        data_file.write_text(content, encoding="utf-8")
        print(f"已保存 {len(learning_log)} 条学习记录")
    except Exception as e:
        print(f"保存文件时出错：{e}")
```

"这里用到了 Week 05 学的 `pathlib`，"老潘点评道，"很好——你在复用之前学过的知识。"

**建议示例文件**：`storage.py`

---

### Step 2：在主程序中导入模块

接下来，小北在 `main.py` 中导入 `storage` 模块：

```python
# main.py - 主入口

from storage import load_learning_log, save_learning_log

def main():
    """主函数"""
    # 启动时加载学习记录
    learning_log = load_learning_log()

    print("=== 欢迎使用 PyHelper！===")
    print(f"当前有 {len(learning_log)} 条学习记录")

    # 退出前保存学习记录
    save_learning_log(learning_log)
    print("再见！")

if __name__ == "__main__":
    main()
```

"哇！"小北兴奋地运行代码，"真的能用了！"

"对，"老潘点头，"`from storage import load_learning_log, save_learning_log` 会从 `storage.py` 文件中导入这两个函数，然后你就可以像使用本地函数一样使用它们。"

**建议示例文件**：`main.py`

---

### Week 05 和 Week 06 的回顾：文件操作和异常处理

在 `storage.py` 中，你用到了 Week 05 学的**文件操作**（`pathlib`、`read_text`、`write_text`）和 Week 06 学的**异常处理**（`try/except`）。

这就是回顾桥的威力——**旧知识在新场景下再次出场**。你会发现，之前学的"文件读写"和"错误捕获"在模块化时特别有用。

"模块化和异常处理经常一起使用，"老潘说，"比如 `load_learning_log` 可能会抛出 `FileNotFoundError`，你在模块里用 `try/except` 捕获它，让调用者不会因为文件问题而崩溃。"

"哦！"小北若有所思，"所以模块化不仅是'分块'，还是'封装错误'——把异常处理封装在模块内部，外部调用者就不用担心了。"

"完美的总结！"老潘点头。

**建议示例文件**：`07_main_with_storage.py`

---

### 小北遇到的 ImportError

小北继续拆分其他模块，创建 `input_handler.py`：

```python
# input_handler.py - 输入校验模块

def get_choice(min_choice=1, max_choice=5):
    """获取用户选择（带异常处理）"""
    while True:
        try:
            choice = int(input(f"\n请输入选择（{min_choice}-{max_choice}）："))
            if min_choice <= choice <= max_choice:
                return choice
            print(f"错误：请输入 {min_choice} 到 {max_choice} 之间的数字")
        except ValueError:
            print("错误：请输入数字，不要输入文字")

def get_date():
    """获取日期（格式：MM-DD）"""
    while True:
        date = input("请输入日期（如 02-09）：")

        if "-" not in date or len(date) != 5:
            print("错误：日期格式不对，请输入类似 '02-09' 的格式")
            continue

        parts = date.split("-")
        if not (parts[0].isdigit() and parts[1].isdigit()):
            print("错误：日期必须是数字，请输入类似 '02-09' 的格式")
            continue

        return date

def get_content():
    """获取学习内容"""
    while True:
        content = input("请输入今天学了什么：")

        if not content.strip():
            print("错误：学习内容不能为空")
            continue

        return content
```

然后在 `main.py` 中导入：

```python
from storage import load_learning_log, save_learning_log
from input_handler import get_choice

def main():
    learning_log = load_learning_log()
    choice = get_choice()
    print(f"你选择了：{choice}")
```

运行后，Python 报错了：

```
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    from input_handler import get_choice
ImportError: No module named 'input_handler'
```

"怎么回事！？"小北盯着屏幕，抓了抓头发，"我明明创建了 `input_handler.py` 啊！Python 是不是瞎了？"

阿码在旁边偷笑："Python 不会瞎，但它的'眼睛'只看特定的地方。"

老潘凑过来看了一眼，问："你的 `input_handler.py` 和 `main.py` 在同一个目录下吗？"

"呃……"小北检查了一下，脸红了，"`input_handler.py` 在桌面上，`main.py` 在文档里。"

"Python 不会去你的桌面找模块，"老潘笑了，"它只会在特定的**搜索路径**（module search path）里找。如果模块文件不在搜索路径里，就会报 `ImportError`。"

小北叹了口气："我觉得自己好像个傻子。"

"别这样，"老潘拍拍他的肩膀，"每个人都犯过这个错。我当年也犯过——那时候我把模块放在了下载文件夹里，然后困惑了半小时。"

---

### 模块搜索路径

"Python 不会去你的桌面找模块，"老潘笑了，"它有自己的一套'搜索路线'。"

他画了个示意图：

**Python 找模块的顺序（就像找人一样）**：

1. **当前目录**（"先看看自己房间里有没有"）——运行脚本所在的目录
2. **PYTHONPATH 环境变量**（"再去常去的几个地方找找"）——用户配置的路径列表
3. **标准库目录**（"最后去公共图书馆查"）——Python 安装时的库目录

"最简单的办法是，"老潘说，"把所有模块文件放在同一个目录下——就像把你要用的书都放在书桌上，伸手就能拿到。"

小北把 `input_handler.py` 移到 `main.py` 所在的目录，再次运行：

```bash
$ python3 main.py
已加载 0 条学习记录
=== 欢迎使用 PyHelper！===

请输入选择（1-5）：1
你选择了：1
```

"成功了！"小北高兴地说。

"对，"老潘点头，"记住：**模块文件必须放在 Python 能找到的地方**。"

**建议示例文件**：`08_module_search_path.py`

---

### 继续拆分：创建更多模块

小北继续拆分其他功能。最终的项目结构是：

```
pyhelper/
├── main.py              # 主入口
├── storage.py           # 文件操作
├── input_handler.py     # 输入校验
├── encouragement.py     # 鼓励语
└── records.py           # 业务逻辑
```

每个模块的职责都很清晰：

| 模块 | 职责 |
|------|------|
| `main.py` | 程序入口，调用其他模块 |
| `storage.py` | 负责文件的读取和写入 |
| `input_handler.py` | 负责用户输入的校验 |
| `encouragement.py` | 负责生成鼓励语和建议 |
| `records.py` | 负责学习记录的增删查统计 |

"这样看起来清楚多了！"小北满意地说，"现在我想改'输入校验'的逻辑，只需要打开 `input_handler.py`，不用在一大堆代码里找半天。"

"没错，"老潘点头，"这就是模块化的价值——**降低认知负担**。"

**建议示例文件**：`09_split_modules_demo.py`

---

> **AI 时代小专栏：AI 如何影响代码组织和模块化**
>
> 你刚学会了如何把自己的代码拆成多个模块。但在 AI 时代，这个问题变得更加重要——AI 生成的代码经常是"能跑的单文件脚本"，缺乏清晰的结构。
>
> 2026 年，AI 代码生成工具正在经历一场"架构转向"。早期的 AI 编程助手（如 GitHub Copilot 的早期版本）擅长生成单文件脚本——你给个需求，它给你几百行代码，能跑，但缺乏结构。企业开始发现：**AI 生成的代码在短期内能跑，但长期难以维护**。
>
> 一项针对 AI 代码的深度分析显示，AI 生成的代码存在严重的"设计天花板"——它能快速生成功能，但难以设计出以下特性的系统：
> - **可扩展性**——系统能否在负载增长时保持性能
> - **可维护性**——新开发者能否快速理解代码结构
> - **模块化**——代码是否被合理拆分、边界是否清晰
>
> 2026 年的行业报告指出，AI 编程工具正在从"代码补全"转向"架构优先的协作开发者"。这意味着：未来的 AI 工具不仅要会写代码，还要会设计**清晰的模块结构**。
>
> 但这并不意味着你可以把模块化交给 AI。相反，**理解模块化原则变得更重要了**——因为：
> 1. 你需要审查 AI 生成的代码结构，判断是否合理
> 2. 你需要给 AI 提供清晰的"架构约束"，让它按照你的设计生成代码
> 3. 你需要重构 AI 生成的"面条代码"，让它变得可维护
>
> 所以，即使你用 AI 辅助编程，**模块化思维仍然是你的核心竞争力**——AI 能帮你写代码，但它不能替你设计架构。
>
> 参考（访问日期：2026-02-09）：
> - [AI coding tools face 2026 reset towards architecture](https://itbrief.news/story/ai-coding-tools-face-2026-reset-towards-architecture/)
> - [AI code generation hits design ceiling - program architecture now the bottleneck](https://thebiggish.com/news/ai-code-generation-hits-design-ceiling-program-architecture-now-the-bottleneck)
> - [AI Coding Agents in 2026: Coherence Through Orchestration](https://mikemason.ca/writing/ai-coding-agents-jan-2026/)
> - [The Advantages of Modular Design in Software Engineering](https://www.csuohio.edu/sites/default/files/98B-The%2520Advantages%2520of%2520Modular%2520Design%2520in%2520Software%2520Engineering.pdf)
>
> ---

现在，你已经学会了如何把单文件代码拆成多模块。但小北在拆分时遇到了一个问题：他想测试 `storage.py` 里的函数，但每次都要从 `main.py` 运行，太麻烦了。

下一节，我们来学习一个重要的技巧——**`__name__` 守卫**，让模块既能被导入也能独立运行。

---

## 4. __name__ 守卫——既能导入也能运行

小北在拆分模块时，遇到了一个问题：他想测试 `storage.py` 里的函数，但每次都要从 `main.py` 运行。

"有没有办法直接运行 `storage.py`，测试它的功能？"小北问。

"有，"老潘说，"用 `if __name__ == "__main__":` 守卫。"

---

### 问题：导入时代码自动运行

小北的 `storage.py` 末尾有这段测试代码：

```python
# storage.py

def load_learning_log():
    # ... 函数实现
    pass

# 测试代码
learning_log = load_learning_log()
print(f"加载了 {len(learning_log)} 条记录")
```

当他在 `main.py` 中导入 `storage` 模块时：

```python
from storage import load_learning_log

def main():
    learning_log = load_learning_log()
    # ...
```

运行 `main.py`，结果输出：

```
加载了 0 条记录  # 这是 storage.py 的测试代码输出的
加载了 0 条记录  # 这是 main.py 的代码输出的
```

"怎么回事！？"小北疑惑道，"我只调用了一次 `load_learning_log`，为什么会输出两次？"

"因为 `storage.py` 的测试代码在导入时自动运行了，"老潘解释道，"当你 `import storage` 时，Python 会执行 `storage.py` 的所有代码——包括测试代码。"

"那怎么办？"小北问，"我想让测试代码在'直接运行 storage.py 时'执行，但'导入 storage 时'不执行。"

"用 `if __name__ == "__main__":` 守卫，"老潘说。

---

### __name__ 守卫的原理

Python 有一个内置变量 `__name__`，它的值取决于模块是如何被运行的：

| 运行方式 | `__name__` 的值 |
|---------|----------------|
| 直接运行（`python3 storage.py`） | `"__main__"` |
| 被导入（`import storage`） | `"storage"`（模块名） |

所以，你可以这样写：

```python
# storage.py

def load_learning_log():
    # ... 函数实现
    pass

# 测试代码（只在直接运行时执行）
if __name__ == "__main__":
    learning_log = load_learning_log()
    print(f"加载了 {len(learning_log)} 条记录")
    print("测试完成！")
```

现在，当你直接运行 `storage.py`：

```bash
$ python3 storage.py
加载了 0 条记录
测试完成！
```

测试代码会执行。

但当你导入 `storage` 模块：

```python
from storage import load_learning_log

learning_log = load_learning_log()
# 不会输出 "测试完成！"
```

测试代码不会执行。

"哦！"小北恍然大悟，"这样模块既能被导入，也能独立运行测试！"

"完美的总结！"老潘点头，"这就是 `__name__` 守卫的价值——**让模块既能当工具，也能当程序**。"

**建议示例文件**：`10_name_guard.py`

---

### Week 03 的回顾：函数定义

在 `__name__` 守卫里，你经常会调用 Week 03 学的**函数**来测试模块：

```python
# storage.py

def load_learning_log():
    # ... 函数实现
    pass

def save_learning_log(learning_log):
    # ... 函数实现
    pass

def test_storage():
    """测试 storage 模块"""
    print("=== 测试 storage 模块 ===")

    learning_log = load_learning_log()
    print(f"加载了 {len(learning_log)} 条记录")

    learning_log["02-09"] = "学习了模块化"
    save_learning_log(learning_log)
    print("测试完成！")

if __name__ == "__main__":
    test_storage()
```

这里定义了一个 `test_storage()` 函数，然后在 `__name__` 守卫里调用它——又是 Week 03 的函数定义在新的场景下出场。

"为什么要多写一个 `test_storage()` 函数？"小北问，"为什么不直接把测试代码写在 `if` 下面？"

"因为**可读性和可维护性**，"老潘说，"把测试代码封装成函数，有两个好处：

1. 代码更清晰——你一眼就能看出'这是测试函数'
2. 方便扩展——如果测试变复杂，你可以添加多个测试函数"

阿码在旁边若有所思："所以我 Week 03 学的函数定义，现在又派上新用场了——它让模块的测试代码也更清晰。"

"没错，"老潘点头，"这就是 Python 的魅力——基础概念在不同的场景下反复出现，每次都有新的价值。"

**建议示例文件**：`11_name_guard_with_test.py`

---

### 老潘的解释：既能当工具也能当程序

老潘给了一个生动的类比：

"`__name__` 守卫就像一个'开关'——当模块被导入时，它是'工具'（只提供函数）；当模块被直接运行时，它是'程序'（执行测试代码）。"

阿码好奇地问："那什么时候需要让模块'既能当工具也能当程序'？"

"两种场景，"老潘说：

**场景 1：测试模块**

你写了一个 `storage.py`，想测试它的功能。你可以在 `__name__` 守卫里写测试代码：

```python
if __name__ == "__main__":
    test_storage()
```

这样，当你直接运行 `storage.py` 时，会执行测试；但当你导入 `storage` 时，不会执行测试。

**场景 2：让模块独立运行**

你写了一个 `records.py`，它既可以被 `main.py` 导入使用，也可以独立运行（比如提供命令行接口）：

```python
# records.py

def add_record(learning_log):
    # ... 函数实现
    pass

def show_records(learning_log):
    # ... 函数实现
    pass

if __name__ == "__main__":
    # 独立运行时的逻辑
    learning_log = {}
    print("=== 独立运行 records.py ===")
    add_record(learning_log)
    show_records(learning_log)
```

这样，`records.py` 既能被其他模块导入使用，也能独立运行。

**建议示例文件**：`12_name_guard_patterns.py`

---

### 常见错误：把所有代码都放在守卫里

小北一开始犯了一个错误——他把所有代码都放在 `__name__` 守卫里：

```python
# storage.py （错误示例）

if __name__ == "__main__":
    def load_learning_log():
        # ... 函数定义
        pass

    def save_learning_log(learning_log):
        # ... 函数定义
        pass

    learning_log = load_learning_log()
    save_learning_log(learning_log)
```

结果，当他导入 `storage` 模块时：

```python
from storage import load_learning_log  # 报错！
```

Python 报错了：

```
ImportError: cannot import name 'load_learning_log' from 'storage'
```

"为什么会这样？"小北不解。

"因为**函数定义在守卫里面**，"老潘解释道，"当你导入 `storage` 时，`__name__` 守卫不会执行，所以函数定义也不会执行——函数根本不存在。"

"哦！"小北恍然大悟，"所以我应该把函数定义写在守卫外面，只把'测试代码'写在守卫里面？"

"完美的总结！"老潘点头，"记住：**函数定义应该在守卫外面，测试代码应该在守卫里面**。"

**建议示例文件**：`13_name_guard_common_mistake.py`

---

现在，你已经掌握了 `__name__` 守卫的用法。下一节，我们来学习**包结构**（package structure）——当文件太多时，怎么组织它们。

---

> **AI 时代小专栏：AI 时代的"长尾代码"问题**

> 你刚学了 `__name__` 守卫，理解了如何让模块"既能导入也能运行"。但在 AI 时代，这个问题变得更加重要——AI 生成的代码经常缺少这个守卫。
>
> 为什么？因为 AI 训练时的"样例代码"大多没有 `__name__` 守卫——教程为了简洁，通常会省略它。AI 学习这些样例后，也就学会了"不写守卫"。
>
> 这导致了一个问题：**AI 生成的代码往往只能被导入，或者只能直接运行，不能两者兼得**。
>
> 2026 年的研究指出，AI 生成的代码存在"可复用性缺陷"——代码能跑，但难以集成到更大的项目中。`__name__` 守卫就是一个典型的例子：
> - 没有 `__name__` 守卫的代码，导入时会自动执行测试代码（可能很慢）
> - 有 `__name__` 守卫的代码，既能当模块导入，也能独立测试
>
> 这就是为什么**你需要理解 `__name__` 守卫**——即使你用 AI 生成代码，也需要手动加上它，让代码更可复用。
>
> 参考（访问日期：2026-02-09）：
> - [The AI Coding Technical Debt Crisis: What 2026-2027 Holds](https://www.pixelmojo.io/blogs/vibe-coding-technical-debt-crisis-2026-2027)
> - [The Hidden Costs of AI-Generated Code in 2026](https://www.codebridge.tech/articles/the-hidden-costs-of-ai-generated-software-why-it-works-isnt-enough)
> - [AI Technical Debt Is Eating Your 2026 Margins](https://wishtreetech.com/blogs/ai/why-technical-debt-is-quietly-eating-away-your-2026-margins/)
> - [When AI-Generated Code Becomes Legacy Debt](https://www.linkedin.com/pulse/when-ai-generated-code-becomes-legacy-debt-why-ai-reda-mansour-phd-iizmc)
> - [Python __main__ — Top-level code environment](https://docs.python.org/3/library/__main__.html)
> - [Real Python: What Does if __name__ == "__main__" Do?](https://realpython.com/if-name-main-python/)

---

## 5. 包与项目结构

到目前为止，你已经学会了如何把单文件代码拆成多个模块。但当模块数量增多时（比如超过 10 个），把它们全部放在同一个目录下也会变得混乱。

这时候，你需要**包结构**（package structure）——用目录来组织模块。

阿码好奇地问："为什么要用包结构？直接把所有 `.py` 文件放在同一目录下不行吗？"

"行，但不好，"老潘说，"想象一下，你有 20 个模块文件，全部堆在一个目录下——这和 1500 行的单文件有什么区别？"

"哦，"阿码点点头，"还是得'按功能分组'。"

---

### 什么是包

**包**（package）就是一个包含 `__init__.py` 文件的目录。Python 用 `__init__.py` 来识别一个目录是包。

"等等，"小北举手，"`__init__.py` 是什么？有什么用？"

"`__init__.py` 是包的'身份证'，"老潘解释，"它告诉 Python'这个目录是一个包'。"

最简单的 `__init__.py` 可以是空的：

```python
# __init__.py （可以是空的）
```

或者，你可以用 `__init__.py` 来简化导入：

```python
# pyhelper/__init__.py

from .storage import load_learning_log, save_learning_log
from .input_handler import get_choice
from .encouragement import get_advice
```

这样，你可以直接从包根目录导入：

```python
from pyhelper import load_learning_log, save_learning_log, get_choice
```

"哦！"小北恍然大悟，"`__init__.py` 就像一个'快捷方式'——它把包里的常用函数暴露出来。"

"完美的类比！"老潘点头。

---

### Week 05 的回顾：pathlib 在项目结构中的使用

还记得 Week 05 你用 `pathlib` 处理文件路径吗？现在，在模块化项目中，`pathlib` 也能帮你大忙。

假设你的项目结构是这样：

```
pyhelper/
├── __init__.py
├── main.py
├── storage.py
├── input_handler.py
└── data/
    └── pyhelper_data.txt
```

你可以在 `storage.py` 中用 `pathlib` 来"智能定位"数据文件：

```python
from pathlib import Path

def get_data_file():
    """获取数据文件的路径"""
    # 假设数据文件在 data/ 目录下
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)  # 如果目录不存在，创建它
    return data_dir / "pyhelper_data.txt"
```

"`__file__` 是什么？"小北问。

"`__file__` 是当前模块文件的路径，"老潘解释，"`Path(__file__).parent` 会得到模块所在的目录。"

"哦！"小北若有所思，"这样无论我把 `pyhelper` 目录放在哪儿，它都能找到 `data/` 目录——就像模块自带了'导航系统'。"

"完美的类比！"老潘点头，"这就是**相对路径**的好处——不依赖当前工作目录。Week 05 你学的 `pathlib`，现在在模块化项目里又派上新用场了。"

**建议示例文件**：`pathlib_in_project.py`

---

### 包结构的最佳实践

老潘给了一个推荐的项目结构：

```
pyhelper/                    # 项目根目录
├── pyhelper/                # 包目录
│   ├── __init__.py          # 包初始化
│   ├── main.py              # 主入口
│   ├── storage.py           # 文件操作
│   ├── input_handler.py     # 输入校验
│   ├── encouragement.py     # 鼓励语
│   └── records.py           # 业务逻辑
├── tests/                   # 测试目录
│   ├── test_storage.py
│   └── test_input_handler.py
├── data/                    # 数据目录
│   └── pyhelper_data.txt
├── examples/                # 示例代码
│   └── basic_usage.py
├── README.md                # 项目说明
├── requirements.txt         # 依赖列表
└── setup.py                 # 安装配置
```

"为什么要这么复杂？"小北不解。

"因为**可维护性和可扩展性**，"老潘说，"这个结构遵循了 Python 社区的最佳实践：代码在 `pyhelper/` 目录下，和 `tests/`、`data/` 分开；测试在 `tests/` 目录下，和代码分开但结构对应；数据在 `data/` 目录下，不会和代码混在一起。此外还有 `README.md` 告诉别人项目是做什么的，`requirements.txt` 列出依赖的第三方库，`setup.py` 让别人能 `pip install` 安装你的项目。"

"哦！"小北眼睛一亮，"这样别人看到这个项目，一眼就能明白'这是什么、怎么用、怎么安装'。"

"完美的总结！"老潘点头。

**建议示例文件**：`project_structure_demo/`

---

### 相对导入

在包内部，你可以用**相对导入**（relative import）来导入同包的其他模块：

```python
# pyhelper/records.py

from .storage import load_learning_log, save_learning_log
from .input_handler import get_date, get_content

def add_record(learning_log):
    date = get_date()
    content = get_content()
    # ...
```

这里的 `.` 表示"当前包"。

"为什么要用相对导入？"阿码问，"直接 `from storage import ...` 不行吗？"

"用相对导入有两个好处，"老潘说：

**好处 1：清晰——一眼就能看出这是'同包内的导入'**
```python
from .storage import load_learning_log  # 相对导入（同包）
from storage import load_learning_log   # 绝对导入（可能混淆）
```

**好处 2：避免命名冲突——如果外部也有一个 `storage` 模块，相对导入会优先使用同包的**

"哦！"阿码若有所思，"相对导入就像说'我隔壁的邻居'，绝对导入就像说'某某市的某某人'。"

"完美的类比！"老潘笑了。

**建议示例文件**：`relative_import_demo.py`

---

### 何时使用包结构

阿码追问："那什么时候需要用包结构？什么时候只用多模块就够了？"

老潘给了一个简单的规则：

| 模块数量 | 推荐结构 | 示例 |
|---------|---------|------|
| 1-3 个 | 单文件或简单多模块 | `script.py` 或 `main.py` + `utils.py` |
| 4-10 个 | 多模块（同目录） | `main.py`, `storage.py`, `input.py` |
| 10+ 个 | 包结构（分目录） | `pyhelper/`, `tests/`, `data/` |

"记住，"老潘说，"**不要过度设计**。如果项目很小，不需要强行套用包结构。但如果你发现项目在增长，及时重构。"

小北点头："对，就像 PyHelper——刚开始只有一个文件，现在拆成了多个模块，未来可能还需要包结构。"

"没错，"老潘说，"**重构是持续的过程**，不是一次性的。"

**建议示例文件**：`15_when_to_use_packages.py`

---

现在，你已经掌握了模块化和项目结构的所有核心技能。下一节，我们把本周学的所有东西应用到 PyHelper 上，把它拆成一个真正的多模块项目。

---

## PyHelper 进度

到目前为止，PyHelper 的所有代码都挤在一个 1500+ 行的文件里。小北早就想把它拆开了，但一直不知道从哪儿开始。

"这周我们学了模块化，"小北兴奋地搓了搓手，"终于可以把 PyHelper 拆开了！我已经准备好剪刀了。"

"别真的拿剪刀剪文件啊，"阿码在旁边开玩笑，"那是物理删除，Python 恢复不了的。"

三人相视而笑。老潘点点头："对，我们按**功能分组**，把 PyHelper 拆成一个多模块项目。不过这次用'剪切粘贴'，不是剪刀。"

---

### 拆分方案

他们一起分析了 PyHelper 的代码，决定这样拆分：

```
pyhelper/
├── main.py              # 主入口
├── storage.py           # 文件操作
├── input_handler.py     # 输入校验
├── encouragement.py     # 鼓励语
└── records.py           # 业务逻辑
```

| 模块 | 职责 | 包含的函数 |
|------|------|-----------|
| `main.py` | 程序入口，调用其他模块 | `main()`, `print_welcome()`, `print_menu()` |
| `storage.py` | 文件操作 | `get_data_file()`, `load_learning_log()`, `save_learning_log()` |
| `input_handler.py` | 输入校验 | `get_choice()`, `get_date()`, `get_content()` |
| `encouragement.py` | 鼓励语 | `get_mood()`, `get_advice()` |
| `records.py` | 业务逻辑 | `add_record()`, `show_records()`, `show_stats()` |

---

### Step 1：创建 storage.py

首先，创建 `storage.py`——负责文件操作：

```python
# storage.py - 文件操作模块

from pathlib import Path

def get_data_file():
    """获取数据文件的路径"""
    return Path.cwd() / "pyhelper_data.txt"

def load_learning_log():
    """从文件加载学习记录（返回字典）"""
    data_file = get_data_file()
    learning_log = {}

    try:
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
    except Exception as e:
        print(f"加载文件时出错：{e}")
        print("将创建新的数据文件")

    return learning_log

def save_learning_log(learning_log):
    """保存学习记录到文件"""
    data_file = get_data_file()

    try:
        content = ""
        for date, log in learning_log.items():
            content += f"{date}: {log}\n"

        data_file.write_text(content, encoding="utf-8")
        print(f"已保存 {len(learning_log)} 条学习记录")
    except Exception as e:
        print(f"保存文件时出错：{e}")

if __name__ == "__main__":
    # 测试代码
    print("=== 测试 storage 模块 ===")
    learning_log = load_learning_log()
    learning_log["02-09"] = "测试：学会了模块化"
    save_learning_log(learning_log)
```

**建议示例文件**：`storage.py`

---

### Step 2：创建 input_handler.py

接下来，创建 `input_handler.py`——负责输入校验：

```python
# input_handler.py - 输入校验模块

def get_choice(min_choice=1, max_choice=5):
    """获取用户选择（带异常处理）"""
    while True:
        try:
            choice = int(input(f"\n请输入选择（{min_choice}-{max_choice}）："))
            if min_choice <= choice <= max_choice:
                return choice
            print(f"错误：请输入 {min_choice} 到 {max_choice} 之间的数字")
        except ValueError:
            print("错误：请输入数字，不要输入文字")

def get_date():
    """获取日期（格式：MM-DD）"""
    while True:
        date = input("请输入日期（如 02-09）：")

        if "-" not in date or len(date) != 5:
            print("错误：日期格式不对，请输入类似 '02-09' 的格式")
            continue

        parts = date.split("-")
        if not (parts[0].isdigit() and parts[1].isdigit()):
            print("错误：日期必须是数字，请输入类似 '02-09' 的格式")
            continue

        return date

def get_content():
    """获取学习内容"""
    while True:
        content = input("请输入今天学了什么：")

        if not content.strip():
            print("错误：学习内容不能为空")
            continue

        return content

if __name__ == "__main__":
    # 测试代码
    print("=== 测试 input_handler 模块 ===")
    choice = get_choice(1, 5)
    print(f"你选择了：{choice}")

    date = get_date()
    print(f"日期：{date}")

    content = get_content()
    print(f"内容：{content}")
```

**建议示例文件**：`input_handler.py`

---

### Step 3：创建 encouragement.py

然后，创建 `encouragement.py`——负责鼓励语：

```python
# encouragement.py - 鼓励语模块

def get_mood():
    """获取用户心情"""
    print("\n今天心情怎么样？")
    print("1. 充满干劲")
    print("2. 一般般")
    print("3. 有点累")

    try:
        mood = int(input("请输入你的心情（1-3）："))
        if mood in [1, 2, 3]:
            return str(mood)
        print("输入无效，默认为一般般")
        return "2"
    except ValueError:
        print("输入无效，默认为一般般")
        return "2"

def get_advice(mood):
    """根据心情返回建议"""
    if mood == "1":
        return "太好了！推荐你今天挑战一个新概念，比如异常处理或模块化。"
    elif mood == "2":
        return "那就做点巩固练习吧，写几个小例子，熟悉一下异常处理。"
    elif mood == "3":
        return "累了就休息一下吧，今天可以只看视频不动手，或者写 10 分钟代码就停。"
    else:
        return "写点巩固练习最稳妥。"

if __name__ == "__main__":
    # 测试代码
    print("=== 测试 encouragement 模块 ===")
    mood = get_mood()
    advice = get_advice(mood)
    print(f"\n建议：{advice}")
```

**建议示例文件**：`encouragement.py`

---

### Step 4：创建 records.py

接着，创建 `records.py`——负责业务逻辑：

```python
# records.py - 业务逻辑模块

from input_handler import get_date, get_content

def add_record(learning_log):
    """添加学习记录（带输入校验）"""
    date = get_date()
    content = get_content()

    if date in learning_log:
        print(f"注意：{date} 的记录已存在")
        overwrite = input("是否覆盖？(y/n)：").lower()
        if overwrite == "y":
            learning_log[date] = content
            print(f"已覆盖：{date} - {content}")
        else:
            print("取消添加")
    else:
        learning_log[date] = content
        print(f"已添加：{date} - {content}")

def show_records(learning_log):
    """查看所有学习记录"""
    if not learning_log:
        print("还没有学习记录哦，去添加一些吧！")
        return

    print("\n=== 学习记录 ===")
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

if __name__ == "__main__":
    # 测试代码
    print("=== 测试 records 模块 ===")
    learning_log = {}
    add_record(learning_log)
    show_records(learning_log)
    show_stats(learning_log)
```

这里用到了**相对导入**（`from input_handler import ...`），因为 `records.py` 和 `input_handler.py` 在同一个目录下。

**建议示例文件**：`records.py`

---

### Step 5：创建 main.py

最后，创建 `main.py`——主入口：

```python
# main.py - 主入口

from storage import load_learning_log, save_learning_log
from input_handler import get_choice
from records import add_record, show_records, show_stats
from encouragement import show_advice

def print_welcome():
    """打印欢迎信息"""
    print("=" * 40)
    print("  欢迎使用 PyHelper！")
    print("=" * 40)
    print()

def print_menu():
    """打印菜单"""
    print("\n请选择功能：")
    print("1. 添加学习记录")
    print("2. 查看所有记录")
    print("3. 统计学习天数")
    print("4. 获取学习建议")
    print("5. 退出并保存")

def main():
    """主函数"""
    # 启动时加载学习记录
    learning_log = load_learning_log()

    print_welcome()

    while True:
        print_menu()
        choice = get_choice(min_choice=1, max_choice=5)

        if choice == 1:
            add_record(learning_log)
        elif choice == 2:
            show_records(learning_log)
        elif choice == 3:
            show_stats(learning_log)
        elif choice == 4:
            show_advice()
        elif choice == 5:
            # 退出前保存学习记录
            save_learning_log(learning_log)
            print("\n再见！祝你学习愉快！")
            break

        print("\n" + "-" * 40)

if __name__ == "__main__":
    main()
```

**建议示例文件**：`main.py`

---

### 最终项目结构

拆分后的项目结构是：

```
pyhelper/
├── main.py              # 主入口（~60 行）
├── storage.py           # 文件操作（~50 行）
├── input_handler.py     # 输入校验（~60 行）
├── encouragement.py     # 鼓励语（~40 行）
└── records.py           # 业务逻辑（~40 行）
```

**拆分前**：1500+ 行的单文件
**拆分后**：5 个模块，每个 40-60 行，职责清晰

"哇！"小北兴奋地说，"现在每个文件都很短，想找什么功能一目了然！"

阿码在旁边点头："而且，如果我想在另一个项目里复用 `input_handler.py`，直接复制过去就行，不用把整个 PyHelper 都复制过去。"

老潘笑了："这就是**模块化的价值**——**降低复杂度、提高复用性、增强可维护性**。"

---

### 运行测试

现在，你可以单独测试每个模块：

```bash
# 测试 storage 模块
$ python3 storage.py
=== 测试 storage 模块 ===
已加载 0 条学习记录
已保存 1 条学习记录

# 测试 input_handler 模块
$ python3 input_handler.py
=== 测试 input_handler 模块 ===

请输入选择（1-5）：3
你选择了：3

# 测试 encouragement 模块
$ python3 encouragement.py
=== 测试 encouragement 模块 ===

今天心情怎么样？
1. 充满干劲
2. 一般般
3. 有点累
请输入你的心情（1-3）：1

建议：太好了！推荐你今天挑战一个新概念，比如异常处理或模块化。

# 运行主程序
$ python3 main.py
已加载 1 条学习记录
========================================
  欢迎使用 PyHelper！
========================================

请选择功能：
1. 添加学习记录
2. 查看所有记录
3. 统计学习天数
4. 获取学习建议
5. 退出并保存

请输入选择（1-5）：...
```

"太好了！"小北高兴地说，"现在 PyHelper 不仅功能完整，而且结构清晰，每个模块都能独立测试。"

老潘点点头："下周我们会给 PyHelper 添加**测试**（testing）——用 pytest 自动验证每个模块的功能是否正确。"

**建议示例文件**：`pyhelper_modular/`

---

## Git 本周要点

本周必会命令：
- `git status` —— 查看当前状态
- `git add -A` —— 添加所有修改
- `git commit -m "message"` —— 提交修改
- `git log --oneline -n 10` —— 查看最近 10 次提交

常见坑：
- **循环导入**——A 模块 import B，B 模块又 import A。解决方法：重构代码，把共同依赖提取到第三个模块
- **相对导入 vs 绝对导入**——在包内导入时，用 `from . import module` 而不是 `from package import module`
- **忘记 `__init__.py`**——Python 3.3+ 虽然支持"命名空间包"，但显式创建 `__init__.py` 仍然是最佳实践
- **`__name__` 守卫误用**——不要把所有代码都放在守卫里面，导入的函数应该在守卫外面
- **模块搜索路径**——导入自定义模块时，确保模块文件在 Python 的搜索路径中（通常是当前目录）

**模块化速查表**：

| 操作 | 语法 | 示例 |
|------|------|------|
| 导入整个模块 | `import module` | `import math` |
| 导入模块的特定函数 | `from module import name` | `from math import sqrt` |
| 导入并重命名 | `import module as alias` | `import numpy as np` |
| 相对导入（同包） | `from . import module` | `from .storage import load` |
| 相对导入（父包） | `from .. import module` | `from ..utils import helper` |

**`__name__` 守卫速查表**：

| 场景 | `__name__` 的值 | 代码是否执行 |
|------|----------------|-------------|
| 直接运行模块 | `"__main__"` | 执行守卫内的代码 |
| 导入模块 | `"module_name"` | 不执行守卫内的代码 |

Pull Request (PR)：
- 本周延续 PR 流程：分支 → 多次提交 → push → PR → review → merge
- PR 描述模板：
  ```markdown
  ## 本周做了什么
  - 把 PyHelper 从单文件拆成多模块项目
  - 使用 `__name__` 守卫让模块既能导入也能运行
  - 设计了清晰的项目结构

  ## 自测
  - [ ] 运行 `python3 -m pytest chapters/week_07/tests -q` 通过
  - [ ] 单独测试每个模块（`python3 storage.py` 等）都能运行
  - [ ] 主程序 `python3 main.py` 功能正常

  ## 待 review
  请重点检查模块拆分的合理性（是否按功能分组）和 `__name__` 守卫的正确性
  ```

---

## 本周小结（供下周参考）

这一周，你学会了把"一坨代码"拆成"模块化项目"。你掌握了 `import` 语句的多种用法（`import module`、`from module import name`、`import module as alias`），理解了模块搜索路径，学会了把单文件代码拆成多个模块，掌握了 `if __name__ == "__main__":` 守卫，理解了包结构和 `__init__.py` 的作用。

你现在写的代码不再是"一团乱麻"——你能按功能分组，设计清晰的项目结构，让代码易于维护、易于复用。这就是**模块化**（modularization）的核心价值。

**本周的 Aha 时刻**：
- 当你第一次把单文件拆成多模块，看着每个文件职责清晰、结构简洁，你可能会想："原来代码可以这样优雅"
- 当你理解 `__name__` 守卫后，看着模块既能被导入也能独立运行，你可能会说："这就是 Python 的设计哲学——简洁而强大"
- 当你把 PyHelper 拆成多模块后，发现想找某个功能只需打开对应的文件，你可能会感慨："模块化真的能降低认知负担"

到目前为止，你已经掌握了 Python 入门和工程进阶的 7 个核心概念：变量、条件判断、函数、数据结构（列表/字典）、文件操作、异常处理、模块化。下周，我们将学习**测试**（testing）——用 pytest 自动验证你的代码是否正确，确保你在修改代码时不会引入新的 bug。

你会发现，测试和模块化经常一起使用——比如给每个模块写独立的测试，确保模块的功能正确。下周 PyHelper 会从"能跑的项目"变成"有质量保障的项目"。

---

## Definition of Done（学生自测清单）

完成本周学习后，请确认你能做到以下事情：

**核心技能**：你能理解模块的概念，掌握 `import` 语句的多种用法（`import module`、`from module import name`、`import module as alias`）；能把单文件代码拆分成多模块，理解模块搜索路径；掌握 `if __name__ == "__main__":` 的作用，让模块既能被导入也能独立运行；理解 Python 的包结构和 `__init__.py` 的作用。

**编程哲学**：你理解**模块化**（modularization）的价值——降低复杂度、提高复用性、增强可维护性。你知道什么时候该用"单文件"、什么时候该用"多模块"、什么时候该用"包结构"。

**实践能力**：你能把一个 500 行的单文件项目拆分成多模块结构；能设计合理的项目目录结构（按功能分组）；能给模块添加 `__name__` 守卫，让模块既能导入也能独立测试；能把 PyHelper 拆成一个真正的多模块项目。

**工程习惯**：你至少提交了 2 次 Git（draft + verify），并且运行 `python3 -m pytest chapters/week_07/tests -q` 通过了所有测试。

---

**如果你想验证自己的掌握程度**，试着回答这些问题：

- `import module` 和 `from module import name` 有什么区别？什么时候用哪种？
- 为什么要用 `if __name__ == "__main__":`？不用会怎样？
- 模块和包的区别是什么？
- 如果导入模块时遇到 `ModuleNotFoundError`，可能是什么原因？
- 相对导入（`from . import module`）和绝对导入（`from package import module`）有什么区别？

如果你能自信地回答这些问题，说明你已经掌握了本周的核心内容。

<!--
章节结构骨架（供 chapter-writer 参考）：

1. 章首导入（引言格言 + 时代脉搏）——已完成
2. 前情提要——已完成
3. 学习目标——已完成
4. 贯穿案例设计说明（HTML 注释）——已完成
5. 认知负荷 + 回顾桥 + 角色出场规划（HTML 注释）——已完成
6. AI 小专栏规划（HTML 注释）——已完成
7. 第 1 节：单文件项目的困境——已完成
8. 第 2 节：import 基础——已完成
9. 第 3 节：拆分自己的模块——已完成
10. 第 4 节：__name__ 守卫——已完成
11. AI 小专栏 #1——已完成
12. 第 5 节：包与项目结构——已完成
13. AI 小专栏 #2——已完成
14. PyHelper 进度——已完成
15. Git 本周要点——已完成
16. 本周小结（供下周参考）——已完成
17. Definition of Done——已完成
-->
