from typing import *
from funcs_aux import *
from object_info import *


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
    """

    TITLE: str = ""
    # COMMENT: str = ""

    result: bool | None = None
    finished: bool | None = None    # as help to see if process is finished - maybe need deprecate!

    LOG_LINES: list[str]
    STEP_HISTORY: list[tuple[Any, bool]]     # as history!

    def __init__(self, title: str = None, steps=None):
        if title:
            self.TITLE = title

        self.clear()

    def clear(self) -> None:
        self.result = None
        self.finished = None

        self.LOG_LINES = []
        self.STEP_HISTORY = []

    def result__apply_step(self, step: Union[bool, Any, Self, list], cumulate: bool = True, msg: Union[None, str, list[str]] = None) -> bool:
        if isinstance(step, list):
            # LIST ------------------------------------------
            for step_i in step:
                if not self.result__apply_step(step_i, cumulate) and cumulate:
                    break
        else:
            # SINGLE ------------------------------------------
            self.STEP_HISTORY.append((step, cumulate))
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


# =====================================================================================================================
