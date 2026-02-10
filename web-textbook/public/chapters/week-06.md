# Week 06：让程序不崩——异常处理与防御性编程

> "Hope for the best, prepare for the worst."
> — 俗语

你有没有经历过这种时刻：精心准备了一个 PPT,演示的时候电脑突然蓝屏；玩游戏打到关键时刻,程序直接闪退；转账填了一堆信息,点击"确认"后网页崩溃——钱扣了,账没转过去。

这些崩溃背后的罪魁祸首,往往是一个叫"未处理异常"的小东西。

2024 年 7 月 19 日凌晨 4 点,安全公司 CrowdStrike 推送了一次软件更新。几分钟后,全球 **850 万台** Windows 设备蓝屏崩溃——航空停飞、银行中断、医院系统瘫痪。这被认为是史上最大规模的 IT 中断之一,全球经济损失超过 **100 亿美元**。

原因不是黑客攻击,而是一个**未处理的异常**——代码读取了一个空指针,程序直接崩溃。

这件事给所有程序员上了一课：**"能跑"和"靠谱"之间,隔着异常处理这道鸿沟**。在 AI 时代,这个问题更明显了——2025 年的研究显示,AI 生成的代码引入的 bug 数量是人工代码的 **1.7 倍**,其中最常见的缺陷之一就是"缺少错误处理"。

这周你将学会让程序"不崩"。不是祈祷"用户别乱输",而是主动防御——用 `try/except` 捕获错误、用 `if` 预判异常、设计友好的错误消息。

---

## 前情提要

上周你学会了让程序"记住"东西——用文件存储数据,下次打开还能恢复。小北的 PyHelper 现在能保存学习记录了,他很高兴,立刻开始用起来。

但三天后,他遇到了一个问题：那天他心情不好,在菜单选择时手滑输入了"abc"而不是数字。

```python
请输入选择（1-5）：abc
Traceback (most recent call last):
  File "pyhelper.py", line 48, in <module>
    choice = int(input("请输入选择（1-5）："))
ValueError: invalid literal for int() with base 10: 'abc'
```

"怎么回事！？"小北盯着红色的错误信息,"我的程序炸了？"

老潘在旁边解释："这是**异常**（exception）——程序遇到了它无法处理的情况,直接崩溃了。你上周学的文件操作也会遇到类似问题：文件不存在、没有权限、编码错误……如果不管这些,程序会在最尴尬的时候崩溃。"

"那怎么办？"小北问。

"学会**防御性编程**（defensive programming）,"老潘说,"不是祈祷'用户别乱输',而是假设'用户一定会乱输',然后让程序优雅地处理这种情况。"

这周我们来解决这个问题。你将学会 `try/except` 结构,学会捕获特定异常（比如 `ValueError`、`FileNotFoundError`）,学会设计友好的错误消息。更重要的是,你会理解 Python 的哲学——**EAFP**（Easier to Ask Forgiveness than Permission）,以及它与 **LBYL**（Look Before You Leap）的区别。

---

## 学习目标

完成本周学习后,你将能够：
1. 理解异常的概念,能读懂 Traceback 报错信息
2. 掌握 `try/except` 结构的基本语法和用法
3. 识别常见异常类型（`ValueError`、`TypeError`、`KeyError`、`FileNotFoundError`）并选择正确的捕获方式
4. 理解 `else` 和 `finally` 子句的作用和使用场景
5. 能用 `raise` 抛出异常,设计自定义错误消息
6. 理解 LBYL vs EAFP 两种编程哲学,知道什么时候用哪种
7. 能设计"输入校验"函数,防止程序因坏输入崩溃

---

<!--
=======================================
贯穿案例：健壮的用户输入处理器
=======================================

演进路线：
- 第 1 节（从崩溃到捕获）：用一个"会崩溃"的除法器开始,遇到除零、非数字输入就炸；引出 try/except 结构,让程序能"捕获"错误
- 第 2 节（捕获特定异常）：从 `except:` 到 `except ValueError:`,理解"捕获所有异常"是坏习惯；学会处理 ValueError（非数字）、TypeError（类型错误）、ZeroDivisionError（除零）
- 第 3 节（else 和 finally）：理解 else（没出错时执行）和 finally（无论是否出错都执行）；用一个"打开配置文件"的例子展示 finally 的价值（确保资源释放）
- 第 4 节（输入校验与 LBYL）：用 `if` 预判异常（检查输入是否合法）,比较 LBYL（先检查）和 EAFP（先尝试）两种风格；设计一个"健壮的输入获取函数"
- 第 5 节（raise 与自定义错误）：学会用 `raise` 抛出异常,设计友好的错误消息；把输入校验封装成可复用的函数

最终成果：一个"健壮的用户输入处理器"——能获取并验证各种类型的输入（整数、浮点数、选项）,遇到坏输入不会崩溃,而是给出友好的错误提示并让用户重试
-->

<!--
=======================================
认知负荷预算
=======================================

本周新概念（5 个,预算上限 5 个）：
1. 异常处理（try/except）—— 基本语法、捕获异常
2. 异常类型（exception types）—— ValueError/TypeError/KeyError/FileNotFoundError/ZeroDivisionError
3. else 和 finally 子句—— 什么时候用、如何配合
4. 输入校验（input validation）—— 用 if 预判异常
5. LBYL vs EAFP —— 两种编程哲学的比较

结论：✅ 在预算内

回顾桥设计（至少引用 Week 03-05 的 2 个概念,实际规划 6 个）：
- [if/else 条件判断]（来自 week_02）：在第 4 节,用 if 预判异常（LBYL 风格）
- [while 循环]（来自 week_02）：在第 4-5 节,用 while 循环让用户"重试直到输入正确"
- [函数]（来自 week_03）：在第 5 节,把输入校验逻辑封装成函数
- [字典]（来自 week_04）：第 1 节用访问不存在的键引出 KeyError
- [文件操作]（来自 week_05）：第 1 节用读取不存在的文件引出 FileNotFoundError
- [with 语句]（来自 week_05）：第 3 节用 with + finally 展示资源释放的重要性
-->

<!--
=======================================
循环角色出场规划
=======================================

- 小北（第 1 节）：写了一个除法器,用户输入"abc"后程序崩溃；引出"为什么程序这么脆弱"的问题
- 老潘（第 1 节）：看到小北用 `except:` 捕获所有异常,摇头说"在公司里我们从来不会这样写,因为会掩盖真正的错误"
- 阿码（第 2 节）：追问"如果我一次捕获多个异常,比如 `except (ValueError, TypeError):`,这样行不行？",引出"捕获特定异常"的讨论
- 小北（第 3 节）：不理解 finally 有什么用（"有 with 不就行了吗？"）,老潘用一个"文件读取+日志记录"的例子说明 finally 的价值
- 阿码（第 4 节）：争论"到底应该先检查（LBYL）还是先尝试（EAFP）",老潘用两种风格的代码对比说明各自适用场景
- 老潘（第 5 节）：看到小北写了一个"万能输入函数",说"这个函数能复用了,工程上就是把常用逻辑封装起来"
-->

<!--
=======================================
AI 小专栏规划
=======================================

AI 小专栏 #1（放在第 2 节之后）：
- 主题：AI 生成的代码为什么经常"缺少错误处理"
- 连接点：你刚学的"捕获特定异常",AI 经常用 `except:` 捕获所有异常（掩盖问题）或完全不捕获（直接崩溃）
- 建议搜索词：GitHub Copilot error handling statistics 2026, AI generated code bugs 2025, AI code quality issues exception handling
- 搜索提示：搜索 2025-2026 年关于 AI 生成代码质量的研究、统计数据,特别关注"错误处理"相关的问题

