import pytest

from funcs_aux import *
from funcs_aux import NamesIndexed_Base


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


# =====================================================================================================================
