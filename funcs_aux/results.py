from typing import *


# =====================================================================================================================
TYPE__FUNC = Callable[..., Any]
TYPE__FUNC_UNDER_VALUE = Callable[[Any], Any]
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

    it will return object in any cases (if you get final result or if there are any errors in execution)!
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
pass    # ----------------------------------------------------
pass    # ----------------------------------------------------
pass    # ----------------------------------------------------
pass    # ----------------------------------------------------
pass    # ----------------------------------------------------
pass    # ----------------------------------------------------
pass    # ----------------------------------------------------
pass    # ----------------------------------------------------


def _explore_and_why_it_need():
    class Cls:
        pass

    # THIS IS OK!!!!!=======
    if False:
        result = Cls.hello

    # IT DEPANDS!!!!!=======
    print(
        all([
            False,
            False and Cls.hello1,  #this is OK!!!!
            # True and Cls.hello2,  #this is EXX!!!! AttributeError: type object 'Cls' has no attribute 'hello2'
        ])
    )

    # THIS IS EXX!!!!!=======
    result = False
    # result &= Cls.hello3,  #this is EXX!!!! AttributeError: type object 'Cls' has no attribute 'hello3'

    print(
        all([
            False,
            Cls,
            # Cls.hello4, #this is EXX!!!! AttributeError: type object 'Cls' has no attribute 'hello4'
        ])
    )

    def func():
        return Cls.hello5  # this is OK!!!!

    # func()      # AttributeError: type object 'Cls' has no attribute 'hello5'


# =====================================================================================================================
# class FailRepresentation(Enum):
#     AS_FAIL = auto()
#     AS_TRUE = auto()
#
#
# class FailContinuation(Enum):
#     STOP = auto()
#     CONTINUE = auto()


class ResultExpectStep:
    # SETTINGS --------------------------------
    VALUE: Union[Any, Callable]
    VALUE_AS_FUNC: bool = True
    VALUE_UNDER_FUNC: TYPE__FUNC_UNDER_VALUE = None
    VALUE_EXPECTED: Union[bool, Any] = True

    ARGS: TYPE__ARGS = None
    KWARGS: TYPE__KWARGS = None

    # markers for CHAIN -----------------------
    CHAIN__USE_RESULT: bool = True
    CHAIN__STOP_ON_FAIL: bool = True

    # STEP_RESULT ----------------------------------
    STEP_RESULT: Optional[bool] = None
    STEP_EXX: Optional[bool] = None

    def __init__(
            self,
            value: Union[Any, Callable],
            value_as_func: bool = True,
            value_under_func: TYPE__FUNC_UNDER_VALUE = None,
            value_expected: Any = True,

            args: TYPE__ARGS = None,
            kwargs: TYPE__KWARGS = None,

            chain__use_result: bool = True,
            chain__stop_on_fail: bool = True,

    ):
        self.VALUE = value
        self.VALUE_AS_FUNC = value_as_func
        self.VALUE_UNDER_FUNC = value_under_func
        self.VALUE_EXPECTED = value_expected

        self.ARGS = args or ()
        self.KWARGS = kwargs or {}

        self.CHAIN__USE_RESULT = chain__use_result
        self.CHAIN__STOP_ON_FAIL = chain__stop_on_fail

    def __call__(self, *args, **kwargs) -> Self:
        return self.run(*args, **kwargs)

    def _clear_result(self) -> None:
        self.STEP_RESULT = None
        self.STEP_EXX = None

    def run(self, *args, **kwargs) -> Self:
        self._clear_result()

        if args:
            self.ARGS = args
        if kwargs:
            self.KWARGS = kwargs

        # CALLS --------------------------------------------------------------
        try:
            # callable ----------------------------
            if self.VALUE_AS_FUNC:
                value = self.VALUE(*self.ARGS, **self.KWARGS)
            else:
                value = self.VALUE

            # VALUE_UNDER_FUNC -----------------------
            if self.VALUE_UNDER_FUNC:
                value = self.VALUE_UNDER_FUNC(value)
        except Exception as exx:
            self.STEP_EXX = exx
            result = False
        else:
            result = value == self.VALUE_EXPECTED

        # FINISH --------------------------------------------------------------
        self.STEP_RESULT = result
        return self


# =====================================================================================================================
class ResultChain:
    pass


# =====================================================================================================================
