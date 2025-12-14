from flask import Blueprint, redirect, render_template, request, url_for

from .state import state

ui = Blueprint("ui", __name__)


MOVE_NAMES = {"k": "Rock", "p": "Paper", "s": "Scissors"}


def _to_english_message(message: str) -> str:
    normalized = (message or "").strip()
    if normalized == "Virheellinen siirto. Peli päättyi.":
        return "Invalid move. Game over."
    if normalized == "Peli on jo päättynyt. Aloita uusi peli.":
        return "The game has already ended. Start a new game."
    return normalized or "Game over."


@ui.get("/")
def index():
    return render_template(
        "index.html",
        score=state.scoreboard,
        last_moves=state.last_moves,
        message=None,
        game_started=state.game_started,
        opponent_label=state.opponent_label,
        move_names=MOVE_NAMES,
        is_human_game=state.is_human_game,
        awaiting_player=state.awaiting_player,
    )


@ui.post("/play")
def play():
    move = (request.form.get("move") or "").strip().lower()

    if move not in {"k", "p", "s"}:
        message = "Invalid move — game ended. Thanks for playing!"
        state.reset()
        return render_template(
            "index.html",
            score=state.scoreboard,
            last_moves=state.last_moves,
            message=message,
            game_started=state.game_started,
            opponent_label=state.opponent_label,
            move_names=MOVE_NAMES,
            is_human_game=state.is_human_game,
            awaiting_player=state.awaiting_player,
        )

    if state.game is None:
        opponent = request.form.get("opponent") or "advanced"
        state.start_new_game(opponent)

    assert state.game is not None

    result = None
    if state.game is not None and state.is_human_game:
        if state.pending_p1_move is None:
            state.pending_p1_move = move
            state.awaiting_player = 2
            message = "Player 2: choose your move."
            return render_template(
                "index.html",
                score=state.scoreboard,
                last_moves=state.last_moves,
                message=message,
                game_started=state.game_started,
                opponent_label=state.opponent_label,
                move_names=MOVE_NAMES,
                is_human_game=state.is_human_game,
                awaiting_player=state.awaiting_player,
            )

        p1_move = state.pending_p1_move
        state.pending_p1_move = None
        state.awaiting_player = 1
        result = state.game.step(p1_move, move)
    else:
        result = state.game.step(move)

    if result.ended and not result.valid:
        message = _to_english_message(result.message)
        state.reset()
        return render_template(
            "index.html",
            score=state.scoreboard,
            last_moves=state.last_moves,
            message=message,
            game_started=state.game_started,
            opponent_label=state.opponent_label,
            move_names=MOVE_NAMES,
            is_human_game=state.is_human_game,
            awaiting_player=state.awaiting_player,
        )

    if result.ended:
        final_score = state.scoreboard
        final_moves = [(result.p1_move or move, result.p2_move or "")]
        if state.is_human_game:
            message = result.message
        else:
            if state.game is not None and state.game.p1_points >= 5:
                message = "Match over. You reached 5 wins."
            else:
                message = "Match over. The opponent reached 5 wins."

        state.reset()
        return render_template(
            "index.html",
            score=final_score,
            last_moves=final_moves,
            message=message,
            game_started=False,
            opponent_label=None,
            move_names=MOVE_NAMES,
            is_human_game=False,
            awaiting_player=1,
        )

    state.last_moves = [(result.p1_move or move, result.p2_move or "")]

    return redirect(url_for("ui.index"))
