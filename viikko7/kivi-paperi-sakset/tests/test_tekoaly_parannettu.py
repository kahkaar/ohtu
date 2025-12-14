from tekoaly_parannettu import TekoalyParannettu


def test_tekoaly_parannettu_initial_returns_k():
    ai = TekoalyParannettu(3)
    assert ai.anna_siirto() == "k"
    ai.aseta_siirto("k")
    assert ai.anna_siirto() == "k"


def test_tekoaly_parannettu_choice_branches():
    # k is most common -> return p
    ai = TekoalyParannettu(10)
    ai.aseta_siirto("k")
    ai.aseta_siirto("k")
    ai.aseta_siirto("k")
    assert ai.anna_siirto() == "p"

    # p is most common -> return s
    ai = TekoalyParannettu(10)
    ai.aseta_siirto("p")
    ai.aseta_siirto("p")
    ai.aseta_siirto("p")
    assert ai.anna_siirto() == "s"

    # otherwise -> return k (e.g. s dominates)
    ai = TekoalyParannettu(10)
    ai.aseta_siirto("s")
    ai.aseta_siirto("s")
    ai.aseta_siirto("s")
    assert ai.anna_siirto() == "k"


def test_tekoaly_parannettu_memory_shifts_when_full():
    ai = TekoalyParannettu(3)
    ai.aseta_siirto("k")
    ai.aseta_siirto("p")
    ai.aseta_siirto("s")

    # Now full; adding one more should shift left.
    ai.aseta_siirto("k")

    assert ai._vapaa_muisti_indeksi == 3
    assert ai._muisti == ["p", "s", "k"]
