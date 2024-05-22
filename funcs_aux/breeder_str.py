from typing import *
from annot_attrs import AnnotsNested


# =====================================================================================================================
class Exx__IndexOverlayed(Exception):
    pass


class Exx__IndexNotSet(Exception):
    pass


class Exx__ItemNotExists(Exception):
    """
    not exists INDEX (out of range) or NAME not in defined values
    """
    pass


class Exx__StartOuterNONE_UsedInStackByRecreation(Exception):
    """
    in stack it will be recreate automatically! so dont use in pure single BreederStrSeries!
    """
    pass


# =====================================================================================================================
class BreederStrSeries(NamedTuple):
    """
    PATTERN FOR BREEDING ONE TYPE OF TEMPLATE STYLE
    used and created special for BreederStrStack
    """
    START_OUTER: int | None  # None used only for recreation in Stack!!! for auto
    COUNT: int
    TEMPLATE: str = "%s"
    START_INNER: int = 1    # just a starting number in values!

    def _raise_if_start_outer_none(self) -> NoReturn | None:
        if self.START_OUTER is None:
            raise Exx__StartOuterNONE_UsedInStackByRecreation()

    def __contains__(self, item: Union[int, str]) -> Union[bool, NoReturn]:
        """
        :param item: one of: 1=OUTER_INDEX (not self-INNER!!!) or 2=ORIGINAL value_NAME
            couse of we usually need to compare OUTER indexes or original VALUES!
        :return:
        """
        self._raise_if_start_outer_none()

        if isinstance(item, int):
            return self.START_OUTER <= item < (self.START_OUTER + self.COUNT)

        elif isinstance(item, str):
            return item in self.get_dict__outer().values()

    def __getitem__(self, item: Union[int, str]) -> Union[int, str, NoReturn]:
        """

        :param item: INTERNAL INDEX! NOT OUTER!!!
        :return: INTERNAL NAME
        """
        _DATA = self.get_dict__inner()

        if item in _DATA:
            return _DATA[item]

        if item in _DATA.values():
            for key, value in _DATA.items():
                if item == value:
                    return key

        msg = f"{item=}"
        raise Exx__ItemNotExists(msg)

    def get_dict__outer(self) -> Dict[int, str] | NoReturn:
        self._raise_if_start_outer_none()

        result_outer_sub = {}
        for index in range(self.COUNT):
            pos = index + self.START_INNER
            value = self.TEMPLATE % pos

            index_outer = index + self.START_OUTER
            result_outer_sub.update({index_outer: value})
        return result_outer_sub

    def get_dict__inner(self) -> Dict[int, str] | NoReturn:
        self._raise_if_start_outer_none()

        result_inner = {}
        for index in range(self.COUNT):
            pos = index + self.START_INNER
            value = self.TEMPLATE % pos

            result_inner.update({pos: value})
        return result_inner

    def get_listed_index__by_outer(self, index: int) -> int | NoReturn:
        """
        usually we have outer index and need to be able get from other list value according to listed index fom this template!

        :param index:
        :return:
        """
        result = 0
        if index in self:
            for _key in self.get_dict__outer():
                if _key == index:
                    return result
                else:
                    result += 1
        else:
            raise Exx__ItemNotExists()

    def get_listed_index__by_value(self, value: str) -> int | NoReturn:
        result = 0
        if value in self:
            for _value in self.get_dict__outer().values():
                if _value == value:
                    return result
                else:
                    result += 1
        else:
            raise Exx__ItemNotExists()


