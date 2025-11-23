import unittest
from unittest.mock import ANY, Mock

from kauppa import Kauppa
from tuote import Tuote
from varasto import Varasto
from viitegeneraattori import Viitegeneraattori


class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        self.viitegeneraattori_mock.uusi.return_value = 42

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock,
                        self.viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("Pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_ostetaan_tuote_jota_on_varastossa(self):
        self.viitegeneraattori_mock.uusi.return_value = 42

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock,
                        self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("Pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "Pekka", 42, "12345", ANY, 5
        )

    def test_ostetaan_kaksi_samaa_tuotetta_jota_on_varastossa(self):
        self.viitegeneraattori_mock.uusi.return_value = 42

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock,
                        self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("Pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "Pekka", 42, "12345", ANY, 10
        )

    def test_ostetaan_kaksi_eri_tuotetta_josta_toinen_ei_ole_varastossa(self):
        self.viitegeneraattori_mock.uusi.return_value = 42

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 0

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 3)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock,
                        self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("Pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "Pekka", 42, "12345", ANY, 5
        )

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        self.viitegeneraattori_mock.uusi.return_value = 42

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock,
                        self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("Kauri", "54321")

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("Pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "Pekka", 42, "12345", ANY, 5
        )

    def test_jokaiselle_maksutapahtumalle_pyydetaan_uusi_viitenumero(self):
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        self.viitegeneraattori_mock.uusi.side_effect = [1, 2, 3]

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock,
                        self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("Kauri", "54321")

        self.viitegeneraattori_mock.uusi.assert_called()
        self.pankki_mock.tilisiirto.assert_called_with(
            "Kauri", 1, "54321", ANY, 5
        )

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("Pekka", "12345")

        self.viitegeneraattori_mock.uusi.assert_called()
        self.pankki_mock.tilisiirto.assert_called_with(
            "Pekka", 2, "12345", ANY, 5
        )

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("Matti", "67890")

        self.viitegeneraattori_mock.uusi.assert_called()
        self.pankki_mock.tilisiirto.assert_called_with(
            "Matti", 3, "67890", ANY, 5
        )

    def test_poista_korista(self):
        self.viitegeneraattori_mock.uusi.return_value = 42

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock,
                        self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.poista_korista(1)
        kauppa.tilimaksu("Pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "Pekka", 42, "12345", ANY, 0
        )
