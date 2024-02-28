from typing import *
import pytest

from funcs_aux import *


# =====================================================================================================================
class Test__collection__get_original_item__case_type_insensitive:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    def setup_method(self, method):
        self.victim = collection__get_original_item__case_type_insensitive

    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__int(self):
        assert self.victim(0, [1]) is None

        assert self.victim(1, [1]) == 1
        assert self.victim(1, [1, 2]) == 1
        assert self.victim(2, [1, 2]) == 2
        assert self.victim(1, ["1", 2]) == "1"

        assert self.victim("1", [1, 2]) == 1
        assert self.victim("1", ["1", 2]) == "1"

    def test__collections(self):
        assert self.victim(1, [1, 2]) == 1
        assert self.victim(1, (1, 2)) == 1
        assert self.victim(1, {1: 11, 2: 22}) == 1
        assert self.victim(1, {1, 2}) == 1
        assert self.victim(2, range(5)) == 2

    def test__case(self):
        assert self.victim("hell", ["hell123", 'hell']) == "hell"
        assert self.victim("hell", ["HELL", 'hell']) == "HELL"
        assert self.victim("hell", ["Hell", ]) == "Hell"


# =====================================================================================================================
