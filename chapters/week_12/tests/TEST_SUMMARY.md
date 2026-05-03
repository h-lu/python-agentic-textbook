# Week 12 测试用例设计总结

## 概述

Week 12 当前测试套件聚焦作业交付物 `habit-cli`，共 **7 个 pytest 契约测试**。测试直接导入 `starter_code/habit.py`，覆盖 argparse 子命令、退出码、stderr、JSON 持久化和日志记录。

## 测试文件结构

```text
chapters/week_12/tests/
├── conftest.py
├── test_week12_habit_cli.py
├── README.md
└── TEST_SUMMARY.md
```

## 测试覆盖详情

| 测试函数 | 类型 | 说明 |
|---------|------|------|
| `test_parser_has_assignment_subcommands` | 正例 | 解析作业要求的所有子命令和关键参数 |
| `test_add_list_and_duplicate_flow` | 正例 / 反例 | 添加、列出、重复添加错误 |
| `test_checkin_log_stats_and_delete_flow` | 正例 | 打卡、记录、统计、删除完整流程 |
| `test_list_active_filters_archived_habits` | 边界 | 非活跃习惯不会出现在 `list --active` 中 |
| `test_error_exit_codes_and_stderr` | 反例 | 空输入、不存在习惯返回 1 并写 stderr |
| `test_logs_are_written_to_temp_file` | 正例 | INFO 与 WARNING 日志写入临时 `habit.log` |
| `test_corrupt_data_file_recovers_with_empty_collection` | 边界 / 反例 | 损坏 JSON 文件恢复为空集合并写 ERROR 日志 |

## 运行结果

```text
7 passed
```

## 质量约束

- 测试使用临时 `habits.json` 和 `habit.log`，避免污染工作区。
- `sys.modules.pop("habit", None)` 和 `sys.modules.pop("solution", None)` 防止跨周同名模块缓存污染。
- 测试通过 `capsys` 区分 stdout 和 stderr，确保 CLI 可被脚本可靠调用。
- `stats --json` 使用 `json.loads()` 断言，避免只检查字符串表面格式。
