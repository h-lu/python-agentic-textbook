# Week 01–08 作业/代码一致性收口报告

生成时间：2026-05-03
分支：`fix/week01-08-alignment`

## 范围

使用 4 路 tmux/codex 子任务并行审计 Week 01–02、03–04、05–06、07–08，随后主会话统一做集成修复和全量验证。

目标是让 `ASSIGNMENT.md`、`starter_code`、测试与 release 校验口径一致；不是重写章节正文。

## 主要修复

- Week 01：补齐 `QA_REPORT.md` release 必需的 `## 阻塞项`；参考实现年龄输出与作业示例保持一致。
- Week 02：澄清参考实现注释中“难度选择/输入校验”属于进阶能力，避免和基础作业口径冲突。
- Week 03：作业增加 `starter_code/` 提交路径说明；参考实现补齐矩形面积/周长接口。
- Week 04：补齐 `QA_REPORT.md` release 必需的 `## 阻塞项`；测试导入前清理 `solution` 模块缓存，避免多周联跑拿到其他周实现。
- Week 05：将作业说明从旧“记账本”口径对齐到现有测试/示例/参考实现的“学习日记/学习记录”文件持久化项目；参考实现补齐日记追加、读取、搜索、计数接口。
- Week 06：作业说明对齐真实 starter/test/example 路径；参考实现补齐作业中点名的正整数、年龄、菜单选择接口；测试导入前清理 `solution` 模块缓存，避免多周联跑污染。
- Week 07：补齐作业承诺的 `starter_code/todo_list.py`。
- Week 08：作业说明中测试/目标文件路径对齐 `starter_code/todo_manager.py`；概念测试显式从 `starter_code` 导入，避免依赖导入缓存。
- Week 03/04：增加周目录 package marker，解决多周 pytest 收集时两个 `tests/conftest.py` 都被注册为 `tests.conftest` 的冲突。

## 验证结果

- `python3 -m py_compile`（Week 01–08 所有非 `__pycache__` Python 文件）：`compiled 135 files`
- `python3 -m pytest chapters/week_01/tests ... chapters/week_08/tests -q`：`1151 passed, 1 xfailed, 1 xpassed`
- `make test W=01..08`：逐周全过
- `python3 scripts/validate_week.py --week 01..08 --mode release`：逐周全 OK
- `python3 -m pytest chapters/week_01/tests ... chapters/week_14/tests -q`：`1429 passed, 1 xfailed, 1 xpassed`
- `python3 scripts/validate_book.py --mode fast`：`[validate-book] OK`

## 备注

4 个 codex 子任务的原始分段报告保留在：

- `reports/week01_08_alignment_agent_w01_02.md`
- `reports/week01_08_alignment_agent_w03_04.md`
- `reports/week01_08_alignment_agent_w05_06.md`
- `reports/week01_08_alignment_agent_w07_08.md`

其中部分子任务在 Codex sandbox 内遇到第三方 pytest 插件 socket 限制；主会话集成验证使用普通执行环境复核，最终无需禁用插件即可通过。
