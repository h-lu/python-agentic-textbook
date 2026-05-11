# PyHelper Week 11

## 继承上周

保留 Week 10 的 JSON 存储、搜索、过滤、导入导出和旧数据迁移。

## 本周新增

增加 `dataclass` 模型 `Note` / `StudyPlan`，并在记录、搜索、序列化中使用模型转换。

## 运行

以下命令默认在本目录运行：

```bash
cd chapters/week_11/pyhelper
python3 main.py
pytest tests -q
```

## 数据文件说明

本周使用 JSON 数据。程序默认从 `sample_records.json` 示例数据读取；写入时会使用系统临时目录，或使用 `PYHELPER_DATA_FILE=/path/to/file` 指定自己的数据文件。
