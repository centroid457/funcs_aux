import re
from typing import *
from object_info import *
from funcs_aux import *


# =====================================================================================================================
TYPE__CALLABLE_NO_PARAMS = Callable[[], Any]
TYPE__CALLABLE_ANY_PARAMS = Callable[..., Any]
TYPE__VALUE_LINK = Union[Any, TYPE__CALLABLE_NO_PARAMS, TYPE__CALLABLE_ANY_PARAMS]
TYPE__VALIDATE_LINK = Union[Any, TYPE__CALLABLE_NO_PARAMS, TYPE__CALLABLE_ANY_PARAMS]

TYPE__SKIP_IF = Union[None, bool, Any, Callable[[], Union[bool, None, NoReturn, Any]]]
TYPE__CHAINS = Iterable[
    Union[
        'ResultExpect_Step',
        'ResultExpect_Chain',
        bool,
        Callable[[], Any],
        Any,
    ]]  # dont use MAP/GEN but only Iters!!!


# =====================================================================================================================
class ResultExpect_Base:  # dont hide it cause of need ability to detect both of ResultExpect_Step/Chain
    """
    DONT USE IT DIRECTLY! this is only a base for *Step/Chain!

    CHAINS
    ------
    if no items - return True!!!
    if skip - return True!!!???
    """
    TITLE: Optional[str] = None
    # COMMENT: str = ""

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

    def __call__(self, *args, **kwargs) -> bool:
        return self.run(*args, **kwargs)

    def __bool__(self) -> bool:
        return self.STEP__RESULT or False

    def __str__(self) -> str:
        return self.MSG

    @property
    def MSG(self) -> str:
        result = f"{self.__class__.__name__}[result={self.STEP__RESULT}/skipped={self.STEP__SKIPPED}//title={self.TITLE}]"
        return result

    def _clear(self) -> None:
        self.STEP__SKIPPED = None
        self.STEP__FINISHED = None
        self.STEP__RESULT = None

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
            self.STEP__SKIPPED = True

            # WORK -----------------------
        if not self.STEP__SKIPPED:
            try:
                self.STEP__RESULT = self._run__wrapped()
            except Exception as exx:
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


# =====================================================================================================================
class ResultExpect_Step(ResultExpect_Base):
    # SETTINGS --------------------------------
    VALUE_LINK: TYPE__VALUE_LINK
    VALIDATE_LINK: TYPE__FUNC_UNDER_VALUE = None

    def __init__(
            self,
            value: Union[Any, Callable],
            validate_link: TYPE__FUNC_UNDER_VALUE = None,

            **kwargs
    ):
        super().__init__(**kwargs)

        self.VALUE_LINK = value
        self.VALIDATE_LINK = validate_link

    def _run__wrapped(self) -> Union[bool, NoReturn]:
        # CALLS ----------------------------------
        if TypeChecker.check__func_or_meth(self.VALUE_LINK):
            self.VALUE_ACTUAL = self.VALUE_LINK(*self.ARGS, **self.KWARGS)
        else:
            self.VALUE_ACTUAL = self.VALUE_LINK

        # VALIDATE_LINK -----------------------
        if self.VALIDATE_LINK:
            self.VALUE_ACTUAL = self.VALIDATE_LINK(self.VALUE_ACTUAL)

        result = self.VALUE_ACTUAL == self.VALUE_EXPECTED or self.VALUE_EXPECTED == self.VALUE_ACTUAL   # this is used for CMP objects

        # FINISH --------------------------------------------------------------
        return result

    @property
    def MSG(self) -> str:
        result = super().MSG
        result += f"value_actual={self.VALUE_ACTUAL}/value_expected={self.VALUE_EXPECTED}"
        return result


# =====================================================================================================================
class ResultExpect_Chain(ResultExpect_Base):
    """
    CHAINS
    ------
    if no items - return True!!!
    """
    # SETTINGS --------------------------------
    CHAINS: TYPE__CHAINS = None

    # AUX --------------------------------
    def __init__(
            self,
            chains: TYPE__CHAINS,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.CHAINS = chains or []

    def _run__wrapped(self) -> bool:
        result = True
        for step in self.CHAINS:
            if isinstance(step, ResultExpect_Base):
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

    def __len__(self) -> int:
        """
        IT IS NOT ACCEPTABLE FOR GENS!
        """
        try:
            return len(self.CHAINS or [])
        except Exception as exx:
            print(f"LEN is not acceptable for such object like MAP/GEN, {exx!r}")
            raise exx

    @property
    def MSG(self) -> str:
        # result = f"ResultExpectChain[/result={self.STEP__RESULT}/skipped={self.STEP__SKIPPED}//title={self.TITLE}]"
        result = super().MSG
        separator = "\n----"
        for step in self.CHAINS:
            try:
                step_msg = step.MSG
            except:
                step_msg = f"DirectValue{step}"

            result += f"{separator}{step_msg}"
        return result


# =====================================================================================================================
