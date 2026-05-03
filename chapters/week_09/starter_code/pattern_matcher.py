"""Week 09 练习 3：正则表达式基础。"""

import re


def find_ip_addresses(text):
    """找出文本中所有形如 xxx.xxx.xxx.xxx 的 IP 地址。"""
    if not text:
        return []
    return re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", text)


def find_emails(text):
    """找出文本中的简化版邮箱地址。"""
    if not text:
        return []
    return re.findall(r"[\w.-]+@[\w.-]+\.\w+", text)


def is_valid_phone(phone):
    """验证中国大陆手机号：1 开头，第二位 3-9，共 11 位。"""
    if not isinstance(phone, str):
        return False
    return re.match(r"^1[3-9]\d{9}$", phone) is not None
