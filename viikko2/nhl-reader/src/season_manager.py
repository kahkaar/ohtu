from rich.prompt import Prompt


class SeasonManager:
    def __init__(self, reader):
        self._seasons = reader.get_seasons()

    @property
    def seasons(self):
        return self._seasons

    def ask(self, title="Season"):
        season = Prompt.ask(
            title,
            choices=self._seasons,
            default=self._seasons[-1]
        )
        return season
