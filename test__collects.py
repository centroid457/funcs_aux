from typing import *
import pytest

from funcs_aux import *


# =====================================================================================================================
class Test__item__get_original__case_insensitive:
    @classmethod
    def setup_class(cls):
        cls.Victim = Iterables
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
        assert self.Victim([1]).item__get_original__case_insensitive(0) is None

        assert self.Victim([1]).item__get_original__case_insensitive(1) == 1
        assert self.Victim([1, 2]).item__get_original__case_insensitive(1) == 1
        assert self.Victim([1, 2]).item__get_original__case_insensitive(2) == 2

        assert self.Victim(["1", 2]).item__get_original__case_insensitive(1) == "1"
        assert self.Victim(["1", 2]).item__get_original__case_insensitive("1") == "1"

        assert self.Victim(["1", 1]).item__get_original__case_insensitive(1) == "1"
        assert self.Victim([1, "1"]).item__get_original__case_insensitive(1) == 1

        assert self.Victim([1, 1]).item__get_original__case_insensitive("1") == 1

    def test__collections_1__iterables(self):
        assert self.Victim([1, 2]).item__get_original__case_insensitive(1) == 1
        assert self.Victim((1, 2)).item__get_original__case_insensitive(1) == 1
        assert self.Victim({1, 2}).item__get_original__case_insensitive(1) == 1
        assert self.Victim(range(5)).item__get_original__case_insensitive(1) == 1

    def test__collections_2__dict(self):
        assert self.Victim({1: 11, 2: 22}).item__get_original__case_insensitive(2) == 2
        assert self.Victim({1: 11, 2: 22}).item__get_original__case_insensitive("2") == 2
        assert self.Victim({1: 11, "2": 22}).item__get_original__case_insensitive(2) == "2"
        assert self.Victim({1: 11, "2": 22}).item__get_original__case_insensitive("2") == "2"

    def test__case(self):
        assert self.Victim(["hello123", 'hello']).item__get_original__case_insensitive("hello") == "hello"
        assert self.Victim(["hello123", 'HELLO']).item__get_original__case_insensitive("hello") == "HELLO"
        assert self.Victim(["hello123", 'Hello']).item__get_original__case_insensitive("heLLO") == "Hello"


# =====================================================================================================================
class Test__collection__path_create_original_names__case_type_insensitive:
    @classmethod
    def setup_class(cls):
        cls.Victim = Iterables
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
        assert self.Victim([[1], 2]).path__get_original([0, ]) == [0, ]
        assert self.Victim([[1], 2]).path__get_original(["0", ]) == [0, ]

        assert self.Victim([1]).path__get_original([0, 0]) is None
        assert self.Victim([[1]]).path__get_original([0, 0]) == [0, 0, ]
        assert self.Victim([[1]]).path__get_original([0, 1]) is None

    def test__value__list__single(self):
        assert self.Victim([1]).path__get_original(0) == [0, ]
        assert self.Victim([1]).path__get_original("0") == [0, ]

        assert self.Victim([1]).path__get_original(1) is None
        assert self.Victim([1]).path__get_original("1") is None

        assert self.Victim([1, 11]).path__get_original(1) == [1, ]
        assert self.Victim([1, 11]).path__get_original("1") == [1, ]

    def test__value__list__multy(self):
        assert self.Victim([[1], 2]).path__get_original(0) == [0, ]
        assert self.Victim([[1], 2]).path__get_original("0") == [0, ]

        assert self.Victim([1]).path__get_original("0/0") is None
        assert self.Victim([[1]]).path__get_original("0/0") == [0, 0, ]
        assert self.Victim([[1]]).path__get_original("0/1") is None
    def test__value__dict_str(self):
        assert self.Victim(["hello", ]).path__get_original("hello") is None

        assert self.Victim({"hello": 1}).path__get_original("hello") == ["hello", ]
        assert self.Victim({"HELLO": 1}).path__get_original("hello") == ["HELLO", ]
        assert self.Victim({"hello": 1}).path__get_original("HELLO") == ["hello", ]

    def test__value__dict_int(self):
        assert self.Victim({"1": 11, }).path__get_original("1") == ["1", ]
        assert self.Victim({1: 11, }).path__get_original("1") == [1, ]
        assert self.Victim({1: 11, }).path__get_original(1) == [1, ]

        assert self.Victim({1: 11, }).path__get_original("1/2") is None
        assert self.Victim({1: {2: 22}, }).path__get_original("1/2") == [1, 2, ]
        assert self.Victim({1: {2: [30, 31, 32]}, }).path__get_original("1/2/1") == [1, 2, 1]

    def test__value__dict__with_list(self):
        assert self.Victim().path__get_original("hello", {"hello": [1]}) == ["hello", ]
        assert self.Victim().path__get_original("hello/1", {"hello": [1]}) is None
        assert self.Victim().path__get_original("hello/0", {"hello": [1]}) == ["hello", 0]

        assert self.Victim().path__get_original("hello1/hello2", {"hello1": {"hello2": [1]}}) == ["hello1", "hello2"]
        assert self.Victim().path__get_original("hello1/hello2/0", {"hello1": {"hello2": [1]}}) == ["hello1", "hello2", 0, ]
        assert self.Victim().path__get_original("hello1/hello2/1", {"hello1": {"hello2": [1]}}) is None


# =====================================================================================================================
