from typing import *
import pathlib

import pytest
from pytest import mark
from pytest_aux import *

from funcs_aux import *


# =====================================================================================================================
class Test__WithUnit:
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
            (1, "1"),
            (1.1, "1.1"),
            ("1", "1"),
            ("1.1", "1.1"),
            ("1,0", "1"),
            ("1,0V", "1V"),

            ("1.1.1", Exception),
            ("hello", Exception),
        ]
    )
    def test__str(self, args, _EXPECTED):
        func_link = lambda: str(Value_WithUnit(args))
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (1, 1),
            (1.1, 1),
            ("1", 1),
            ("1.1", 1),
            ("1,0V", 1),
            ("1,0mV", 10 ** (-3)),
            ("1,0 mV", 10 ** (-3)),
            ("0 mV", 10 ** (-3)),
            ("0MV", 10 ** (+6)),

            ("0M", 10 ** (+6)),

            ("0M V", Exception),
        ]
    )
    def test__multiplier(self, args, _EXPECTED):
        func_link = lambda: Value_WithUnit(args).MULTIPLIER
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source1, source2, _EXPECTED",
        argvalues=[
            # minus/plus ------------------
            ("-1", 1, -1),
            ("- 1", 1, -1),
            ("-  1", -1, 0),
            ("+1", -1, 1),
            ("+1", +1, 0),

            # unit ------------------
            ("1", 1, 0),
            ("1.0", 1, 0),
            ("1.0V", 1, 0),
            ("1.0V", "1 V", 0),

            ("1V", "1A", Exception),

            # multiplier ------------------
            ("0.001V", "1mV", 0),
            ("0.002V", "1mV", 1),
            ("0.001V", "11 mV", -1),
            ("0.001V", "1,1mV", -1),

            ("hello", 2, Exception),
        ]
    )
    def test__cmp(self, source1, source2, _EXPECTED):
        func_link = lambda: Value_WithUnit(source1).__cmp__(source2)
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


# =====================================================================================================================