AI 小专栏 #2（放在第 4 节之后）：
- 主题：为什么 Python 社区偏爱 EAFP（先尝试再道歉）
- 连接点：你刚学的 LBYL vs EAFP,Python 的设计哲学是 EAFP——这和 AI 编程工具的生成方式有什么关系？
- 建议搜索词：Python EAFP philosophy 2026, LBYL vs EAFP Python best practices, exception handling Python style guide
- 搜索提示：搜索 Python 官方文档、PEP 8、社区讨论中关于 EAFP 的说明和案例

注意：两个侧栏必须基于真实数据和 URL,使用 WebSearch 或 perplexity MCP 查证。禁止编造统计数据和链接。
-->

## 1. 程序为什么崩溃

小北这周想做个简单的除法器,测试的时候一切正常——10 除以 2,得 5；100 除以 4,得 25。他觉得自己简直是个天才程序员。

直到他手滑在分母输入了 `0`。

```
请输入分子：10
请输入分母：0
Traceback (most recent call last):
  File "calculator.py", line 3, in <module>
    result = numerator / denominator
ZeroDivisionError: division by zero
```

程序直接崩了,红色报错刷满屏幕,像一盆冷水浇在小北头上。

"怎么回事！？"小北盯着屏幕,"我的程序炸了？我明明测试了好多遍都好好的啊！"

老潘在旁边瞥了一眼,笑了："哦,这是**异常**（exception）。Python 遇到了它处理不了的情况——除以零在数学上没意义——所以它就'炸'了。"

"但这……这也太脆弱了吧？"小北崩溃道,"我就输错一个数字,程序就给我看这个？"

老潘点点头："**异常**不是 bug,而是程序在说：'这里有问题,我处理不了,你来决定怎么办。'"

Python 会用一个"诊断报告"（Traceback）告诉你三件事：
- 出错在哪一行（`line 3`）
- 错误的类型（`ZeroDivisionError`）
- 错误的原因（`division by zero`）

小北盯着报错信息看了半天,嘟囔着："好吧,ZeroDivisionError……除以零错误。那如果我不小心输入了字母呢？"

他又试了一次,这次在分子输入了 `"abc"`：

```
请输入分子：abc
Traceback (most recent call last):
  File "calculator.py", line 1, in <module>
    numerator = int(input("请输入分子："))
ValueError: invalid literal for int() with base 10: 'abc'
```

又崩了。这次是 `ValueError`。

"哦！原来不同的错误会有不同的名字,"小北若有所思,"ZeroDivisionError、ValueError……这些名字其实挺形象的,一看就知道发生了什么。"

"对,"老潘说,"Python 的异常名字都很直观——看到名字你就知道发生了什么。但问题是怎么让程序'不崩'。"

"对啊！"小北眼睛一亮,"要是程序能像人一样,发现我输错了就提醒我'嘿,你输错了',而不是直接崩溃,该多好。"

"这就是这周要学的——**异常处理**（exception handling）,"老潘说,"不是祈祷'用户别乱输',而是假设'用户一定会乱输',然后让程序优雅地处理。"

**建议示例文件**：`01_crashing_calculator.py`

---

## 2. 捕获异常——try/except 结构

小北的除法器一遇到坏输入就崩溃。怎么让它"不崩"？Python 提供了一个结构来"捕获"这些异常：**`try/except`**。

基本思想很简单：**尝试执行代码，如果出错了，执行另一段代码而不是崩溃**。

```python
try:
    # 尝试执行的代码（可能抛出异常）
    numerator = int(input("请输入分子："))
    denominator = int(input("请输入分母："))
    result = numerator / denominator
    print(f"结果：{result}")
except:
    # 如果出错了,执行这段代码
    print("出错了！请检查你的输入。")
```

现在无论用户输入什么,程序都不会崩溃：

```
请输入分子：10
请输入分母：0
出错了！请检查你的输入。
```

小北很高兴："这样就行了！无论用户输入什么,程序都不会崩,太完美了！"

老潘摇摇头："**不完美**。你用了裸的 `except:`——这会捕获所有异常,包括你没预料到的 bug。"

"什么意思？"小北不解,"捕获所有异常不是好事吗？程序不就永远不会崩了吗？"

老潘叹了口气："想象一下,你写了一个程序,里面有个 bug——变量名拼错了,或者逻辑写错了。如果你用裸的 `except:`,程序会'吞掉'这个错误,继续执行——但结果是错的。"

"哦！"小北脸色一变,"那我不是永远发现不了这个 bug？"

"对,"老潘说,"更可怕的是,如果你用裸的 `except:`,它甚至会捕获 `KeyboardInterrupt`——也就是用户按 Ctrl+C 想要退出程序。"

"等等,"阿码举手,"你是说,如果用户按 Ctrl+C,程序不会退出？"

"对,"老潘点点头,"裸的 `except:` 会捕获 `KeyboardInterrupt`,然后打印'出错了！',继续执行——用户想停都停不了。"

小北倒吸一口冷气："这太糟糕了！那我赶紧把裸的 `except:` 改掉……"

**建议示例文件**：`02_catch_all_exceptions.py`

---

```python
try:
    numerator = int(input("请输入分子："))
    denominator = int(input("请输入分母："))
    result = numerator / denominator
    print(f"结果：{result}")
except:
    print("出错了！")

print("程序继续运行...")
```

如果用户输入了 `0`,程序会输出"出错了！"——但你不知道**为什么**。是除以零？还是输入了非数字？裸的 `except:` 把所有信息都吞掉了。

阿码问："那我应该怎么办？"

"捕获**特定异常**,"老潘说,"这样你才知道到底出了什么问题。"

小北在旁边小声嘀咕："终于不是'你看报错信息'了……上次老潘让我看 Traceback,我看了十分钟才找到问题在哪。"

老潘笑了笑："现在你学会捕获异常,就不用盯着一堆红色报愁眉苦脸了。"

---

### 捕获特定异常——像侦探一样找线索

你刚才用的裸 `except:` 就像是"地毯式搜索"——把所有异常都抓起来,但你不知道抓到的是什么。

Python 有很多内置异常类型,每个都像一条"线索"：

| 异常类型 | 何时抛出 | 像什么 |
|---------|---------|------|
| `ValueError` | 值不合法 | 你点了一份不存在的菜 |
| `TypeError` | 类型不匹配 | 你试图用钥匙开密码锁 |
| `ZeroDivisionError` | 除以零 | 你试图把蛋糕分给 0 个人 |
| `KeyError` | 字典键不存在 | 你查字典找一个不存在的字 |
| `IndexError` | 索引越界 | 你翻书翻到了第 1000 页,但书只有 200 页 |
| `FileNotFoundError` | 文件不存在 | 你打开一个已经被删除的文件 |

阿码眼睛一亮："这些异常名字……不就是线索吗？"

"对！"老潘说,"不同的异常就像不同的线索,你可以根据线索'对症下药'。"

你可以指定捕获哪种异常：

```python
try:
    numerator = int(input("请输入分子："))
    denominator = int(input("请输入分母："))
    result = numerator / denominator
    print(f"结果：{result}")
except ValueError:
    print("错误：请输入数字,不要输入文字")
except ZeroDivisionError:
    print("错误：分母不能为零")
```

