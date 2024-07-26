from typing import *
import pytest
from pytest import mark
from pytest_aux import *
from funcs_aux import *


# =====================================================================================================================
class Test__ValidChains:
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
        argnames="chains, _EXPECTED",
        argvalues=[
            ([True, ], True),
            ([False, ], False),
            ([None, ], False),

            ([0, ], False),
            ([1, ], True),

            ([[], ], False),
            ([[None, ], ], True),

        ]
    )
    def test__single_types(self, chains, _EXPECTED):
        func_link = ValidChains(chains).run
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


# =====================================================================================================================
