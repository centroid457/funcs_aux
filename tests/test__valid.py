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


# ---------------------------------------------------------------------------------------------------------------------
def test__str():
    victim = Valid(True)
    victim.run()
    print(victim)

    victim = ValidChains([True, ])
    victim.run()
    print(victim)


# =====================================================================================================================
class Test__Valid_ClsMethods:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #     cls.Victim = type("Victim", (ValueUnit,), {})
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

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (Exception, False),
            (Exception(), False),
            (LAMBDA_EXX, False),

            (True, True),
            (False, False),
            (None, False),
            (LAMBDA_TRUE, True),
            (LAMBDA_FALSE, False),
            (LAMBDA_NONE, False),

            (([]), False),
            ((LAMBDA_LIST_DIRECT), False),

            (([1, ]), True),

            (ClsBoolTrue(), True),
            (ClsBoolFalse(), False),
            (ClsBoolExx(), False),
        ]
    )
    def test__get_bool(self, args, _EXPECTED):
        func_link = Valid.get_bool
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================
class Test__ValidVariants:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #     cls.Victim = type("Victim", (ValueUnit,), {})
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
            # BOOLING ---------------
            # direct TRUE
            ((0,), False),
            ((2,), False),  # careful about 1 comparing (assert 0 == False, assert 1 == True, assert 2 != True)
            (([],), False),
            (([None,],), False),
            (([1,],), False),

            ((0, True), False),
            ((2, True), False),
            (([], True), False),
            (([None, True],), False),
            (([1, ], True), False),

            # active BOOL
            ((0, bool), False),
            ((2, bool), True),
            (([], bool), False),
            (([None, ], bool), True),
            (([1, ], bool), True),

            # -----------------------
            ((LAMBDA_TRUE,), True),
            ((LAMBDA_TRUE, True), True),
            ((LAMBDA_TRUE, False), False),
            ((LAMBDA_TRUE, LAMBDA_TRUE), True),
            ((LAMBDA_TRUE, LAMBDA_FALSE), False),

            ((LAMBDA_NONE,), False),

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
    def test__validate__types(self, args, _EXPECTED):
        func_link = Valid(*args).run
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, args, kwargs, validate, _EXPECTED",
        argvalues=[
            # bool --------------------
            (0, (), {}, True, False),
            (0, (1,2,), {1:1}, True, False),

            (2, (), {}, bool, True),
            (2, (1,2,), {1:1}, bool, True),

            # VALUE --------------------
            (LAMBDA_LIST_VALUES, (1,2,), {}, [1,2], True),
            (LAMBDA_LIST_VALUES, (1,2,), {"1":11, }, [1,2,11], True),
        ]
    )
    def test__validate__value_with_args_kwargs(self, source, args, kwargs, validate, _EXPECTED):
        func_link = Valid(value_link=source, validate_link=validate, args__value=args, kwargs__value=kwargs).run
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, args, kwargs, validate, _EXPECTED",
        argvalues=[
            # bool --------------------
            (0, (), {}, True, False),
            (0, (1, 2,), {1: 1}, True, False),

            (2, (), {}, bool, True),
            (2, (1, 2,), {1: 1}, bool, False),

            # VALUE --------------------
            (LAMBDA_LIST_VALUES, (1, 2,), {}, [1, 2], False),
            (LAMBDA_LIST_VALUES, (1, 2,), {}, [], True),

            (LAMBDA_LIST_VALUES, (1, 2,), {"1": 11, }, [1, 2, 11], False),
            (LAMBDA_LIST_VALUES, (1, 2,), {"1": 11, }, [], True),

            # VALUE --------------------
            (0, (1, 3,), {}, Valid.legt, False),
            (1, (1, 3,), {}, Valid.legt, True),
            (2, (1, 3,), {}, Valid.legt, True),
            (3, (1, 3,), {}, Valid.legt, False),
            (4, (1, 3,), {}, Valid.legt, False),
        ]
    )
    def test__validate_with_args_kwargs__value(self, source, args, kwargs, validate, _EXPECTED):
        func_link = Valid(value_link=source, validate_link=validate, args__validate=args, kwargs__validate=kwargs).run
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args",
        argvalues=[
            # BOOLING ---------------
            # direct TRUE
            (0,),
            (2,),  # careful about 1 comparing (assert 0 == False, assert 1 == True, assert 2 != True)
            ([],),
            ([None,],),
            ([1,],),

            (0, True),
            (2, True),
            (([], True)),
            ([None, True],),
            ([1, ], True),

            # active BOOL
            (0, bool),
            (2, bool),
            ([], bool),
            ([None, ], bool),
            ([1, ], bool),

            # -----------------------
            (LAMBDA_TRUE,),
            (LAMBDA_TRUE, True),
            (LAMBDA_TRUE, False),
            (LAMBDA_TRUE, LAMBDA_TRUE),
            (LAMBDA_TRUE, LAMBDA_FALSE),

            (LAMBDA_NONE,),

            (LAMBDA_FALSE,),
            (LAMBDA_FALSE, False),
            (LAMBDA_FALSE, LAMBDA_TRUE),
            (LAMBDA_FALSE, LAMBDA_EXX),

            (LAMBDA_EXX, True),
            (LAMBDA_EXX, LAMBDA_TRUE),
            (LAMBDA_EXX,),
            (LAMBDA_EXX, LAMBDA_EXX),
            (LAMBDA_EXX, Exception),

            (True, None),
            (lambda: True, None),

            (True, lambda val: val is True),
            (LAMBDA_TRUE, lambda val: val is True),

            (lambda: 1, lambda val: 0 < val < 2),
            (lambda: 1, lambda val: 0 < val < 1),

            (lambda: "1", lambda val: 0 < val < 2),
            (lambda: "1", lambda val: 0 < int(val) < 2),
            (lambda: "1.0", lambda val: 0 < int(val) < 2),
            (lambda: "1.0", lambda val: 0 < float(val) < 2),
        ]
    )
    def test__str(self, args):
        assert str(Valid(*args)) is not None


# =====================================================================================================================
