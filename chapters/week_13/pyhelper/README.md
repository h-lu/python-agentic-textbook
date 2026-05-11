# PyHelper Week 13

## 继承上周

保留 Week 12 的 argparse CLI、dataclass 模型、JSON 存储、搜索、导出和统计。

## 本周新增

增加 agent team：Reader/Planner/Reviewer，并接入 `plan` / `review` CLI 命令。

## 运行

以下命令默认在本目录运行：

```bash
cd chapters/week_13/pyhelper
PYHELPER_DATA_FILE=/tmp/pyhelper_week13.json python3 main.py add "整理 agent plan #agent" --date 2026-05-11
PYHELPER_DATA_FILE=/tmp/pyhelper_week13.json python3 main.py plan
PYHELPER_DATA_FILE=/tmp/pyhelper_week13.json python3 main.py review
```

## 数据文件说明

本周使用 JSON 数据。程序默认从 `sample_records.json` 示例数据读取；写入时会使用系统临时目录，或使用 `PYHELPER_DATA_FILE=/path/to/file` 指定自己的数据文件。
