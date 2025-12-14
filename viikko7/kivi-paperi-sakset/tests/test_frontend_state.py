from frontend.state import GameState


def test_frontend_state_initial_and_reset_scoreboard():
    s = GameState()
    assert s.game is None
    assert s.game_started is False
    assert s.is_human_game is False
    assert "Score:" in s.scoreboard
    assert "Ties:" in s.scoreboard

    s.start_new_game("basic")
    assert s.game_started is True
    assert s.opponent_label == "Basic AI"

    s.reset()
    assert s.game is None
    assert s.pending_p1_move is None
    assert s.awaiting_player == 1


def test_frontend_state_start_new_game_modes_and_scoreboard_updates():
    s = GameState()

    s.start_new_game("human")
    assert s.is_human_game is True
    assert s.opponent_label == "Human (2 players)"
    r = s.game.step("k", "s")
    assert r.valid is True
    assert "Score: 1 - 0" in s.scoreboard

    s.reset()
    s.start_new_game("basic")
    assert s.is_human_game is False
    assert s.opponent_label == "Basic AI"

    s.reset()
    s.start_new_game("advanced")
    assert s.opponent_label == "Improved AI"
