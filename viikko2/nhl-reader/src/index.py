from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from player_reader import PlayerReader
from player_statistics import PlayerStats
from season_manager import SeasonManager
from season_reader import SeasonReader


def build_table(title):
    table = Table(title)

    table.add_column("Player", style="cyan", no_wrap=True)
    table.add_column("Team(s)", style="magenta")
    table.add_column("Goals", justify="right", style="green")
    table.add_column("Assists", justify="right", style="green")
    table.add_column("Points", justify="right", style="green")

    return table


def nationality_loop(console, stats, season):
    nationalities = stats.nationalities

    while True:
        nationality = Prompt.ask(
            "Nationality",
            choices=nationalities,
            case_sensitive=False,
            default="",
        ).upper()

        if not nationality:
            break

        table = build_table(f"Season {season} players from {nationality}")

        players = stats.top_scorers_by_nationality(nationality)

        for p in players:
            table.add_row(*p.table_row())

        console.print(table)


def main():
    console = Console()

    seasons_url = "https://studies.cs.helsinki.fi/nhlstats/"
    season_reader = SeasonReader(seasons_url)

    season_manager = SeasonManager(season_reader)
    season = season_manager.ask()

    players_url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    player_reader = PlayerReader(players_url)
    stats = PlayerStats(player_reader)

    nationality_loop(console, stats, season)


if __name__ == "__main__":
    main()
