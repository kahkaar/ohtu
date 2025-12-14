import errno
import types

import pytest

import frontend.__main__ as m


def test_is_port_free_returns_true_when_bind_succeeds(monkeypatch):
    class FakeSock:
        def bind(self, addr):
            return None

        def close(self):
            return None

    monkeypatch.setattr(m.socket, "socket", lambda *args, **kwargs: FakeSock())
    assert m._is_port_free("127.0.0.1", 5000) is True


def test_is_port_free_returns_false_on_eaddrinuse(monkeypatch):
    class FakeSock:
        def bind(self, addr):
            raise OSError(errno.EADDRINUSE, "in use")

        def close(self):
            return None

    monkeypatch.setattr(m.socket, "socket", lambda *args, **kwargs: FakeSock())
    assert m._is_port_free("127.0.0.1", 5000) is False


def test_is_port_free_raises_on_unexpected_oserror(monkeypatch):
    class FakeSock:
        def bind(self, addr):
            raise OSError(errno.EPERM, "nope")

        def close(self):
            return None

    monkeypatch.setattr(m.socket, "socket", lambda *args, **kwargs: FakeSock())
    with pytest.raises(OSError):
        m._is_port_free("127.0.0.1", 5000)


def test_main_calls_app_run_with_selected_port(monkeypatch, capsys):
    run_args = {}

    class FakeApp:
        def run(self, **kwargs):
            run_args.update(kwargs)

    monkeypatch.setattr(m, "create_app", lambda: FakeApp())
    monkeypatch.setattr(m, "_pick_port", lambda **kwargs: 5001)

    m.main()

    out = capsys.readouterr().out
    assert "switching to 5001" in out
    assert "http://127.0.0.1:5001" in out

    assert run_args["debug"] is True
    assert run_args["host"] == "127.0.0.1"
    assert run_args["port"] == 5001
    assert run_args["use_reloader"] is False
