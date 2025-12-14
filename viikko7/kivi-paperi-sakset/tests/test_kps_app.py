import pytest

from kps_app import KPSApp
from kps_logic import KPSAdvancedAILogic, KPSAILogic, KPSLogic
from user_io import UserIO


class FakeIO(UserIO):
    def __init__(self, inputs):
        self._inputs = list(inputs)
        self.shown = []

    def get(self, prompt: object = "", /):
        if not self._inputs:
            raise AssertionError("No more inputs")
        return self._inputs.pop(0)

    def show(self, *values):
        self.shown.append(" ".join(str(v) for v in values))


def test_kps_app_display_and_logic_factory():
    io = FakeIO(inputs=[])
    app = KPSApp(io)

    app._display_options()
    assert any("Valitse pelataanko" in s for s in io.shown)

    assert isinstance(app.logic_factory("a"), KPSLogic)
    assert isinstance(app.logic_factory("b"), KPSAILogic)
    assert isinstance(app.logic_factory("c"), KPSAdvancedAILogic)

    with pytest.raises(ValueError):
        app.logic_factory("x")


def test_kps_app_run_happy_path_exits_on_invalid_option():
    # Pick option a, then provide invalid moves to end the round, then exit menu.
    io = FakeIO(inputs=["a", "x", "k", "x"])
    app = KPSApp(io)

    app.run()

    assert any("Peli loppuu" in s for s in io.shown)
    assert any("Kiitos!" in s for s in io.shown)
