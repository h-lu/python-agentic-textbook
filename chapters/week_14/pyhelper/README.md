# PyHelper Week 14

## 继承上周

保留 Week 13 的 CLI、JSON 存储、dataclass 模型、搜索导出和 agent team 学习计划追踪。

## 本周新增

收敛为 PyHelper v1.0.0 发布包，补充 README 与 RELEASE_NOTES。

## 运行

以下命令默认在本目录运行：

```bash
cd chapters/week_14/pyhelper
PYHELPER_DATA_FILE=/tmp/pyhelper_week14.json python3 main.py add "整理发布说明 #release" --date 2026-05-11
PYHELPER_DATA_FILE=/tmp/pyhelper_week14.json python3 main.py plan
PYHELPER_DATA_FILE=/tmp/pyhelper_week14.json python3 main.py review
```

## 数据文件说明

本周使用 JSON 数据。程序默认从 `sample_records.json` 示例数据读取；写入时会使用系统临时目录，或使用 `PYHELPER_DATA_FILE=/path/to/file` 指定自己的数据文件。
