from typing import *
import pytest
from pytest import mark
from pytest_aux import *
from funcs_aux import *
from object_info import *


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
class Test__ResultFunc:
    # @classmethod
    # def setup_class(cls):
    #     # cls.Victim = ResultFunc
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    def setup_method(self, method):
        self.Victim = ResultFunc

        pass

    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__bool(self):

        victim = self.Victim(func=bool)

        assert victim.FUNC == bool
        assert victim.ARGS == ()
        assert victim.KWARGS == {}

        assert victim.RESULT__VALUE is None
        assert victim.RESULT__EXX is None
        assert victim.RESULT__IS_CORRECT is True

        # ------------------------------
        victim(0)

        assert victim.FUNC == bool
        assert victim.ARGS == (0, )
        assert victim.KWARGS == {}

        assert victim.RESULT__VALUE is False
        assert victim.RESULT__EXX is None
        assert victim.RESULT__IS_CORRECT is True

        # ------------------------------
        victim(1)

        assert victim.FUNC == bool
        assert victim.ARGS == (1, )
        assert victim.KWARGS == {}

        assert victim.RESULT__VALUE is True
        assert victim.RESULT__EXX is None
        assert victim.RESULT__IS_CORRECT is True

        # ------------------------------
        victim(0, 1)

        assert victim.FUNC == bool
        assert victim.ARGS == (0, 1, )
        assert victim.KWARGS == {}

        assert victim.RESULT__VALUE is None
        assert victim.RESULT__EXX is not None
        assert victim.RESULT__IS_CORRECT is False

    def test__RUN_ON_INIT(self):
        victim = self.Victim(func=bool, args=(0,1), run_on_init=False)

        assert victim.FUNC == bool
        assert victim.ARGS == (0, 1)
        assert victim.KWARGS == {}

        assert victim.RESULT__VALUE is None
        assert victim.RESULT__EXX is None
        assert victim.RESULT__IS_CORRECT is True

        # ------------------------------
        victim = self.Victim(func=bool, args=(0,1), run_on_init=True)

        assert victim.FUNC == bool
        assert victim.ARGS == (0, 1)
        assert victim.KWARGS == {}

        assert victim.RESULT__VALUE is None
        assert victim.RESULT__EXX is not None
        assert victim.RESULT__IS_CORRECT is False

    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (1, 1),
            (1+1, 2),
            (LAMBDA_TRUE, True),
            (LAMBDA_NONE, None),
            (LAMBDA_EXX, Exception),
        ]
    )
    def test__get_result_or_exx(self, args, _EXPECTED):
        func_link = ResultFunc.get_result_or_exx
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
