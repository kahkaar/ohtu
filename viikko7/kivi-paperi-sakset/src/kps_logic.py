from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from tuomari import Tuomari
from user_io import UserIO


class KPSLogic():
    """Class for basic game logic."""

    _WIN_TARGET = 5

    def __init__(self, io: UserIO) -> None:
        self._ref = Tuomari()
        self._io = io
        self._legal_moves = {"k", "p", "s"}

    def _moves_are_valid(self, *moves: str) -> bool:
        """Check if all provided moves are valid."""
        for move in moves:
            # Only check the last character to allow user to spam inputs
            if not move or (move[-1] not in self._legal_moves):
                return False
        return True

    def player1_move(self) -> str:
        """
        Get the move for the first player.
        Default implementation gets input from user.
        """
        return self._io.get("Ensimmäisen pelaajan siirto: ")

    def player2_move(self) -> str:
        """
        Get the move for the second player.
        Default implementation gets input from user.
        """
        return self._io.get("Toisen pelaajan siirto: ")

    def memorize_move(self, _move: str) -> None:
        """
        Memorize the move of the first player.
        Default implementation does nothing.
        """
        return None

    def play(self):
        """Logic for playing the game."""
        while True:
            p1_move = self.player1_move()
            p2_move = self.player2_move()

            if not self._moves_are_valid(p1_move, p2_move):
                break

            self._ref.kirjaa_siirto(p1_move, p2_move)
            self._io.show(self._ref)

            if (
                self._ref.ekan_pisteet >= self._WIN_TARGET
                or self._ref.tokan_pisteet >= self._WIN_TARGET
            ):
                self._io.show(
                    f"Peli päättyi: {self._WIN_TARGET} voittoa täynnä."
                )
                break

            # For AI logic. Memorize the first player's move
            self.memorize_move(p1_move)

        self._io.show("Kiitos!")
        self._io.show(self._ref)


class KPSAILogic(KPSLogic):
    """Class for AI game logic. Inherits from `KPSLogic`."""

    def __init__(self, io: UserIO) -> None:
        super().__init__(io)
        self._ai = Tekoaly()

    def player2_move(self) -> str:
        """Get the move for the AI player."""
        if not self._ai:
            raise ValueError("AI object is not defined.")

        move = self._ai.anna_siirto()
        self._io.show(f"Tietokone valitsi: {move}")
        return move


class KPSAdvancedAILogic(KPSAILogic):
    """
    Class for advanced AI game logic.
    Inherits from `KPSAILogic`.
    """

    def __init__(self, io: UserIO, memory_size: int = 10) -> None:
        super().__init__(io)
        self._ai = TekoalyParannettu(memory_size)

    def memorize_move(self, move: str) -> None:
        """Memorize the move for the advanced AI."""
        self._ai.aseta_siirto(move)
