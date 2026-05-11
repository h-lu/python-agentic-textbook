# PyHelper Week 12

## 继承上周

保留 Week 11 的 dataclass 模型、JSON 存储、搜索、导出和统计。

## 本周新增

增加 `argparse` CLI：`add/list/search/export/stats/advice`。

## 运行

以下命令默认在本目录运行：

```bash
cd chapters/week_12/pyhelper
PYHELPER_DATA_FILE=/tmp/pyhelper_week12.json python3 main.py add "学习 argparse #cli" --date 2026-05-11
PYHELPER_DATA_FILE=/tmp/pyhelper_week12.json python3 main.py list
python3 main.py export
```

## 数据文件说明

本周使用 JSON 数据。程序默认从 `sample_records.json` 示例数据读取；写入时会使用系统临时目录，或使用 `PYHELPER_DATA_FILE=/path/to/file` 指定自己的数据文件。
