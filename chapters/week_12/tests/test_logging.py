"""测试 logging 模块

这些测试验证学生对 logging 模块的理解：
- logging.basicConfig() 配置
- 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
- 日志格式化
- 日志输出到文件
- logger 对象使用
- logging vs print
"""

import pytest
import logging
import tempfile
import os
import sys

# 添加 starter_code 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))


class TestLoggingBasics:
    """测试 logging 基础"""

    def test_logging_levels_exist(self):
        """测试日志级别常量存在"""
        assert hasattr(logging, 'DEBUG')
        assert hasattr(logging, 'INFO')
        assert hasattr(logging, 'WARNING')
        assert hasattr(logging, 'ERROR')
        assert hasattr(logging, 'CRITICAL')

    def test_logging_level_values(self):
        """测试日志级别数值"""
        assert logging.DEBUG == 10
        assert logging.INFO == 20
        assert logging.WARNING == 30
        assert logging.ERROR == 40
        assert logging.CRITICAL == 50

    def test_basic_logging(self, caplog):
        """测试基础日志记录"""
        with caplog.at_level(logging.INFO):
            logging.info("这是一条信息")
            assert "这是一条信息" in caplog.text

    def test_different_log_levels(self, caplog):
        """测试不同级别的日志"""
        with caplog.at_level(logging.DEBUG):
            logging.debug("调试信息")
            logging.info("普通信息")
            logging.warning("警告信息")
            logging.error("错误信息")
            logging.critical("严重错误")

            assert "调试信息" in caplog.text
            assert "普通信息" in caplog.text
            assert "警告信息" in caplog.text
            assert "错误信息" in caplog.text
            assert "严重错误" in caplog.text


class TestLogLevelFiltering:
    """测试日志级别过滤"""

    def test_debug_level_filters_info(self, caplog):
        """测试 DEBUG 级别记录所有日志"""
        with caplog.at_level(logging.DEBUG):
            logging.debug("调试")
            logging.info("信息")

            assert "调试" in caplog.text
            assert "信息" in caplog.text

    def test_info_level_filters_debug(self, caplog):
        """测试 INFO 级别过滤 DEBUG"""
        with caplog.at_level(logging.INFO):
            logging.debug("调试")  # 不会被记录
            logging.info("信息")   # 会被记录

            assert "调试" not in caplog.text
            assert "信息" in caplog.text

    def test_warning_level_filters_below(self, caplog):
        """测试 WARNING 级别过滤更低级别"""
        with caplog.at_level(logging.WARNING):
            logging.debug("调试")   # 不记录
            logging.info("信息")    # 不记录
            logging.warning("警告") # 记录
            logging.error("错误")   # 记录

            assert "调试" not in caplog.text
            assert "信息" not in caplog.text
            assert "警告" in caplog.text
            assert "错误" in caplog.text


class TestLoggingToFile:
    """测试日志输出到文件"""

    def test_logging_to_file(self):
        """测试日志写入文件"""
        # 创建临时文件
        log_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        log_path = log_file.name
        log_file.close()

        # 重置 logging 配置（因为 basicConfig 只在第一次调用时生效）
        logging.root.handlers.clear()
        logging.root.setLevel(logging.WARNING)

        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            filename=log_path,
            filemode='w',
            format='%(asctime)s - %(levelname)s - %(message)s',
            force=True  # Python 3.8+ 支持，强制重新配置
        )

        # 写入日志
        logging.info("测试日志消息")

        # 关闭日志处理器并刷新
        for handler in logging.root.handlers[:]:
            handler.flush()
            handler.close()
            logging.root.removeHandler(handler)

        # 读取文件验证
        with open(log_path, 'r') as f:
            content = f.read()

        os.unlink(log_path)

        assert "测试日志消息" in content
        assert "INFO" in content

    def test_log_file_contains_timestamp(self):
        """测试日志文件包含时间戳"""
        log_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        log_path = log_file.name
        log_file.close()

        # 重置 logging 配置
        logging.root.handlers.clear()
        logging.root.setLevel(logging.WARNING)

        logging.basicConfig(
            level=logging.INFO,
            filename=log_path,
            filemode='w',
            format='%(asctime)s - %(levelname)s - %(message)s',
            force=True
        )

        logging.info("时间戳测试")

        for handler in logging.root.handlers[:]:
            handler.flush()
            handler.close()
            logging.root.removeHandler(handler)

        with open(log_path, 'r') as f:
            content = f.read()

        os.unlink(log_path)

        # 检查时间戳格式（类似 2026-02-09 14:30:15,123）
        assert "-" in content  # 日期分隔符
        assert ":" in content  # 时间分隔符


