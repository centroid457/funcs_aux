import pytest
from pytest_aux import *
from funcs_aux import *

from funcs_aux import args__ensure_tuple


# =====================================================================================================================
class Test__ResultValue:
    # @classmethod
    # def setup_class(cls):
    #     # cls.Victim = ResultFunc
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__1(self):
        assert ResultValue(None).VALUE is None
        assert ResultValue(()).VALUE == ()
        assert ResultValue([]).VALUE == []
        assert ResultValue({}).VALUE == {}

        assert ResultValue(111).VALUE == 111
        assert ResultValue([111]).VALUE == [111]
        assert ResultValue({111}).VALUE == {111}
        assert ResultValue({111: 222}).VALUE == {111: 222}

    def test__call(self):
        assert ResultValue(None)() is None
        assert ResultValue(111)() == 111


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        # NONE -----------------------
        (None, ()),
        ((None, ), (None, )),

        # COLLECTION -----------------------
        ((), ()),
        ([], ()),
        ({}, ()),

        (range(3), (range(3), )),
        (ClsGen, (ClsGen, )),
        (, (ClsGen(), )),

        (0, (0, )),
        (1, (1, )),
        (2, (2, )),

    ]
)
def test__args__ensure_tuple(args, _EXPECTED):
    func_link = args__ensure_tuple
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
