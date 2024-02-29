from funcs_aux import ResultSucceed


# =====================================================================================================================
def test__ResultSucceed():
    assert ResultSucceed(123)() == 123

    assert ResultSucceed(123).VALUE == 123
    assert ResultSucceed([123]).VALUE == [123]
    assert ResultSucceed({123}).VALUE == {123}
    assert ResultSucceed({123: 123}).VALUE == {123: 123}


# =====================================================================================================================
