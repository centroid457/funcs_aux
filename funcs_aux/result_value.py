from typing import *
from funcs_aux import *
from object_info import *


# =====================================================================================================================
TYPE__FUNC = Callable[..., Any]
TYPE__FUNC_UNDER_VALUE = Callable[[Any], Any]

TYPE__ARGS = tuple[Any, ...] | Any  # Note: dont use None directly -will change to blankTuple!!! only withing Tuple!
TYPE__KWARGS = dict[str, Any]


# =====================================================================================================================
def args__ensure_tuple(args: TYPE__ARGS = None) -> tuple[Any, ...]:
    """
    CREATED SPECIALLY FOR
    ---------------------
    Valid
    but can be used in any funcs!

    :param args:
        NONE - is equivalent to not passed! if need exact None as value - pass it in container!!! like (None, )
        any elementaryCollection - will convert to tuple!
        for others (classes/instances/irerables/generators/...) will assumed as single Object!!! and applied in tuple!!!
    :return:
    """
    if args is None:
        result = ()
    elif not TypeChecker.check__elementary_collection(args):
        result = (args,)
    else:
        result = tuple(args)
    return result


# =====================================================================================================================
class ResultValue(NamedTuple):
    """
    GOAL
    ----
    1. solve NONE-VALUE as result ambiguity by simple way
    2. show/pass explicitly the EXACT VALUE like None/[]/()

    RULES
    -----
    return object if you get final result!
    return None if there are any errors in execution

    WHY: NamedTuple
    ----------------
    cause of we need to be able to compare different objects by values.
    maybe we need just add __eq__ method instead of it!!!

    USAGE
    -----
        from funcs_aux import *

        def func(a, b) -> Optional[ResultValue]:
            if a in b:
                return ResultValue(a)
            else:
                return

        result = func("None", [None, ])
        assert result is None

        result = func(None, [None, ])
        assert result == ResultValue(None)

        if result:
            print(result.VALUE)     # None
            print(result())         # None
    """
    VALUE: Any

    def __call__(self, *args, **kwargs) -> Any:
        # it is not so useful! but ... in future it should be deprecated!
        return self.VALUE


# =====================================================================================================================
