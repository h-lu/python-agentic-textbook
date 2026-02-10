# Week 03：把问题切小

> "Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."
> - Antoine de Saint-Exupéry，《小王子》作者

2026 年的软件行业正在经历一场有趣的"回归"。几年前，微服务（microservices）架构是所有人的答案——把系统拆成几十上百个小服务，每个服务独立部署、独立运行。但到了 2026 年，数据显示 42% 的组织开始放弃纯微服务，转而采用"模块化单体"（modular monolith）架构。就连 Amazon Prime Video 团队也通过从微服务回归单体，将成本降低了 90%。

这背后的原因很简单：过度拆分会带来无法承受的复杂度。真正重要的不是"服务之间的边界"，而是"代码内部的模块化"。把一个大函数拆成几个小函数，把混乱的逻辑整理成清晰的模块——这种"分解问题"的能力，才是编程的核心。本周，你将学会 Python 里做这件事的基础工具：**函数**（function）。

---

## 前情提要

上周你的猜数字游戏已经能做选择、能重复了。如果你把所有代码写在一起，大概会有几十行——还能看得清楚。但想象一下，如果游戏有 10 种难度、20 种道具、30 个特殊规则，代码会变成什么样？上周你用 `if` 和 `while` 写的 PyHelper 也是这样——能跑，但所有逻辑都挤在一起，"获取建议""打印欢迎""处理输入"全都混在一块。

这周我们要解决这个问题：把代码"打包"成函数，让每个功能独立、清晰、可复用。

---

## 学习目标

完成本周学习后，你将能够：
1. 使用 `def` 语句定义函数，把重复的代码"打包"
2. 理解参数的作用，让函数接受不同的输入
3. 使用 `return` 返回计算结果，而不是直接打印
4. 理解作用域的基本概念，知道变量"在哪里能用"
5. 把一个大问题分解为多个小函数，设计清晰的调用关系

---

<!--
贯穿案例：单位换算器

演进路线：
- 第 1 节（函数定义）：从一个"什么都能换"但一坨代码的换算器开始，发现重复代码和难以维护的问题
- 第 2 节（参数）：把换算逻辑抽成函数，接受不同数值作为参数
- 第 3 节（返回值）：函数返回换算结果，而不是直接打印，让结果可以被复用
- 第 4 节（作用域 + 函数分解）：拆成多个小函数（显示菜单、获取输入、执行换算），加菜单循环选择

最终成果：一个模块化的单位换算器，有文字菜单、支持多种换算功能（长度、重量、温度）、代码整洁易维护
-->

<!--
认知负荷预算：
- 本周新概念（4 个，预算上限 4 个）：
  1. 函数定义（def 语句）
  2. 参数（parameter）
  3. 返回值（return）
  4. 作用域（scope）
- 结论：✅ 在预算内

回顾桥设计（至少引用 Week 01-02 的 2 个概念，实际规划 3 个）：
- [变量]（来自 week_01）：在第 1 节，函数是"给一段代码起个变量名"，用变量的概念帮助理解函数名
- [if/elif/else]（来自 week_02）：在第 4 节，菜单选择用到 if/elif/else 做分支
- [while 循环]（来自 week_02）：在第 4 节，菜单循环用到 while 让用户持续选择
-->

<!--
角色出场规划：
- 小北（第 1 节）：写函数时忘记写 def 或冒号，或调用时忘记加括号，引出"定义 vs 调用"的区别
- 阿码（第 3 节）：追问"return 和 print 有什么区别？为什么不能直接 print？"，引出返回值的价值
- 老潘（第 4 节）：给出工程建议——"函数超过 20 行就考虑拆分"，"一个函数只做一件事"
-->

## 1. 50 行代码的噩梦——为什么你需要函数

想象你刚接手了一份别人的代码——一个简单的单位换算器。你想改个输出格式，把"="改成"是"，于是打开了文件：

