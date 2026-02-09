# Week 12 示例代码说明

本目录包含 Week 12《命令行工具开发》的所有示例代码。

## 文件列表

### 基础示例（按学习顺序）

1. **01_simple_argparse.py** - 最简单的 argparse 程序
   - 演示如何创建 ArgumentParser
   - 演示位置参数（必需参数）
   - 演示自动生成的帮助信息

2. **02_optional_args.py** - 可选参数与默认值
   - 演示短选项（-p）和长选项（--priority）
   - 演示参数默认值
   - 演示 choices 限制取值范围

3. **03_mutually_exclusive.py** - 互斥参数组
   - 演示如何创建互斥参数组
   - 演示 action="store_true" 的用法
   - 演示 argparse 自动检测参数冲突

4. **04_subcommands.py** - 子命令架构
   - 演示如何用 add_subparsers() 创建子命令
   - 演示每个子命令有独立的参数
   - 演示用 set_defaults(func=...) 路由到处理函数

5. **05_exit_codes.py** - 退出码
   - 演示如何用 sys.exit() 返回退出码
   - 演示退出码约定（0 成功，1 失败）
   - 演示错误消息输出到 stderr

6. **06_logging.py** - 日志记录
   - 演示 logging.basicConfig() 的基本用法
   - 演示日志级别（DEBUG/INFO/WARNING/ERROR）
   - 演示日志输出到文件

### 综合示例

7. **07_todo_cli_complete.py** - 完整的 todo-cli 工具
   - 综合运用所有本周知识
   - 完整的子命令架构（add/list/done/delete/stats）
   - dataclass 数据模型（关联 Week 11）
   - JSON 文件存储（关联 Week 10）
   - 退出码和日志记录

### PyHelper 超级线

**pyhelper/cli.py** - PyHelper 命令行工具
   - 演示如何在真实项目中应用 CLI 开发
   - 支持子命令：add/list/search/export/stats
   - 日志记录到 ~/.pyhelper/pyhelper.log
   - 数据存储到 ~/.pyhelper/notes.json

## 运行方式

### 基础示例

```bash
# 01 - 最简单的 argparse
python3 chapters/week_12/examples/01_simple_argparse.py "写作业"
python3 chapters/week_12/examples/01_simple_argparse.py --help

# 02 - 可选参数
python3 chapters/week_12/examples/02_optional_args.py "写作业" --priority high
python3 chapters/week_12/examples/02_optional_args.py "写作业" -p high -t "Python,作业"

# 03 - 互斥参数
python3 chapters/week_12/examples/03_mutually_exclusive.py --pending
python3 chapters/week_12/examples/03_mutually_exclusive.py --all --pending  # 会报错

# 04 - 子命令
python3 chapters/week_12/examples/04_subcommands.py add "写作业" --priority high
python3 chapters/week_12/examples/04_subcommands.py list --pending
python3 chapters/week_12/examples/04_subcommands.py done 1

# 05 - 退出码
python3 chapters/week_12/examples/05_exit_codes.py "写作业"
echo $?  # 查看退出码

# 06 - 日志
python3 chapters/week_12/examples/06_logging.py "写作业"
cat todo.log  # 查看日志文件
```

### 完整 todo-cli 工具

```bash
cd chapters/week_12/examples

# 添加待办事项
python3 07_todo_cli_complete.py add "完成 Week 12 作业" --priority high
python3 07_todo_cli_complete.py add "复习 Python" --priority medium

# 列出待办事项
python3 07_todo_cli_complete.py list
python3 07_todo_cli_complete.py list --pending
python3 07_todo_cli_complete.py list --done

# 标记完成
python3 07_todo_cli_complete.py done 1

# 删除
python3 07_todo_cli_complete.py delete 2

# 统计
python3 07_todo_cli_complete.py stats
python3 07_todo_cli_complete.py stats --json
```

### PyHelper CLI

```bash
# 添加笔记
python3 -m chapters.week_12.examples.pyhelper.cli add "今天学了 argparse" --tags Python CLI

# 列出笔记
python3 -m chapters.week_12.examples.pyhelper.cli list
python3 -m chapters.week_12.examples.pyhelper.cli list --pending

# 搜索笔记
python3 -m chapters.week_12.examples.pyhelper.cli search "argparse"

# 导出笔记
python3 -m chapters.week_12.examples.pyhelper.cli export --format json
python3 -m chapters.week_12.examples.pyhelper.cli export -o backup.csv --format csv

# 统计
python3 -m chapters.week_12.examples.pyhelper.cli stats
python3 -m chapters.week_12.examples.pyhelper.cli stats --json

# 查看日志
cat ~/.pyhelper/pyhelper.log
```

## 学习要点

### 本周新知识

1. **argparse** - 命令行参数解析
   - 位置参数 vs 可选参数
   - 短选项（-p）vs 长选项（--priority）
   - 互斥参数组
   - 子命令架构

2. **退出码** - 告诉调用者执行结果
   - 0 表示成功，非 0 表示失败
   - sys.exit() 返回退出码
   - 错误消息输出到 stderr

3. **logging** - 日志记录
   - 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
   - logging.basicConfig() 配置
   - 日志输出到文件

### 复习之前的知识

- **Week 10**: JSON 序列化（to_dict / from_dict）
- **Week 11**: dataclass 数据模型、类型提示
- **Week 06**: 异常处理（try/except）
- **Week 07**: 模块化项目结构

## 测试

运行所有示例测试：

```bash
python3 -m pytest chapters/week_12/tests/test_examples.py -v
```

## 数据文件

运行示例后会生成以下文件：

- `todo_cli.json` - todo-cli 的数据文件
- `todo_cli.log` - todo-cli 的日志文件
- `~/.pyhelper/notes.json` - PyHelper 的笔记数据
- `~/.pyhelper/pyhelper.log` - PyHelper 的日志

可以安全删除这些文件重新开始。