# =====================================================================================================================
class BreederStrStack(AnnotsNested):
    """
    created specially for applying in Gui tableModels (PyQt5) as header structure

    VULNERABILITIES # FIXME:
    ------------------------
    1. if exists same names cause of patterns - it would return always first index!
        class BreederStrStack_Example2(BreederStrStack):
            TAIL = BreederStrSeries(2, 2, "%s")
            TAIL2 = BreederStrSeries(4, 2, "%s")

        BreederStrStack_Example2()["2"] = 1

    DEFINE
    ------
    !. names (as attributes)
        - dont use underscore as first simble
        - it will be as value for index
    1. dont keep SKIPPED indexes - use all final range!
    2. BreederStrSeries
     - use if need template for some range
     - use any count of such items

    USAGE
    -----
    1. COMPARE BY INDEXES OVER NAME
    if colIndex == MyHeders.attr0:
        pass

    2. GET HEADER NAME BY INDEX or INDEX by NAME!
    headerName = MyHeders[colIndex]
    headerIndex = MyHeders[colName]

    RULES
    -----
    1. use always any ANNOTATIONS for your indexes!!
    2. hide names by using underscore!
    3. use None for AUTOINDEX!!!
    4. nesting available with correct order!
        class ClsFirst(BreederStrStack):
            atr1: int
            atr3: int = None

        class ClsLast(BreederStrStack):
            atr2: int = None
            atr4: int

        for key, value in ClsLast.annotations__get_nested_list().items():
            print(f"{key}:{value}")

        # atr1:<class 'int'>
        # atr3:<class 'int'>
        # atr2:<class 'int'>
        # atr4:<class 'int'>
    """
    # settings ----------------------
    _RAISE_IF_INDEX_SKIPPED: bool = True

    # aux ----------------------
    _DATA: dict[int, str] = {}

    def __init__(self):
        index_last = 0
        result = {}

        # ATTRS ------------------
        attrs: List[str] = []
        for attr in self.annotations__get_nested():
            if not attr.startswith("_") and not callable(getattr(self, attr)):
                attrs.append(attr)

        # WORK -------------------
        for attr in attrs:
            index = getattr(self, attr)

            # apply AUTO ----------
            if index is None:
                index = index_last + 1
                index_last = index
                setattr(self, attr, index)

            # work INT ----------
            if isinstance(index, int):
                if index in result:
                    msg = f"{index=} from {result=}"
                    raise Exx__IndexOverlayed(msg)
                result.update({index: attr})
                index_last = index

            # work BreederStrSeries ----------
            if isinstance(index, BreederStrSeries):
                # apply AUTO by recreation
                if index.START_OUTER is None:
                    index = BreederStrSeries(index_last + 1, index.COUNT, index.TEMPLATE, index.START_INNER)
                    setattr(self, attr, index)

                # work
                result_sub_dict = index.get_dict__outer()
                for key, value in result_sub_dict.items():
                    if key in result:
                        msg = f"{key=} from {result_sub_dict=}"
                        raise Exx__IndexOverlayed(msg)
                    result.update({key: value})
                    index_last = key

        # RESULT -------------------
        self._DATA = dict(sorted(result.items()))

        # CHECK SKIPPED -----------
        if self._RAISE_IF_INDEX_SKIPPED:
            self.raise_if_index_skipped()

    def __getitem__(self, item: Union[int, str]) -> Union[int, str]:
        if item in self._DATA:
            return self._DATA[item]

        if item in self._DATA.values():
            for name, value in self._DATA.items():
                if item == value:
                    return name

        msg = f"{item=}"
        raise Exx__ItemNotExists(msg)

    def __contains__(self, item: Union[int, str]) -> bool:
        """
        :param item: OUTER INDEX (not self INNER!!!) or inner value NAME
        :return:
        """
        return item in self._DATA or item in self._DATA.values()

    def count(self) -> int:
        return len(self._DATA)

    @classmethod
    def raise_if_index_skipped(cls) -> None | NoReturn:
        index_prev = None
        for index in cls._DATA:
            if index_prev is None:
                index_prev = index
                continue

            if index - index_prev != 1:
                msg = f"index [{index-1}]"
                raise Exx__IndexNotSet(msg)
            index_prev = index


# =====================================================================================================================
class BreederStrStack_Example(BreederStrStack):
    name0: int = 0
    name1: int = 1
    TAIL: BreederStrSeries = BreederStrSeries(2, 2, "%s")


class BreederStrStack_Example__BestUsage(BreederStrStack):
    INDEX: int = 0
    TESTCASE: int = None
    ASYNC: int = None
    STARTUP: int = None
    DUTS: BreederStrSeries = BreederStrSeries(None, 10, "TC_DUT_%s")


# =====================================================================================================================