```python
# 单位换算器 v1——没有函数，一团混乱
print("单位换算器")
print("1. 公里 → 英里")
print("2. 公斤 → 磅")
print("3. 摄氏度 → 华氏度")

choice = input("选择换算类型（1-3）：")

if choice == "1":
    km = float(input("输入公里数："))
    miles = km * 0.621371
    print(f"{km} 公里 = {miles} 英里")
elif choice == "2":
    kg = float(input("输入公斤数："))
    pounds = kg * 2.20462
    print(f"{kg} 公斤 = {pounds} 磅")
elif choice == "3":
    celsius = float(input("输入摄氏度："))
    fahrenheit = celsius * 9/5 + 32
    print(f"{celsius}°C = {fahrenheit}°F")
```

改第一处。好，改第二处。改第三处……等等，如果有 50 种换算呢？

这里用的是上周学的**print 函数**（print）输出信息，和**条件判断**（if/elif/else）做分支——写多了你会发现，这些 `print` 和 `if` 重复出现，改一处还好，改 50 处就是噩梦。

老潘看到这段代码，摇摇头："能跑，但维护起来是噩梦。我当年接手过一个 500 行的函数，想改个输出格式，改了 50 多处还漏了两处——后来 bug 找了我三天。"

小北在旁边听完脸色发白："那我写的代码……以后也会变成别人的噩梦吗？"

"现在还不会，"老潘笑笑，"因为你还不知道怎么把代码'打包'。"

**函数**（function）就是解决这个问题的工具。它不只是"少写代码"，更是"改动时只改一个地方"。

你可以把函数想成"给一段经常用到的代码起个名字"。就像上周学的**变量**（variable）是给数据起名字，函数是给**代码**起名字。

```python
# 定义一个函数——给代码起个名字
def km_to_miles():
    km = float(input("输入公里数："))
    miles = km * 0.621371
    print(f"{km} 公里 = {miles} 英里")

# 调用这个函数——用名字来执行它
km_to_miles()
```

`def` 是"定义"（define）的缩写。`km_to_miles` 是函数名，后面必须加括号 `()`——这是 Python 知道"这是一个函数"的标志。

**哦！时刻来了**：当你定义了这个函数之后，以后任何时候想换算公里到英里，只需要写一行 `km_to_miles()`，而不是复制粘贴那四行代码。如果你想改进换算精度？只改函数定义内部，调用它的代码一行都不用动。这就是函数的威力——**改一处，处处生效**。

小北照着教材敲完代码，自信满满地按下回车——然后什么都没发生。

"怎么回事？我明明定义了函数啊？是不是 Python 坏了？"小北盯着屏幕，反复按了五次回车，还在那儿等着。

阿码在旁边探头看了一眼，忍不住笑出声："你只写了菜谱，没照着做啊！"

你发现问题了吗？小北只写了**定义**，但**没有调用**。

```python
# 只定义，不调用——什么都不会发生
def km_to_miles():
    km = float(input("输入公里数："))
    miles = km * 0.621371
    print(f"{km} 公里 = {miles} 英里")

# 必须调用，函数才会执行
km_to_miles()
```

定义函数就像把菜谱写在纸上——菜不会自己做好。调用函数才是"照着菜谱做菜"，这时候代码才会真正执行。小北的代码就像写了一本菜谱集摆在书架上，但他从没进过厨房。

小北吃过亏后，第二次调用时又犯了一个错——他写成了这样：

```python
km_to_miles  # 忘记括号！
```

运行后——什么都没发生。

"又怎么了！？"小北把手里的笔都摔了。

`km_to_miles`（不带括号）只是提到函数的名字，就像把菜谱拿在手里看；`km_to_miles()`（带括号）才是真正开始做菜。那两个括号就像是说"现在就开始执行！"的信号。

---

## 2. 让函数变得更灵活——参数

