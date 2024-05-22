from typing import *

from enum import Enum, auto


# =====================================================================================================================
TYPE__BREED_RESULT__ITEM = Union[Any, Exception]
TYPE__BREED_RESULT__GROUP = Union[
    TYPE__BREED_RESULT__ITEM,        # SINGLE variant
    list[TYPE__BREED_RESULT__ITEM]   # LIST variant
]
TYPE__BREED_RESULT__GROUPS = dict[str, TYPE__BREED_RESULT__GROUP]


# =====================================================================================================================
class Exx__BreederObjectList_GroupsNotGenerated(Exception):
    pass


class Exx__BreederObjectList_GroupNotExists(Exception):
    pass


class Exx__BreederObjectList_ObjCantAccessIndex(Exception):
    pass


# =====================================================================================================================
class BreederObjectList_GroupType(Enum):
    SINGLE = auto()
    LIST = auto()
    NOT_EXISTS = auto()


# =====================================================================================================================
class BreederObjectList:
    """
    class which keep all objects in one place!
    useful for multyObject systems.

    If you need just one object_instance for all duts - use direct attribute,
    else use LIST__*NAME* and dont forget to create annotation for direct Indexed item access!

    so you could
    - pass just one instance into all other classes!
    - check all devices for PRESENT (or else) in one place!
    - init all and check correctness for all

    AFTER GENERATING OBJECTS - ACCESS TO OBJECTS LIST USED OVER THE CLASS!!!
        OBJS_CLS = BreederObjectList
        OBJS = OBJS_CLS()
        devs = OBJS_CLS.LIST__DEV
    """
    # SETTINGS ----------------------
    COUNT: int = 1

    # usage EXAMPLES ------------------------------------------------------
    # CLS_LIST__DUT: Type[DutBase] = DutBase
    # LIST__DUT: List[DutBase]
    # DUT: DutBase

    # CLS_SINGLE__ATC: Callable[..., DeviceBase]
    # ATC: DeviceBase

    # AUX ----------------------------------------------------------
    # definitions -----
    _STARTSWITH__DEFINE__CLS_LIST: str = "CLS_LIST__"
    _STARTSWITH__DEFINE__CLS_SINGLE: str = "CLS_SINGLE__"

    # access ----------
    _STARTSWITH__ACCESS__OBJECT_LIST: str = "LIST__"

    # -----------------
    _GROUPS: dict[str, Union[Any, list[Any]]]

    # instance ---
    INDEX: int | None = None    # index used only in OBJECT INSTANCE

    def __init__(self, index: int):
        """
        init only when you need to do access to exact items!
        """
        self.INDEX = index      # need first!
        super().__init__()
        # self.generate__objects()

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def generate__objects(cls) -> None:
        """exact and only one method to Gen all objects - dont forget to call it!
        """
        if cls.groups_count__existed():
            return

        # WORK --------------------------------------
        cls._GROUPS = {}
        for attr_name in dir(cls):
            # LIST --------------------------------------
            if attr_name.startswith(cls._STARTSWITH__DEFINE__CLS_LIST):
                group_name = attr_name.removeprefix(cls._STARTSWITH__DEFINE__CLS_LIST)
                obj_list__name = f"{cls._STARTSWITH__ACCESS__OBJECT_LIST}{group_name}"
                obj_list__value = []
                for index in range(cls.COUNT):
                    obj_cls = getattr(cls, attr_name)
                    try:
                        obj_instance = obj_cls(index)
                    except Exception as exx:
                        obj_instance = exx
                    obj_list__value.append(obj_instance)

                # apply GROUP to class -------
                setattr(cls, obj_list__name, obj_list__value)
                cls._GROUPS.update({group_name: obj_list__value})

            # SINGLE --------------------------------------
            if attr_name.startswith(cls._STARTSWITH__DEFINE__CLS_SINGLE):
                group_name = attr_name.removeprefix(cls._STARTSWITH__DEFINE__CLS_SINGLE)
                obj_cls = getattr(cls, attr_name)
                try:
                    obj_instance = obj_cls()
                except Exception as exx:
                    obj_instance = exx
                # apply -------
                setattr(cls, group_name, obj_instance)
                cls._GROUPS.update({group_name: obj_instance})

    # -----------------------------------------------------------------------------------------------------------------
    def __getattr__(self, item: str) -> Union[None, Any, NoReturn]:
        if self.INDEX is None:
            return

        # ACCESS TO OBJECT ----------------------------
        if self.group_check__exists(item):
            group_objs = self._GROUPS[item]
            if isinstance(group_objs, list):
                obj = group_objs[self.INDEX]
            else:
                obj = group_objs
            return obj

        # FINAL not found -----------------------------
        msg = f"{item=}/{self.INDEX=}"
        print(msg)
        raise Exx__BreederObjectList_GroupNotExists(msg)

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def groups_check__generated(cls) -> bool:
        """
        check if objects/groups was generated
        """
        return hasattr(cls, "_GROUPS")

    @classmethod
    def groups_count__existed(cls) -> int | None:
        """
        work only after called generate__objects(),
        so if you wasnot call generate__objects it will return None!
        """
        if cls.groups_check__generated():
            return len(cls._GROUPS)

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def group_check__exists(cls, name: str) -> bool:
        return cls.group_get__type(name) != BreederObjectList_GroupType.NOT_EXISTS

    @classmethod
    def group_get__type(cls, name: str) -> BreederObjectList_GroupType:
        if f"{cls._STARTSWITH__DEFINE__CLS_SINGLE}{name}" in dir(cls):
            return BreederObjectList_GroupType.SINGLE

        if f"{cls._STARTSWITH__DEFINE__CLS_LIST}{name}" in dir(cls):
            return BreederObjectList_GroupType.LIST

        return BreederObjectList_GroupType.NOT_EXISTS

    @classmethod
    def group_get__objects(cls, name: str) -> Union[None, Any, list[Any]]:
        if cls.group_check__exists(name) and cls.groups_check__generated():
            return cls._GROUPS[name]

    @classmethod
    def group_call__(cls, meth: str, group: str | None = None, *args, **kwargs) -> Union[NoReturn, TYPE__BREED_RESULT__GROUP, TYPE__BREED_RESULT__GROUPS]:
        """
        call one method on exact group (every object in group) or all groups (every object in all groups).
        created specially for call connect/disconnect for devices in TP.

        :param meth:
        :param group:

        :param args:
        :param kwargs:
        :return:
            RAISE only if passed group and group is not exists! or groups are not generated
        """
        if not cls.groups_check__generated():
            raise Exx__BreederObjectList_GroupsNotGenerated()

        # CALL ON ALL GROUPS -------------------------------------------------
        if group is None:
            results = {}
            for group_name in cls._GROUPS:
                results.update({group_name: cls.group_call__(meth, group_name, *args, **kwargs)})
            return results

        # if group is not exists ---------------------------------------------
        if not cls.group_check__exists(group):
            raise Exx__BreederObjectList_GroupNotExists(group)

        # EXACT ONE GROUP ----------------------------------------------------
        group_objs = cls._GROUPS[group]

        if isinstance(group_objs, list):
            results = []
            for obj in group_objs:
                try:
                    obj_meth = getattr(obj, meth)
                    obj_result = obj_meth(*args, **kwargs)
                except Exception as exx:
                    obj_result = exx
                results.append(obj_result)
        else:
            obj = group_objs
            try:
                obj_meth = getattr(obj, meth)
                obj_result = obj_meth(*args, **kwargs)
            except Exception as exx:
                obj_result = exx
            results = obj_result

        return results


# =====================================================================================================================