现在程序会根据不同的"线索"给出不同的提示：

```
请输入分子：abc
错误：请输入数字,不要输入文字
```

```
请输入分子：10
请输入分母：0
错误：分母不能为零
```

小北松了一口气："这样用户就知道自己错在哪了,而不是看到一堆红色的报错信息一脸茫然。"

**建议示例文件**：`03_specific_exceptions.py`

---

阿码问："如果我一次捕获多个异常,比如 `except (ValueError, TypeError):`,这样行不行？"

"可以,"老潘说,"但你要确定这两种异常的处理方式是一样的。"

```python
try:
    numerator = int(input("请输入分子："))
    denominator = int(input("请输入分母："))
    result = numerator / denominator
    print(f"结果：{result}")
except (ValueError, TypeError):
    print("错误：输入不合法,请检查")
except ZeroDivisionError:
    print("错误：分母不能为零")
```

小北突然插嘴："等等,`TypeError` 是什么？什么时候会抛出 `TypeError`？"

阿码得意地说："我知道！`TypeError` 是类型不匹配的错误。比如 `'2' + 3`——字符串不能直接加数字,就会抛出 `TypeError`。"

"哦！"小北恍然大悟,"那在这个除法器里,什么时候会抛出 `TypeError`？"

阿码想了想,挠挠头："呃……好像不会？`int()` 会先把输入转成整数,如果转不成功就抛出 `ValueError` 了,轮不到 `TypeError` 出场。"

老潘笑了："观察得很仔细！阿码说得对,在这个除法器里,`TypeError` 确实不太可能被抛出。但如果你想写一个'通用'的计算器,可能接受不同类型的输入（整数、浮点数、分数）,那 `TypeError` 就有可能出现了。"

小北松了一口气："还好这个除法器只处理整数,不然我得捕获十几种异常……"

"哈哈,"老潘笑了,"记住,不要捕获你'预期不到'的异常。你只捕获你能处理的,其他的让它崩——这样你才能发现真正的 bug。"

**建议示例文件**：`04_multiple_exceptions.py`

---

小北问："那如果我真的想捕获所有异常呢？"

"那就用 `except Exception:`,"老潘说,"不要用裸的 `except:`。"

```python
try:
    # 一些代码
except Exception as e:
    print(f"出错了：{e}")
```

`Exception` 是所有"非致命异常"的基类。`except Exception as e:` 会捕获大多数异常,但不会捕获 `SystemExit`、`KeyboardInterrupt`（用户按 Ctrl+C）这种"程序退出"类的异常。

而且 `as e` 会把异常对象赋值给 `e`,你可以打印出错误信息。

老潘补充道："在公司里,我们几乎不会用 `except:` 或 `except Exception:`——因为它们会掩盖真正的 bug。正确的做法是**捕获你预期的异常**,其他的让程序崩溃,这样你才能发现问题。"

---

现在,让我们用 `try/except` 改进除法器,让它能处理各种坏输入。

```python
def safe_divide():
    """安全的除法器"""
    try:
        numerator = int(input("请输入分子："))
        denominator = int(input("请输入分母："))

        if denominator == 0:
            print("错误：分母不能为零")
            return

        result = numerator / denominator
        print(f"结果：{result}")
        return result

    except ValueError:
        print("错误：请输入数字,不要输入文字")
        return None

# 测试
print("=== 测试 1：正常输入 ===")
safe_divide()

print("\n=== 测试 2：除以零 ===")
safe_divide()

print("\n=== 测试 3：非数字输入 ===")
safe_divide()
```

这里用到了 Week 03 学的**函数**——把除法逻辑封装成函数,用 `return` 提前退出。

**建议示例文件**：`05_safe_divider.py`

---

下一节,我们来学两个"补充条款"——`else` 和 `finally`。它们会让你的异常处理更完整。

---

> **AI 时代小专栏：AI 生成的代码为什么经常"缺少错误处理"**

