from typing import cast

import pytest

from kps_logic import KPSAdvancedAILogic, KPSAILogic, KPSLogic
from user_io import UserIO


class FakeIO(UserIO):
    def __init__(self, inputs):
        self._inputs = list(inputs)
        self.shown = []

    def get(self, prompt: object = "", /) -> str:
        if not self._inputs:
            raise AssertionError("No more inputs")
        return self._inputs.pop(0)

    def show(self, *values):
        self.shown.append(" ".join(str(v) for v in values))


def test_kps_logic_moves_are_valid_and_play_loop_exits():
    io = FakeIO(inputs=["k", "p", "x", "k"])  # second round invalid
    logic = KPSLogic(io)

    assert logic._moves_are_valid("spamk", "p") is True
    assert logic._moves_are_valid("", "p") is False

    logic.play()

    assert any("Kiitos!" in s for s in io.shown)
    assert any("Pelitilanne:" in s for s in io.shown)


def test_kps_logic_stops_when_someone_reaches_five_wins():
    # 5 rounds where p1 wins (k vs s), then extra inputs that should not be consumed.
    io = FakeIO(inputs=["k", "s"] * 5 + ["k", "s"])
    logic = KPSLogic(io)

    logic.play()

    assert any("5 voittoa" in s for s in io.shown)
    assert len(io._inputs) == 2


def test_kps_ai_logic_player2_move_and_guard():
    io = FakeIO(inputs=[])
    logic = KPSAILogic(io)

    move = logic.player2_move()
    assert move in {"k", "p", "s"}
    assert any("Tietokone valitsi" in s for s in io.shown)

    # Force the negative branch (guard) even though it's not a valid runtime type.
    # pyright: ignore[reportAttributeAccessIssue]
    logic._ai = cast(object, None)
    with pytest.raises(ValueError):
        logic.player2_move()


def test_kps_advanced_ai_logic_memorize_move_calls_ai():
    io = FakeIO(inputs=[])
    logic = KPSAdvancedAILogic(io, memory_size=2)

    called = []

    class DummyAI:
        def aseta_siirto(self, move):
            called.append(move)

    # Inject a dummy AI for unit testing.
    # pyright: ignore[reportAttributeAccessIssue]
    logic._ai = cast(object, DummyAI())
    logic.memorize_move("k")
    assert called == ["k"]