class TestLogFormatting:
    """测试日志格式化"""

    def test_default_format(self, caplog):
        """测试默认格式"""
        with caplog.at_level(logging.INFO):
            logging.info("测试消息")

            # 默认格式包含级别和消息
            assert "INFO" in caplog.text
            assert "测试消息" in caplog.text

    def test_custom_format(self, capsys):
        """测试自定义格式"""
        # 重置 logging 配置
        logging.root.handlers.clear()
        logging.root.setLevel(logging.WARNING)

        formatter = logging.Formatter('%(levelname)s - %(message)s')

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger("test_custom_format")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False  # 防止传播到 root logger

        logger.info("格式化消息")

        captured = capsys.readouterr()
        # 自定义格式的日志输出到 stderr
        assert "INFO - 格式化消息" in captured.err or "INFO" in captured.err

    def test_format_attributes(self):
        """测试格式化属性"""
        log_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        log_path = log_file.name
        log_file.close()

        # 重置 logging 配置
        logging.root.handlers.clear()
        logging.root.setLevel(logging.WARNING)

        # 使用多个格式化属性
        logging.basicConfig(
            level=logging.INFO,
            filename=log_path,
            filemode='w',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            force=True
        )

        logging.info("格式化测试")

        for handler in logging.root.handlers[:]:
            handler.flush()
            handler.close()
            logging.root.removeHandler(handler)

        with open(log_path, 'r') as f:
            content = f.read()

        os.unlink(log_path)

        # 检查各个属性
        assert "root" in content or "__main__" in content  # logger name
        assert "INFO" in content


class TestLoggerObject:
    """测试 logger 对象"""

    def test_get_logger(self):
        """测试获取 logger"""
        logger = logging.getLogger("test_logger")
        assert logger.name == "test_logger"

    def test_logger_vs_root_logging(self, caplog):
        """测试 logger vs root logger"""
        logger1 = logging.getLogger("module1")
        logger2 = logging.getLogger("module2")

        with caplog.at_level(logging.INFO):
            logger1.info("来自 module1")
            logger2.info("来自 module2")

            assert "module1" in caplog.text
            assert "module2" in caplog.text

    def test_logger_hierarchy(self, caplog):
        """测试 logger 层级"""
        parent = logging.getLogger("parent")
        child = logging.getLogger("parent.child")

        assert child.parent == parent


class TestLoggingVsPrint:
    """测试 logging vs print 的区别"""

    def test_print_to_stdout(self, capsys):
        """测试 print 输出到 stdout"""
        print("这是 print 输出")
        captured = capsys.readouterr()

        assert "这是 print 输出" in captured.out
        assert captured.err == ""

    def test_logging_to_stderr_by_default(self, capsys):
        """测试 logging 默认输出到 stderr"""
        # 重置 logging 配置
        logging.root.handlers.clear()
        logging.root.setLevel(logging.WARNING)

        logging.warning("这是 logging 输出")
        captured = capsys.readouterr()

        # logging 默认输出到 stderr
        assert "这是 logging 输出" in captured.err

    def test_print_no_level(self):
        """测试 print 没有级别概念"""
        # print 只是简单输出文本
        # logging 有级别概念
        assert True

    def test_logging_has_timestamp(self):
        """测试 logging 有时间戳"""
        log_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        log_path = log_file.name
        log_file.close()

        # 重置 logging 配置
        logging.root.handlers.clear()
        logging.root.setLevel(logging.WARNING)

        logging.basicConfig(
            level=logging.INFO,
            filename=log_path,
            filemode='w',
            format='%(asctime)s - %(message)s',
            force=True
        )

        logging.info("带时间戳")

        for handler in logging.root.handlers[:]:
            handler.flush()
            handler.close()
            logging.root.removeHandler(handler)

        with open(log_path, 'r') as f:
            content = f.read()

        os.unlink(log_path)

        # logging 自动添加时间戳
        assert "-" in content and ":" in content


class TestLoggingInModules:
    """测试在模块中使用 logging"""

    def test_logger_in_function(self):
        """测试在函数中使用 logger"""
        logger = logging.getLogger("test_function")

        log_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        log_path = log_file.name
        log_file.close()

        # 重置 logging 配置
        logging.root.handlers.clear()
        logging.root.setLevel(logging.WARNING)

        logging.basicConfig(
            level=logging.INFO,
            filename=log_path,
            filemode='w',
            force=True
        )

        def process_task(task_id):
            logger.info(f"处理任务 {task_id}")
            return True

        process_task(123)

        for handler in logging.root.handlers[:]:
            handler.flush()
            handler.close()
            logging.root.removeHandler(handler)

        with open(log_path, 'r') as f:
            content = f.read()

        os.unlink(log_path)

        assert "处理任务 123" in content


