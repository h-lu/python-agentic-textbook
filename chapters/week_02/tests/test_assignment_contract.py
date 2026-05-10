"""Week 02 assignment contract: the guessing game functions handle real gameplay."""

import sys
from pathlib import Path

STARTER = Path(__file__).resolve().parents[1] / "starter_code"
sys.path.insert(0, str(STARTER))
sys.modules.pop("solution", None)

import solution


def test_get_difficulty_returns_config(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _prompt="": "2")
    assert solution.get_difficulty() == (100, 5)


def test_play_game_gives_hints_and_success(monkeypatch, capsys):
    guesses = iter(["40", "42"])
    monkeypatch.setattr(solution.random, "randint", lambda low, high: 42)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(guesses))

    solution.play_game(max_num=100, max_attempts=5)

    out = capsys.readouterr().out
    assert "太小了" in out
    assert "恭喜" in out
    assert "42" in out
