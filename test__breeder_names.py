import pytest

from funcs_aux import *
from funcs_aux import NamesIndexed_Base


# =====================================================================================================================
class Test__NamesIndexed_Templated:
    @classmethod
    def setup_class(cls):
        cls.Victim = NamesIndexed_Templated

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

    def test__dicts(self):
        victim = self.Victim(0, 1, "test_%s", 0)
        assert victim.get_dict__inner() == {0: "test_0"}
        assert victim.get_dict__outer() == {0: "test_0"}

        victim = self.Victim(0, 1, "test_%s", 1)
        assert victim.get_dict__inner() == {1: "test_1"}
        assert victim.get_dict__outer() == {0: "test_1"}

        victim = self.Victim(0, 2, "test_%s", 1)
        assert victim.get_dict__inner() == {1: "test_1", 2: "test_2"}
        assert victim.get_dict__outer() == {0: "test_1", 1: "test_2"}

    def test__contains(self):
        # --------------------------------------------------
        victim = self.Victim(0, 1, "test_%s", 1)

        # indexes
        assert 0 in victim
        assert 1 not in victim
        assert 2 not in victim

        # values
        assert "test_0" not in victim
        assert "test_1" in victim
        assert "test_2" not in victim

        # --------------------------------------------------
        victim = self.Victim(0, 2, "test_%s", 1)

        # indexes
        assert 0 in victim
        assert 1 in victim
        assert 2 not in victim

        # values
        assert "test_0" not in victim
        assert "test_1" in victim
        assert "test_2" in victim

        # --------------------------------------------------
        victim = self.Victim(1, 2, "test_%s", 0)

        # indexes
        assert 0 not in victim
        assert 1 in victim
        assert 2 in victim

        # values
        assert "test_0" in victim
        assert "test_1" in victim
        assert "test_2" not in victim

    def test__getitem(self):
        # --------------------------------------------------
        victim = self.Victim(0, 1, "test_%s", 0)
        # indexes
        assert victim[0] == "test_0"
        try:
            result = victim[1]
            assert False
        except:
            assert True

        # values
        assert victim["test_0"] == 0
        try:
            result = victim["test_1"]
            assert False
        except:
            assert True

        # --------------------------------------------------
        victim = self.Victim(0, 1, "test_%s", 1)
        # indexes
        try:
            result = victim[0]
            assert False
        except:
            assert True
        assert victim[1] == "test_1"


        # values
        try:
            result = victim["test_0"]
            assert False
        except:
            assert True
        assert victim["test_1"] == 1

    def test__listed_index__by_outer(self):
        # --------------------------------------------------
        victim = self.Victim(0, 2, "test_%s", 0)
        assert victim.get_dict__inner() == {0: "test_0", 1: "test_1"}
        assert victim.get_dict__outer() == {0: "test_0", 1: "test_1"}

        assert list(victim.get_dict__outer()) == [0, 1]
        assert list(victim.get_dict__inner()) == [0, 1]

        assert victim.get_listed_index__by_outer(0) == 0
        assert victim.get_listed_index__by_outer(1) == 1
        try:
            assert victim.get_listed_index__by_outer(2)
            assert False
        except:
            assert True

        # --------------------------------------------------
        victim = self.Victim(0, 2, "test_%s", 1)
        assert victim.get_dict__inner() == {1: "test_1", 2: "test_2"}
        assert victim.get_dict__outer() == {0: "test_1", 1: "test_2"}

        assert list(victim.get_dict__outer()) == [0, 1]
        assert list(victim.get_dict__inner()) == [1, 2]

        assert victim.get_listed_index__by_outer(0) == 0
        assert victim.get_listed_index__by_outer(1) == 1
        try:
            assert victim.get_listed_index__by_outer(2)
            assert False
        except:
            assert True

    def test__listed_index__by_value(self):
        # --------------------------------------------------
        victim = self.Victim(0, 2, "test_%s", 0)
        assert victim.get_dict__inner() == {0: "test_0", 1: "test_1"}
        assert victim.get_dict__outer() == {0: "test_0", 1: "test_1"}

        assert victim.get_listed_index__by_value("test_0") == 0
        assert victim.get_listed_index__by_value("test_1") == 1
        try:
            assert victim.get_listed_index__by_value("test_2")
            assert False
        except:
            assert True

        # --------------------------------------------------
        victim = self.Victim(0, 2, "test_%s", 1)
        assert victim.get_dict__inner() == {1: "test_1", 2: "test_2"}
        assert victim.get_dict__outer() == {0: "test_1", 1: "test_2"}

        try:
            assert victim.get_listed_index__by_value("test_0")
            assert False
        except:
            assert True
        assert victim.get_listed_index__by_value("test_1") == 0
        assert victim.get_listed_index__by_value("test_2") == 1


