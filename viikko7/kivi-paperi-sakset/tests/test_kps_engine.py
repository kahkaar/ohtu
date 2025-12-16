import pytest

from kps_engine import Game, GameType
from tekoaly_parannettu import TekoalyParannettu


def test_game_normalize_move_and_invalid_ends_game():
    g = Game(GameType.HUMAN)

    assert g.ended is False
    assert isinstance(g.scoreboard, str)
    assert g.last_round is None

    # _normalize_move behavior (tested indirectly through step):
    r = g.step("x", "k")
    assert r.ended is True
    assert r.valid is False

    assert g.ended is True
    assert g.last_round is r

    # Once ended, further step returns already-ended message.
    r2 = g.step("k", "k")
    assert r2.ended is True
    assert r2.valid is False


def test_game_human_valid_round_and_invalid_p2():
    g = Game(GameType.HUMAN)

    ok = g.step("k", "s")
    assert ok.valid is True
    assert ok.ended is False
    assert ok.p1_move == "k"
    assert ok.p2_move == "s"

    # Allow spam input: last char is used.
    ok2 = g.step("rockk", "papers")
    assert ok2.valid is True
    assert ok2.p1_move == "k"
    assert ok2.p2_move == "s"

    g2 = Game(GameType.HUMAN)
    bad = g2.step("k", "")
    assert bad.ended is True
    assert bad.valid is False


def test_game_ai_and_advanced_ai_paths():
    g = Game(GameType.AI)
    r = g.step("k")
    assert r.valid is True
    assert r.p2_move in {"k", "p", "s"}

    g2 = Game(GameType.ADVANCED_AI, memory_size=3)
    r2 = g2.step("k")
    assert r2.valid is True

    # Advanced AI should memorize p1 move.
    assert isinstance(g2._ai, TekoalyParannettu)
    assert g2._ai._vapaa_muisti_indeksi == 1
    assert g2._ai._muisti[0] == "k"


def test_game_ends_when_someone_reaches_three_wins():
    g = Game(GameType.HUMAN)

    last = None
    for _ in range(3):
        last = g.step("k", "s")  # p1 wins each round

    assert last is not None
    assert last.valid is True
    assert last.ended is True
    assert g.ended is True
    assert g.p1_points == 3
    assert g.p2_points == 0

    after = g.step("k", "k")
    assert after.ended is True
    assert after.valid is False


def test_game_ends_when_player2_reaches_three_wins():
    g = Game(GameType.HUMAN)

    last = None
    for _ in range(3):
        last = g.step("k", "p")  # p2 wins each round

    assert last is not None
    assert last.valid is True
    assert last.ended is True
    assert g.ended is True
    assert g.p1_points == 0
    assert g.p2_points == 3


def test_game_ai_object_missing_guard():
    g = Game(GameType.AI)
    g._ai = None
    with pytest.raises(ValueError):
        g.step("k")

    g2 = Game(GameType.ADVANCED_AI)
    g2._ai = None
    with pytest.raises(ValueError):
        g2.step("k")


def test_game_advanced_ai_memorize_guard_when_ai_disappears_mid_step():
    g = Game(GameType.ADVANCED_AI)

    class FlakyAI:
        def __init__(self, game: Game):
            self._game = game

        def anna_siirto(self):
            # Choose a valid move, but then drop the AI reference so the
            # memorize block hits its guard.
            self._game._ai = None
            return "k"

    g._ai = FlakyAI(g)

    with pytest.raises(ValueError):
        g.step("k")
