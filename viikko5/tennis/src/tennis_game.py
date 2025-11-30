# Constants for tennis scoring.
# Defined at module level, since they are the rules of the game and not specific to any instance.
_ADVANTAGE = 1
_WIN_THRESHOLD = 4
_WIN_THRESHOLD_MARGIN = 2
_DEUCE_THRESHOLD = 3
_SCORE = {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}


class TennisGame:
    def __init__(self, player1, player2):
        self._p1 = player1
        self._p1_score = 0
        self._p2 = player2
        self._p2_score = 0

    def _even_score(self):
        if self._p1_score >= _DEUCE_THRESHOLD:
            return "Deuce"
        return f"{_SCORE[self._p1_score]}-All"

    def _uneven_score(self):
        score_diff = self._p1_score - self._p2_score

        if score_diff == _ADVANTAGE:
            return f"Advantage {self._p1}"

        if score_diff == -_ADVANTAGE:
            return f"Advantage {self._p2}"

        if score_diff >= _WIN_THRESHOLD_MARGIN:
            return f"Win for {self._p1}"

        return f"Win for {self._p2}"

    def won_point(self, player_name):
        if player_name.lower() == self._p1.lower():
            self._p1_score += 1
            return

        self._p2_score += 1

    def get_score(self):
        if self._p1_score == self._p2_score:
            return self._even_score()

        if self._p1_score >= _WIN_THRESHOLD or self._p2_score >= _WIN_THRESHOLD:
            return self._uneven_score()

        return f"{_SCORE[self._p1_score]}-{_SCORE[self._p2_score]}"