# =====================================================================================================================
class Test__NamesIndexed_Base:
    @classmethod
    def setup_class(cls):
        class NamesIndexed_Example(NamesIndexed_Base):
            name0 = 0
            name1 = 1
            TAIL = NamesIndexed_Templated(2, 2, "%s")

        cls.victim = NamesIndexed_Example()
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
    def test__exx_1__overlayd_1(self):
        class NamesIndexed_Example2(NamesIndexed_Base):
            name0 = 0
            name1 = 1
            name2 = 1
            TAIL = NamesIndexed_Templated(2, 2, "%s")

        try:
            victim = NamesIndexed_Example2()
            assert False
        except:
            pass

    def test__exx_1__overlayd_2(self):
        class NamesIndexed_Example2(NamesIndexed_Base):
            name0 = 0
            name1 = 1
            TAIL = NamesIndexed_Templated(1, 2, "%s")

        try:
            victim = NamesIndexed_Example2()
            assert False
        except:
            pass

    def test__exx_1__skipped_1(self):
        class NamesIndexed_Example2(NamesIndexed_Base):
            name0 = 0
            name1 = 1
            TAIL = NamesIndexed_Templated(2, 2, "%s")
            TAIL2 = NamesIndexed_Templated(20, 2, "%s")

        try:
            victim = NamesIndexed_Example2()
            assert False
        except:
            pass

    def test__exx_1__skipped_2(self):
        class NamesIndexed_Example2(NamesIndexed_Base):
            name0 = 0
            # name1 = 1
            TAIL = NamesIndexed_Templated(2, 2, "%s")

        try:
            victim = NamesIndexed_Example2()
            assert False
        except:
            pass

    def test_1__main_1__getitem(self):
        assert self.victim[0] == "name0"
        assert self.victim[1] == "name1"
        assert self.victim[2] == "1"
        assert self.victim[3] == "2"
        try:
            assert self.victim[4]
            assert False
        except:
            pass

        assert self.victim["name0"] == 0
        assert self.victim["name1"] == 1
        assert self.victim["1"] == 2
        assert self.victim["2"] == 3
        try:
            assert self.victim["3"]
            assert False
        except:
            pass

    def test_1__main_2__contain(self):
        assert 0 in self.victim
        assert 1 in self.victim
        assert 2 in self.victim
        assert 3 in self.victim
        assert 4 not in self.victim
        assert 5 not in self.victim

        assert "name0" in self.victim
        assert "name1" in self.victim
        assert "attr11111" not in self.victim

        assert "0" not in self.victim
        assert "1" in self.victim
        assert "2" in self.victim
        assert "3" not in self.victim
        assert "4" not in self.victim
        assert "5" not in self.victim

    def test_2__sub_2__getitem(self):
        try:
            assert self.victim.TAIL[0]
            assert False
        except:
            pass
        assert self.victim.TAIL[1] == "1"
        assert self.victim.TAIL[2] == "2"
        try:
            assert self.victim[3]
            assert False
        except:
            pass

        # 2--------
        try:
            assert self.victim.TAIL["0"]
            assert False
        except:
            pass
        assert self.victim.TAIL["1"] == 1
        assert self.victim.TAIL["2"] == 2
        try:
            assert self.victim.TAIL["3"]
            assert False
        except:
            pass

    def test_2__sub_2__contain(self):
        assert 0 not in self.victim.TAIL
        assert 1 not in self.victim.TAIL
        assert 2 in self.victim.TAIL
        assert 3 in self.victim.TAIL
        assert 4 not in self.victim.TAIL
        assert 5 not in self.victim.TAIL

        assert "0" not in self.victim.TAIL
        assert "1" in self.victim.TAIL
        assert "2" in self.victim.TAIL
        assert "3" not in self.victim.TAIL
        assert "4" not in self.victim.TAIL
        assert "5" not in self.victim.TAIL

    def test__count(self):
        class Victim(NamesIndexed_Base):
            name0 = 0
            name1 = 1
            TAIL = NamesIndexed_Templated(2, 2, "%s")

        assert Victim().count() == 4

        class Victim(NamesIndexed_Base):
            name0 = 0
            name1 = 1
            TAIL = NamesIndexed_Templated(2, 2, "%s")
            TAIL2 = NamesIndexed_Templated(4, 2, "%s")

        assert Victim().count() == 6


# =====================================================================================================================
