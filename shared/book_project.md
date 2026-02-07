# 全书贯穿项目：PyHelper — 命令行学习助手

## 设计理念

每周独立的贯穿案例让学生有"当周成就感"，但 14 个互不相关的小项目缺乏连贯性。PyHelper 是一条**超级线**——一个从 Week 01 开始、逐周增长、到 Week 14 变成 Capstone 作品的命令行工具。

它解决一个学生真正有的需求：**管理自己的学习笔记和进度**。

## 每周推进清单

### Week 01：能打印一句鼓励的话

```python
# examples/05_pyhelper.py
print("欢迎使用 PyHelper！")
print("今日一句：写代码就像搭积木，一块一块来。")
```

学到的概念应用：print、字符串。
**这不是完整项目，只是一个种子。** 让读者知道"这个东西后面会长大"。

### Week 02：根据心情推荐建议

用 `input()` 问用户心情，用 `if/else` 给不同建议。
学到的概念应用：input、if/elif/else、while（是否继续）。

### Week 03：拆成函数 + 菜单

把 Week 02 的代码重构成函数。加一个文字菜单：
1. 获取学习建议
2. 查看今日名言
3. 退出

学到的概念应用：函数定义、参数、返回值。

### Week 04：用字典存学习记录

用字典存储学习笔记（日期→内容），支持添加、查看、统计。
学到的概念应用：dict、list、遍历、过滤。

### Week 05：存到文件

学习记录不再"关了就没"——存到 `pyhelper_data.txt`（或简单的文本格式），下次打开自动加载。
学到的概念应用：文件读写、pathlib、with 语句。

### Week 06：不怕坏输入

加 try/except 处理各种非法输入（空字符串、非法日期格式、文件损坏等）。
学到的概念应用：异常处理、输入校验。

### Week 07：拆成多文件

从单文件拆成项目结构：
```
pyhelper/
├── main.py          # 入口 + 菜单
├── notes.py         # 笔记增删查
├── storage.py       # 文件读写
└── encouragement.py # 鼓励语生成
```
学到的概念应用：import、模块、__name__ 守卫。

### Week 08：补测试

给 `notes.py` 和 `storage.py` 写 pytest 测试。
学到的概念应用：pytest 断言、fixture、参数化。

### Week 09：搜索和过滤笔记

支持按关键词搜索笔记、按日期范围过滤。
学到的概念应用：字符串方法、正则表达式、边界用例。

### Week 10：改用 JSON 格式

数据文件从纯文本升级为 JSON，支持导入/导出。
学到的概念应用：JSON 序列化、数据契约。

### Week 11：dataclass 建模

用 `@dataclass` 定义 `Note`、`StudyPlan` 等数据模型。
学到的概念应用：dataclass、类型提示、状态管理。

### Week 12：完整 CLI

用 `argparse` 把 PyHelper 变成真正的命令行工具：
```bash
pyhelper add "今天学了异常处理"
pyhelper list --date 2025-03-15
pyhelper search "异常"
pyhelper export --format json
pyhelper stats
```
学到的概念应用：argparse 子命令、退出码、logging。

### Week 13：AI 协作完善

用 agent team 模式协作：一个 agent 补文档、一个 agent 补测试、一个 agent 做 code review。
学到的概念应用：agent team、review checklist。

### Week 14：Capstone 发布

收敛所有功能，补 README、写 release notes、做最终 PR。
发布 PyHelper v1.0。

## 代码演进规则

1. **增量修改**：每周在上周代码基础上修改，不从头重写
2. **代码放在 `examples/` 最后编号**：如 `05_pyhelper.py`（Week 01-06 单文件），Week 07+ 放在 `examples/pyhelper/` 目录
3. **可运行**：每周的 PyHelper 代码必须能独立运行
4. **chapter-writer 在 CHAPTER.md 中写 `## PyHelper 进度` 小节**：展示本周改了什么、为什么这么改、运行效果

## 与每周独立案例的关系

每周有两个案例维度：

| 维度 | 例子（Week 04） | 目的 |
|------|-----------------|------|
| 独立贯穿案例 | 班级成绩单 | 当周知识的完整演练 |
| PyHelper 超级线 | 用字典存学习记录 | 把当周知识织入全书项目 |

独立案例占正文 70-80%，PyHelper 占 20-30%。不要让超级线喧宾夺主。
