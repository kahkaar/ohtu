class Player:
    def __init__(self, obj):
        self.name = obj["name"]
        self.nationality = obj["nationality"]
        self.assists = obj["assists"]
        self.goals = obj["goals"]
        self.team = obj["team"]
        self.games = obj["games"]
        self.id = obj["id"]

    @property
    def points(self):
        return self.goals + self.assists

    def table_row(self):
        return (
            self.name,
            self.team,
            str(self.goals),
            str(self.assists),
            str(self.points),
        )

    def __str__(self):
        return (
            f"{self.name:<22} "
            f"{self.team:<16} "
            f"{self.goals:<2} + "
            f"{self.assists:<2} = "
            f"{self.points:<2}"
        )

    def __repr__(self) -> str:
        return (
            "Player("
            f"{self.name}, "
            f"{self.nationality}, "
            f"{self.assists}, "
            f"{self.goals}, "
            f"{self.team}, "
            f"{self.games}, "
            f"{self.id}"
            ")"
        )
