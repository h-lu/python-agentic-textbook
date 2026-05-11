import importlib.util
from pathlib import Path

def load(name):
    path = Path(__file__).resolve().parents[1] / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"week08_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def test_date_validation_and_menu_choice():
    ih = load("input_handler")
    assert ih.is_valid_date("2026-05-11")
    assert not ih.is_valid_date("2026-99-99")
    assert ih.get_menu_choice(" 2 ", {"1", "2"}) == "2"
    assert ih.get_menu_choice("9", {"1", "2"}) is None
