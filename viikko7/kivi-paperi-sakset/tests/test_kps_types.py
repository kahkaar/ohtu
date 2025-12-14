from kps_types import KPSType, KPSTypes


def test_kps_type_and_types_lookup_and_keys():
    t1 = KPSType("a", "Human")
    t2 = KPSType("b", "AI")
    types = KPSTypes(t1, t2)

    assert t1.key == "a"
    assert t1.option == "Human"
    assert str(t1) == "(a) Human"

    assert types.get_types() == (t1, t2)
    assert types.get_type("a") is t1
    assert types.get_type("missing") is None
    assert types.get_key_of_types() == ["a", "b"]
