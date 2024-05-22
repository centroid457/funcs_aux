# =====================================================================================================================
# VERSION = (0, 0, 1)   # use import EXACT_OBJECTS! not *
#   from .main import *                 # INcorrect
#   from .main import EXACT_OBJECTS     # CORRECT


# =====================================================================================================================
from .arrays import array_2d_get_compact_str
from .iterables import (
    # BASE
    Iterables,

    # AUX

    # TYPES
    TYPE__ITERABLE_PATH_KEY,
    TYPE__ITERABLE_PATH_ORIGINAL,
    TYPE__ITERABLE_PATH_EXPECTED,
    TYPE__ITERABLE,

    # EXX
)
from .results import (
    # BASE
    ResultValue,
    ResultFunc,

    ResultExpect_Base,
    ResultExpect_Step,
    ResultExpect_Chain,

    # AUX

    # TYPES
    TYPE__FUNC,
    TYPE__FUNC_UNDER_VALUE,
    TYPE__ARGS,
    TYPE__KWARGS,

    # EXX
)
from .strings import (
    # BASE
    Strings,

    # AUX

    # TYPES
    TYPES_ELEMENTARY_SINGLE,
    TYPES_ELEMENTARY_COLLECTION,
    TYPES_ELEMENTARY,
    TYPE_ELEMENTARY,

    # EXX
)
from .breeder_str import (
    # BASE
    BreederStrSeries,
    BreederStrStack,

    # AUX
    BreederStrStack_Example,
    BreederStrStack_Example__BestUsage,

    # EXX
    Exx__IndexOverlayed,
    Exx__IndexNotSet,
    Exx__ItemNotExists,
    Exx__StartOuterNONE_UsedInStackByRecreation,
)
from .breeder_objects import (
    # BASE
    BreederObjectList,

    # AUX
    BreederObjectList_GroupType,

    # TYPES
    TYPE__BREED_RESULT__ITEM,
    TYPE__BREED_RESULT__GROUP,
    TYPE__BREED_RESULT__GROUPS,

    # EXX
    Exx__BreederObjectList_GroupsNotGenerated,
    Exx__BreederObjectList_GroupNotExists,
    Exx__BreederObjectList_ObjCantAccessIndex,
)


# =====================================================================================================================
