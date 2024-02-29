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

    def test__collections(self):
        assert self.Victim([1, 2]).item__get_original__case_insensitive(1) == 1
        assert self.Victim((1, 2)).item__get_original__case_insensitive(1) == 1
        assert self.Victim({1, 2}).item__get_original__case_insensitive(1) == 1
        assert self.Victim(range(5)).item__get_original__case_insensitive(1) == 1

        assert self.Victim({1: 11, 2: 22}).item__get_original__case_insensitive(1) == 1

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
    def test__list__single(self):
        assert self.Victim([1]).path__get_original(0) == [0, ]
        assert self.Victim([1]).path__get_original("0") == [0, ]

        assert self.Victim([1]).path__get_original(1) is None
        assert self.Victim([1]).path__get_original("1") is None

        assert self.Victim([1, 11]).path__get_original(1) == [1, ]
        assert self.Victim([1, 11]).path__get_original("1") == [1, ]





        # FIXME: FINISH
        # FIXME: FINISH
        # FIXME: FINISH
        # FIXME: FINISH
        # FIXME: FINISH
        # FIXME: FINISH
        # FIXME: FINISH


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
