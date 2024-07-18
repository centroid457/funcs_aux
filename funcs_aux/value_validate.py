from typing import *
from funcs_aux import *
from object_info import *


# =====================================================================================================================
class ValueValidate:
    """
    NOTE
    ----

    GOAL
    ----
    1. get value from somewhere and clearly validate it.
    2. ability to log result in appropriate way

    SAME AS: seems same as ResultExpect but maybe we need to use this instead of Expected (cause of too sophisticated!)
    DIFFERENCE: more clear understanding

    CREATED SPECIALLY FOR
    ---------------------
    testplans

    CONSTRAINTS
    -----------

    BEST USAGE
    ----------

    WHY NOT: 1?
    ----------

    WHY NOT: 2?
    ----------
    """

    TITLE: str = ""
    COMMENT: str = ""

    VALUE_LINK: Any | Callable[[], Any]
    VALIDATE_LINK: Callable[[Any], bool | Exception] = lambda val: val is True
    LOG_PATTERN: str = "validate_last={0.validate_last}[{0.TITLE}]value_last={0.value_last}"

    value_last: Any | Exception = None
    validate_last: None | bool | Exception = None
    log_last: str = ""

    def __init__(
            self,
            value_link,
            result_link: Any | Callable[[Any], bool | Exception] = True,
            log_pattern: str = None,

            title: str = None,
            comment: str = None,
    ):

        self.VALUE_LINK = value_link
        self.VALIDATE_LINK = result_link

        if log_pattern:
            self.LOG_PATTERN = log_pattern
        if title:
            self.TITLE = title
        if comment:
            self.COMMENT = comment

    def run(self) -> bool:
        # VALUE ---------------------
        if TypeChecker.check__func_or_meth(self.VALUE_LINK):
            try:
                self.value_last = self.VALUE_LINK()
            except Exception as exx:
                self.value_last = exx
        else:
            self.value_last = self.VALUE_LINK

        # VALIDATE ---------------------
        try:
            self.validate_last = self.VALIDATE_LINK(self.value_last)
        except Exception as exx:
            self.validate_last = exx

        # FINAL ---------------------
        self.log_last = self.LOG_PATTERN.format(self)
        return self.validate_last


# =====================================================================================================================
