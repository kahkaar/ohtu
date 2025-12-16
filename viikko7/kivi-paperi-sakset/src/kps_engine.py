from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from tuomari import Tuomari


class GameType(str, Enum):
    HUMAN = "a"
    AI = "b"
    ADVANCED_AI = "c"


@dataclass(frozen=True)
class RoundResult:
    valid: bool
    ended: bool
    message: str
    p1_move: Optional[str] = None
    p2_move: Optional[str] = None
    scoreboard: str = ""


class Game:
    _WIN_TARGET = 3

    def __init__(self, game_type: GameType, memory_size: int = 10) -> None:
        self._ref = Tuomari()
        self._game_type = game_type
        self._legal_moves = {"k", "p", "s"}

        self._ai: Optional[object]
        if game_type == GameType.AI:
            self._ai = Tekoaly()
        elif game_type == GameType.ADVANCED_AI:
            self._ai = TekoalyParannettu(memory_size)
        else:
            self._ai = None

        self._ended = False
        self._last_round: Optional[RoundResult] = None

    @property
    def ended(self) -> bool:
        return self._ended

    @property
    def scoreboard(self) -> str:
        return str(self._ref)

    @property
    def p1_points(self) -> int:
        return int(getattr(self._ref, "ekan_pisteet"))

    @property
    def p2_points(self) -> int:
        return int(getattr(self._ref, "tokan_pisteet"))

    @property
    def ties(self) -> int:
        return int(getattr(self._ref, "tasapelit"))

    @property
    def last_round(self) -> Optional[RoundResult]:
        return self._last_round

    def _normalize_move(self, move: Optional[str]) -> Optional[str]:
        if not move:
            return None
        normalized = move[-1].lower()
        if normalized not in self._legal_moves:
            return None
        return normalized

    def step(self, p1_move: str, p2_move: Optional[str] = None) -> RoundResult:
        if self._ended:
            return RoundResult(
                valid=False,
                ended=True,
                message="Peli on jo päättynyt. Aloita uusi peli.",
                scoreboard=self.scoreboard,
            )

        p1 = self._normalize_move(p1_move)
        if p1 is None:
            self._ended = True
            self._last_round = RoundResult(
                valid=False,
                ended=True,
                message="Virheellinen siirto. Peli päättyi.",
                scoreboard=self.scoreboard,
            )
            return self._last_round

        if self._game_type in (GameType.AI, GameType.ADVANCED_AI):
            # AI chooses its move
            ai = self._ai
            if ai is None:
                raise ValueError("AI object is not defined.")
            p2 = getattr(ai, "anna_siirto")()
        else:
            p2 = self._normalize_move(p2_move)
            if p2 is None:
                self._ended = True
                self._last_round = RoundResult(
                    valid=False,
                    ended=True,
                    message="Virheellinen siirto. Peli päättyi.",
                    scoreboard=self.scoreboard,
                )
                return self._last_round

        self._ref.kirjaa_siirto(p1, p2)

        if self.p1_points >= self._WIN_TARGET:
            self._ended = True
            self._last_round = RoundResult(
                valid=True,
                ended=True,
                message=f"Match over. Player 1 reached {self._WIN_TARGET} wins.",
                p1_move=p1,
                p2_move=p2,
                scoreboard=self.scoreboard,
            )
            return self._last_round

        if self.p2_points >= self._WIN_TARGET:
            self._ended = True
            self._last_round = RoundResult(
                valid=True,
                ended=True,
                message=f"Match over. Player 2 reached {self._WIN_TARGET} wins.",
                p1_move=p1,
                p2_move=p2,
                scoreboard=self.scoreboard,
            )
            return self._last_round

        if self._game_type == GameType.ADVANCED_AI:
            ai2 = self._ai
            if ai2 is None:
                raise ValueError("AI object is not defined.")
            getattr(ai2, "aseta_siirto")(p1)

        self._last_round = RoundResult(
            valid=True,
            ended=False,
            message="OK",
            p1_move=p1,
            p2_move=p2,
            scoreboard=self.scoreboard,
        )
        return self._last_round
