from tekoaly import Tekoaly


def test_tekoaly_cycles_moves_and_aseta_siirto_noop():
    ai = Tekoaly()

    # Sequence should be p, s, k, p ... due to modulo logic.
    assert ai.anna_siirto() == "p"
    assert ai.anna_siirto() == "s"
    assert ai.anna_siirto() == "k"
    assert ai.anna_siirto() == "p"

    # Should not raise.
    ai.aseta_siirto("k")
