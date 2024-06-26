from typing import *
from _aux__release_files import release_files_update


# =====================================================================================================================
# VERSION = (0, 0, 3)   # 1/deprecate _VERSION_TEMPLATE from PRJ object +2/place update_prj here in __main__ +3/separate finalize attrs
VERSION = (0, 0, 4)     # add AUTHOR_NICKNAME_GITHUB for badges


# =====================================================================================================================
class PROJECT:
    # AUTHOR -----------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"
    AUTHOR_NICKNAME_GITHUB: str = "centroid457"

    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "funcs_aux"
    KEYWORDS: List[str] = [
        "functions",
        "auxiliary", "auxiliary funcs",
        "np funcs",
        "collections funcs",
        "strings funcs",
        "result object",
    ]
    CLASSIFIERS_TOPICS_ADD: List[str] = [
        # "Topic :: Communications",
        # "Topic :: Communications :: Email",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "useful funcs in one place"
    DESCRIPTION_LONG: str = """
    
Now its just a beginning!
Designed to collect useful funcs in one place!
"""
    FEATURES: List[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        [
            "RESULTS",
            "ResultValue - resolved ambiguity with None-result for any method result!",
            "ResultFunc",
         ],
        [
            "ITERABLES",
            "work with any iterable data by path/...",
        ],
        [
            "STRINGS",
        ],
    ]

    # HISTORY -----------------------------------------------
    VERSION: Tuple[int, int, int] = (0, 3, 5)
    TODO: List[str] = [
        "..."
    ]
    FIXME: List[str] = [
        "..."
    ]
    NEWS: List[str] = [
        "[testPrimitives] zero move into pytest_aux"
    ]

    # FINALIZE -----------------------------------------------
    VERSION_STR: str = ".".join(map(str, VERSION))
    NAME_INSTALL: str = NAME_IMPORT.replace("_", "-")


# =====================================================================================================================
if __name__ == '__main__':
    release_files_update(PROJECT)


# =====================================================================================================================
