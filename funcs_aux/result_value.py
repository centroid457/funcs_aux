from typing import *
from funcs_aux import *
from object_info import *


# =====================================================================================================================
TYPE__FUNC = Callable[..., Any]
TYPE__FUNC_UNDER_VALUE = Callable[[Any], Any]
TYPE__ARGS = Tuple[Any, ...]
TYPE__KWARGS = Dict[str, Any]


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