上一节的函数有个大问题：每次调用都让你输入公里数。如果你想换算 10、42、100 公里，得运行三次程序，每次输入一个数字。

"这也太蠢了，"小北抱怨道，"我想把一个表里的数据全换算一遍，难道要输入一千次？"

当然不用。你可以直接"告诉"函数要换算多少公里——用**参数**（parameter）。

```python
# 带参数的函数
def km_to_miles(km):
    miles = km * 0.621371
    print(f"{km} 公里 = {miles} 英里")

# 调用时传入具体的值
km_to_miles(10)
km_to_miles(42)
km_to_miles(100)
```

`km` 就是参数——它是函数的"入口"。你可以把它想成上周学的**变量**，只是这个变量的值不是在函数里写死的，而是从外面"传进来"的。

**哦！又来一个**：带参数之后，函数就像个"模板"——你传什么进去，它就处理什么。这比每次都写一遍同样的逻辑强一万倍。

阿码在旁边举手："等一下，这里有两个词——参数和参数，它们有什么区别？"

好问题！中文翻译一样，但英文不一样：
- **参数**（parameter）：定义函数时写的"占位符"（这里是 `km`）
- **参数**（argument）：调用时传入的"实际值"（这里是 `10`、`42`、`100`）

现在可以做一个更有意思的事情：让用户输入一个数字，然后换算不同的单位。

```python
def km_to_miles(km):
    miles = km * 0.621371
    print(f"{km} 公里 = {miles} 英里")

# 用户输入一次，可以换算多个值
user_value = float(input("输入一个数值："))
km_to_miles(user_value)
km_to_miles(user_value * 2)
km_to_miles(user_value / 2)
```

小北试了一下，输入 `10`，结果输出了三行：10 公里、20 公里、5 公里的换算结果。

"等等，"小北突然瞪大眼睛，"我没再输入数字啊！它怎么知道要算 20 和 5 的？"

**这就是函数的魔法**：你传给它什么，它就处理什么。`km_to_miles(user_value * 2)` 这行代码里，`user_value * 2` 会先算出结果（20），然后才传给函数。函数根本不知道你"怎么"得到这个 20 的——它只负责换算。

```python
def convert_length(value, from_unit, to_unit):
    print(f"将 {value} {from_unit} 转换为 {to_unit}")

convert_length(100, "公里", "英里")
convert_length(50, "千克", "磅")
```

参数也是**变量**，但它的作用范围只限于函数内部。这引出了本周最重要的概念之一：**作用域**（scope）。我们下节会详细讲。

---

## 3. 函数的产出——返回值

到目前为止，我们的函数都是直接打印结果。但这样有个问题：函数的结果只能"给人看"，不能"给程序用"。

```python
# 直接打印的函数——结果只能看
def km_to_miles(km):
    miles = km * 0.621371
    print(f"{km} 公里 = {miles} 英里")

# 想把结果存起来？做不到
result = km_to_miles(10)  # result 会是 None
# 无法用结果做运算
double_result = result * 2  # 会报错
```

小北试着运行了这段代码，结果看到一行 `None`。他以为是自己写错了，反复检查了三遍。

"这什么意思？为什么是 None？"小北一脸困惑，"我明明看到它打印出了正确的换算结果啊！"

阿码在旁边举手："那怎么办？我想让函数返回一个值，然后我可以用这个值做别的事情。比如我想算出'公里转英里，再乘以 2'——用 print 版本的函数做不到。"

好问题——这就是**返回值**（return value）的作用。

```python
# 用 return 返回结果
def km_to_miles(km):
    miles = km * 0.621371
    return miles  # 返回计算结果

# 现在可以把结果存进变量
result = km_to_miles(10)
print(result)  # 6.21371

# 可以用结果做运算
double_result = result * 2
print(double_result)  # 12.42742

# 可以传给另一个函数
print(f"10 公里是 {km_to_miles(10)} 英里")
```

