from funcs_aux import ResultSucceedSimple


# =====================================================================================================================
def test__ResultSucceed():
    assert ResultSucceedSimple(123)() == 123

    assert ResultSucceedSimple(123).VALUE == 123
    assert ResultSucceedSimple([123]).VALUE == [123]
    assert ResultSucceedSimple({123}).VALUE == {123}
    assert ResultSucceedSimple({123: 123}).VALUE == {123: 123}


# =====================================================================================================================
