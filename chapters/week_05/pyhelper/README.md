# PyHelper Week 05

## 继承上周

保留 Week 04 的菜单、心情建议、内存学习记录和统计。

## 本周新增

增加 `pyhelper_data.txt` 文本文件持久化，启动加载、退出保存。

## 运行

以下命令默认在本目录运行：

```bash
cd chapters/week_05/pyhelper
python3 app.py
```

## 数据文件说明

本周开始包含 `pyhelper_data.txt` 示例数据。程序默认从示例数据读取；写入时会使用系统临时目录，或使用 `PYHELPER_DATA_FILE=/path/to/file` 指定自己的数据文件。
