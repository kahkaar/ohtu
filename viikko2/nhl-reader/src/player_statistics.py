class PlayerStats:
    def __init__(self, reader):
        self._players = reader.get_players()
        self.nationalities = sorted(set([p.nationality for p in self._players]))

    def _sort_by_points(self, player):
        return player.points

    def top_scorers_by_nationality(self, nationality):
        result = sorted(filter(
            lambda p: p.nationality == nationality,
            self._players
        ),
        reverse=True,
        key=self._sort_by_points)

        return result
