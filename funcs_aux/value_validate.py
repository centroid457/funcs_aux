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
    -----------

    WHY NOT: 2?
    -----------
    """

    TITLE: str = ""
    COMMENT: str = ""

    VALUE_LINK: Any | Callable[[], Any]
    VALIDATE_LINK: Callable[[Any], bool | Exception] = lambda self, val: val is True    # dont use bool(val)!!!
    STR_PATTERN: str = "ValueValidate(validate_last={0.validate_last},value_last={0.value_last},title={0.TITLE})"

    value_last: Any | Exception = None
    validate_last: None | bool | Exception = None
    validate_last_bool: bool = False
    log_last: str = ""

    finished: bool | None = None

    def __init__(
            self,
            value_link: Any | Callable[[], Any],
            validate_link: Optional[Any | Callable[[Any], bool | Exception]] = None,
            str_pattern: Optional[str] = None,

            title: Optional[str] = None,
            comment: Optional[str] = None,
    ):
        self.VALUE_LINK = value_link

        if validate_link:
            self.VALIDATE_LINK = validate_link
        if str_pattern:
            self.STR_PATTERN = str_pattern
        if title:
            self.TITLE = title
        if comment:
            self.COMMENT = comment

    def run(self) -> bool:
        self.finished = False
        # VALUE ---------------------
        self.value_last = self.get_result_or_exx(self.VALUE_LINK)

        # VALIDATE ------------------
        if TypeChecker.check__func_or_meth(self.VALIDATE_LINK):
            self.validate_last = self.get_result_or_exx(lambda: self.VALIDATE_LINK(self.value_last))
        else:
            try:
                self.validate_last = self.value_last == self.VALIDATE_LINK or self.VALIDATE_LINK == self.value_last
            except Exception as exx:
                self.validate_last = exx

        self.validate_last_bool = bool(self)

        # FINISH ---------------------
        self.log_last = self.STR_PATTERN.format(self)
        self.finished = True
        return self.validate_last_bool

    def __bool__(self) -> bool:
        return self.validate_last is True   # dont use validate_last_bool!

    def __str__(self) -> str:
        return self.log_last

    def __repr__(self) -> str:
        return self.log_last

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_result_or_exx(cls, source: Any | Callable[..., Any], args: list[Any] = None, kwargs: dict[str, Any] = None) -> Any | Exception:
        """
        GOAL
        ----
        if callable meth/func - call and return result or Exx.
        else - return source.

        attempt to simplify result by not using try-sentence.

        USEFUL IDEA
        -----------
        1. in gui when its enough to get str() on result and see the result
        """
        args = args or []
        kwargs = kwargs or {}

        if TypeChecker.check__func_or_meth(source):
            try:
                result = source(*args, **kwargs)
            except Exception as exx:
                result = exx
        else:
            result = source
        return result

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def compare_doublesided(cls, obj1: Any, obj2: Any) -> bool | Exception:
        """
        GOAL
        ----
        just a direct code like
            self.validate_last = self.value_last == self.VALIDATE_LINK or self.VALIDATE_LINK == self.value_last
        will not work correctly

        if get exx and false - false will be return
        """
        result = obj1 == obj2

        # result = self.value_last == self.VALIDATE_LINK or self.VALIDATE_LINK == self.value_last

        return result


# =====================================================================================================================