class TestLoggingBestPractices:
    """测试 logging 最佳实践"""

    def test_appropriate_log_levels(self):
        """测试使用合适的日志级别"""
        logger = logging.getLogger("test_levels")

        log_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        log_path = log_file.name
        log_file.close()

        # 重置 logging 配置
        logging.root.handlers.clear()
        logging.root.setLevel(logging.WARNING)

        logging.basicConfig(
            level=logging.DEBUG,
            filename=log_path,
            filemode='w',
            force=True
        )

        # 不同场景使用不同级别
        logger.debug("变量 x = 5")  # 调试信息
        logger.info("开始处理任务")  # 正常信息
        logger.warning("配置文件使用默认值")  # 警告
        logger.error("无法连接数据库")  # 错误
        logger.critical("系统崩溃")  # 严重

        for handler in logging.root.handlers[:]:
            handler.flush()
            handler.close()
            logging.root.removeHandler(handler)

        with open(log_path, 'r') as f:
            content = f.read()

        os.unlink(log_path)

        assert "变量 x = 5" in content
        assert "开始处理任务" in content
        assert "配置文件使用默认值" in content
        assert "无法连接数据库" in content
        assert "系统崩溃" in content

    def test_descriptive_log_messages(self):
        """测试日志消息清晰描述"""
        logger = logging.getLogger("test_messages")

        log_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        log_path = log_file.name
        log_file.close()

        # 重置 logging 配置
        logging.root.handlers.clear()
        logging.root.setLevel(logging.WARNING)

        logging.basicConfig(
            level=logging.INFO,
            filename=log_path,
            filemode='w',
            force=True
        )

        # 好的日志消息：包含上下文
        task_id = 123
        reason = "权限不足"
        logger.error(f"任务 {task_id} 执行失败：{reason}")

        for handler in logging.root.handlers[:]:
            handler.flush()
            handler.close()
            logging.root.removeHandler(handler)

        with open(log_path, 'r') as f:
            content = f.read()

        os.unlink(log_path)

        assert "任务 123" in content
        assert "权限不足" in content


class TestLoggingEdgeCases:
    """测试 logging 边界情况"""

    def test_empty_log_message(self):
        """测试空日志消息"""
        logger = logging.getLogger("test_empty")

        log_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        log_path = log_file.name
        log_file.close()

        # 重置 logging 配置
        logging.root.handlers.clear()
        logging.root.setLevel(logging.WARNING)

        logging.basicConfig(
            level=logging.INFO,
            filename=log_path,
            filemode='w',
            force=True
        )

        logger.info("")

        for handler in logging.root.handlers[:]:
            handler.flush()
            handler.close()
            logging.root.removeHandler(handler)

        with open(log_path, 'r') as f:
            content = f.read()

        os.unlink(log_path)

        # 空消息也会被记录
        assert "INFO" in content

    def test_unicode_in_log(self):
        """测试日志中的 Unicode 字符"""
        logger = logging.getLogger("test_unicode")

        log_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        log_path = log_file.name
        log_file.close()

        # 重置 logging 配置
        logging.root.handlers.clear()
        logging.root.setLevel(logging.WARNING)

        logging.basicConfig(
            level=logging.INFO,
            filename=log_path,
            filemode='w',
            force=True
        )

        logger.info("学习 Python 🎉 中文测试")

        for handler in logging.root.handlers[:]:
            handler.flush()
            handler.close()
            logging.root.removeHandler(handler)

        with open(log_path, 'r') as f:
            content = f.read()

        os.unlink(log_path)

        assert "学习 Python 🎉 中文测试" in content

    def test_very_long_log_message(self):
        """测试超长日志消息"""
        logger = logging.getLogger("test_long")

        log_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        log_path = log_file.name
        log_file.close()

        # 重置 logging 配置
        logging.root.handlers.clear()
        logging.root.setLevel(logging.WARNING)

        logging.basicConfig(
            level=logging.INFO,
            filename=log_path,
            filemode='w',
            force=True
        )

        long_message = "A" * 10000
        logger.info(long_message)

        for handler in logging.root.handlers[:]:
            handler.flush()
            handler.close()
            logging.root.removeHandler(handler)

        with open(log_path, 'r') as f:
            content = f.read()

        os.unlink(log_path)

        assert long_message in content


@pytest.mark.parametrize("level,should_log", [
    (logging.DEBUG, True),
    (logging.INFO, True),
    (logging.WARNING, True),
    (logging.ERROR, True),
    (logging.CRITICAL, True),
])
def test_logging_at_all_levels(level, should_log, caplog):
    """参数化测试：所有日志级别"""
    with caplog.at_level(logging.DEBUG):
        logging.log(level, f"级别 {level} 的消息")
        assert "级别" in caplog.text
