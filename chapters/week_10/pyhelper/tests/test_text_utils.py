import importlib.util
from pathlib import Path

def load_text_utils():
    path = Path(__file__).resolve().parents[1] / "text_utils.py"
    spec = importlib.util.spec_from_file_location("week09_text_utils", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def test_keyword_tags_and_date_range():
    t = load_text_utils()
    assert t.contains_keyword("学习 Python", "python")
    assert t.extract_tags("复习 #Python #函数") == ["Python", "函数"]
    assert t.in_date_range("2026-05-11", "2026-05-01", "2026-05-31")
