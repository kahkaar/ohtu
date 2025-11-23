from ostos import Ostos
from tuote import Tuote


class Ostoskori:
    def __init__(self):
        self._ostokset = []

    def _tuotteet(self):
        return [o.tuotteen_nimi() for o in self._ostokset]

    def tavaroita_korissa(self):
        summa = sum([o.lukumaara() for o in self._ostokset])
        return summa

    def hinta(self):
        summa = sum([o.hinta() for o in self._ostokset])
        return summa

    def lisaa_tuote(self, lisattava: Tuote):
        if not lisattava.nimi() in self._tuotteet():
            self._ostokset.append(Ostos(lisattava))
            return

        for ostos in self._ostokset:
            if ostos.tuotteen_nimi() == lisattava.nimi():
                ostos.muuta_lukumaaraa(1)
                return

    def poista_tuote(self, poistettava: Tuote):
        if not poistettava.nimi() in self._tuotteet():
            return
        for ostos in self._ostokset:
            if ostos.tuotteen_nimi() == poistettava.nimi():
                ostos.muuta_lukumaaraa(-1)
                if ostos.lukumaara() == 0:
                    self._ostokset.remove(ostos)

    def tyhjenna(self):
        self._ostokset = []

    def ostokset(self):
        lista = []
        for ostos in self._ostokset:
            lista.append(ostos)

        return lista
