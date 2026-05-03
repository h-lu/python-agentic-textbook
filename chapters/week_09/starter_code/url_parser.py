"""Week 09 挑战 1：URL 参数提取器。"""

from urllib.parse import parse_qsl, quote_plus, unquote_plus, urlsplit


def parse_query_params(url):
    """解析 URL 查询参数，返回字典。"""
    query = urlsplit(url).query
    return {key: value for key, value in parse_qsl(query)}


def parse_path_params(url):
    """把 URL 或路径拆成非空路径片段。"""
    path = urlsplit(url).path if "://" in url else url
    return [unquote_plus(part) for part in path.split("/") if part]


def reconstruct_url(base, params):
    """根据基础 URL 和参数字典重建查询 URL。"""
    if not params:
        return base

    query = "&".join(
        f"{quote_plus(str(key))}={quote_plus(str(value))}"
        for key, value in params.items()
    )
    separator = "&" if "?" in base else "?"
    return f"{base}{separator}{query}"
