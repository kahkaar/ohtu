import builtins

from user_io import UserIO


def test_user_io_get_strips_and_lowercases(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda prompt="": "  K  ")
    io = UserIO()
    assert io.get("prompt") == "k"


def test_user_io_show_prints(capsys):
    io = UserIO()
    io.show("hello", 123)
    out = capsys.readouterr().out
    assert out.strip() == "hello 123"
