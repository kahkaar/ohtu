import unittest

from player import Player
from statistics_service import StatisticsService


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_player(self):
        result = self.stats.search("Semenko")

        self.assertEqual(str(result), "Semenko EDM 4 + 12 = 16")

    def test_search_unknown_player(self):
        result = self.stats.search("Kapanen")

        self.assertIsNone(result)

    def test_correct_team(self):
        result = self.stats.team("EDM")

        self.assertEqual(len(result), 3)

    def test_incorrect_team(self):
        result = self.stats.team("MTL")

        self.assertFalse(result)

    def test_top_three(self):
        result = self.stats.top(2)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "Gretzky")
        self.assertEqual(result[1].name, "Lemieux")
        self.assertEqual(result[2].name, "Yzerman")
