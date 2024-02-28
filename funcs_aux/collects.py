from typing import *
import time
from object_info import ObjectInfo


# =====================================================================================================================
def collection__get_original_item__case_type_insensitive(item: Any, data: Collection) -> Optional[Any]:
    """
    NOTES:
    1. DONT TRY use None in keys

    USEFUL in case-insensitive systems (like terminals or serial devices):
    1. get key in dict
    2. find attribute name in objects

    :param item:
    :param data:
    :return:
    """
    # FIXME: what if several items? - it is not useful!!! returning first is most expected!
    for value in list(data):
        if str(value).lower() == str(item).lower():
            return value


def collection__path_create_original_names__case_type_insensitive(path: Union[str, List], data: Collection) -> Optional[List[Any]]:
    """
    NOTES:
    1. path used as address as index for list and key for dicts
    2. separator is simple SLASH!

    :param item:
    :param data:
    :return:
        None - if path is unreachable/incorrect
        List[Any] - reachable path which could be used to get value from data by chain data[i1][i2][i3]
    """

    # TODO: add tests!!!
    if not isinstance(path, list):
        path = str(path)

    if isinstance(path, str):
        path = path.split("/")

    # work ----------------------------
    result_path = []
    for path_part in path:
        if isinstance(data, dict):
            # DICT ----------------
            address_original = collection__get_original_item__case_type_insensitive(path_part, data)
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
        result_path.append(address_original)

    return result_path


# =====================================================================================================================
