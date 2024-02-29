from typing import *
import pytest

from funcs_aux import *


# =====================================================================================================================
def test__ResultSucceed():
    assert ResultSucceed(123)() == 123

    assert ResultSucceed(123).VALUE == 123
    assert ResultSucceed([123]).VALUE == [123]
    assert ResultSucceed({123}).VALUE == {123}
    assert ResultSucceed({123: 123}).VALUE == {123: 123}


# =====================================================================================================================
class Test__1:
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

        assert self.victim(1, [1]) == ResultSucceed(1)
        assert self.victim(1, [1, 2]) == ResultSucceed(1)
        assert self.victim(2, [1, 2]) == ResultSucceed(2)

        assert self.victim(1, ["1", 2]) == ResultSucceed("1")
        assert self.victim("1", ["1", 2]) == ResultSucceed("1")

        assert self.victim(1, ["1", 1]) == ResultSucceed("1")
        assert self.victim(1, [1, "1"]) == ResultSucceed(1)

        assert self.victim("1", [1, 1]) == ResultSucceed(1)

    def test__collections_1__iterables(self):
        assert self.victim(1, [1, 2]) == ResultSucceed(1)
        assert self.victim(1, (1, 2)) == ResultSucceed(1)
        assert self.victim(1, {1, 2}) == ResultSucceed(1)
        assert self.victim(1, range(5)) == ResultSucceed(1)

    def test__collections_2__dict(self):
        assert self.victim(2, {1: 11, 2: 22}) == ResultSucceed(2)
        assert self.victim("2", {1: 11, 2: 22}) == ResultSucceed(2)
        assert self.victim(2, {1: 11, "2": 22}) == ResultSucceed("2")
        assert self.victim("2", {1: 11, "2": 22}) == ResultSucceed("2")

    def test__case(self):
        assert self.victim("hell", ["hello123", 'hello']) is None

        assert self.victim("hello", ["hello123", 'hello']) == ResultSucceed("hello")
        assert self.victim("hello", ["hello123", 'HELLO']) == ResultSucceed("HELLO")
        assert self.victim("heLLO", ["hello123", 'Hello']) == ResultSucceed("Hello")


# =====================================================================================================================
class Test__2:
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
        assert self.victim([0, ], [[1], 2]) == ResultSucceed([0, ])
        assert self.victim(["0", ], [[1], 2]) == ResultSucceed([0, ])

        assert self.victim([0, 0], [1]) is None
        assert self.victim([0, 0], [[1]]) == ResultSucceed([0, 0, ])
        assert self.victim([0, 1], [[1]]) is None

    def test__value__list__single(self):
        assert self.victim(0, [1]) == ResultSucceed([0, ])
        assert self.victim("0", [1]) == ResultSucceed([0, ])

        assert self.victim(1, [1]) is None
        assert self.victim("1", [1]) is None

        assert self.victim(1, [1, 11]) == ResultSucceed([1, ])
        assert self.victim("1", [1, 11]) == ResultSucceed([1, ])

    def test__value__list__multy(self):
        assert self.victim(0, [[1], 2]) == ResultSucceed([0, ])
        assert self.victim("0", [[1], 2]) == ResultSucceed([0, ])

        assert self.victim("0/0", [1]) is None
        assert self.victim("0/0", [[1]]) == ResultSucceed([0, 0, ])
        assert self.victim("0/1", [[1]]) is None

    def test__value__dict_str(self):
        assert self.victim("hello", ["hello", ]) is None

        assert self.victim("hello", {"hello": 1}) == ResultSucceed(["hello", ])
        assert self.victim("hello", {"HELLO": 1}) == ResultSucceed(["HELLO", ])
        assert self.victim("HELLO", {"hello": 1}) == ResultSucceed(["hello", ])

    def test__value__dict_int(self):
        assert self.victim("1", {"1": 11, }) == ResultSucceed(["1", ])
        assert self.victim("1", {1: 11, }) == ResultSucceed([1, ])
        assert self.victim(1, {1: 11, }) == ResultSucceed([1, ])

        assert self.victim("1/2", {1: 11, }) is None
        assert self.victim("1/2", {1: {2: 22}, }) == ResultSucceed([1, 2, ])
        assert self.victim("1/2/1", {1: {2: [30, 31, 32]}, }) == ResultSucceed([1, 2, 1])

    def test__value__dict__with_list(self):
        assert self.victim("hello", {"hello": [1]}) == ResultSucceed(["hello", ])
        assert self.victim("hello/1", {"hello": [1]}) is None
        assert self.victim("hello/0", {"hello": [1]}) == ResultSucceed(["hello", 0])

        assert self.victim("hello1/hello2", {"hello1": {"hello2": [1]}}) == ResultSucceed(["hello1", "hello2"])
        assert self.victim("hello1/hello2/0", {"hello1": {"hello2": [1]}}) == ResultSucceed(["hello1", "hello2", 0, ])
        assert self.victim("hello1/hello2/1", {"hello1": {"hello2": [1]}}) is None


# =====================================================================================================================
class Test__3:
    @classmethod
    def setup_class(cls):
        cls.victim = Iterables().value_by_path__get
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
        assert self.victim("hello", {"hello": [1]}) == ResultSucceed([1])
        assert self.victim("hello/1", {"hello": [1]}) is None
        assert self.victim("hello/0", {"hello": [1]}) == ResultSucceed(1)


# =====================================================================================================================
class Test__4:
    @classmethod
    def setup_class(cls):
        cls.victim = Iterables().value_by_path__set
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
        data = [0,1,2,]
        assert not self.victim(5, 11, data)
        assert data[1] == 1
        assert data == [0,1,2,]

        data = [0,1,2,]
        assert self.victim(1, 11, data) is True
        assert data[1] == 11
        assert data == [0,11,2,]

        data = [[0],1,2,]
        assert self.victim("0/0", 11, data) is True
        assert data[0] == [11]
        assert data == [[11],1,2,]

        data = {"hello": [0,1,2,]}
        assert self.victim("hello", 11, data) is True
        assert data == {"hello": 11}

        data = {"hello": [0,1,2,]}
        assert self.victim("hello/1", 11, data) is True
        assert data == {"hello": [0,11,2,]}


# =====================================================================================================================
