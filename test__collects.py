from typing import *
import pytest

from funcs_aux import *


# =====================================================================================================================
class Test__item__get_original__case_insensitive:
    @classmethod
    def setup_class(cls):
        cls.victim = Iterables().item__get_original__case_insensitive
        pass

    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
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
        assert self.victim("1", ["1", 2]) == "1"

        assert self.victim(1, ["1", 1]) == "1"
        assert self.victim(1, [1, "1"]) == 1

        assert self.victim("1", [1, 1]) == 1

    def test__collections_1__iterables(self):
        assert self.victim(1, [1, 2]) == 1
        assert self.victim(1, (1, 2)) == 1
        assert self.victim(1, {1, 2}) == 1
        assert self.victim(1, range(5)) == 1

    def test__collections_2__dict(self):
        assert self.victim(2, {1: 11, 2: 22}) == 2
        assert self.victim("2", {1: 11, 2: 22}) == 2
        assert self.victim(2, {1: 11, "2": 22}) == "2"
        assert self.victim("2", {1: 11, "2": 22}) == "2"

    def test__case(self):
        assert self.victim("hello", ["hello123", 'hello']) == "hello"
        assert self.victim("hello", ["hello123", 'HELLO']) == "HELLO"
        assert self.victim("heLLO", ["hello123", 'Hello']) == "Hello"


# =====================================================================================================================
class Test__path__get_original:
    @classmethod
    def setup_class(cls):
        cls.victim = Iterables().path__get_original
        pass

    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__path__list(self):
        assert self.victim([0, ], [[1], 2]) == [0, ]
        assert self.victim(["0", ], [[1], 2]) == [0, ]

        assert self.victim([0, 0], [1]) is None
        assert self.victim([0, 0], [[1]]) == [0, 0, ]
        assert self.victim([0, 1], [[1]]) is None

    def test__value__list__single(self):
        assert self.victim(0, [1]) == [0, ]
        assert self.victim("0", [1]) == [0, ]

        assert self.victim(1, [1]) is None
        assert self.victim("1", [1]) is None

        assert self.victim(1, [1, 11]) == [1, ]
        assert self.victim("1", [1, 11]) == [1, ]

    def test__value__list__multy(self):
        assert self.victim(0, [[1], 2]) == [0, ]
        assert self.victim("0", [[1], 2]) == [0, ]

        assert self.victim("0/0", [1]) is None
        assert self.victim("0/0", [[1]]) == [0, 0, ]
        assert self.victim("0/1", [[1]]) is None

    def test__value__dict_str(self):
        assert self.victim("hello", ["hello", ]) is None

        assert self.victim("hello", {"hello": 1}) == ["hello", ]
        assert self.victim("hello", {"HELLO": 1}) == ["HELLO", ]
        assert self.victim("HELLO", {"hello": 1}) == ["hello", ]

    def test__value__dict_int(self):
        assert self.victim("1", {"1": 11, }) == ["1", ]
        assert self.victim("1", {1: 11, }) == [1, ]
        assert self.victim(1, {1: 11, }) == [1, ]

        assert self.victim("1/2", {1: 11, }) is None
        assert self.victim("1/2", {1: {2: 22}, }) == [1, 2, ]
        assert self.victim("1/2/1", {1: {2: [30, 31, 32]}, }) == [1, 2, 1]

    def test__value__dict__with_list(self):
        assert self.victim("hello", {"hello": [1]}) == ["hello", ]
        assert self.victim("hello/1", {"hello": [1]}) is None
        assert self.victim("hello/0", {"hello": [1]}) == ["hello", 0]

        assert self.victim("hello1/hello2", {"hello1": {"hello2": [1]}}) == ["hello1", "hello2"]
        assert self.victim("hello1/hello2/0", {"hello1": {"hello2": [1]}}) == ["hello1", "hello2", 0, ]
        assert self.victim("hello1/hello2/1", {"hello1": {"hello2": [1]}}) is None


# =====================================================================================================================
class Test__value__get_by_path:
    @classmethod
    def setup_class(cls):
        cls.victim = Iterables().value__get_by_path
        pass

    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__1(self):
        assert self.victim("hello", {"hello": [1]}) == ResultWithStatus(True, [1, ])
        assert self.victim("hello/1", {"hello": [1]}) == ResultWithStatus(None, None)
        assert self.victim("hello/0", {"hello": [1]}) == ResultWithStatus(True, 1)


# =====================================================================================================================
