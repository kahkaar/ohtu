# pylint: disable=R0903
import re

import requests


class SeasonReader:
    def __init__(self, url):
        self._url = url

    def get_seasons(self):
        # Get seasons from html body; did not find a json endpoint for this
        response = requests.get(self._url, timeout=15).text

        pattern = r"\b(\d{4}-\d{2})\b"
        seasons = re.findall(pattern, response)

        return seasons
