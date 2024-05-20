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

        # BLANC --------------------
        assert Victim.INDEX is None
        assert Victim.groups_count__existed() is None
        try:
            assert Victim._GROUPS == {}
            assert False
        except:
            assert True

        # GENERATE --------------------
        Victim.generate__objects()
        assert Victim.INDEX is None
        assert Victim._GROUPS == {}
        assert Victim.groups_count__existed() == 0

        assert Victim.group_get__objects("ITEM_SINGLE") is None
        assert Victim.group_get__objects("ITEM_LIST") is None

    def test__with_groups__single(self):
        class Victim(self.Victim):
            COUNT = 2
            CLS_SINGLE__ITEM_SINGLE = ItemSingle

        # BLANC --------------------
        assert Victim.INDEX is None

        assert Victim.groups_count__existed() is None

        assert Victim.group_get__type("ITEM_SINGLE") == BreederObjectList_GroupType.SINGLE
        assert Victim.group_get__type("ITEM_LIST") == BreederObjectList_GroupType.NOT_EXISTS

        assert Victim.group_check__exists("ITEM_SINGLE") is True
        assert Victim.group_check__exists("ITEM_LIST") is False

        assert Victim.group_get__objects("ITEM_SINGLE") is None
        assert Victim.group_get__objects("ITEM_LIST") is None
        try:
            assert Victim._GROUPS == {}
            assert False
        except:
            assert True

        try:
            assert isinstance(Victim.ITEM_SINGLE, ItemSingle)
            assert False
        except AttributeError:
            assert True

        # GENERATE --------------------
        Victim.generate__objects()
        assert Victim.INDEX is None
        assert Victim.groups_count__existed() == 1

        assert Victim.group_get__type("ITEM_SINGLE") == BreederObjectList_GroupType.SINGLE
        assert Victim.group_get__type("ITEM_LIST") == BreederObjectList_GroupType.NOT_EXISTS

        assert Victim.group_check__exists("ITEM_SINGLE") is True
        assert Victim.group_check__exists("ITEM_LIST") is False

        assert Victim.group_get__objects("ITEM_SINGLE") is Victim._GROUPS["ITEM_SINGLE"]
        assert Victim.group_get__objects("ITEM_LIST") is None

        assert list(Victim._GROUPS) == ["ITEM_SINGLE", ]
        assert isinstance(Victim._GROUPS["ITEM_SINGLE"], ItemSingle)

        assert isinstance(Victim.ITEM_SINGLE, ItemSingle)

        try:
            assert isinstance(Victim.ITEM_LIST, ItemList)
            assert False
        except AttributeError:
            assert True

        # INSTANCE -------------------
        assert Victim(0).ITEM_SINGLE is Victim._GROUPS["ITEM_SINGLE"]
        assert isinstance(Victim(0).ITEM_SINGLE, ItemSingle)

    def test__with_groups__list(self):
        class Victim(self.Victim):
            COUNT = 2
            CLS_LIST__ITEM_LIST = ItemList

        # BLANC --------------------
        assert Victim.INDEX is None
        assert Victim.groups_count__existed() is None

        assert Victim.group_get__type("ITEM_SINGLE") == BreederObjectList_GroupType.NOT_EXISTS
        assert Victim.group_get__type("ITEM_LIST") == BreederObjectList_GroupType.LIST

        assert Victim.group_check__exists("ITEM_SINGLE") is False
        assert Victim.group_check__exists("ITEM_LIST") is True

        assert Victim.group_get__objects("ITEM_SINGLE") is None
        assert Victim.group_get__objects("ITEM_LIST") is None

        try:
            assert Victim._GROUPS == {}
            assert False
        except:
            assert True

        try:
            assert isinstance(Victim.ITEM_LIST, ItemList)
            assert False
        except AttributeError:
            assert True

        # GENERATE --------------------
        Victim.generate__objects()
        assert Victim.INDEX is None

        assert Victim.groups_count__existed() == 1

        assert Victim.group_get__type("ITEM_SINGLE") == BreederObjectList_GroupType.NOT_EXISTS
        assert Victim.group_get__type("ITEM_LIST") == BreederObjectList_GroupType.LIST

        assert Victim.group_check__exists("ITEM_SINGLE") is False
        assert Victim.group_check__exists("ITEM_LIST") is True

        assert Victim.group_get__objects("ITEM_SINGLE") is None
        assert Victim.group_get__objects("ITEM_LIST") == Victim._GROUPS["ITEM_LIST"]

        assert list(Victim._GROUPS) == ["ITEM_LIST", ]
        assert len(Victim._GROUPS["ITEM_LIST"]) == Victim.COUNT

        assert isinstance(Victim._GROUPS["ITEM_LIST"][0], ItemList)
        assert isinstance(Victim.LIST__ITEM_LIST[0], ItemList)

        assert len(Victim.group_get__objects("ITEM_LIST")) == len(Victim._GROUPS["ITEM_LIST"]) == Victim.COUNT

        try:
            assert isinstance(Victim.ITEM_SINGLE, ItemList)
            assert False
        except AttributeError:
            assert True

        # INSTANCE -------------------
        assert Victim(0).ITEM_LIST is Victim._GROUPS["ITEM_LIST"][0]
        assert isinstance(Victim(0).ITEM_LIST, ItemList)


# =====================================================================================================================
