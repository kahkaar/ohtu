from email.policy import default
from random import choice

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from player_reader import PlayerReader
from player_statistics import PlayerStats


def main():
    console = Console()

    seasons = [
        "2018-19",
        "2019-20",
        "2020-21",
        "2021-22",
        "2022-23",
        "2023-24",
        "2024-25",
    ]

    season = Prompt.ask(
        "Season",
        choices=seasons,
        default=seasons[-1]
    )

    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"

    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    nats = stats.nationalities

    while True:
        nationality = Prompt.ask(
            "Nationality",
            choices=nats,
            case_sensitive=False,
            default=""
        ).upper()

        if not nationality:
            break

        table = Table(title=f"Season {season} players from {nationality}")

        table.add_column("Player", style="cyan", no_wrap=True)
        table.add_column("Team(s)", style="magenta")
        table.add_column("Goals", justify="right", style="green")
        table.add_column("Assists", justify="right", style="green")
        table.add_column("Points", justify="right", style="green")

        players = stats.top_scorers_by_nationality(nationality)

        for p in players:
            table.add_row(p.name, p.team, str(p.goals), str(p.assists), str(p.points))

        console.print(table)

if __name__ == "__main__":
    main()
