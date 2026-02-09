#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：日志记录（第 5 节）

本示例演示：
1. logging.basicConfig() 的基本用法
2. 日志级别：DEBUG/INFO/WARNING/ERROR/CRITICAL
3. 日志格式化（时间戳、级别、消息）
4. 日志输出到文件
5. 用 --verbose 参数控制日志级别

运行方式：
    python3 chapters/week_12/examples/06_logging.py
    python3 chapters/week_12/examples/06_logging.py --verbose
    cat todo.log
预期输出：
    - 终端显示简洁的用户消息
    - 日志文件记录详细的运行信息
"""

import argparse
import logging
import sys
from pathlib import Path


# =====================
# 配置日志（全局）
# =====================

LOG_FILE = Path("todo.log")

logging.basicConfig(
    level=logging.INFO,  # 默认记录 INFO 及以上
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOG_FILE,
    encoding="utf-8"
)

# 创建当前模块的 logger
logger = logging.getLogger(__name__)


# =====================
# 创建解析器
# =====================

parser = argparse.ArgumentParser(description="任务管理工具")
parser.add_argument("title", help="任务标题")
parser.add_argument(
    "--verbose",
    action="store_true",
    help="显示详细日志（DEBUG 级别）"
)
args = parser.parse_args()


# =====================
# 调整日志级别
# =====================

if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)
    logger.debug("verbose 模式已启用")


# =====================
# 业务逻辑（带日志）
# =====================

logger.info("尝试添加任务")
logger.debug(f"任务标题：{args.title}")

# 验证输入
if not args.title.strip():
    logger.warning("任务标题为空")
    print("✗ 错误：任务标题不能为空", file=sys.stderr)
    sys.exit(1)

# 模拟添加任务
logger.info(f"任务添加成功：{args.title}")
print(f"✓ 添加任务：{args.title}")

logger.info("程序执行完毕")
print(f"\n提示：日志已保存到 {LOG_FILE}")


# =====================
# 坏例子演示
# =====================

def bad_example_using_print():
    """
    坏例子：用 print() 记录日志

    问题：
    1. 所有日志混在用户输出中
    2. 没有时间戳和级别
    3. 无法控制日志详细程度
    4. 生产环境不适用
    """
    print("\n" + "=" * 50)
    print("【坏例子】用 print() 记录日志")
    print("=" * 50)

    title = "写作业"

    print("2026-02-09 10:00:00 - INFO - 尝试添加任务")  # 手动拼接
    print(f"2026-02-09 10:00:01 - DEBUG - 任务标题：{title}")  # 手动拼接
    print("✓ 添加任务：写作业")
    print("2026-02-09 10:00:02 - INFO - 任务添加成功")

    print("\n问题：")
    print("  - 用户输出和日志混在一起")
    print("  - 需要手动拼接时间戳和级别")
    print("  - 无法控制日志详细程度")
    print("  - 用 logging 模块自动处理")


def bad_example_wrong_level():
    """
    坏例子：日志级别使用不当

    问题：
    1. 生产环境用 DEBUG 级别产生大量日志
    2. 关键错误用 INFO 级别被过滤
    3. 级别混乱，难以筛选
    """
    print("\n" + "=" * 50)
    print("【坏例子】日志级别使用不当")
    print("=" * 50)

    print("错误的日志级别使用：\n")

    print("1. 生产环境用 DEBUG 级别：")
    print("   logging.basicConfig(level=logging.DEBUG)")
    print("   问题：产生大量日志，影响性能\n")

    print("2. 关键错误用 INFO 级别：")
    print("   logging.info('数据库连接失败，程序退出')")
    print("   问题：用户设置 level=WARNING 时会过滤掉\n")

    print("3. 不分级别，全用 INFO：")
    print("   logging.info('用户登录')")
    print("   logging.info('数据库连接失败')")
    print("   问题：无法区分正常信息和错误信息\n")

    print("正确做法：")
    print("  - DEBUG：开发调试信息")
    print("  - INFO：正常运行信息")
    print("  - WARNING：警告（不影响运行）")
    print("  - ERROR：错误（影响功能）")
    print("  - CRITICAL：严重错误（程序无法继续）")


def bad_example_logging_sensitive_info():
    """
    坏例子：记录敏感信息

    问题：
    1. 密码、令牌被记录到日志
    2. 日志文件可能被其他用户读取
    3. 安全隐患
    """
    print("\n" + "=" * 50)
    print("【坏例子】记录敏感信息")
    print("=" * 50)

    print("错误的日志记录：\n")

    print("1. 记录密码：")
    print("   logging.info(f'用户登录：user={username}, password={password}')")
    print("   问题：密码明文记录到日志文件\n")

    print("2. 记录令牌：")
    print("   logging.info(f'API 调用：token={api_token}')")
    print("   问题：令牌泄露\n")

    print("正确做法：")
    print("  - 敏感信息不记录：logging.info(f'用户登录：user={username}')")
    print("  - 脱敏处理：logging.info(f'令牌：{token[:8]}...')")
    print("  - 使用环境变量，不在日志中显示")


def good_example_logging_best_practices():
    """
    好例子：logging 最佳实践
    """
    print("\n" + "=" * 50)
    print("【好例子】logging 最佳实践")
    print("=" * 50)

    print("1. 合理的日志级别：")
    print("   - 开发环境：level=logging.DEBUG")
    print("   - 生产环境：level=logging.INFO 或 WARNING\n")

    print("2. 清晰的日志消息：")
    print("   logging.info(f'任务 {task_id} 添加成功')")
    print("   logging.error(f'任务 {task_id} 添加失败：{reason}')\n")

    print("3. 分离用户输出和日志：")
    print("   print('✓ 添加任务成功')  # 给用户看")
    print("   logger.info('任务添加成功')  # 给开发者看\n")

    print("4. 用参数控制日志级别：")
    print("   parser.add_argument('--verbose', action='store_true')")
    print("   if args.verbose:")
    print("       logging.getLogger().setLevel(logging.DEBUG)")


if __name__ == "__main__":
    # 主流程已经在上面执行
    # 坏例子需要单独调用
    pass
