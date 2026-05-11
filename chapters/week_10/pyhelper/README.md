# PyHelper Week 10

## 继承上周

保留 Week 09 的模块化、测试、搜索、日期过滤和 tag 提取。

## 本周新增

把文本存储升级为 JSON，支持导入、导出和旧文本数据迁移。

## 运行

以下命令默认在本目录运行：

```bash
cd chapters/week_10/pyhelper
python3 main.py
pytest tests -q
```

## 数据文件说明

本周使用 JSON 数据。程序默认从 `sample_records.json` 示例数据读取；写入时会使用系统临时目录，或使用 `PYHELPER_DATA_FILE=/path/to/file` 指定自己的数据文件。
