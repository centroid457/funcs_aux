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
class ResultFunc:
    """
    GOAL
    ----
    use always Object as result with absolut unambiguity!

    it will return object in any cases (if you get final result or if there are any errors in execution)!
    """
    # SETTINGS -----------------------------
    RUN_ON_INIT: bool = None

    # INPUT ---------------------------------
    FUNC: TYPE__FUNC
    ARGS: TYPE__ARGS = None
    KWARGS: TYPE__KWARGS = None

    # RESULT --------------------------------
    RESULT__VALUE: Optional[Any] = None
    RESULT__EXX: Optional[Exception] = None
    RESULT__IS_CORRECT: bool

    def __init__(self, func: TYPE__FUNC, args: TYPE__ARGS = None, kwargs: TYPE__KWARGS = None, run_on_init: bool = None):
        self.RUN_ON_INIT = run_on_init

        self.FUNC = func
        self.ARGS = args or ()
        self.KWARGS = kwargs or {}

        if self.RUN_ON_INIT:
            self.run()

    def __call__(self, *args, **kwargs) -> Self:
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs) -> Self:
        # init ---------------
        self._clear()

        if args:
            self.ARGS = args
        if kwargs:
            self.KWARGS = kwargs

        # WORK ---------------
        try:
            self.RESULT__VALUE = self.FUNC(*self.ARGS, **self.KWARGS)
        except Exception as exx:
            self.RESULT__EXX = exx

        return self

    def _clear(self) -> None:
        self.RESULT__VALUE = None
        self.RESULT__EXX = None

    @property
    def RESULT__IS_CORRECT(self) -> bool:
        return self.RESULT__EXX is None

    @classmethod
    def get_result_or_exx(cls, source: Any | Callable) -> Any | Exception:
        """
        GOAL
        ----
        if callable meth/func - call and return result or Exx.
        else - return source.

        attempt to simplify result by not using try-sentence.
        """
        if TypeChecker.check__func_or_meth(source):
            try:
                result = source()
            except Exception as exx:
                result = exx
        else:
            result = source
        return result


# =====================================================================================================================
