# PyHelper Week 07

## 继承上周

保留 Week 06 的欢迎、心情建议、学习记录、文本持久化和输入校验。

## 本周新增

把单文件拆成 `main.py`、`storage.py`、`input_handler.py`、`encouragement.py`、`records.py`。

## 运行

以下命令默认在本目录运行：

```bash
cd chapters/week_07/pyhelper
python3 main.py
python3 app.py  # 兼容入口
```

## 数据文件说明

本周开始包含 `pyhelper_data.txt` 示例数据。程序默认从示例数据读取；写入时会使用系统临时目录，或使用 `PYHELPER_DATA_FILE=/path/to/file` 指定自己的数据文件。
