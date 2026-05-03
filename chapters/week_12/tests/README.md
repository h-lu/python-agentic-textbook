# Week 12 测试文件说明

本目录包含 Week 12（命令行习惯追踪器 habit-cli）的作业契约测试。

## 测试文件概览

| 文件 | 作用 |
|------|------|
| `conftest.py` | 添加 `starter_code/` 到导入路径，并清理 `habit` / `solution` 模块缓存 |
| `test_week12_habit_cli.py` | 验证 habit-cli 的子命令、退出码、stderr、JSON 持久化和日志文件 |

## 覆盖矩阵

| 测试函数 | 覆盖内容 |
|---------|---------|
| `test_parser_has_assignment_subcommands` | `add/list/checkin/log/delete/stats` 子命令和关键参数 |
| `test_add_list_and_duplicate_flow` | 添加、列出、重复习惯报错 |
| `test_checkin_log_stats_and_delete_flow` | 打卡、查看记录、统计 JSON、删除 |
| `test_list_active_filters_archived_habits` | `list --active` 过滤非活跃习惯 |
| `test_error_exit_codes_and_stderr` | 空输入和不存在习惯的退出码与 stderr |
| `test_logs_are_written_to_temp_file` | `habit.log` 中的 INFO / WARNING 日志 |
| `test_corrupt_data_file_recovers_with_empty_collection` | 损坏 JSON 文件恢复为空集合并写 ERROR 日志 |

## 运行测试

```bash
# 运行 Week 12 全部测试
python3 -m pytest chapters/week_12/tests -q

# 运行单个契约测试
python3 -m pytest chapters/week_12/tests/test_week12_habit_cli.py::test_checkin_log_stats_and_delete_flow -q
```

当前期望结果：

```text
7 passed
```

## 测试隔离

测试通过 `monkeypatch` 把 `habit.DATA_FILE` 和 `habit.LOG_FILE` 指向临时目录，不会读写仓库根目录的 `habits.json` 或 `habit.log`。`today_string()` 也会固定为 `2026-02-09`，确保断言稳定。

## 测试覆盖的本周核心概念

1. **argparse**
   - `ArgumentParser`
   - 子命令和参数解析

2. **子命令**
   - `add/list/checkin/log/delete/stats`
   - `set_defaults(func=...)` 路由

3. **退出码与 stderr**
   - 成功返回 0
   - 空输入、重复添加、不存在习惯返回 1
   - 错误消息写入 stderr

4. **logging 与持久化**
   - JSON 数据文件读写
   - INFO、WARNING、ERROR 日志写入 `habit.log`
