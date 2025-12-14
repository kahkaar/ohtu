import types

import pytest

from frontend import create_app
from frontend.__main__ import _pick_port


def test_create_app_registers_blueprint():
    app = create_app()
    rules = {r.rule for r in app.url_map.iter_rules()}
    assert "/" in rules
    assert "/play" in rules


def test_pick_port_skips_used(monkeypatch):
    # Deterministic: make first port unavailable and second available.
    calls = []

    def fake_is_port_free(host: str, port: int) -> bool:
        calls.append((host, port))
        return port != 5000

    import frontend.__main__ as m

    monkeypatch.setattr(m, "_is_port_free", fake_is_port_free)
    assert _pick_port(host="127.0.0.1", start_port=5000, max_tries=3) == 5001
    assert calls[0] == ("127.0.0.1", 5000)


def test_pick_port_raises_when_no_free_ports(monkeypatch):
    import frontend.__main__ as m

    monkeypatch.setattr(m, "_is_port_free", lambda host, port: False)
    with pytest.raises(RuntimeError):
        _pick_port(host="127.0.0.1", start_port=5000, max_tries=2)
