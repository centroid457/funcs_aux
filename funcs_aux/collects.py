from typing import *
import time
from object_info import ObjectInfo


# =====================================================================================================================
Type__IterablePath_Key = Union[str, int]
Type__IterablePath_Original = List[Type__IterablePath_Key]
Type__IterablePath_Expected = Union[Type__IterablePath_Key, Type__IterablePath_Original]
Type__Iterable = Union[dict, list, tuple, set, Iterable]


class ResultWithStatus(NamedTuple):
    """
    main idea - solve NONE-value ambiguity
    by simple way
    """
    OK: Optional[bool] = None
    VALUE: Any = None


class Iterables:
    """
    collect universal funcs which work with collections
    """
    # AUX ---------------------
    DATA: Type__Iterable
    PATH: List[Type__IterablePath_Key]

    def __init__(self, data: Optional[Type__Iterable] = None):
        self.DATA = data or {}
        self.PATH = []

    def item__get_original__case_insensitive(
            self,
            item_expected: Any,
            data: Optional[Type__Iterable] = None
    ) -> Optional[Any]:
        """
        get FIRST original item from any collection by comparing str(expected).lower()==str(original).lower().

        NOTE:
        1. NONE VALUE - dont try find it! this is an exact special value!
        2. SEVERAL VALUES - not used! by now it is just FIRST matched!

        USEFUL in case-insensitive systems (like terminals or serial devices) or object structured by prefix-names:
        1. get key in dict
        2. find attribute name in objects

        :param data:
        :param item_expected:
        :return: actual item from collection
            None - if value is unreachable
        """
        # FIXME: what if several items? - it is not useful!!! returning first is most expected!

        if data is None:
            data = self.DATA
        for value in list(data):
            if str(value).lower() == str(item_expected).lower():
                return value

    def path__get_original(
            self,
            path_expected: Type__IterablePath_Expected,
            data: Optional[Type__Iterable] = None,
    ) -> Optional[Type__IterablePath_Original]:
        """
        NOTES:
        1. path used as address KEY for dicts and as INDEX for other listed data
        2. SEPARATOR is only simple SLASH '/'!

        :param data:
        :param path_expected:
        :return:
            None - if path is unreachable/incorrect
            List[Any] - reachable path which could be used to get value from data by chain data[i1][i2][i3]
        """
        if data is None:
            data = self.DATA

        # prepare type ----------------------------
        if isinstance(path_expected, (list, tuple, set)):
            path_expected = list(path_expected)
        else:
            path_expected = str(path_expected)

        if isinstance(path_expected, str):
            path_expected = path_expected.split("/")

        # work ----------------------------
        path_original = []
        for path_part in path_expected:
            if isinstance(data, dict):
                # DICT ----------------
                address_original = self.item__get_original__case_insensitive(path_part, data)
                if address_original is None:
                    return
                data = data[address_original]

            elif isinstance(data, (list, tuple)):
                # ITERABLE ----------------
                try:
                    address_original = int(path_part)
                    data = data[address_original]
                except:
                    return
            else:
                return
            path_original.append(address_original)

        return path_original

    def value__get_by_path(
            self,
            path_expected: Type__IterablePath_Expected,
            data: Optional[Type__Iterable] = None
    ) -> ResultWithStatus:
        if data is None:
            data = self.DATA

        # work ----------------------------
        path_original = self.path__get_original(path_expected, data)
        try:
            for path_part in path_original:
                data = data[path_part]
        except:
            return ResultWithStatus()

        return ResultWithStatus(True, data)


# =====================================================================================================================
