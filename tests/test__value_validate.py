from typing import *
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
            ((True, None), True),
            ((lambda: True, None), True),

            ((True, lambda val: val is True), True),
            ((lambda: True, lambda val: val is True), True),

            ((lambda: 1, lambda val: 0 < val < 2), True),
            ((lambda: 1, lambda val: 0 < val < 1), False),

            ((lambda: "1", lambda val: 0 < val < 2), False),
            ((lambda: "1", lambda val: 0 < int(val) < 2), True),
            ((lambda: "1.0", lambda val: 0 < int(val) < 2), False),
            ((lambda: "1.0", lambda val: 0 < float(val) < 2), True),
        ]
    )
    def test__validate(self, args, _EXPECTED):
        func_link = ValueValidate(*args).run
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


# =====================================================================================================================
