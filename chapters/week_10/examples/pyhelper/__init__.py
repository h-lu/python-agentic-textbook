"""
PyHelper - Week 10 JSON 格式版本

本周改进：
- 数据文件从自定义文本格式升级为 JSON 格式
- 添加 export_notes() 函数，支持导出为 JSON/TXT 格式
- 添加 import_notes() 函数，支持从 JSON 文件导入
- 添加数据版本兼容性处理（数据迁移）
- 强化异常处理，处理 JSONDecodeError 等边界情况

项目结构：
├── storage.py          # 文件操作（重构为 JSON 格式）
├── records.py          # 业务逻辑
├── text_utils.py       # 文本处理
└── tests/              # 测试目录
"""
