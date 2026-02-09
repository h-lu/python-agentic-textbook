"""pytest 配置和共享 fixtures

用于 Week 12 测试的共享配置
"""

import pytest
import tempfile
import logging
import sys
import os

# 添加 starter_code 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))


@pytest.fixture
def temp_log_file():
    """创建临时日志文件"""
    log_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
    log_path = log_file.name
    log_file.close()

    yield log_path

    # 清理
    if os.path.exists(log_path):
        os.unlink(log_path)


@pytest.fixture
def temp_data_file():
    """创建临时 JSON 数据文件"""
    data_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    data_path = data_file.name
    data_file.close()

    # 初始化为空列表
    import json
    with open(data_path, 'w') as f:
        json.dump([], f)

    yield data_path

    # 清理
    if os.path.exists(data_path):
        os.unlink(data_path)


@pytest.fixture
def reset_logging():
    """重置 logging 配置

    在每个测试后清理 logging handlers，避免日志配置污染
    """
    # 测试前
    root_handlers = logging.root.handlers[:]

    yield

    # 测试后：清理所有 handlers
    for handler in logging.root.handlers[:]:
        handler.close()
        logging.root.removeHandler(handler)


@pytest.fixture
def sample_todos_data():
    """示例待办事项数据"""
    return [
        {"id": 1, "title": "买牛奶", "done": False},
        {"id": 2, "title": "写作业", "done": False},
        {"id": 3, "title": "学习 Python", "done": True},
    ]


@pytest.fixture
def cli_parser():
    """创建示例 CLI 解析器

    返回一个配置好的 argparse.ArgumentParser 对象
    用于测试 CLI 功能
    """
    import argparse

    parser = argparse.ArgumentParser(description="任务管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # add 子命令
    add_parser = subparsers.add_parser("add", help="添加任务")
    add_parser.add_argument("title", help="任务标题")
    add_parser.add_argument("--priority", choices=["low", "medium", "high"],
                          default="medium", help="优先级")

    # list 子命令
    list_parser = subparsers.add_parser("list", help="列出任务")
    group = list_parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="显示所有任务")
    group.add_argument("--pending", action="store_true", help="只显示未完成")
    group.add_argument("--done", action="store_true", help="只显示已完成")

    # done 子命令
    done_parser = subparsers.add_parser("done", help="标记任务完成")
    done_parser.add_argument("id", type=int, help="任务 ID")

    # delete 子命令
    delete_parser = subparsers.add_parser("delete", help="删除任务")
    delete_parser.add_argument("id", type=int, help="任务 ID")

    return parser


@pytest.fixture
def mock_args():
    """模拟命令行参数对象"""
    class MockArgs:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    return MockArgs


@pytest.fixture
def sample_script_path():
    """创建示例 Python 脚本并返回路径

    用于 subprocess 测试
    """
    import tempfile

    script = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py')
    path = script.name
    script.close()

    yield path

    # 清理
    if os.path.exists(path):
        os.unlink(path)
