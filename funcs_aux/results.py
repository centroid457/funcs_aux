from typing import *


# =====================================================================================================================
TYPE__FUNC = Callable[..., Any]
TYPE__ARGS = Tuple[Any, ...]
TYPE__KWARGS = Dict[str, Any]


# =====================================================================================================================
class ResultValue(NamedTuple):
    """
    MAIN GOAL:
    ----------
    solve NONE-value as result ambiguity by simple way

    MAIN RULES:
    -----------
    return object if you get final result!
    return None if there are any errors in execution

    USAGE:
    ------
    def func(a, b) -> Optional(ResultValue):
        if a in b:
            return ResultValue(a)
        else:
            return

    result = func("None", [None, ])
    assert result is None

    result = func(None, [None, ])
    assert result == ResultValue(None)

    if result:
        print(result.RESULT_VALUE)
        print(result())
    """
    RESULT_VALUE: Any

    def __call__(self, *args, **kwargs) -> Any:
        return self.run()

    def run(self) -> Any:
        return self.RESULT_VALUE


# =====================================================================================================================
class ResultFunc:
    """
    MAIN GOAL:
    ----------
    use always Object as result with absolut unambiguity!

    MAIN RULES:
    -----------
    return object in any cases (if you get final result or if there are any errors in execution)!
    """
    # SETTINGS -----------------------------
    RUN_ON_INIT: bool = None

    # INPUT ---------------------------------
    FUNC: TYPE__FUNC
    ARGS: TYPE__ARGS = None
    KWARGS: TYPE__KWARGS = None

    # RESULT --------------------------------
    RESULT_VALUE: Optional[Any] = None
    RESULT_EXX: Optional[Exception] = None
    RESULT_OK: bool

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
        self._clear_result()

        if args:
            self.ARGS = args
        if kwargs:
            self.KWARGS = kwargs

        # WORK ---------------
        try:
            self.RESULT_VALUE = self.FUNC(*self.ARGS, **self.KWARGS)
        except Exception as exx:
            self.RESULT_EXX = exx

        return self

    def _clear_result(self) -> None:
        self.RESULT_VALUE = None
        self.RESULT_EXX = None

    @property
    def RESULT_OK(self) -> bool:
        return self.RESULT_EXX is None


# =====================================================================================================================
class ChainManager:
    pass


# =====================================================================================================================
