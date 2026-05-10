"""Week 07 assignment contract: validate the student-facing module artifacts."""

import subprocess
import sys
from pathlib import Path

STARTER = Path(__file__).resolve().parents[1] / "starter_code"
sys.path.insert(0, str(STARTER))


def test_standard_library_practice_module():
    import practice1_standard_library as practice

    assert practice.random_encouragement(["A"]) == "A"
    assert len(practice.today_iso()) == 10
    assert practice.project_file("data.txt").name == "data.txt"


def test_calculator_import_is_quiet_and_functions_work(capsys):
    import calculator

    captured = capsys.readouterr()
    assert captured.out == ""
    assert calculator.add(2, 3) == 5
    assert calculator.divide(8, 2) == 4
    assert calculator.divide(5, 0) is None


def test_calculator_runs_guarded_demo():
    script = STARTER / "calculator.py"
    result = subprocess.run([sys.executable, str(script)], text=True, capture_output=True, timeout=5)
    assert result.returncode == 0, result.stderr
    assert "所有测试通过" in result.stdout


def test_todo_app_modules_roundtrip(tmp_path):
    from todo_app.storage import load_todos, save_todos
    from todo_app.todo_manager import add_todo, complete_todo

    todos = []
    assert add_todo(todos, "写作业") is True
    assert add_todo(todos, "   ") is False
    assert complete_todo(todos, 1) is True

    path = tmp_path / "todos.txt"
    save_todos(todos, path)
    assert load_todos(path) == [{"title": "写作业", "done": True}]


def test_grades_package_exports_calculators():
    from grades import average, total

    assert total([80, 90, 100]) == 270
    assert average([80, 90, 100]) == 90
