class PlayerStats:
    def __init__(self, reader):
        self._players = reader.get_players()
        self._nationalities = sorted({p.nationality for p in self._players})

    @property
    def nationalities(self):
        return self._nationalities

    def top_scorers_by_nationality(self, nationality):
        def sort_by_points(player):
            return player.points

        result = sorted(filter(
            lambda p: p.nationality == nationality,
            self._players
        ),
            reverse=True,
            key=sort_by_points)

        return result
