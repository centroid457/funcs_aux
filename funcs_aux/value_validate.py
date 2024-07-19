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
    2. ability to log result in appropriate way by using template-pattern for msg log

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
    VALIDATE_LINK: Callable[[Any], bool | Exception] = lambda self, val: val is True
    LOG_PATTERN: str = "ValueValidate(validate_last={0.validate_last},value_last={0.value_last},title=[{0.TITLE}])"

    value_last: Any | Exception = None
    validate_last: None | bool | Exception = None
    validate_last_bool: bool = False
    log_last: str = ""

    finished: bool | None = None

    def __init__(
            self,
            value_link: Any | Callable[[], Any],
            validate_link: Optional[Any | Callable[[Any], bool | Exception]] = None,
            log_pattern: Optional[str] = None,

            title: Optional[str] = None,
            comment: Optional[str] = None,
    ):
        self.VALUE_LINK = value_link
        if validate_link:
            self.VALIDATE_LINK = validate_link
        if log_pattern:
            self.LOG_PATTERN = log_pattern
        if title:
            self.TITLE = title
        if comment:
            self.COMMENT = comment

    def run(self) -> bool:
        self.finished = False
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

        self.validate_last_bool = bool(self)

        # FINISH ---------------------
        self.log_last = self.LOG_PATTERN.format(self)
        self.finished = True
        return self.validate_last_bool

    def __bool__(self) -> bool:
        return self.validate_last is True

    def __str__(self) -> str:
        return self.log_last

    def __repr__(self) -> str:
        return self.log_last


# =====================================================================================================================
