#!/bin/bash
# 清理 Week 12 示例生成的数据文件

echo "清理 Week 12 示例数据文件..."

# 清理 examples 目录下的数据文件
rm -f chapters/week_12/examples/todo_cli.json
rm -f chapters/week_12/examples/todo_cli.log
rm -f chapters/week_12/examples/todo.log

# 清理 PyHelper 数据
rm -rf ~/.pyhelper/

echo "✓ 清理完成"
