from typing import *


# =====================================================================================================================
class ResultSucceedSimple(NamedTuple):
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
    def func(a, b) -> Optional(ResultSucceedSimple):
        if a in b:
            return ResultSucceedSimple(a)
        else:
            return

    result = func("None", [None, ])
    assert result is None

    result = func(None, [None, ])
    assert result == ResultSucceedSimple(None)

    if result:
        print(result.VALUE)
        print(result())
    """
    VALUE: Any

    def __call__(self, *args, **kwargs) -> Any:
        return self.VALUE


# =====================================================================================================================
class ResultFull:
    """
    MAIN GOAL:
    ----------
    use always Object as result with absolut unambiguity!

    MAIN RULES:
    -----------
    return object in any cases (if you get final result or if there are any errors in execution)!
    """
    # TODO: add TESTS
    # TODO: add TESTS
    # TODO: add TESTS
    # TODO: add TESTS
    # TODO: add TESTS
    # TODO: add TESTS

    # INPUT
    FUNC: Callable
    ARGS: Tuple[Any, ...] = []
    KWARGS: Dict[str, Any] = {}

    # RESULTS
    OK: Optional[bool] = None
    RESULT: Optional[Any] = None
    EXX: Optional[Exception] = None

    def __call__(self, *args, **kwargs) -> None:
        # init ---------------
        self.OK = None
        self.RESULT = None
        self.EXX = None

        self.ARGS = args        # FIXME: resolve work with args!
        self.KWARGS = kwargs    # FIXME:

        # WORK ---------------
        try:
            self.RESULT = self.FUNC(*args, **kwargs)
            self.OK = True
        except Exception as exx:
            self.EXX = exx
            self.OK = False

# =====================================================================================================================