`return` 的作用是"把结果交出去"。函数执行到 `return` 就结束了，后面的代码不会再运行。

```python
def km_to_miles(km):
    miles = km * 0.621371
    return miles
    print("这行永远不会执行")  # 死代码

result = km_to_miles(10)
```

阿码追问："那 `return` 和 `print` 到底有什么区别？不就是都能输出吗？"

这是个好问题，很多新手都会混淆。

- `print` 是"给人看"——把信息输出到屏幕，但程序拿不到这个值
- `return` 是"给程序用"——把值返回给调用者，可以在代码里继续用

```python
# print 版本——只能看，不能复用
def add_with_print(a, b):
    print(a + b)

add_with_print(3, 5)  # 屏幕显示 8
# result = add_with_print(3, 5) * 2  # 会报错！因为返回的是 None

# return 版本——可以复用
def add_with_return(a, b):
    return a + b

result = add_with_return(3, 5) * 2  # result = 16
print(result)  # 16
```

一个常见的错误是忘记写 `return`：

```python
def km_to_miles(km):
    miles = km * 0.621371
    # 忘记写 return！

result = km_to_miles(10)
print(result)  # None！
```

如果你忘了写 `return`，Python 会默认返回 `None`（一个特殊的值，表示"什么都没有"）。

---

## 4. 把大问题拆小——函数分解与作用域

现在我们的换算器还很简单，只有一个换算函数。但如果它要支持 10 种换算、有菜单选择、有输入验证呢？

一个 100 行的函数是维护噩梦。老潘的建议是："函数超过 20 行就考虑拆分，一个函数只做一件事。"

让我们来看看怎么把一个"大函数"拆成多个"小函数"。

```python
# 之前：所有逻辑混在一起
def converter():
    print("单位换算器")
    print("1. 公里 → 英里")
    print("2. 公斤 → 磅")
    # ... 省略 50 行代码

# 之后：拆成多个小函数
def show_menu():
    """显示菜单"""
    print("单位换算器")
    print("1. 公里 → 英里")
    print("2. 公斤 → 磅")
    print("3. 摄氏度 → 华氏度")
    print("4. 退出")

def get_choice():
    """获取用户选择"""
    return input("请选择（1-4）：")

def km_to_miles(km):
    """公里转英里"""
    return km * 0.621371

def kg_to_pounds(kg):
    """公斤转磅"""
    return kg * 2.20462

def celsius_to_fahrenheit(c):
    """摄氏度转华氏度"""
    return c * 9/5 + 32
```

每个函数只做一件事，名字就能说明它在干什么。这样代码更容易理解、更容易测试、更容易复用。

但在拆分函数时，你会遇到一个新问题：**变量在哪里能用？**

这就是**作用域**（scope）的概念——而且它经常会给人"反直觉"的体验。

```python
x = 10  # 全局变量——函数外面也能访问

def my_function():
    y = 20  # 局部变量——只能在函数里面用
    print(x)  # 可以！函数里可以读取全局变量
    print(y)  # 可以！

print(x)  # 可以
print(y)  # 报错！NameError: name 'y' is not defined
```

小北试了一下这段代码，果然在 `print(y)` 那里报错了。

"为什么函数里的变量外面访问不到？"小北一脸困惑，"我明明定义了啊！"

**局部变量**（local variable）就像你手机里的私人通讯录——只有你拿着手机才能看，别人看不见。函数执行的时候，Python 会为它开辟一个"私密空间"，函数里的变量就住在这里。函数结束了，空间清空，里面的东西也就没了。

**全局变量**（global variable）呢？就像公共广场上的广告牌——哪里都能看到。

**哦！意外时刻**：小北一直以为"定义了就能用"，但作用域告诉他——"在哪里定义"比"有没有定义"更重要。函数里的变量就像借来的东西，函数执行完就得还回去，外面根本拿不到。

