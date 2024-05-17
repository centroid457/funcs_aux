import pytest

from funcs_aux import *
from funcs_aux import BreederObjectList


# =====================================================================================================================
class Test__NamesIndexed_Templated:
    @classmethod
    def setup_class(cls):
        cls.Victim = BreederObjectList

    # # @classmethod
    # # def teardown_class(cls):
    # #     pass
    # #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__init_params(self):
        victim = self.Victim(0, 1, "test_%s", 1)
        assert victim.START_OUTER == 0
        assert victim.COUNT == 1
        assert victim.TEMPLATE == "test_%s"
        assert victim.START_INNER == 1

        assert victim.get_dict__inner() == {1: "test_1"}
        assert victim.get_dict__outer() == {0: "test_1"}

        victim = self.Victim(1, 1, "test_%s", 1)
        assert victim.START_OUTER == 1
        assert victim.COUNT == 1
        assert victim.TEMPLATE == "test_%s"
        assert victim.START_INNER == 1

        victim = self.Victim(1, 2, "test_%s", 1)
        assert victim.START_OUTER == 1
        assert victim.COUNT == 2
        assert victim.TEMPLATE == "test_%s"
        assert victim.START_INNER == 1


# =====================================================================================================================
