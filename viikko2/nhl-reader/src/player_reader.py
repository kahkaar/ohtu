# pylint: disable=R0903
import requests

from player import Player


class PlayerReader:
    def __init__(self, url):
        self._url = url

    def get_players(self):
        response = requests.get(self._url, timeout=15).json()
        players = [Player(p) for p in response]
        return players
