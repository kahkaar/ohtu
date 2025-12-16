from frontend.app import create_app
from frontend.routes import _to_english_message
from frontend.state import state


def test_to_english_message_variants():
    assert _to_english_message(
        "Virheellinen siirto. Peli päättyi.") == "Invalid move. Game over."
    assert (
        _to_english_message("Peli on jo päättynyt. Aloita uusi peli.")
        == "The game has already ended. Start a new game."
    )
    assert _to_english_message(" ") == "Game over."
    assert _to_english_message("Hello") == "Hello"


def test_index_route_renders():
    app = create_app()
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200
    assert b"Rock" in r.data


def test_play_invalid_move_renders_message_and_resets():
    app = create_app()
    client = app.test_client()

    state.start_new_game("human")
    r = client.post("/play", data={"move": "x"})
    assert r.status_code == 200
    assert b"Invalid move" in r.data
    assert state.game is None


def test_play_advanced_default_redirects_and_sets_last_moves():
    app = create_app()
    client = app.test_client()

    r = client.post("/play", data={"move": "k", "opponent": "advanced"})
    assert r.status_code == 302

    r2 = client.get("/")
    assert r2.status_code == 200
    assert state.last_moves


def test_play_human_two_step_flow_and_opponent_locked():
    app = create_app()
    client = app.test_client()

    r1 = client.post("/play", data={"move": "k", "opponent": "human"})
    assert r1.status_code == 200
    assert b"Player 2: choose your move." in r1.data
    assert state.pending_p1_move == "k"
    assert state.awaiting_player == 2

    # Attempt to switch opponent mid-game should be ignored.
    r2 = client.post("/play", data={"move": "p", "opponent": "basic"})
    assert r2.status_code == 302
    assert state.opponent_label == "Human (2 players)"

    r3 = client.get("/")
    assert b"Last round" in r3.data
    assert state.awaiting_player == 1


def test_play_when_game_already_ended_renders_reset_message():
    app = create_app()
    client = app.test_client()

    state.start_new_game("basic")
    assert state.game is not None
    state.game._ended = True

    r = client.post("/play", data={"move": "k"})
    assert r.status_code == 200
    assert b"already ended" in r.data
    assert state.game is None


def test_play_human_game_ends_at_three_wins_and_resets_state():
    app = create_app()
    client = app.test_client()

    state.start_new_game("human")

    # First two rounds should redirect back to index.
    for _ in range(2):
        r1 = client.post("/play", data={"move": "k", "opponent": "human"})
        assert r1.status_code == 200
        r2 = client.post("/play", data={"move": "s", "opponent": "human"})
        assert r2.status_code == 302

    # Third win ends the match and renders the final screen directly.
    r1 = client.post("/play", data={"move": "k", "opponent": "human"})
    assert r1.status_code == 200
    r2 = client.post("/play", data={"move": "s", "opponent": "human"})
    assert r2.status_code == 200
    assert b"Match over" in r2.data
    assert b"Score: 3 - 0" in r2.data
    assert state.game is None


def test_play_ai_match_end_message_when_you_reach_three_wins():
    app = create_app()
    client = app.test_client()

    state.start_new_game("basic")
    assert state.game is not None

    class AlwaysScissors:
        def anna_siirto(self):
            return "s"

    state.game._ai = AlwaysScissors()

    # Preload the score to 2-0, then win once via /play.
    for _ in range(2):
        state.game._ref.kirjaa_siirto("k", "s")

    r = client.post("/play", data={"move": "k"})
    assert r.status_code == 200
    assert b"You reached 3 wins" in r.data
    assert b"Score: 3 - 0" in r.data
    assert state.game is None


def test_play_ai_match_end_message_when_opponent_reaches_three_wins():
    app = create_app()
    client = app.test_client()

    state.start_new_game("basic")
    assert state.game is not None

    class AlwaysPaper:
        def anna_siirto(self):
            return "p"

    state.game._ai = AlwaysPaper()

    # Preload the score to 0-2, then lose once via /play.
    for _ in range(2):
        state.game._ref.kirjaa_siirto("k", "p")

    r = client.post("/play", data={"move": "k"})
    assert r.status_code == 200
    assert b"opponent reached 3 wins" in r.data
    assert b"Score: 0 - 3" in r.data
    assert state.game is None