但老潘有个警告："在公司里，我们几乎不用全局变量。为什么？因为它会让代码的行为变得难以预测。你调用一个函数，结果它偷偷改了走廊里的东西，十分钟后你自己都不知道谁改的。"

小北不信邪："真的有那么夸张吗？"

```python
# 全局变量
message = "你好"

def greet():
    # 函数里可以读取全局变量
    print(message)

greet()  # 输出：你好

# 但不要在函数里修改全局变量——这会让人困惑
def change_message():
    global message  # 必须加 global 才能修改
    message = "你好啊"

change_message()
print(message)  # 输出：你好啊
```

小北试了一下，发现 `message` 真的被改了。

"等等，"小北突然反应过来，"那如果我有十个函数都在改 `message`，最后它变成什么鬼样子我都不知道？"

"对！"老潘拍桌子，"所以我当年接手那个 500 行函数的项目时，光是理清'谁在什么时候改了哪个全局变量'就花了我一周。这就是为什么我们说——**函数通过参数获取输入，通过返回值输出结果**。不要依赖全局变量，也不要偷偷修改全局变量。"

现在让我们把所有东西组合起来，写一个模块化的单位换算器。

先看三个核心的换算函数——它们都很短，只做一件事：

```python
def km_to_miles(km):
    """公里转英里"""
    return km * 0.621371

def kg_to_pounds(kg):
    """公斤转磅"""
    return kg * 2.20462

def celsius_to_fahrenheit(c):
    """摄氏度转华氏度"""
    return c * 9/5 + 32
```

小北看完这段代码，皱起眉头："等等，就这？每行函数只有一行代码？这也要写成函数？"

"对，"阿码在旁边说，"等你以后要写测试的时候就知道有多爽了——每个函数都可以单独测试，而且函数名直接告诉你它干什么。"

然后是处理菜单和用户输入的函数——注意 `get_choice()` 里用了上周学的 `while` 循环：

```python
def show_menu():
    """显示菜单"""
    print("\n=== 单位换算器 ===")
    print("1. 公里 → 英里")
    print("2. 公斤 → 磅")
    print("3. 摄氏度 → 华氏度")
    print("4. 退出")

def get_choice():
    """获取用户选择，带输入验证"""
    while True:
        choice = input("请选择（1-4）：")
        if choice in ["1", "2", "3", "4"]:
            return choice
        print("无效输入，请输入 1-4")
```

最后是主函数——它把所有东西串联起来：

```python
def do_conversion(choice):
    """执行换算"""
    if choice == "1":
        km = float(input("输入公里数："))
        result = km_to_miles(km)
        print(f"{km} 公里 = {result:.2f} 英里")
    elif choice == "2":
        kg = float(input("输入公斤数："))
        result = kg_to_pounds(kg)
        print(f"{kg} 公斤 = {result:.2f} 磅")
    elif choice == "3":
        c = float(input("输入摄氏度："))
        result = celsius_to_fahrenheit(c)
        print(f"{c}°C = {result:.2f}°F")

def main():
    """主函数"""
    while True:
        show_menu()
        choice = get_choice()

        if choice == "4":
            print("再见！")
            break

        do_conversion(choice)

# 启动程序
main()
```

这个程序把上周学的 `while` 循环和这周学的函数结合起来了。`main()` 函数是入口，它调用其他函数来完成任务。每个函数都很短，名字清晰，职责单一。

老潘看到这段代码，点点头："这就对了。以后如果我想加一个新的换算类型，只需要：
1. 写一个新的换算函数（如 `miles_to_km`）
2. 在 `show_menu()` 里加一个选项
3. 在 `do_conversion()` 里加一个 `elif` 分支

改动是局部的，不会影响其他部分。这就是模块化的价值。"

---

> **AI 时代小专栏：函数是编程的"积木"**

