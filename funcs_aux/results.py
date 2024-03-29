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
        print(result.RESULT__VALUE)
        print(result())
    """
    VALUE: Any

    def __call__(self, *args, **kwargs) -> Any:
        return self.run()

    def run(self) -> Any:
        return self.VALUE


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
    RESULT__VALUE: Optional[Any] = None
    RESULT__EXX: Optional[Exception] = None
    RESULT__CORRECT: bool

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
        self._result__clear()

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

    def _result__clear(self) -> None:
        self.RESULT__VALUE = None
        self.RESULT__EXX = None

    @property
    def RESULT__CORRECT(self) -> bool:
        return self.RESULT__EXX is None


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
class _ResultExpect_Base:
    TITLE: Optional[str] = None

    ARGS: TYPE__ARGS = None
    KWARGS: TYPE__KWARGS = None

    # markers for CHAIN -----------------------
    CHAIN__USE_RESULT: bool = True
    CHAIN__STOP_ON_FAIL: bool = True

    # RESULT ----------------------------------
    STEP__RESULT: Optional[bool] = None
    STEP__EXX: Optional[bool] = None

    def __init__(
            self,
            # _ResultExpect_Base ---------------------
            title: Optional[str] = None,

            args: TYPE__ARGS = None,
            kwargs: TYPE__KWARGS = None,

            chain__use_result: bool = True,
            chain__stop_on_fail: bool = True,
    ):
        # _ResultExpect_Base ---------------------
        self.TITLE = title

        self.ARGS = args or ()
        self.KWARGS = kwargs or {}

        self.CHAIN__USE_RESULT = chain__use_result
        self.CHAIN__STOP_ON_FAIL = chain__stop_on_fail

    def __call__(self, *args, **kwargs) -> Self:
        return self.run(*args, **kwargs)

    @property
    def MSG(self) -> str:
        result = f"[result={self.STEP__RESULT}]{self.TITLE or ''}"
        return result

    def _result__clear(self) -> None:
        self.STEP__RESULT = False
        self.STEP__EXX = None

    def run(self, *args, **kwargs) -> bool:
        self._result__clear()

        if args:
            self.ARGS = args
        if kwargs:
            self.KWARGS = kwargs

        # WORK -----------------------
        try:
            self.STEP__RESULT = self._run__wrapped()
        except Exception as exx:
            self.STEP__EXX = exx

        print(self.MSG)
        return self.STEP__RESULT

    def _run__wrapped(self) -> Union[bool, NoReturn]:
        pass


class ResultExpect_Step(_ResultExpect_Base):
    # SETTINGS --------------------------------
    VALUE: Union[Any, Callable]
    VALUE_AS_FUNC: bool = True
    VALUE_UNDER_FUNC: TYPE__FUNC_UNDER_VALUE = None
    VALUE_EXPECTED: Union[bool, Any] = True

    def __init__(
            self,
            value: Union[Any, Callable],
            value_as_func: bool = True,
            value_under_func: TYPE__FUNC_UNDER_VALUE = None,
            value_expected: Any = True,

            **kwargs
    ):
        super().__init__(**kwargs)

        self.VALUE = value
        self.VALUE_AS_FUNC = value_as_func
        self.VALUE_UNDER_FUNC = value_under_func
        self.VALUE_EXPECTED = value_expected

    def _run__wrapped(self) -> Union[bool, NoReturn]:
        # CALLS ----------------------------------
        if self.VALUE_AS_FUNC:
            value = self.VALUE(*self.ARGS, **self.KWARGS)
        else:
            value = self.VALUE

        # VALUE_UNDER_FUNC -----------------------
        if self.VALUE_UNDER_FUNC:
            value = self.VALUE_UNDER_FUNC(value)

        result = value == self.VALUE_EXPECTED

        # FINISH --------------------------------------------------------------
        return result


# =====================================================================================================================
class ResultExpect_Chain(_ResultExpect_Base):
    # SETTINGS --------------------------------
    CHAINS: List[Union[_ResultExpect_Base]] = None

    # AUX --------------------------------
    STEP__INDEX: int = -1

    def __init__(
            self,
            chains: List[Union[ResultExpect_Step, Self]],
            **kwargs
    ):
        super().__init__(**kwargs)

        self.CHAINS = chains

    def _run__wrapped(self) -> bool:
        self.STEP__INDEX = -1
        result = True
        for step in self.CHAINS:
            self.STEP__INDEX += 1
            if isinstance(step, _ResultExpect_Base):
                step.run(*self.ARGS, **self.KWARGS)

                if step.CHAIN__USE_RESULT:
                    result &= bool(step.STEP__RESULT)

                if not step.STEP__RESULT and step.CHAIN__STOP_ON_FAIL:
                    break
        return result

    @property
    def CHAINS_COUNT(self) -> int:
        return len(self.CHAINS or [])


# =====================================================================================================================
