from pyhelper.cli import format_note, main


def test_format_note_builds_markdown():
    assert format_note("学习 Python", "完成 Week 14") == "# 学习 Python\n\n完成 Week 14"


def test_format_note_rejects_blank_title():
    try:
        format_note("   ")
    except ValueError as exc:
        assert "title" in str(exc)
    else:
        raise AssertionError("blank title should fail")


def test_main_note_command(capsys):
    assert main(["note", "发布准备"]) == 0
    assert "# 发布准备" in capsys.readouterr().out
