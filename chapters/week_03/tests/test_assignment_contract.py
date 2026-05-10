"""Week 03 assignment contract: solution.py exposes the converter API."""

import sys
from pathlib import Path

STARTER = Path(__file__).resolve().parents[1] / "starter_code"
sys.path.insert(0, str(STARTER))
sys.modules.pop("solution", None)

import solution


def test_converter_solution_exports_required_functions():
    assert abs(solution.km_to_miles(10) - 6.21371) < 0.0001
    assert abs(solution.miles_to_km(6.21371) - 10) < 0.0001
    assert abs(solution.kg_to_pounds(5) - 11.0231) < 0.0001
    assert abs(solution.pounds_to_kg(11.0231) - 5) < 0.0001
    assert solution.celsius_to_fahrenheit(0) == 32
    assert solution.fahrenheit_to_celsius(32) == 0
    assert solution.rectangle_area(3, 4) == 12
    assert solution.rectangle_perimeter(3, 4) == 14


def test_scope_analysis_answer_exists():
    answer = STARTER / "scope_analysis.txt"
    text = answer.read_text(encoding="utf-8")
    assert "局部变量" in text
    assert "全局变量" in text
