from typing import *
import time
from object_info import ObjectInfo


# =====================================================================================================================
def collection__get_original_item__case_type_insensitive(item: Any, collection: Collection) -> Optional[Any]:
    """
    NOTES:
    1. DONT TRY

    :param item:
    :param collection:
    :return:
    """
    # FIXME: what if several items? - it is not useful!!! returning first is most expected!
    for value in list(collection):
        if str(value).lower() == str(item).lower():
            return value


# =====================================================================================================================
