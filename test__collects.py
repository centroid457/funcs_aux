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
        self.victim = collection__get_original_item__case_insensitive

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
class Test__collection__path_create_original_names__case_type_insensitive:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     pass

    def setup_method(self, method):
        self.victim = collection__path_create_original_names

    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__list__single(self):
        assert self.victim(0, [1]) == [0, ]
        assert self.victim("0", [1]) == [0, ]

        assert self.victim(1, [1]) is None
        assert self.victim("1", [1]) is None

        assert self.victim(1, [1, 11]) == [1, ]
        assert self.victim("1", [1, 11]) == [1, ]

    def test__list__multy(self):
        assert self.victim(0, [[1], 2]) == [0, ]
        assert self.victim("0", [[1], 2]) == [0, ]

        assert self.victim("0/0", [1]) is None
        assert self.victim("0/0", [[1], 2]) == [0, 0,]

    def test__dict_str(self):
        assert self.victim("hello", {"hello": 1}) == ["hello", ]
        assert self.victim("hello", {"HELLO": 1}) == ["HELLO", ]
        assert self.victim("HELLO", {"hello": 1}) == ["hello", ]

    def test__dict_int(self):
        assert self.victim("1", {"1": 1}) == ["1", ]
        assert self.victim(1, {"1": 1}) == ["1", ]
        assert self.victim(1, {1: 1}) == [1, ]
        assert self.victim("1", {1: 1}) == [1, ]

        assert self.victim("1/2", {1: 1}) is None
        assert self.victim("1/2", {1: {2: 2}}) == [1, 2, ]

    def test__dict__with_list(self):
        assert self.victim("hello", {"hello": [1]}) == ["hello", ]
        assert self.victim("hello/1", {"hello": [1]}) is None
        assert self.victim("hello/0", {"hello": [1]}) == ["hello", 0]

        assert self.victim("hello1/hello2", {"hello1": {"hello2": [1]}}) == ["hello1", "hello2"]
        assert self.victim("hello1/hello2/0", {"hello1": {"hello2": [1]}}) == ["hello1", "hello2", 0, ]
        assert self.victim("hello1/hello2/1", {"hello1": {"hello2": [1]}}) is None


# =====================================================================================================================
