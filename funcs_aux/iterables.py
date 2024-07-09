from typing import *
from funcs_aux import ResultValue


# =====================================================================================================================
TYPE__ITERABLE_PATH_KEY = Union[str, int]
TYPE__ITERABLE_PATH_ORIGINAL = List[TYPE__ITERABLE_PATH_KEY]
TYPE__ITERABLE_PATH_EXPECTED = Union[TYPE__ITERABLE_PATH_KEY, TYPE__ITERABLE_PATH_ORIGINAL]
TYPE__ITERABLE = Union[dict, list, tuple, set, Iterable]


# =====================================================================================================================
class Iterables:
    """
    collect universal funcs which work with collections
    """
    # AUX ---------------------
    DATA: TYPE__ITERABLE
    PATH: List[TYPE__ITERABLE_PATH_KEY]

    def __init__(self, data: Optional[TYPE__ITERABLE] = None):
        self.DATA = data or {}
        self.PATH = []

    def item__get_original__case_insensitive(
            self,
            item_expected: Any,
            data: Optional[TYPE__ITERABLE] = None
    ) -> Optional[ResultValue]:
        """
        get FIRST original item from any collection by comparing str(expected).lower()==str(original).lower().

        NOTE:
        1. NONE RESULT__VALUE - RESOLVED!!!
        2. SEVERAL VALUES - not used! by now it is just FIRST matched!
            several items? - it is not useful!!! returning first is most expected!

        USEFUL in case-insensitive systems (like terminals or serial devices) or object structured by prefix-names:
        1. get key in dict
        2. find attribute name in objects

        :param data:
        :param item_expected:
        :return: actual item from collection
            None - if VALUE is unreachable
        """
        if data is None:
            data = self.DATA
        for value in list(data):
            if str(value).lower() == str(item_expected).lower():
                return ResultValue(value)

    def path__get_original(
            self,
            path_expected: TYPE__ITERABLE_PATH_EXPECTED,
            data: Optional[TYPE__ITERABLE] = None,
    ) -> Optional[ResultValue]:
        """
        NOTES:
        1. path used as address KEY for dicts and as INDEX for other listed data
        2. SEPARATOR_OUTPUT is only simple SLASH '/'!

        :param data:
        :param path_expected:
        :return:
            None - if path is unreachable/incorrect
            List[Any] - reachable path which could be used to get VALUE from data by chain data[i1][i2][i3]
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
                if not address_original:
                    return
                address_original = address_original.VALUE
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

        return ResultValue(path_original)

    def value_by_path__get(
            self,
            path_expected: TYPE__ITERABLE_PATH_EXPECTED,
            data: Optional[TYPE__ITERABLE] = None
    ) -> Optional[ResultValue]:
        if data is None:
            data = self.DATA

        # work ----------------------------
        path_original = self.path__get_original(path_expected, data)
        try:
            for path_part in path_original.VALUE:
                data = data[path_part]
        except:
            return

        return ResultValue(data)

    def value_by_path__set(
            self,
            path_expected: TYPE__ITERABLE_PATH_EXPECTED,
            value: Any,
            data: Optional[TYPE__ITERABLE] = None
    ) -> bool:
        if data is None:
            data = self.DATA

        # work ----------------------------
        path_original = self.path__get_original(path_expected, data)
        try:
            length = len(path_original.VALUE)
            for pos, path_part in enumerate(path_original.VALUE, start=1):
                if pos == length:
                    data[path_part] = value
                else:
                    data = data[path_part]
        except:
            return False

        return True


# =====================================================================================================================