> 你刚学了"捕获特定异常",知道不能随便用 `except:` 吞掉所有错误。但 AI 代码生成工具（如 GitHub Copilot、ChatGPT）经常犯这个错误——要么完全不捕获异常（程序直接崩溃）,要么用裸的 `except:` 掩盖问题。
>
> 2025 年多项研究发现,AI 生成的代码质量存在显著问题：一份针对 AI 代码的深度分析显示,AI 生成的代码引入的 bug 数量是人工代码的 **1.7 倍**（平均 10.83 个问题 vs 6.45 个问题）。另一项研究则发现,**40-62%** 的 AI 生成代码包含安全漏洞或设计缺陷,其中最常见的包括 SQL 注入和不安全的文件处理。
>
> 为什么？因为 AI 训练时的"样例代码"大多是"快乐路径"（happy path）——即"一切正常时的执行流程"。开发者写教程时,通常不会把所有异常处理都写进去,因为这会让代码变得冗长。AI 学习这些样例后,也就学会了"只写快乐路径"。
>
> 还有一个问题：AI 不理解**业务上下文**。比如"用户输入年龄",AI 不知道是 `-1` 算错误、还是 `200` 算错误、还是 `0.5` 算错误——这些需要人类根据业务逻辑定义,AI 无法自动推断。
>
> 所以,AI 编程时代,**异常处理反而更重要了**。你需要：
> 1. 学会识别 AI 代码中的"缺少错误处理"的地方
> 2. 主动添加输入校验和异常捕获
> 3. 用测试验证各种边界情况
>
> 这就像 AI 能帮你写房子的"主体结构",但"门窗锁、防震、消防"这些安全措施,还得你自己来。
>
> 参考（访问日期：2026-02-09）：
> - [AI-Generated Code Quality Metrics and Statistics for 2026](https://www.secondtalent.com/resources/ai-generated-code-quality-metrics-and-statistics-for-2026/)
> - [Stack Overflow Blog - Bugs and Incidents with AI Coding Agents](https://stackoverflow.blog/2026/01/28/are-bugs-and-incidents-inevitable-with-ai-coding-agents/)
> - [CodeRabbit - AI vs Human Code Generation Report](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report)

---

## 3. else 和 finally——完整的异常处理

到目前为止,你的 `try/except` 只有两个部分：`try`（尝试执行）和 `except`（出错了执行）。但 Python 还提供了两个"补充条款"：**`else`** 和 **`finally`**。

---

### else：成功后才做的事

`else` 会在 `try` 块**没有抛出任何异常**时执行。

```python
try:
    numerator = int(input("请输入分子："))
    denominator = int(input("请输入分母："))
    result = numerator / denominator
except ValueError:
    print("错误：请输入数字")
except ZeroDivisionError:
    print("错误：分母不能为零")
else:
    # 只有没出错时才会执行
    print(f"计算成功！结果：{result}")
```

小北挠挠头："这有什么用？直接把 `print` 放在 `try` 里不就行了吗？"

"好问题,"老潘说,"如果 `print` 本身抛出异常呢？"

```python
try:
    numerator = int(input("请输入分子："))
    denominator = int(input("请输入分母："))
    result = numerator / denominator
    print(f"计算成功！结果：{result}")  # 如果这里出错呢？
except ValueError:
    print("错误：请输入数字")
except ZeroDivisionError:
    print("错误：分母不能为零")
```

"等等,"阿码举手,"`print` 怎么可能出错？它就是打印个文字啊！"

"你说得对,`print` 很少出错,"老潘说,"但如果你在 `else` 里做的事情更复杂呢？比如写入日志、发送通知、更新数据库——这些操作都可能出错。"

"哦！我懂了！"小北突然说,"`else` 的意思是：'只有计算成功了,我才做这些后续操作'。如果计算失败了,我就不会去做这些事。"

"宾果！"老潘竖起大拇指,"而且 `else` 让代码的**意图更清晰**：
- `try`：可能出错的代码
- `except`：出错了怎么处理
- `else`：没出错时做什么
- `finally`：无论是否出错都要做的事（下面会讲）"

**建议示例文件**：`06_else_clause.py`

---

### finally：最后一定会做的事

`finally` 最特殊：**无论是否抛出异常,它都会执行**。

最常见的用途是**资源释放**——比如关闭文件、释放网络连接、清理临时文件。

```python
file = None
try:
    file = open("data.txt", "r", encoding="utf-8")
    content = file.read()
    print(content)
except FileNotFoundError:
    print("文件不存在")
finally:
    # 无论是否出错,都会执行
    if file:
        file.close()
        print("文件已关闭")
```

小北疑惑道："有 `with` 语句了,为什么还需要 `finally`？我记得 Week 05 学过 `with` 会自动关闭文件啊。"

"`with` 适合简单的场景,"老潘说,"但想象一下：你需要'读取文件 + 处理数据 + 记录日志 + 清理临时文件'——这时候 `finally` 就更灵活。"

阿码好奇地问："`finally` 到底会在什么时候执行？如果我 `return` 了,它还会执行吗？"

"这是个好问题！"老潘说,"`finally` 几乎'一定会执行'——无论你是 `return`、`break`、`continue`,还是抛出了新的异常。"

```python
def test_finally():
    try:
        print("try 块执行")
        return "try 的返回值"
    finally:
        print("finally 块执行")

result = test_finally()
print(f"返回值：{result}")
```

输出：
```
try 块执行
finally 块执行
返回值：try 的返回值
```

"哇！"小北惊讶道,"`finally` 在 `return` **之后**执行？"

"对,`finally` 会在函数真正返回之前执行,"老潘说,"这就是为什么它特别适合做'清理工作'——无论函数怎么退出,清理工作一定会做。"

"就像……"小北想了想,"就像你做饭,无论做成功还是做失败了,最后都要洗碗、关火、收拾厨房？"

"完美的类比！"老潘笑了,"`finally` 就是你的'厨房清理员'。"

```python
import tempfile
import os

temp_file = None
try:
    # 创建一个临时文件
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
    temp_file.write("临时数据\n")
    temp_file.close()

    # 做一些处理（可能抛出异常）
    result = do_something_with_file(temp_file.name)
    print(f"处理结果：{result}")

except Exception as e:
    print(f"处理失败：{e}")
finally:
    # 无论处理是否成功,都删除临时文件
    if temp_file and os.path.exists(temp_file.name):
        os.remove(temp_file.name)
        print("临时文件已清理")
```

这里 `finally` 确保临时文件**一定会被删除**,即使 `do_something_with_file()` 抛出了异常。

**建议示例文件**：`07_finally_cleanup.py`

---

阿码问："`finally` 和 `with` 能一起用吗？"

"可以,"老潘说,"但要注意顺序。"

```python
try:
    with open("data.txt", "r", encoding="utf-8") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("文件不存在")
finally:
    print("finally 执行了")
```

运行结果：

```
（如果文件存在）
<文件内容>
finally 执行了

（如果文件不存在）
文件不存在
finally 执行了
```

`with` 会在退出块时自动关闭文件,`finally` 会在这之后执行。

**建议示例文件**：`08_with_and_finally.py`

---

现在,让我们用完整的 `try/except/else/finally` 改进除法器。

```python
def safe_divide():
    """安全的除法器（完整版）"""
    try:
        print("=== 除法计算器 ===")
        numerator = int(input("请输入分子："))
        denominator = int(input("请输入分母："))

        result = numerator / denominator

    except ValueError:
        print("错误：请输入数字,不要输入文字")
        return None

    except ZeroDivisionError:
        print("错误：分母不能为零")
        return None

    else:
        # 只有没出错时才会执行
        print(f"计算成功！结果：{result}")
        return result

    finally:
        # 无论是否出错,都会执行
        print("=== 计算结束 ===\n")

# 测试
safe_divide()  # 正常输入
safe_divide()  # 输入非数字
safe_divide()  # 输入除以零
```

输出：

```
=== 除法计算器 ===
请输入分子：10
请输入分母：2
计算成功！结果：5.0
=== 计算结束 ===
```

```
=== 除法计算器 ===
请输入分子：abc
错误：请输入数字,不要输入文字
=== 计算结束 ===
```

```
=== 除法计算器 ===
请输入分子：10
请输入分母：0
错误：分母不能为零
=== 计算结束 ===
```

你会发现,无论是否出错,`=== 计算结束 ===` 都会打印。

**建议示例文件**：`09_complete_exception_handler.py`

---

下一节,我们来学两种编程哲学：**LBYL**（先检查）和 **EAFP**（先尝试）。你会发现,Python 社区偏爱 EAFP——但这不代表 LBYL 没有用。

---

## 4. LBYL vs EAFP——两种编程哲学

上一节你学到了完整的异常处理结构：`try/except/else/finally`。这套结构很强大，但你有没有想过一个问题——**什么时候应该用 try/except，什么时候应该用 if 检查？**

这个问题其实触及了 Python 的核心哲学。

到目前为止，你一直在用 **EAFP**（Easier to Ask Forgiveness than Permission）风格——"先尝试，再道歉"。

```python
# EAFP：先尝试,失败了再处理
try:
    result = numerator / denominator
except ZeroDivisionError:
    print("分母不能为零")
```

另一种风格是 **LBYL**（Look Before You Leap）——"先看再跳"。

```python
# LBYL：先检查,确保没问题再执行
if denominator != 0:
    result = numerator / denominator
else:
    print("分母不能为零")
```

"等等,"阿码突然举手,"这不就是'先斩后奏'和'三思后行'的区别吗？"

老潘笑了："有点像。EAFP 是'先做再说,出事了再道歉'——像某些人的性格；LBYL 是'先检查确认,再做决定'——像某些人的谨慎。"

"那到底哪种更好？"小北问。

老潘看看阿码,又看看小北："问得好。你俩觉得自己平时的风格,哪种更对？"

阿码立刻说："当然是 EAFP！先尝试再说,有问题再改。写代码就是要快！"

小北则犹豫道："我……我觉得 LBYL 更稳妥吧？先把可能出错的地方都检查一遍,这样就不会崩了。"

"有趣的分歧,"老潘笑笑,"Python 社区偏爱 EAFP,但 LBYL 也有用武之地。关键不是'哪种更好',而是'哪种更适合这个场景'。"

---

### EAFP 什么时候更合适

EAFP 适合**"检查的开销比失败大"**的场景。

比如"访问字典"：

```python
# EAFP（推荐）
scores = {"小北": 85, "阿码": 90}
try:
    print(f"小北的分数：{scores['小北']}")
except KeyError:
    print("找不到这个学生")
```

如果你用 LBYL：

```python
# LBYL（不推荐）
if "小北" in scores:
    print(f"小北的分数：{scores['小北']}")
else:
    print("找不到这个学生")
```

阿码皱起眉头："等等,`"小北" in scores` 不就是检查一下吗？怎么会比 `try` 慢？"

"好问题,"老潘说,"LBYL 需要遍历字典检查'小北'是否存在,然后再**再次遍历**获取值。EAFP 只需要一次操作——直接尝试访问,失败了再处理。"

"哦！"阿码恍然大悟,"就像你要找一个人,LBYL 是'先查他在不在,再去叫他',EAFP 是'直接去叫他,不在就拉倒'。"

"对,EAFP 就像'快速试错'——失败了成本很低,但成功了就省了一步检查。"

**建议示例文件**：`10_eafp_dict.py`

---

另一个例子是"文件操作"：

```python
# EAFP（推荐）
try:
    with open("data.txt", "r", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    print("文件不存在")
```

如果你用 LBYL：

```python
# LBYL（不推荐）
import os

if os.path.exists("data.txt"):
    with open("data.txt", "r", encoding="utf-8") as file:
        content = file.read()
else:
    print("文件不存在")
```

"等等,"阿码举手,"如果我用 LBYL,先检查文件存在,然后……在'检查'和'打开'之间文件被删除了呢？"

"哦！这个问题问得好！"老潘眼睛一亮,"这就是**竞态条件**（race condition）——检查和操作之间有时间差,世界变了。EAFP 不会有这个问题,因为它'只操作一次'。"

---

### LBYL 什么时候更合适

LBYL 适合**"失败的开销比检查大"**或**"失败很频繁"**的场景。

比如"用户输入验证"：

```python
# LBYL（推荐）
age_str = input("请输入你的年龄：")

if age_str.isdigit() and 0 < int(age_str) < 120:
    age = int(age_str)
    print(f"你的年龄：{age}")
else:
    print("输入无效：年龄必须是 1-119 之间的整数")
```

如果你用 EAFP：

```python
# EAFP（不推荐）
try:
    age = int(input("请输入你的年龄："))
    if not (0 < age < 120):
        raise ValueError("年龄超出范围")
    print(f"你的年龄：{age}")
except ValueError:
    print("输入无效：年龄必须是 1-119 之间的整数")
```

"等等,"小北举手,"为什么用户输入要用 LBYL？我试了 EAFP,好像也能跑啊？"

"能跑不代表高效,"老潘说,"用户输入'abc'会抛出异常,而**异常的开销比 if 判断大得多**。"

"多大？"阿码好奇地问。

"想象一下,LBYL 是'先敲门,有人再开门'——成本很低；EAFP 是'直接撞门,撞不开再处理'——每次失败都要'撞'一下,成本高。"

"哦！"小北笑了,"所以用户输入这种场景,用户很可能会输错——比如手滑、不小心、随便乱输——失败频率很高,这时候 LBYL 就更合适。"

"没错,"老潘说,"而字典访问这种场景,大部分时候键都存在,失败频率低,这时候 EAFP 就更高效。"

**建议示例文件**：`12_lbyl_input.py`

---

老潘给了一个简单的规则：

| 场景 | 推荐风格 | 原因 |
|------|---------|------|
| 访问字典/列表 | EAFP | 检查的开销大,失败的开销小 |
| 文件操作 | EAFP | 检查和打开之间可能有竞态条件 |
| 用户输入验证 | LBYL | 失败频繁,异常开销大 |
| 数组/字符串索引 | EAFP | Python 的 IndexError 很轻量 |
| 网络请求 | LBYL | 网络失败的开销很大（超时） |

"记住,"老潘说,"没有绝对的好坏,只有'适不适合'。"

---

现在,让我们用 LBYL + EAFP 混合风格,写一个"健壮的输入获取函数"。

```python
def get_positive_integer(prompt):
    """获取一个正整数（LBYL 风格）"""
    while True:  # 用 Week 02 学的 while 循环
        value_str = input(prompt)

        # 先检查输入是否合法（LBYL）
        if not value_str.isdigit():
            print("错误：请输入一个正整数")
            continue

        value = int(value_str)

        if value <= 0:
            print("错误：请输入大于 0 的整数")
            continue

        return value

def get_dictionary_value(dictionary, key, default=None):
    """获取字典的值（EAFP 风格）"""
    try:
        return dictionary[key]
    except KeyError:
        return default

# 测试
print("=== 测试 get_positive_integer ===")
age = get_positive_integer("请输入你的年龄：")
print(f"你的年龄：{age}")

print("\n=== 测试 get_dictionary_value ===")
scores = {"小北": 85, "阿码": 90}
score = get_dictionary_value(scores, "小北", 0)
print(f"小北的分数：{score}")

missing_score = get_dictionary_value(scores, "老潘", 0)
print(f"老潘的分数：{missing_score}")
```

这里 `get_positive_integer` 用 LBYL（用户输入验证）,`get_dictionary_value` 用 EAFP（字典访问）。不同的场景用不同的风格。

**建议示例文件**：`13_mixed_style.py`

---

下一节,我们来学 **`raise`**——主动抛出异常。这让你不仅能"捕获"异常,还能"创建"异常。

---

> **AI 时代小专栏：为什么 Python 社区偏爱 EAFP**

> 你刚学了 LBYL vs EAFP 两种编程风格。Python 官方文档明确推荐 EAFP（Easier to Ask Forgiveness than Permission）——"先尝试,再道歉"。
>
> 这个哲学出自 Python 之禅（Zen of Python）：**"Errors should never pass silently. Unless explicitly silenced."**（错误不应该被静默忽略,除非你明确这样做）。
>
> EAFP 的好处是：
> 1. **代码更简洁**：不需要在每个操作前写一堆 `if` 检查
> 2. **避免竞态条件**：检查和操作之间不会有时间差
> 3. **异常更明确**：出了错你知道为什么,而不是"静默失败"
>
> 但 AI 代码生成工具（如 GitHub Copilot）更倾向于生成 LBYL 风格的代码——因为 AI 的训练数据中,C++、Java 等语言的代码更多,而这些语言更偏向 LBYL（因为异常开销大）。
>
> 这导致一个问题：AI 生成的 Python 代码经常"不 Pythonic"（不符合 Python 风格）。比如：
>
> ```python
> # AI 生成的代码（LBYL,不推荐）
> if "key" in my_dict:
>     value = my_dict["key"]
>
> # Pythonic 的代码（EAFP,推荐）
> try:
>     value = my_dict["key"]
> except KeyError:
>     value = default_value
> ```
>
> 所以,即使你用 AI 辅助编程,也需要**理解 Python 的设计哲学**——否则 AI 写的代码能跑,但不够优雅。
>
> 参考（访问日期：2026-02-09）：
> - [Real Python: LBYL vs EAFP](https://realpython.com/python-lbyl-vs-eafp/)
> - [Microsoft Python Blog: Idiomatic Python - EAFP versus LBYL](https://devblogs.microsoft.com/python/idiomatic-python-eafp-versus-lbyl/)
> - [Real Python: Exception Handling Best Practices](https://realpython.com/ref/best-practices/exception-handling/)
> - [Stack Overflow: Why is it "easier to ask forgiveness than it is to get permission" in Python](https://stackoverflow.com/questions/32901886/why-is-it-easier-to-ask-forgiveness-than-it-is-to-get-permission-in-python)

---

## 5. raise——主动抛出异常

到目前为止，你一直在"防守"——等待错误发生，然后捕获它们。但有时候，你需要"主动出击"——**自己抛出异常**。

小北发现了一个问题："如果我在函数里发现输入不对，我想告诉调用者'这里有问题'，但仅仅打印一个错误信息不够……"

"对，"老潘说，"这时候你需要 `raise`——主动抛出异常，让调用者知道'这里出了问题，你来处理'。"

---

### 什么时候需要 raise？

你刚才一直在"等待" Python 抛出异常——比如用户输入"abc"，Python 抛出 `ValueError`。

但有时候，你需要**主动抛出异常**——告诉调用者："这里有问题，你来处理。"

`raise` 语句可以抛出任何异常：

```python
age = int(input("请输入你的年龄："))

if age < 0:
    raise ValueError("年龄不能为负数")

if age > 120:
    raise ValueError("年龄超出合理范围")

print(f"你的年龄：{age}")
```

如果用户输入 `-5`,程序会抛出 `ValueError`：

```
Traceback (most recent call last):
  File "raise_example.py", line 4, in <module>
    raise ValueError("年龄不能为负数")
ValueError: 年龄不能为负数
```

小北问："这有什么用？为什么不直接 `print` 一个错误信息？比如 `print('年龄不能为负数')`？"

"`print` 不会让程序停下来,"老潘说,"但 `raise` 会——而且它会把这个错误'上报'给调用者。"

"什么意思？"小北一脸困惑。

老潘笑了："来,我给你看一个场景。假设你在写一个'银行转账'函数,如果余额不足,你是希望 `print` 一个错误信息,然后继续执行？还是希望程序停下来,告诉调用者'转账失败了'？"

小北想了想："当然是停下来啊！如果转账失败了,我肯定不能继续往下做——比如给对方发通知什么的。"

"对,这就是 `raise` 的价值,"老潘说,"它不只是'报错',它是'上报问题'——让调用者知道'这里出了问题,你需要处理'。"

**建议示例文件**：`14_basic_raise.py`

---

### 为什么需要 raise

假设你在写一个"银行转账"函数：

```python
def transfer(from_account, to_account, amount):
    """转账函数"""
    if from_account.balance < amount:
        print("余额不足,转账失败")
        return

    from_account.balance -= amount
    to_account.balance += amount
    print("转账成功")
```

小北看完,疑惑道："这不是挺好的吗？"

"问题是,"老潘说,"调用者怎么知道转账成功了还是失败了？"

```python
transfer(alice, bob, 100)
print("给 Bob 发送通知...")  # 转账失败也会执行
```

如果转账失败,`transfer` 函数只是 `print` 了一个错误信息,但程序会继续执行——给 Bob 发送通知,这显然不对。

如果你用 `raise`：

```python
def transfer(from_account, to_account, amount):
    """转账函数"""
    if from_account.balance < amount:
        raise ValueError("余额不足,转账失败")

    from_account.balance -= amount
    to_account.balance += amount

# 调用者
try:
    transfer(alice, bob, 100)
    print("给 Bob 发送通知...")
except ValueError as e:
    print(f"转账失败：{e}")
    # 不发送通知
```

现在,调用者可以"捕获"异常,根据失败与否决定是否发送通知。

**建议示例文件**：`15_why_raise.py`

---

### 封装输入校验函数

让我们把"输入校验"逻辑封装成函数：

```python
def get_positive_integer(prompt):
    """获取一个正整数（会抛出 ValueError）"""
    while True:
        value_str = input(prompt)

        if not value_str.isdigit():
            print("错误：请输入一个正整数")
            continue

        value = int(value_str)

        if value <= 0:
            print("错误：请输入大于 0 的整数")
            continue

        return value

def get_age():
    """获取年龄（18-120 之间）"""
    age = get_positive_integer("请输入你的年龄：")

    if age < 18:
        raise ValueError("年龄必须大于等于 18")

    if age > 120:
        raise ValueError("年龄超出合理范围")

    return age

# 测试
try:
    age = get_age()
    print(f"你的年龄：{age}")
except ValueError as e:
    print(f"输入错误：{e}")
```

`get_age` 函数会调用 `get_positive_integer`,然后**额外检查**年龄是否在 18-120 之间。如果不满足,它会**主动抛出** `ValueError`。

**建议示例文件**：`16_input_validation_functions.py`

---

### 设计友好的错误消息

老潘看到一个同学写的代码：

```python
if age < 0:
    raise ValueError("error")
```

他摇摇头："这个错误信息太模糊了。"

"有什么问题？"小北不解,"用户不就知道出错了吗？"

"想象一下,"老潘说,"你使用一个 ATM 机,取钱的时候屏幕突然显示'Error 404'——你会怎么想？"

小北皱起眉头："我肯定会想：什么鬼？404 是什么意思？我钱被吞了吗？我卡被锁了吗？"

"对,"老潘说,"模糊的错误信息会让用户焦虑、困惑,甚至愤怒。"

"好的错误信息应该告诉用户三件事：
1. **出了什么错**——年龄不能为负数
2. **为什么出错**——你输入了 -5
3. **怎么修复**——请输入一个正整数（0-120）"

```python
# ❌ 坏：太模糊
raise ValueError("error")
raise ValueError("invalid input")

# ⚠️ 一般：能看懂,但不完整
raise ValueError("年龄不能为负数")

# ✅ 好：清晰、可操作
raise ValueError("年龄不能为负数,请输入一个正整数（0-120）")
raise ValueError(f"年龄 {age} 超出合理范围（0-120）,请重新输入")
```

阿码在旁边嘟囔："写这么长的错误信息,会不会太啰嗦？"

"啰嗦总比模糊好,"老潘说,"用户看到清晰的错误信息,会想'哦,我懂了,我该怎么改'；看到模糊的错误信息,会想'这什么破软件,完全不告诉人怎么回事'。"

小北问："用中文还是英文？"

"看你的用户,"老潘说,"关键是**清晰**,不是语言。如果你的用户是中国人,用中文；如果是国际用户,用英文。但无论用什么语言,都要遵循'出了什么错、为什么、怎么修复'这三个原则。"

**建议示例文件**：`17_error_messages.py`

---

现在,让我们整合所有东西,写一个"健壮的用户输入处理器"。

```python
def get_positive_integer(prompt):
    """获取一个正整数"""
    while True:
        value_str = input(prompt)

        if not value_str.isdigit():
            print("错误：请输入一个正整数")
            continue

        value = int(value_str)

        if value <= 0:
            print("错误：请输入大于 0 的整数")
            continue

        return value

def get_choice(prompt, valid_choices):
    """获取用户选择（从有效选项中选）"""
    while True:
        choice = input(prompt)

        if choice in valid_choices:
            return choice

        print(f"错误：请选择 {', '.join(valid_choices)} 之一")

def get_age(min_age=18, max_age=120):
    """获取年龄（在指定范围内）"""
    while True:
        age_str = input(f"请输入你的年龄（{min_age}-{max_age}）：")

        if not age_str.isdigit():
            print("错误：请输入一个整数")
            continue

        age = int(age_str)

        if age < min_age or age > max_age:
            print(f"错误：年龄必须在 {min_age}-{max_age} 之间")
            continue

        return age

# 主程序
print("=== 用户信息收集 ===")

name = input("请输入你的姓名：")
print(f"姓名：{name}")

age = get_age(min_age=18, max_age=120)
print(f"年龄：{age}")

count = get_positive_integer("请输入购买数量：")
print(f"购买数量：{count}")

choice = get_choice("请选择配送方式（快递/自提）：", ["快递", "自提"])
print(f"配送方式：{choice}")

print("\n=== 信息收集完成 ===")
```

这个程序会持续提示用户,直到输入正确为止。无论用户输入什么,它都不会崩溃。

**建议示例文件**：`18_robust_input_processor.py`

---

老潘看完这段代码,点点头："现在你的程序'不怕坏输入'了。用户输入'abc'、'-5'、'999',程序都不会崩溃,而是会友好地提示错误并让用户重试。这就是**防御性编程**的核心思想。"

"防御性编程？"小北问。

"对,"老潘说,"防御性编程不是'防止用户犯错',而是'假设用户一定会犯错',然后让程序能优雅地处理这些错误。你不是在'防守',而是在'容错'。"

阿码在旁边问："那如果我想要'自动重试 3 次,3 次后退出'呢？我不想让用户无限重试。"

"那你就加一个计数器,"老潘说,"用 `for` 循环限制重试次数。"

```python
def get_positive_integer(prompt, max_attempts=3):
    """获取一个正整数（最多重试 max_attempts 次）"""
    for attempt in range(max_attempts):
        value_str = input(prompt)

        if not value_str.isdigit():
            remaining_attempts = max_attempts - attempt - 1
            print(f"错误：请输入一个正整数（剩余尝试次数：{remaining_attempts}）")
            continue

        value = int(value_str)

        if value <= 0:
            remaining_attempts = max_attempts - attempt - 1
            print(f"错误：请输入大于 0 的整数（剩余尝试次数：{remaining_attempts}）")
            continue

        return value

    # 重试次数用完,抛出异常
    raise ValueError(f"输入错误次数过多,超过 {max_attempts} 次")

# 测试
try:
    count = get_positive_integer("请输入购买数量：", max_attempts=3)
    print(f"购买数量：{count}")
except ValueError as e:
    print(f"输入失败：{e}")
```

"哇！"小北惊讶道,"这个 `for` 循环还能这么用？我以为 `for` 只能用来遍历列表或者 `range()` 计数呢！"

"`for` 可以用来'限制尝试次数',"老潘说,"你循环 `max_attempts` 次,如果用户输入正确,就用 `return` 提前退出；如果循环结束了还没返回,说明用户用光了所有机会,这时候抛出异常。"

阿码好奇地问："为什么要用 `raise` 而不是 `print`？"

"好问题！"老潘说,"如果用 `print`,调用者怎么知道输入失败了？它需要检查返回值（比如 `None`）。但如果用 `raise`,调用者可以用 `try/except` 捕获异常,知道'输入失败了'。"

"哦！"小北说,"所以 `raise` 不只是'报错',它还是一种'沟通方式'——函数告诉调用者'这里出了问题'。"

"没错,"老潘笑了,"这就是异常的真正价值：它不只是'错误处理',它还是'函数和调用者之间的沟通机制'。"

**建议示例文件**：`19_retry_with_limit.py`

---

现在,你已经掌握了异常处理的所有核心技能。下一节,我们把本周学的所有东西应用到 PyHelper 上,让它变得"不怕坏输入"。

---

## PyHelper 进度

到目前为止,PyHelper 有一个致命弱点：如果你在菜单选择时输入了"abc"而不是数字——它直接崩溃。

```python
请输入选择（1-5）：abc
Traceback (most recent call last):
  File "pyhelper.py", line 48, in <module>
    choice = int(input("请输入选择（1-5）："))
ValueError: invalid literal for int() with base 10: 'abc'
```

小北盯着红色的报错,叹了口气："上周我手滑输入了'abc',PyHelper 就这样挂了……最气的是,我写了一下午的学习记录全没了。"

"全没了？"阿码惊讶道,"怎么会全没了？你不是保存到文件了吗？"

"问题是,"小北无奈地说,"程序在保存之前就崩了。我选了功能 1（添加记录）,输入了日期和内容,然后回到菜单时手滑输入了'abc'——程序直接崩溃,根本没走到保存那一步。"

"哦不……"阿码同情道,"那确实很崩溃。"

"这就是这周要学的,"老潘说,"给 PyHelper 穿上'防弹衣'——让它'不怕坏输入'。无论用户输入什么,程序都不会崩,而是会友好地提示错误并让用户重试。"

```python
# PyHelper - 你的命令行学习助手
# Week 06：异常处理与防御性编程

from pathlib import Path

# ===== 文件操作函数（Week 05）=====

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
            print("首次运行,将创建新的数据文件")
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

# ===== 输入校验函数（Week 06）=====

def get_choice(min_choice=1, max_choice=5):
    """获取用户选择（带异常处理）"""
    while True:
        try:
            choice = int(input(f"\n请输入选择（{min_choice}-{max_choice}）："))
            if min_choice <= choice <= max_choice:
                return choice
            print(f"错误：请输入 {min_choice} 到 {max_choice} 之间的数字")
        except ValueError:
            print("错误：请输入数字,不要输入文字")

def get_date():
    """获取日期（格式：MM-DD）"""
    while True:
        date = input("请输入日期（如 02-09）：")

        # 简单校验：日期格式必须是 XX-XX
        if "-" not in date or len(date) != 5:
            print("错误：日期格式不对,请输入类似 '02-09' 的格式")
            continue

        # 校验是否为数字
        parts = date.split("-")
        if not (parts[0].isdigit() and parts[1].isdigit()):
            print("错误：日期必须是数字,请输入类似 '02-09' 的格式")
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

# ===== 原有功能函数（Week 03-04）=====

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
        print("还没有学习记录哦,去添加一些吧！")
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
        print("不错的开始,继续加油！")
    else:
        print("万事开头难,加油！")

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
        print("输入无效,默认为一般般")
        return "2"
    except ValueError:
        print("输入无效,默认为一般般")
        return "2"

def get_advice(mood):
    """根据心情返回建议"""
    if mood == "1":
        return "太好了！推荐你今天挑战一个新概念,比如异常处理或模块化。"
    elif mood == "2":
        return "那就做点巩固练习吧,写几个小例子,熟悉一下异常处理。"
    elif mood == "3":
        return "累了就休息一下吧,今天可以只看视频不动手,或者写 10 分钟代码就停。"
    else:
        return "写点巩固练习最稳妥。"

def show_advice():
    """显示学习建议"""
    mood = get_mood()
    advice = get_advice(mood)
    print(f"\n{advice}")

# ===== 主函数 =====

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

# 启动程序
if __name__ == "__main__":
    main()
```

现在无论用户输入什么乱七八糟的东西,PyHelper 都不会崩了——它会耐心地等你输入正确的选项。

小北兴奋地运行了一遍,故意输入"abc"、"-5"、"999",每次 PyHelper 都友好地提示错误,让他重新输入。

"太神奇了！"小北高兴地说,"现在 PyHelper 感觉'活'了——它不再是一个脆弱的玻璃玩具,而是一个能应对各种情况的'助手'。"

阿码在旁边开玩笑："你有没有发现,PyHelper 现在比你更有耐心？如果是我,你输入三次'abc',我就不想理你了。"

小北笑了："哈哈,这就是程序的好处——永远不会发脾气。"

老潘看到这段代码会说什么？"这就对了。用户永远会做你想不到的事情。你无法预测他们会输入什么,但你可以让程序'不怕坏输入'——这就是防御性编程。"

**建议示例文件**：`06_pyhelper.py`

---

小北问："那下周呢？PyHelper 还会继续长大吗？"

"当然,"老潘笑笑,"下周它会学会'分身'——把代码拆成多个文件,变成一个真正的**项目**。这就是**模块化**（modularization）。"

"分身？"阿码好奇道,"像孙悟空那样？"

"哈哈,有点像,"老潘说,"目前 PyHelper 的所有代码都在一个文件里——1500 多行。下周我们会把它拆成多个模块：`menu.py` 负责菜单,`storage.py` 负责文件操作,`input.py` 负责输入校验……每个文件各司其职。"

"哦！"小北眼睛一亮,"就像一个团队,每个人做自己的工作,然后配合起来？"

"完美的类比！"老潘点头,"现在 PyHelper 是一个'独角戏',下周它会变成一个'团队'。"

---

## Git 本周要点

本周必会命令：
- `git status` —— 查看当前状态
- `git diff` —— 查看修改内容
- `git add -A` —— 添加所有修改到暂存区
- `git commit -m "message"` —— 提交修改
- `git log --oneline -n 10` —— 查看最近 10 次提交

常见坑：
- **用裸的 `except:` 捕获所有异常**——这会掩盖真正的 bug。应该捕获特定异常（`except ValueError:`）
- **忘记 `raise`**——输入校验发现错误后,只是 `print` 一个错误信息,然后继续执行。应该用 `raise` 抛出异常
- **错误信息不清晰**——`raise ValueError("error")` 这样的错误信息没有意义。应该告诉用户"出了什么错、为什么、怎么修复"
- **finally 里 return**——`finally` 里的 `return` 会覆盖 `try` 或 `except` 的 `return`,这通常不是你想要的
- **混用 LBYL 和 EAFP**——在同一个项目里,应该保持一致的风格。不要有些地方用 LBYL,有些地方用 EAFP,会让代码难以维护

**异常处理速查表**：

| 异常类型 | 何时抛出 | 捕获方式 |
|---------|---------|---------|
| `ValueError` | 值不合法（如 `int("abc")`） | `except ValueError:` |
| `TypeError` | 类型不匹配（如 `"2" + 3`） | `except TypeError:` |
| `ZeroDivisionError` | 除以零 | `except ZeroDivisionError:` |
| `KeyError` | 字典键不存在 | `except KeyError:` |
| `IndexError` | 列表索引越界 | `except IndexError:` |
| `FileNotFoundError` | 文件不存在 | `except FileNotFoundError:` |

**LBYL vs EAFP 速查表**：

| 场景 | 推荐风格 | 示例 |
|------|---------|------|
| 访问字典/列表 | EAFP | `try: value = dict[key] except KeyError: ...` |
| 文件操作 | EAFP | `try: with open(...) ... except FileNotFoundError: ...` |
| 用户输入验证 | LBYL | `if value_str.isdigit(): ...` |
| 数组/字符串索引 | EAFP | `try: item = list[i] except IndexError: ...` |
| 网络请求 | LBYL | `if url_is_valid(url): ...` |

Pull Request (PR)：
- 本周延续 PR 流程：分支 → 多次提交 → push → PR → review → merge
- PR 描述模板：
  ```markdown
  ## 本周做了什么
  - 实现了异常处理（try/except）
  - 给 PyHelper 添加了输入校验
  - 用 LBYL/EAFP 混合风格优化代码

  ## 自测
  - [ ] 运行 `python3 -m pytest chapters/week_06/tests -q` 通过
  - [ ] PyHelper 输入"abc"不会崩溃,会提示错误
  - [ ] 除法器输入除以零不会崩溃,会提示错误

  ## 待 review
  请重点检查异常处理的完整性（是否捕获了所有预期的异常）
  ```

---

## 本周小结（供下周参考）

这一周,你学会了让程序"不崩"——用 **`try/except`** 捕获异常,用 **`raise`** 主动抛出异常,用 **LBYL/EAFP** 两种风格处理不同的场景。你还学会了设计友好的错误消息,让程序在出错时能告诉用户"出了什么错、为什么、怎么修复"。

你现在写的程序不再是"玻璃做的"——一碰就碎。相反,它们能优雅地处理各种坏输入,给用户友好的提示。这就是**防御性编程**（defensive programming）的核心思想：不是防止用户犯错,而是假设用户一定会犯错,然后让程序能容错。

**本周的 Aha 时刻**：
- 当你第一次用 `try/except` 让崩溃的程序"复活"时,你可能会想："原来程序可以这么温柔"
- 当你理解 LBYL vs EAFP 时,你可能会发现："哦,原来 Python 社区的'先尝试再道歉'哲学,不是鲁莽,而是高效"
- 当你给 PyHelper 添加异常处理后,看着它不再因为一个错误的输入就崩溃,你可能会说："这才是我想要的程序"

到目前为止,你已经掌握了 Python 入门和工程进阶的 6 个核心概念：变量、条件判断、函数、数据结构（列表/字典）、文件操作、异常处理。下周,我们将学习**模块化**（modularization）——把代码拆成多个文件,变成一个真正的"项目"。

你会发现,模块化和异常处理经常一起使用——比如把"输入校验函数"放到一个单独的文件里,让其他模块可以复用。下周 PyHelper 会从"一个巨大的文件"变成"一个有组织结构的项目"。

---

## Definition of Done（学生自测清单）

完成本周学习后,请确认你能做到以下事情：

**核心技能**：你能理解异常的概念,读懂 Traceback 报错信息；掌握 `try/except` 的基本语法,能捕获特定异常（如 `ValueError`、`KeyError`、`FileNotFoundError`）而不是用裸的 `except:`；理解 `else` 和 `finally` 子句的作用；能用 `raise` 主动抛出异常,设计友好的错误消息。

**编程哲学**：你理解 LBYL vs EAFP 两种编程风格的区别,知道什么时候该用"先检查"（LBYL）,什么时候该用"先尝试"（EAFP）。

**实践能力**：你能设计"输入校验"函数,用 `while` 循环实现"重试直到输入正确",用 `for` 循环限制重试次数；能完成健壮的除法器（处理除零、非数字输入）和健壮的用户输入处理器；能给 PyHelper 添加异常处理,让程序"不怕坏输入"。

**工程习惯**：你至少提交了 2 次 Git（draft + verify）,并且运行 `python3 -m pytest chapters/week_06/tests -q` 通过了所有测试。

---

**如果你想验证自己的掌握程度**,试着回答这些问题：

- 如果用户输入了 `"abc"` 而不是数字,程序会抛出什么异常？如何捕获它？
- `else` 和 `finally` 有什么区别？`finally` 在什么场景下特别有用？
- LBYL 和 EAFP 各自适合什么场景？为什么 Python 社区偏爱 EAFP？
- 如果一个函数需要"上报"错误给调用者,应该用 `print` 还是 `raise`？为什么？

如果你能自信地回答这些问题,说明你已经掌握了本周的核心内容。

<!--
章节结构骨架（供 chapter-writer 参考）：

1. 章首导入（引言格言 + 时代脉搏）——已完成
2. 前情提要——已完成
3. 学习目标——已完成
4. 贯穿案例设计说明（HTML 注释）——已完成
5. 认知负荷 + 回顾桥 + 角色出场规划（HTML 注释）——已完成
6. AI 小专栏规划（HTML 注释）——已完成
7. 第 1 节：程序为什么崩溃——异常是什么——已完成
8. 第 2 节：捕获异常——try/except 结构——已完成
9. 第 3 节：else 和 finally——异常处理的完整版——已完成
10. 第 4 节：LBYL vs EAFP——两种编程哲学——已完成
11. 第 5 节：raise 与自定义错误——主动抛出异常——已完成
12. PyHelper 进度——已完成
13. Git 本周要点——已完成
14. 本周小结（供下周参考）——已完成
15. Definition of Done——已完成
-->
