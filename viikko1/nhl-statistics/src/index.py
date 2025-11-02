from player_reader import PlayerReader
from statistics_service import SortBy, StatisticsService


def main():
    stats = StatisticsService(
      PlayerReader("https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt")
    )

    print("Top point getters:")
    for player in stats.top(5, SortBy.POINTS):
        print(player)

    print()
    for player in stats.top(5):
        print(player)

    print()
    print("Top point goal scorers:")
    for player in stats.top(5, SortBy.GOALS):
        print(player)

    print()
    print("Top by assists:")
    for player in stats.top(5, SortBy.ASSISTS):
        print(player)


if __name__ == "__main__":
    main()
