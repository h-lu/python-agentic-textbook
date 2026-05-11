# PyHelper Week 08

## 继承上周

保留 Week 07 的完整模块化结构、文本持久化和兼容入口。

## 本周新增

增加 pytest 测试，覆盖输入校验、记录业务逻辑和存储层。

## 运行

以下命令默认在本目录运行：

```bash
cd chapters/week_08/pyhelper
python3 main.py
pytest tests -q
```

## 数据文件说明

本周开始包含 `pyhelper_data.txt` 示例数据。程序默认从示例数据读取；写入时会使用系统临时目录，或使用 `PYHELPER_DATA_FILE=/path/to/file` 指定自己的数据文件。
