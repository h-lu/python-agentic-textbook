"""Week 07 练习 1：使用标准库模块。"""

from datetime import date
from pathlib import Path
import random


def random_encouragement(options=None):
    """从候选鼓励语中随机返回一句。"""
    choices = options or ["继续加油", "再试一次", "你已经在进步"]
    return random.choice(choices)


def today_iso():
    """返回今天的 ISO 日期字符串。"""
    return date.today().isoformat()


def project_file(name):
    """用 pathlib 生成当前项目下的文件路径。"""
    return Path(name)


if __name__ == "__main__":
    print(today_iso())
    print(random_encouragement())
