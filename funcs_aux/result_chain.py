from typing import *
from object_info import TypeChecker

from funcs_aux import TYPE__FUNC_UNDER_VALUE, TYPE__ARGS, TYPE__KWARGS


# =====================================================================================================================
TYPE__SKIP_IF = Union[None, bool, Any, Callable[[], Union[bool, None, NoReturn, Any]]]
TYPE__CHAINS = list[Union['ResultExpect_Step', 'ResultExpect_Chain', bool, Callable[[], Any], Any]]


# =====================================================================================================================
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
class ResultExpect_Base:    # dont hide it cause of need ability to detect both of ResultExpect_Step/Chain
    """
    [CHAINS]
    --------
    if no items - return True!!!
    if skip - return True!!!???
    """
    TITLE: Optional[str] = None

    ARGS: TYPE__ARGS = None
    KWARGS: TYPE__KWARGS = None

    # markers for CHAIN -----------------------
    SKIP_IF: TYPE__SKIP_IF = None
    USE_RESULT: bool = True
    CHAIN__STOP_ON_FAIL: bool = True

    # RESULT ----------------------------------
    STEP__SKIPPED: Optional[bool] = None
    STEP__FINISHED: Optional[bool] = None
    STEP__RESULT: Optional[bool] = None
    STEP__EXX: Optional[bool] = None

    STEP__INDEX: int = None

    def __init__(
            self,
            # ResultExpect_Base ---------------------
            title: Optional[str] = None,

            args: TYPE__ARGS = None,
            kwargs: TYPE__KWARGS = None,

            skip_if: bool | None = None,
            use_result: bool | None = None,
            chain__stop_on_fail: bool = True,
    ):
        # ResultExpect_Base ---------------------
        self.TITLE = title

        self.ARGS = args or ()
        self.KWARGS = kwargs or {}

        if skip_if is not None:
            self.SKIP_IF = skip_if
        if use_result is not None:
            self.USE_RESULT = use_result
        self.CHAIN__STOP_ON_FAIL = chain__stop_on_fail

    def __call__(self, *args, **kwargs) -> Self:
        return self.run(*args, **kwargs)

    def __bool__(self) -> bool:
        return self.STEP__RESULT or False

    def __str__(self) -> str:
        return "\n".join(self.MSGS)

    @property
    def MSG(self) -> str:
        result = f"ResultExpect[index={self.STEP__INDEX}/result={self.STEP__RESULT}/exx={self.STEP__EXX}/skipped={self.STEP__SKIPPED}//title={self.TITLE}]"
        return result

    @property
    def MSGS(self) -> list[str]:
        """here it is useful to keep universal access to MSGS both to STEP/CHAIN
        """
        return [self.MSG, ]

    def _clear(self) -> None:
        self.STEP__SKIPPED = None
        self.STEP__FINISHED = None
        self.STEP__RESULT = None
        self.STEP__EXX = None

    def run(self, *args, **kwargs) -> bool:
        self._clear()

        if args:
            self.ARGS = args
        if kwargs:
            self.KWARGS = kwargs

        # SKIP -----------------------
        try:
            if TypeChecker.check__func_or_meth(self.SKIP_IF):
                self.STEP__SKIPPED = self.SKIP_IF()
            else:
                self.STEP__SKIPPED = self.SKIP_IF
            self.STEP__SKIPPED = bool(self.STEP__SKIPPED)

        except Exception as exx:
            self.STEP__EXX = exx
            self.STEP__SKIPPED = True

            # WORK -----------------------
        if not self.STEP__SKIPPED:
            try:
                self.STEP__RESULT = self._run__wrapped()
            except Exception as exx:
                self.STEP__EXX = exx
                self.STEP__RESULT = None
        else:
            self.STEP__RESULT = True

        # FINISH ------------------
        print(self.MSG)
        self.STEP__FINISHED = True
        return self.STEP__RESULT

    def run__if_not_finished(self) -> bool:
        if self.STEP__FINISHED:
            return self.STEP__RESULT
        else:
            return self.run()

    def _run__wrapped(self) -> Union[bool, NoReturn]:
        pass


# =====================================================================================================================
class ResultExpect_Step(ResultExpect_Base):
    # SETTINGS --------------------------------
    VALUE: Union[Any, Callable]
    VALUE_UNDER_FUNC: TYPE__FUNC_UNDER_VALUE = None
    VALUE_EXPECTED: Union[bool, Any] = True

    def __init__(
            self,
            value: Union[Any, Callable],
            value_under_func: TYPE__FUNC_UNDER_VALUE = None,
            value_expected: Any = True,

            **kwargs
    ):
        super().__init__(**kwargs)

        self.VALUE = value
        self.VALUE_UNDER_FUNC = value_under_func
        self.VALUE_EXPECTED = value_expected

    def _run__wrapped(self) -> Union[bool, NoReturn]:
        # CALLS ----------------------------------
        if TypeChecker.check__func_or_meth(self.VALUE):
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
class ResultExpect_Chain(ResultExpect_Base):
    """
    [CHAINS]
    --------
    if no items - return True!!!
    """
    # SETTINGS --------------------------------
    CHAINS: TYPE__CHAINS = None

    # AUX --------------------------------
    STEP__INDEX: int = -1   # [0] - is the first index! [-1] - is the no one steps started!!!

    def __init__(
            self,
            chains: TYPE__CHAINS,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.CHAINS = chains or []

    def _run__wrapped(self) -> bool:
        self.STEP__INDEX = -1

        result = True
        for step in self.CHAINS:
            self.STEP__INDEX += 1
            if isinstance(step, ResultExpect_Base):
                step.STEP__INDEX = self.STEP__INDEX
                step.run(*self.ARGS, **self.KWARGS)

                if step.USE_RESULT:
                    result &= bool(step.STEP__RESULT)

                if not step.STEP__RESULT and step.CHAIN__STOP_ON_FAIL:
                    break
            else:
                if TypeChecker.check__func_or_meth(step):
                    result = step()
                result &= bool(step)

        return result

    @property
    def CHAINS_COUNT(self) -> int:
        return len(self.CHAINS or [])

    @property
    def MSGS(self) -> list[str]:
        result = []
        for step in self.CHAINS:
            result.append(step.MSG)
        return result


# =====================================================================================================================
