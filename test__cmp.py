import os
import time

import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
from configparser import ConfigParser

from funcs_aux import *
from pytest_aux import *


# =====================================================================================================================
class ExampleCmp(Cmp):
    def __init__(self, val):
        self.VAL = val

    def __len__(self):
        try:
            return len(self.VAL)
        except:
            pass

        return int(self.VAL)

    def __cmp__(self, other):
        other = self.__class__(other)

        # equel ----------------------
        if len(self) == len(other):
            return 0

        # final ------------
        return int(len(self) > len(other)) or -1


# =====================================================================================================================
class Test__Cmp:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #     cls.Victim = ExampleCmp
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
        argnames="variant",
        argvalues=[
            # INT ----------------
            ExampleCmp(1) == 1,
            ExampleCmp(1) != 11,

            ExampleCmp(1) < 2,
            ExampleCmp(1) <= 2,
            ExampleCmp(1) <= 1,

            ExampleCmp(1) > 0,
            ExampleCmp(1) >= 0,
            ExampleCmp(1) >= 1,

            # STR ----------------
            ExampleCmp("a") == "a",
            ExampleCmp("a") == "b",
            ExampleCmp("a") == 1,
            ExampleCmp("aa") > 1,
        ]
    )
    def test__inst__cmp__eq(self, variant):
        pytest_func_tester__no_args_kwargs(variant)


# =====================================================================================================================

