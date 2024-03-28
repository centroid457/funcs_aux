from typing import *


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


# =====================================================================================================================
class NamesIndexed_Templated(NamedTuple):
    START_OUTER: int
    COUNT: int
    TEMPLATE: str = "%s"
    START_INNER: int = 1

    def __contains__(self, item: Union[int, str]) -> bool:
        """
        :param item: OUTER INDEX (not self INNER!!!) or inner value NAME
        :return:
        """
        if isinstance(item, int):
            return self.START_OUTER <= item < (self.START_OUTER + self.COUNT)

        elif isinstance(item, str):
            return item in self.get_dict__outer().values()

    def __getitem__(self, item: Union[int, str]) -> Union[int, str]:
        """

        :param item: INTERNAL INDEX! NOT OUTER!!!
        :return: INTERNAL NAME
        """
        _DATA = self.get_dict__inner()

        if item in _DATA:
            return _DATA[item]

        if item in _DATA.values():
            for name, value in _DATA.items():
                if item == value:
                    return name

        msg = f"{item=}"
        raise Exx__ItemNotExists(msg)

    def get_dict__outer(self) -> Dict[int, str]:
        result_outer_sub = {}
        for index in range(self.COUNT):
            pos = index + self.START_INNER
            value = self.TEMPLATE % pos

            index_outer = index + self.START_OUTER
            result_outer_sub.update({index_outer: value})
        return result_outer_sub

    def get_dict__inner(self) -> Dict[int, str]:
        result_inner = {}
        for index in range(self.COUNT):
            pos = index + self.START_INNER
            value = self.TEMPLATE % pos

            result_inner.update({pos: value})
        return result_inner


# =====================================================================================================================
class NamesIndexed_Base:
    """
    created specially for applying in Gui tableModels (PyQt5) as header structure

    VULNERABILITIES # FIXME:
    ------------------------
    1. if exists same names cause of patterns - it would return always first index!
        class NamesIndexed_Example2(NamesIndexed_Base):
            TAIL = NamesIndexed_Templated(2, 2, "%s")
            TAIL2 = NamesIndexed_Templated(4, 2, "%s")

        NamesIndexed_Example2()["2"] = 1

    DEFINE
    ------
    !. names (as attributes)
        - dont use underscore as first simble
        - it will be as value for index
    1. dont keep SKIPPED indexes - use all final range!
    2. NamesIndexed_Templated
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
    """
    _DATA: Dict[int, str] = {}

    def __init__(self):
        result = {}

        # ATTRS ------------------
        attrs: List[str] = []
        for attr in dir(self):
            if not attr.startswith("_") and not callable(getattr(self, attr)):
                attrs.append(attr)

        # WORK -------------------
        for value in attrs:
            index = getattr(self, value)
            if isinstance(index, int):
                if index in result:
                    msg = f"{index=} from {result=}"
                    raise Exx__IndexOverlayed(msg)
                result.update({index: value})
            elif isinstance(index, NamesIndexed_Templated):
                result_sub = index.get_dict__outer()
                for index in result_sub:
                    if index in result:
                        msg = f"{index=} from {result_sub=}"
                        raise Exx__IndexOverlayed(msg)
                result.update(result_sub)

        # CHECK SKIPPED -----------
        index_prev = None
        for index in sorted(result):
            if index_prev is None:
                index_prev = index
                continue

            if index - index_prev != 1:
                msg = f"index [{index-1}]"
                raise Exx__IndexNotSet(msg)
            index_prev = index

        # RESULT -------------------
        self._DATA = result

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


# =====================================================================================================================
class NamesIndexed_Example(NamesIndexed_Base):
    name0 = 0
    name1 = 1
    TAIL = NamesIndexed_Templated(2, 2, "%s")


class NamesIndexed_Example__BestUsage(NamesIndexed_Base):
    INDEX = 0
    TESTCASE = 1
    ASYNC = 2
    STARTUP = 3
    DUTS = NamesIndexed_Templated(4, 10, "TC_DUT_%s")


# =====================================================================================================================
