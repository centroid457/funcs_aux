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
            (-0, True),
            (0, True),
            (-1, True),
            (1, True),
            (1.1, True),
            ("1", True),
            ("1.1", True),
            ("1,0", True),
            ("1,0V", True),
            ("1, 0V", False),
            ("1 ,0V", False),
            ("1,,0V", False),
            ("1,.0V", False),

            ("1мк", True),
            ("1мкB", True),
            ("1мкV", True),
            ("1vV", True),
            ("1vHello", True),
            ("1vПривет", True),
            ("1v Привет", False),

            ("  -  1,0   mV   ", True),
            ("  --  1,0   mV   ", False),

            ("1.1.1", False),
            ("hello", False),
        ]
    )
    def test__validate(self, args, _EXPECTED):
        func_link = Value_WithUnit.validate
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, val_orig, val_pure, mult, unit, unit_mult, unit_base",
        argvalues=[
            # minus/plus/space ------------------
            ("  - 1   k   ", -1, -1000, 1000, "k", "k", ""),
            ("-0", 0, 0, 1, "", "", ""),
            (" + 1 ", 1, 1, 1, "", "", ""),

            # DOTS ------------------------
            ("1,0", 1, 1, 1, "", "", ""),
            ("1.0", 1, 1, 1, "", "", ""),
            ("1.1", 1.1, 1.1, 1, "", "", ""),

            # mult ------------------------
            ("1k", 1, 1000, 1000, "k", "k", ""),
            ("1мк", 1, 10 ** (-6), 10 ** (-6), "мк", "мк", ""),
            ("-1k", -1, -1000, 1000, "k", "k", ""),

            # UNIT ------------------------
            ("1kHELLO", 1, 1000, 1000, "kHELLO", "k", "HELLO"),
            ("1kПРИВЕТ", 1, 1000, 1000, "kПРИВЕТ", "k", "ПРИВЕТ"),
        ]
    )
    def test__parse(self, source, val_orig, val_pure, mult, unit, unit_mult, unit_base):
        victim = Value_WithUnit(source)
        assert victim.VALUE == val_orig
        assert victim.VALUE_PURE == val_pure
        assert victim.MULT == mult
        assert victim.UNIT == unit
        assert victim.UNIT_MULT == unit_mult
        assert victim.UNIT_BASE == unit_base

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (1, "1"),
            (1.1, "1.1"),
            ("1", "1"),
            ("1.1", "1.1"),
            ("1,1", "1.1"),
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
        func_link = lambda: Value_WithUnit(args).MULT
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source1, source2, _EXPECTED",
        argvalues=[
            # minus/plus -----------------
            ("-1", 1, -1),
            ("- 1", 1, -1),
            ("-  1", -1, 0),
            ("+1", -1, 1),
            ("+1", +1, 0),

            # unit -----------------------
            ("1", 1, 0),
            ("1.0", 1, 0),
            ("1.0V", 1, 0),
            ("1.0V", "1 V", 0),

            ("1.0HELLO", 1, 0),
            ("1.0kHELLO", 1000, 0),
            ("1.0kHELLO", '1k', 0),

            ("1V", "1A", Exception),

            # multiplier ------------------
            ("0.001V", "1mV", 0),
            ("0.002V", "1mV", 1),
            ("0.001V", "11 mV", -1),
            ("0.001V", "1,1mV", -1),

            ("hello", 2, Exception),

            # baseWoUnit ------------------
            ("0.001V", "1m", 0),
            ("0.001", "1m", 0),
            ("1k", "1000", 0),

            # RUS/ENG
            ("1d", "1д", 0),
        ]
    )
    def test__cmp(self, source1, source2, _EXPECTED):
        func_link = lambda: Value_WithUnit(source1).__cmp__(source2)
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


# =====================================================================================================================
