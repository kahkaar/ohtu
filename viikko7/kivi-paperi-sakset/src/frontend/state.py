from __future__ import annotations

from typing import Optional

from kps_engine import Game, GameType
from tuomari import Tuomari


class GameState:
    def __init__(self) -> None:
        self.game: Optional[Game] = None
        self.game_type: Optional[GameType] = None
        self.opponent_label: Optional[str] = None
        self.last_moves: list[tuple[str, str]] = []
        self.pending_p1_move: Optional[str] = None
        self.awaiting_player: int = 1

        self.reset()

    def reset(self) -> None:
        self.game: Optional[Game] = None
        self.game_type: Optional[GameType] = None
        self.opponent_label: Optional[str] = None
        self.last_moves: list[tuple[str, str]] = []
        self.pending_p1_move: Optional[str] = None
        self.awaiting_player: int = 1

    @property
    def scoreboard(self) -> str:
        if self.game is None:
            ref = Tuomari()
            return f"Score: {ref.ekan_pisteet} - {ref.tokan_pisteet}\nTies: {ref.tasapelit}"
        return (
            f"Score: {self.game.p1_points} - {self.game.p2_points}\n"
            f"Ties: {self.game.ties}"
        )

    @property
    def game_started(self) -> bool:
        return self.game is not None

    @property
    def is_human_game(self) -> bool:
        return self.game_type == GameType.HUMAN

    def start_new_game(self, opponent: str) -> None:
        normalized = (opponent or "advanced").strip().lower()
        if normalized == "human":
            self.game_type = GameType.HUMAN
            self.game = Game(GameType.HUMAN)
            self.opponent_label = "Human (2 players)"
        elif normalized == "basic":
            self.game_type = GameType.AI
            self.game = Game(GameType.AI)
            self.opponent_label = "Basic AI"
        else:
            self.game_type = GameType.ADVANCED_AI
            self.game = Game(GameType.ADVANCED_AI, memory_size=10)
            self.opponent_label = "Improved AI"

        self.pending_p1_move = None
        self.awaiting_player = 1


state = GameState()
