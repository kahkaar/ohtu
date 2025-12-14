from tuomari import Tuomari


def test_tuomari_scoring_and_str_and_helpers():
    t = Tuomari()

    assert t._tasapeli("k", "k") is True
    assert t._tasapeli("k", "p") is False

    assert t._eka_voittaa("k", "s") is True
    assert t._eka_voittaa("s", "p") is True
    assert t._eka_voittaa("p", "k") is True
    assert t._eka_voittaa("k", "p") is False

    t.kirjaa_siirto("k", "k")
    assert t.tasapelit == 1

    t.kirjaa_siirto("k", "s")
    assert t.ekan_pisteet == 1

    t.kirjaa_siirto("k", "p")
    assert t.tokan_pisteet == 1

    s = str(t)
    assert "Pelitilanne:" in s
    assert "Tasapelit:" in s
