from typing import *
import pathlib

import pytest
from pytest import mark
from pytest_aux import *

from funcs_aux import *


# =====================================================================================================================
class Test__WithUnit:
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = type("Victim", (Value_WithUnit,), {})
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
    def test__str(self):
        victim = self.Victim()
        assert victim.VALUE == 0
        assert victim.UNIT == ""
        assert victim.SEPARATOR_OUTPUT == ""
        assert str(victim) == "0"

        victim = self.Victim(1)
        assert victim.VALUE == 1
        assert victim.UNIT == ""
        assert victim.SEPARATOR_OUTPUT == ""
        assert str(victim) == "1"

        victim = self.Victim(1, unit="V")
        assert victim.VALUE == 1
        assert victim.UNIT == "V"
        assert victim.SEPARATOR_OUTPUT == ""
        assert str(victim) == "1V"

        victim = self.Victim(1, unit="V", separator_output=" ")
        assert victim.VALUE == 1
        assert victim.UNIT == "V"
        assert victim.SEPARATOR_OUTPUT == " "
        assert str(victim) == "1 V"

    def test__cmp__same(self):
        assert self.Victim() == self.Victim()
        assert self.Victim(1, separator_output=" ") == self.Victim(1, separator_output="")
        assert self.Victim(1.0) == self.Victim(1)

        assert self.Victim(1) != self.Victim(2)

    def test__cmp__other(self):
        assert self.Victim() == 0
        assert self.Victim(1, separator_output=" ") == 1
        assert self.Victim(1.0) == 1

        assert self.Victim(1) != 2


# =====================================================================================================================
