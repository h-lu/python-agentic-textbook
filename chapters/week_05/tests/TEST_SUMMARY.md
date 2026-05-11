# Week 05 测试用例总结

## 测试文件概览

为 Week 05（文件读写）创建了 5 个测试文件，共 112 个测试用例（含作业契约测试）：

### 1. test_file_basics.py - 文件基础测试 (25 个测试)

**测试类：**

- **TestFileWrite**
  - 单行写入
  - 多行写入
  - 换行符使用
  - 不换行时内容连接

- **TestFileRead**
  - read() 读取全部内容
  - readlines() 返回列表
  - readline() 读取单行
  - 逐行遍历文件
  - 读取空文件
  - 使用 strip() 去除换行符

- **TestWithStatement**
  - with 语句自动关闭文件
  - with 确保数据落盘

- **TestFileModes**
  - "w" 写入模式覆盖已有内容
  - "a" 追加模式添加到末尾
  - 追加模式创建不存在的文件
  - "r" 读取模式文件不存在时报错

- **TestFileHandling**
  - split() 分割行内容
  - split() 处理多个分隔符
  - 将字典写入文件
  - 从文件读取并重建字典

- **TestEdgeCases**
  - 写入空字符串
  - 写入特殊字符
  - 写入超长行
  - 写入 Unicode emoji
  - 处理空行

### 2. test_pathlib.py - pathlib 测试 (31 个测试)

**测试类：**

- **TestPathBasics**
  - 创建 Path 对象
  - Path.home() 获取用户主目录
  - Path.cwd() 获取当前工作目录
  - 用 / 运算符拼接路径

- **TestPathProperties**
  - 获取文件名 (name)
  - 获取扩展名 (suffix)
  - 获取父目录 (parent)
  - 获取文件名不含扩展名 (stem)

- **TestPathOperations**
  - 检查文件是否存在 (exists())
  - 判断文件/目录 (is_file/is_dir)
  - 创建多级目录 (mkdir with parents)
  - exist_ok 参数避免重复创建

- **TestPathReadWrite**
  - write_text() 基本用法
  - read_text() 基本用法
  - 读写中文内容
  - 读写多行文本
  - 读写空文件

- **TestPathCrossPlatform**
  - 路径分隔符自动适配
  - Path 对象是操作系统感知的
  - 相对路径的使用

- **TestPathPractical**
  - 构建数据文件路径（模拟 PyHelper）
  - 读取前检查文件是否存在
  - 列出目录中的文件
  - 获取文件大小

- **TestPathEdgeCases**
  - 处理带空格的路径
  - 处理 Unicode 文件名
  - 空文件名
  - 多个点的文件名
  - 末尾斜杠行为

### 3. test_encoding.py - 编码测试 (25 个测试)

**测试类：**

- **TestUTF8Encoding**
  - UTF-8 读写中文
  - 读写混合语言文本
  - pathlib 的 UTF-8 读写
  - 中文在字典格式中的存储
  - Unicode emoji 字符

- **TestEncodingBasics**
  - 字符串编码为字节
  - 字节解码为字符串
  - 不同编码产生不同字节
  - 错误编码解码会失败

- **TestEncodingInFileOperations**
  - UTF-8 写入和读取匹配
  - 用错误编码读取会报错
  - 中文必须指定正确编码

- **TestSpecialCharacters**
  - 换行符处理
  - 制表符和空格
  - 引号和反斜杠
  - 各种标点符号

- **TestEncodingEdgeCases**
  - 空字符串编码
  - 很长的中文文本
  - ASCII 和中文混合
  - Unicode 转义序列
  - BOM (Byte Order Mark)
  - 生僻中文字符

- **TestPracticalEncodingScenarios**
  - 中文日记的存储和读取
  - 带日期的学习记录
  - 搜索中文内容

### 4. test_diary_app.py - 日记本工具测试 (29 个测试)

**包含的实现函数：**
- `add_diary_entry()` - 添加日记条目
- `read_all_diaries()` - 读取所有日记
- `search_diaries()` - 搜索日记
- `count_diaries()` - 统计日记条数

**测试类：**

- **TestAddDiaryEntry**
  - 添加单条日记
  - 添加多条日记
  - 追加模式不覆盖
  - 添加中文日记
  - 添加包含特殊字符的日记
  - 添加长日记

- **TestReadDiaries**
  - 读取不存在的文件
  - 读取单条日记
  - 读取多条日记
  - 读取内容与写入一致
  - 空行过滤
  - 读取中文内容

- **TestSearchDiaries**
  - 搜索单个关键词
  - 多个匹配结果
  - 搜索不存在的内容
  - 搜索中文关键词
  - 搜索日期格式
  - 部分匹配搜索

- **TestCountDiaries**
  - 统计空日记
  - 统计单条日记
  - 统计多条日记

- **TestDiaryIntegration**
  - 完整的写-读-搜工作流
  - 数据持久化验证
  - Unicode 内容正确保存

- **TestDiaryEdgeCases**
  - 空日记内容
  - 很长的日记条目
  - 特殊字符在日记中
  - 搜索空关键词
  - 连续添加操作

### 5. test_assignment_contract.py - 作业契约测试 (2 个测试)

- 作业入口文件存在
- 必要函数 / 运行契约保持稳定

## 测试覆盖矩阵

| 测试维度 | 正例 | 边界 | 反例 |
|---------|-----|------|-----|
| 文件读写 | ✅ 基本读写、多行、字典格式 | ✅ 空文件、超长行、特殊字符 | ✅ 文件不存在、错误模式 |
| with 语句 | ✅ 自动关闭、数据落盘 | - | - |
| pathlib | ✅ 路径操作、读写、跨平台 | ✅ 空文件名、Unicode 文件名、多空格 | ✅ 文件不存在、重复创建目录 |
| 编码 | ✅ UTF-8 读写、中文、emoji | ✅ 空字符串、超长文本、生僻字 | ✅ 错误编码解码 |
| 日记本 | ✅ 写/读/搜/统计 | ✅ 空内容、超长条目 | ✅ 搜索不存在的内容 |

## 测试特点

1. **使用 tmp_path fixture**：所有测试自动使用临时目录，测试后自动清理
2. **清晰的 docstring**：每个测试都有中文说明
3. **完整的命名**：测试函数名清晰描述测试场景
4. **跨平台兼容**：测试考虑了不同操作系统的路径差异
5. **UTF-8 重点**：大量测试覆盖中文和 Unicode 字符

## 运行测试

```bash
# 运行所有测试
python3 -m pytest chapters/week_05/tests -q

# 运行特定测试文件
python3 -m pytest chapters/week_05/tests/test_file_basics.py -v

# 运行带标记的测试
python3 -m pytest chapters/week_05/tests -m encoding

# 查看详细输出
python3 -m pytest chapters/week_05/tests -v
```

## 测试结果

```
112 passed
```

所有测试通过 ✅
