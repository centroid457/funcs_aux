from typing import *
from funcs_aux import *
from object_info import *


# =====================================================================================================================
TYPE__RESULT_CUM_STEP = Union[bool, Any, ValueValidate]
TYPE__RESULT_CUM_STEPS = Union[TYPE__RESULT_CUM_STEP, list[TYPE__RESULT_CUM_STEP]]


# =====================================================================================================================
class ResultCum:
    """
    GOAL
    ----
    apply cumulated result with log lines

    CREATED SPECIALLY FOR
    ---------------------
    testplans

    REPLACE: ResultExpected

    CONSTRAINTS
    -----------

    BEST USAGE
    ----------
        # some example
        def meth() -> ResultCum:
            result_cum = ResultCum()

            result_step = 1+1 == 2
            result_cum.result__apply_step(result_step)
            result_cum.log_lines__add('check 1+1 == 2')

            result_step = 1+2 == 4
            result_cum.result__apply_step(result_step)
            result_cum.log_lines__add('check 1+2 == 4')

            result_cum.finish()
            return result_cum

    """

    TITLE: str = ""
    # COMMENT: str = ""

    result: bool | None = None
    finished: bool | None = None    # as help to see if process is finished - maybe need deprecate!

    LOG_LINES: list[str]
    STEP_HISTORY: list[tuple[TYPE__RESULT_CUM_STEP, bool]]     # as history! step+cumSettings

    def __init__(self, title: str = None):        #, steps=None):  #dont use steps here
        if title:
            self.TITLE = title

        self.clear()

    def clear(self) -> None:
        self.result = None
        self.finished = None

        self.LOG_LINES = []
        self.STEP_HISTORY = []

    def result__apply_step(self, step: TYPE__RESULT_CUM_STEPS, cumulate: bool | Any = True, msg: Union[None, str, list[str]] = None) -> bool:
        if isinstance(step, list):
            # LIST ------------------------------------------
            for step_i in step:
                if not self.result__apply_step(step_i, cumulate):
                    break
        else:
            # SINGLE ------------------------------------------
            self.STEP_HISTORY.append((step, cumulate))
            # TODO: if isinstance(step, ResultCum):   - what do i need to do here?? decide!
            if isinstance(step, ValueValidate):
                if not step.finished:
                    step.run()
                self.log_lines__add(step.log_last)

        if msg:
            self.log_lines__add(msg)

        if bool(cumulate):
            if self.result is None:
                self.result = bool(step)
            else:
                self.result &= bool(step)

        return self.result

    def log_lines__add(self, new: Union[str, list[str]]) -> None:
        if isinstance(new, list):
            self.LOG_LINES.extend(new)
        if isinstance(new, str):
            self.LOG_LINES.append(new)

    def finish(self) -> None:
        self.finished = True

    def __bool__(self) -> bool:
        return bool(self.result)

    def __str__(self):
        result = f"{self.__class__.__name__}(result={self.result},finished={self.finished},TITLE={self.TITLE},LOG_LINES={self.LOG_LINES})"
        return result

    def __repr__(self):
        return str(self)

    def step_last__get(self) -> Any | NoReturn:
        return self.STEP_HISTORY[-1][0]

    def log_last__get(self) -> str | None:
        try:
            return self.LOG_LINES[-1]
        except:
            pass


# =====================================================================================================================
