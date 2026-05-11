import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from text_utils import contains_keyword, extract_tags


def test_contains_keyword_case_insensitive():
    assert contains_keyword("PyHelper Search", "pyhelper")


def test_extract_tags():
    assert extract_tags("学习 #regex 和 #搜索") == ["regex", "搜索"]
