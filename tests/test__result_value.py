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