> 你刚学的函数定义，本质上是在"构建积木"。有意思的是，2026 年最先进的 AI 系统——从大语言模型到自动驾驶——内部也是由无数个函数组成的。
>
> 软件工程领域有一个核心原则叫**模块化设计**（modular design），它的核心思想是：把复杂系统拆成独立的、可复用的模块，每个模块只做一件事。这正是你写 `km_to_miles()`、`show_menu()` 时在做的事情。
>
> 研究表明，高质量的软件系统通常有这些特征：**高内聚**（一个函数内的代码紧密相关）、**低耦合**（函数之间的依赖关系尽量少）。简单说就是：每个函数只做一件事，函数之间不要互相缠绕。
>
> 2026 年的架构趋势也在印证这一点：42% 的组织正在从过度复杂的微服务回归"模块化单体"，因为**真正的模块化不在服务边界，而在代码内部**。一个写得很烂的微服务，不如一个结构清晰的单体。就连 Amazon Prime Video 团队也通过从微服务回归单体，将成本降低了 90%——这背后体现的就是"过度拆分的代价"。
>
> 你今天学的函数分解思维——把大问题拆成小函数、给函数起清晰的名字、用参数传递输入、用返回值输出结果——就是所有软件系统设计的基础。AI 可以帮你写代码，但"如何拆分问题"还得你自己来。
>
> 参考（访问日期：2026-02-08）：
> - [Monolith vs. Microservices: Which Architecture Wins in 2026?](https://itidoltechnologies.com/blog/monolith-vs-microservices-which-architecture-wins-in-2026/)
> - [Monolith vs. Modular Monolith vs. Microservices: How to Choose the Right Architecture](https://vitex.asia/monolith-vs-modular-monolith-vs-microservices-how-to-choose-the-right-architecture/)
> - [Understanding Modern Software Architecture: From Microservices Consolidation to Modular Monoliths](https://www.softwareseni.com/understanding-modern-software-architecture-from-microservices-consolidation-to-modular-monoliths)
> - [Mastering Modular Programming: How to Take Your Python Skills to the Next Level](https://medium.com/data-science/mastering-modular-programming-how-to-take-your-python-skills-to-the-next-level-ba14339e8429)

---

> **AI 时代小专栏：AI 写的函数有什么特点**

> 你刚学会了 `return` 和 `print` 的区别——一个重要但容易混淆的概念。有意思的是，2026 年的很多研究都发现：**AI 生成的代码经常犯这个错误**。
>
> 研究显示，GitHub Copilot 已经在编写用户代码的 **46%**（在 Java 项目中甚至达到 **61%**），开发者使用 Copilot 后**完成任务快了 55%**。但另一项研究发现，AI 生成的代码中**只有约 30% 被开发者接受**——剩下的 70% 要么有 bug，要么不够好。
>
> 为什么？一个重要原因是：AI 模型是从海量代码中训练的，而网络上的示例代码为了"直观"，经常直接 `print` 结果。这导致 AI 也养成了这个习惯。但真正工程化的代码需要**可复用性**——函数应该返回结果，让调用者决定是打印、存文件还是做进一步计算。
>
> 还有一个问题：AI 生成的函数经常**过长、职责不清**。一个 50 行的函数可能混了输入验证、数据转换、结果输出三件事。老潘的"20 行原则"和"一个函数只做一件事"——这些工程经验，AI 还没完全学会。
>
> 所以你刚学的函数设计原则——**短函数、单一职责、用参数传递、用返回值输出**——不仅能让你写出更好的代码，还能帮你审查和改进 AI 生成的东西。在 AI 时代，"理解为什么这样写"比"自己写出来"更重要。
>
> 参考（访问日期：2026-02-08）：
> - [GitHub Copilot Statistics 2026](https://www.getpanto.ai/blog/github-copilot-statistics)
> - [AI Coding Assistants in 2026: GitHub Copilot, ChatGPT, Developer Productivity & Python](https://www.programming-helper.com/tech/ai-coding-assistants-2026-github-copilot-chatgpt-developer-productivity-python)
> - [Assessing the Quality of GitHub Copilot's Code Generation](https://dl.acm.org/doi/10.1145/3558489.3559072)
> - [AI Generated Code Statistics](https://www.netcorpsoftwaredevelopment.com/blog/ai-generated-code-statistics)

---

## PyHelper 进度

上周 PyHelper 已经能根据心情给出建议了，但如果你回头看代码——所有东西都挤在一起。`if/elif/else` 判断、`print` 输出、`input` 输入全都混在一块，像个没整理的房间。

这周我们用函数把它"重新装修"一下。

**重构**（refactoring）的意思是**改善代码结构，但不改变它的功能**。就像你把房间里的东西重新摆放，更好用、更整洁——但东西还是那些东西。

```python
# PyHelper - 你的命令行学习助手
# Week 03：函数重构 + 菜单

def print_welcome():
    """打印欢迎信息"""
    print("=" * 40)
    print("  欢迎使用 PyHelper！")
    print("=" * 40)
    print()

def print_menu():
    """打印菜单"""
    print("请选择功能：")
    print("1. 获取学习建议")
    print("2. 查看今日名言")
    print("3. 退出")

def get_choice():
    """获取用户选择，带输入验证"""
    while True:
        choice = input("\n请输入选择（1-3）：")
        if choice in ["1", "2", "3"]:
            return choice
        print("无效输入，请输入 1-3")

def get_mood():
    """获取用户心情"""
    print("\n今天心情怎么样？")
    print("1. 充满干劲")
    print("2. 一般般")
    print("3. 有点累")
    mood = input("请输入你的心情（1-3）：")
    return mood

def get_advice(mood):
    """根据心情返回建议（注意：返回而非打印）"""
    if mood == "1":
        return "太好了！推荐你今天挑战一个新概念，比如开始学习函数或者列表。"
    elif mood == "2":
        return "那就做点巩固练习吧，复习上周的变量和字符串，写几个小例子。"
    elif mood == "3":
        return "累了就休息一下吧，今天可以只看视频不动手，或者写 10 分钟代码就停。"
    else:
        return "写点巩固练习最稳妥。"

def get_quote():
    """返回今日名言"""
    return "学编程是马拉松，不是百米冲刺。找到自己的节奏最重要。"

def show_advice():
    """功能1：显示学习建议"""
    mood = get_mood()
    advice = get_advice(mood)
    print(f"\n{advice}")
    print(get_quote())

def show_quote():
    """功能2：显示名言"""
    print(f"\n今日一句：{get_quote()}")

def main():
    """主函数"""
    print_welcome()

    while True:
        print_menu()
        choice = get_choice()

        if choice == "1":
            show_advice()
        elif choice == "2":
            show_quote()
        elif choice == "3":
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
1. 获取学习建议
2. 查看今日名言
3. 退出

请输入选择（1-3）：1

今天心情怎么样？
1. 充满干劲
2. 一般般
3. 有点累
请输入你的心情（1-3）：2

那就做点巩固练习吧，复习上周的变量和字符串，写几个小例子。
学编程是马拉松，不是百米冲刺。找到自己的节奏最重要。

----------------------------------------

请选择功能：
1. 获取学习建议
2. 查看今日名言
3. 退出

请输入选择（1-3）：3

再见！祝你学习愉快！
```

对比上周的代码，你会发现几个变化：

1. **功能被拆成小函数**：`print_welcome()`、`get_mood()`、`get_advice()` 各司其职
2. **函数有返回值**：`get_advice()` 返回建议字符串，而不是直接打印
3. **有菜单循环**：用 `while True` 让用户可以持续使用不同的功能
4. **输入验证**：`get_choice()` 会检查输入是否有效，无效就让你重输

老潘看到这段代码，点点头："现在每个函数只做一件事。如果以后想加'功能4：查看学习记录'，只需要：
1. 写一个 `show_records()` 函数
2. 在 `print_menu()` 里加一个选项
3. 在 `main()` 的 `if/elif` 里加一个分支

改动是局部的，不会影响其他功能。我当年写过一个 500 行的函数，改一个 bug 要从头读到尾——那种痛苦，你以后就懂了。"

小北在旁边："所以函数拆小不只是好看，主要是为了以后好改？"

"对，"老潘说，"代码写一次，会被改十次。好代码是写给未来的自己（和同事）看的。"

---

## Git 本周要点

本周必会命令：
- `git switch -c feature-name` 或 `git checkout -b feature-name` —— 创建并切换到新分支
- `git branch` —— 查看所有分支
- `git switch main` 或 `git checkout main` —— 切换回主分支
- `git merge feature-name` —— 合并分支

常见坑：
- 函数定义的常见错误：忘记冒号（`def foo():` 不是 `def foo()`）、缩进错误（函数体要缩进 4 个空格）
- 调用函数的常见错误：忘记加括号（`foo` 不是 `foo()`）、参数数量不匹配
- 作用域相关困惑：在函数外面访问函数里的局部变量会报 `NameError`

分支工作流（入门）：
- 创建分支开发新功能（如 `git switch -c add-temp-converter`）
- 在分支上提交代码（`git add -A && git commit -m "feat: add temperature conversion"`）
- 切回主分支并合并（`git switch main && git merge add-temp-converter`）
- 合并后可以删除分支（`git branch -d add-temp-converter`）

Pull Request (PR)：
- Week 03 暂不要求 PR，但建议练习分支工作流——把"菜单功能"和"换算功能"分别在不同分支开发，然后合并

---

## 本周小结（供下周参考）

这一周，你学会了把代码"打包"成函数——用 `def` 定义函数，用参数传递输入，用 `return` 返回结果。更重要的是，你理解了作用域的概念（变量"在哪里能用"），以及函数分解的思维方式（把大问题拆成小任务）。

下周，我们将学习"列表和字典"——这是 Python 里"装东西的容器"。你会发现，函数和容器是编程的两个核心抽象：一个包装"行为"，一个包装"数据"。

---

## Definition of Done（学生自测清单）

完成本周学习后，请确认你能：

- [ ] 使用 `def` 语句定义函数，正确书写函数名、参数列表、冒号和缩进
- [ ] 理解参数的作用，能定义带参数的函数（如 `km_to_miles(km)`）
- [ ] 理解返回值的作用，能使用 `return` 返回计算结果
- [ ] 理解 `return` 和 `print` 的区别（返回值 vs 输出）
- [ ] 理解作用域的基本概念（局部变量 vs 全局变量）
- [ ] 能把一个大问题分解为多个小函数，设计清晰的函数调用关系
- [ ] 完成单位换算器项目（支持长度、重量、温度等多种换算，有菜单选择）
- [ ] Git 至少提交 2 次（draft + verify），尝试使用分支工作流
- [ ] 运行 `python3 -m pytest chapters/week_03/tests -q` 并通过所有测试

<!--
章节结构骨架（供 chapter-writer 参考）：

1. 章首导入（引言格言 + 时代脉搏）——已完成
2. 前情提要——已完成
3. 学习目标——已完成
4. 贯穿案例设计说明（HTML 注释）——已完成
5. 认知负荷 + 回顾桥 + 角色出场规划（HTML 注释）——已完成
6. AI 小专栏规划（HTML 注释）——已完成
7. 第 1 节：50 行代码的噩梦——为什么你需要函数——已完成
8. 第 2 节：把代码打包——定义你的第一个函数——已完成
9. 第 3 节：让函数变得更灵活——参数与返回值——已完成
10. 第 4 节：把大问题拆小——函数分解与作用域——已完成
11. PyHelper 进度——已完成
12. Git 本周要点——已完成
13. 本周小结（供下周参考）——已完成
14. Definition of Done——已完成
-->
