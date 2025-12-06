from enum import Enum
from tkinter import StringVar, constants, ttk


class Komento(Enum):
    SUMMA = 1
    EROTUS = 2
    NOLLAUS = 3
    KUMOA = 4


class Summa:
    def __init__(self, sovelluslogiikka, syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._syote = syote

    def suorita(self):
        arvo = self._syote()
        self._sovelluslogiikka.plus(arvo)


class Erotus:
    def __init__(self, sovelluslogiikka, syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._syote = syote

    def suorita(self):
        arvo = self._syote()
        self._sovelluslogiikka.miinus(arvo)


class Nollaus:
    def __init__(self, sovelluslogiikka):
        self._sovelluslogiikka = sovelluslogiikka

    def suorita(self):
        self._sovelluslogiikka.nollaa()


class Kayttoliittyma:
    def __init__(self, sovelluslogiikka, root):
        self._sovelluslogiikka = sovelluslogiikka
        self._root = root

        self._komennot = {
            Komento.SUMMA: lambda: Summa(self._sovelluslogiikka, self._lue_syote),
            Komento.EROTUS: lambda: Erotus(self._sovelluslogiikka, self._lue_syote),
            Komento.NOLLAUS: lambda: Nollaus(self._sovelluslogiikka),
        }

    def kaynnista(self):
        self._arvo_var = StringVar()
        self._arvo_var.set(self._sovelluslogiikka.arvo())
        self._syote_kentta = ttk.Entry(master=self._root)

        tulos_teksti = ttk.Label(textvariable=self._arvo_var)

        summa_painike = ttk.Button(
            master=self._root,
            text="Summa",
            command=lambda: self._suorita_komento(Komento.SUMMA)
        )

        erotus_painike = ttk.Button(
            master=self._root,
            text="Erotus",
            command=lambda: self._suorita_komento(Komento.EROTUS)
        )

        self._nollaus_painike = ttk.Button(
            master=self._root,
            text="Nollaus",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.NOLLAUS)
        )

        self._kumoa_painike = ttk.Button(
            master=self._root,
            text="Kumoa",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.KUMOA)
        )

        tulos_teksti.grid(columnspan=4)
        self._syote_kentta.grid(
            columnspan=4,
            sticky=(constants.E, constants.W),
        )
        summa_painike.grid(row=2, column=0)
        erotus_painike.grid(row=2, column=1)
        self._nollaus_painike.grid(row=2, column=2)
        self._kumoa_painike.grid(row=2, column=3)

    def _lue_syote(self):
        try:
            arvo = int(self._syote_kentta.get())
        except (TypeError, ValueError):
            arvo = 0

        return arvo

    def _suorita_komento(self, komento):
        if not isinstance(komento, Komento):
            raise TypeError("Tuntematon komento")

        komento_olio = self._komennot[komento]
        komento_olio.suorita()
        self._kumoa_painike["state"] = constants.NORMAL

        if self._sovelluslogiikka.arvo() == 0:
            self._nollaus_painike["state"] = constants.DISABLED
        else:
            self._nollaus_painike["state"] = constants.NORMAL

        self._syote_kentta.delete(0, constants.END)
        self._arvo_var.set(self._sovelluslogiikka.arvo())
