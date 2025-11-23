from tuote import Tuote


class Ostos:
    def __init__(self, tuote: Tuote):
        self.tuote = tuote
        self._lukumaara = 1

    def tuotteen_nimi(self):
        return self.tuote.nimi()

    def muuta_lukumaaraa(self, muutos: int):
        self._lukumaara += muutos
        if self._lukumaara < 0:
            self._lukumaara = 0

    def lukumaara(self):
        return self._lukumaara

    def hinta(self):
        return self._lukumaara * self.tuote.hinta()

    def __str__(self):
        return f"{self._lukumaara} kpl tuotetta \"{self.tuote.nimi()}\""

    def __repr__(self):
        return f"{self.__class__!s}({self.__dict__!r})"
