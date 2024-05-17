import pytest

from funcs_aux import *
from funcs_aux import BreederObjectList, BreederObjectList_GroupType, Exx__BreederObjectList_GroupNotExists


# =====================================================================================================================
class ItemSingle:
    def __init__(self):
        pass


class ItemList:
    def __init__(self, index: int):
        self.INDEX = index


# =====================================================================================================================
class Test__BreederObjectList:
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
    def test__wo_groups(self):
        class Victim(self.Victim):
            COUNT = 2

        assert Victim.INDEX is None
        assert Victim._GROUPS == {}
        assert Victim.groups_count__existed() == 0

        Victim.generate__objects()
        assert Victim.INDEX is None
        assert Victim._GROUPS == {}
        assert Victim.groups_count__existed() == 0

    def test__with_groups__single(self):
        class Victim(self.Victim):
            COUNT = 2
            CLS_SINGLE__ITEM_SINGLE = ItemSingle

        assert Victim.INDEX is None
        assert Victim.groups_count__existed() == 0
        assert Victim._GROUPS == {}
        try:
            assert isinstance(Victim.ITEM_SINGLE, ItemSingle)
            assert False
        except AttributeError:
            assert True

        assert Victim.group_get__type("ITEM_SINGLE") == BreederObjectList_GroupType.SINGLE

        Victim.generate__objects()
        assert Victim.INDEX is None
        assert Victim.groups_count__existed() == 1
        assert list(Victim._GROUPS) == ["ITEM_SINGLE", ]
        assert isinstance(Victim._GROUPS["ITEM_SINGLE"], ItemSingle)
        assert isinstance(Victim.ITEM_SINGLE, ItemSingle)
        assert Victim.group_get__type("ITEM_SINGLE") == BreederObjectList_GroupType.SINGLE

        try:
            assert isinstance(Victim.ITEM_SINGLE_222222, ItemSingle)
            assert False
        except AttributeError:
            assert True


# =====================================================================================================================
