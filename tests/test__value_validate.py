from typing import *
import pytest
from pytest import mark
from pytest_aux import *
from funcs_aux import *


# =====================================================================================================================
def test__1():
    assert ClsEq(1) == 1
    assert ClsEq(1) != 2

    assert 1 == ClsEq(1)
    assert 2 != ClsEq(1)


# =====================================================================================================================
class Test__Validate:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #     cls.Victim = type("Victim", (Value_WithUnit,), {})
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
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            ((LAMBDA_TRUE,), True),
            ((LAMBDA_TRUE, True), True),
            ((LAMBDA_TRUE, False), False),
            ((LAMBDA_TRUE, LAMBDA_TRUE), True),
            ((LAMBDA_TRUE, LAMBDA_FALSE), False),

            ((LAMBDA_FALSE,), False),
            ((LAMBDA_FALSE, False), True),
            ((LAMBDA_FALSE, LAMBDA_TRUE), True),
            ((LAMBDA_FALSE, LAMBDA_EXX), False),

            ((LAMBDA_EXX, True), False),
            ((LAMBDA_EXX, LAMBDA_TRUE), False),
            ((LAMBDA_EXX,), False),
            ((LAMBDA_EXX, LAMBDA_EXX), False),
            ((LAMBDA_EXX, Exception), True),

            ((True, None), True),
            ((lambda: True, None), True),

            ((True, lambda val: val is True), True),
            ((LAMBDA_TRUE, lambda val: val is True), True),

            ((lambda: 1, lambda val: 0 < val < 2), True),
            ((lambda: 1, lambda val: 0 < val < 1), False),

            ((lambda: "1", lambda val: 0 < val < 2), False),
            ((lambda: "1", lambda val: 0 < int(val) < 2), True),
            ((lambda: "1.0", lambda val: 0 < int(val) < 2), False),
            ((lambda: "1.0", lambda val: 0 < float(val) < 2), True),
        ]
    )
    def test__validate(self, args, _EXPECTED):
        func_link = Valid(*args).run
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
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
        func_link = Valid.get_result_or_exx
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            ((1, 1), True),
            ((1, 2), False),
            ((LAMBDA_TRUE, True), False),

            ((ClsEq(1), 1), True),
            ((ClsEq(1), 2), False),
            ((1, ClsEq(1)), True),
            ((2, ClsEq(1)), False),

            ((ClsEqExx(), 1), Exception),
            ((1, ClsEqExx()), Exception),
        ]
    )
    def test__compare_doublesided(self, args, _EXPECTED):
        func_link = Valid.compare_doublesided
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
