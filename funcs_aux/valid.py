from typing import *
from funcs_aux import *
from object_info import *


# =====================================================================================================================
TYPE__VALUE_LINK = Union[Any, Exception, Callable[[], Any | Exception]]
TYPE__BOOL_LINK = Union[bool, Any, Exception, Callable[[Any], bool | Exception]]


# =====================================================================================================================
class Valid:
    """
    GOAL
    ----
    1. get value from somewhere and clearly validate it.
    2. ability to log result in appropriate way by using template-pattern for msg log

    CREATED SPECIALLY FOR
    ---------------------
    testplans sequences or same staff

    CONSTRAINTS
    -----------
    1. Exceptions
    any exception is a special state!
    so dont try to compare Exception with any real NoExx value or validate it in validator_link!
    if expect exception just place it directly in Validator!

    2. Callables
    only funcs/methods will be called
    if Class - no call! no init!

    BEST USAGE
    ----------

    WHY NOT: 1?
    -----------

    WHY NOT: 2?
    -----------
    """

    TITLE: str = ""
    COMMENT: str = ""

    VALUE_LINK: TYPE__VALUE_LINK
    VALIDATE_LINK: TYPE__BOOL_LINK = lambda self, val: val is True      # dont use bool(val)!!!
    SKIP_LINK: TYPE__BOOL_LINK = False
    STR_PATTERN: str = "Valid(validate_last_bool={0.validate_last_bool},validate_last={0.validate_last},value_last={0.value_last},skip_last={0.skip_last},title={0.TITLE})"

    value_last: Any | Exception = None
    validate_last: None | bool | Exception = True   # decide using only bool
    validate_last_bool: bool = True
    skip_last: bool = False
    str_last: str = ""

    finished: bool | None = None

    def get_finished_result_or_none(self) -> None | bool:
        """
        GOAL
        ----
        attempt to make ability to get clear result by one check (for Gui)

        :return: if not finished - None
            if finished - validate_last_bool
        """
        if self.finished is None:
            result = None
        else:
            result = self.validate_last_bool
        return result

    def __init__(
            self,
            value_link: TYPE__VALUE_LINK,
            validate_link: Optional[TYPE__BOOL_LINK] = None,
            skip_link: Optional[TYPE__BOOL_LINK] = None,
            str_pattern: Optional[str] = None,

            title: Optional[str] = None,
            comment: Optional[str] = None,
    ):
        self.VALUE_LINK = value_link

        if validate_link is not None:
            self.VALIDATE_LINK = validate_link
        if skip_link is not None:
            self.SKIP_LINK = skip_link
        if str_pattern:
            self.STR_PATTERN = str_pattern
        if title:
            self.TITLE = title
        if comment:
            self.COMMENT = comment

    def run(self) -> bool:
        self.finished = False
        # SKIP ---------------------
        self.skip_last = self.get_bool(self.SKIP_LINK)

        if not self.skip_last:
            # VALUE ---------------------
            self.value_last = self.get_result_or_exx(self.VALUE_LINK)

            # TODO: maybe add ArgsKwargs but it is too complicated! add only in critical obligatory situation!
            # if TypeChecker.check__func_or_meth(self.VALUE_LINK):
            #     self.VALUE_ACTUAL = self.VALUE_LINK(*self.ARGS, **self.KWARGS)
            # else:
            #     self.VALUE_ACTUAL = self.VALUE_LINK

            # VALIDATE ------------------
            if isinstance(self.value_last, Exception) and not TypeChecker.check__exception(self.VALIDATE_LINK):
                self.validate_last = False

            elif TypeChecker.check__exception(self.VALIDATE_LINK):
                self.validate_last = TypeChecker.check__nested__by_cls_or_inst(self.value_last, self.VALIDATE_LINK)

            elif TypeChecker.check__func_or_meth(self.VALIDATE_LINK):
                self.validate_last = self.get_result_or_exx(lambda: self.VALIDATE_LINK(self.value_last))

            else:
                self.validate_last = self.compare_doublesided(self.value_last, self.VALIDATE_LINK)

            self.validate_last_bool = bool(self)

        # FINISH ---------------------
        self.str_last = self.STR_PATTERN.format(self)
        self.finished = True
        return self.validate_last_bool

    def __bool__(self) -> bool:
        return self.validate_last is True   # dont use validate_last_bool!

    def __str__(self) -> str:
        return self.str_last

    def __repr__(self) -> str:
        return self.str_last

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
    def get_bool(cls, source: Any | Callable[..., Any], args: list[Any] = None, kwargs: dict[str, Any] = None) -> bool:
        """
        GOAL
        ----
        ability to get bool result with meanings:
            - methods/funcs must be called
                assert get_bool(LAMBDA_TRUE) is True
                assert get_bool(LAMBDA_NONE) is False

            - Exceptions assumed as False
                assert get_bool(Exception) is False
                assert get_bool(Exception("FAIL")) is False
                assert get_bool(LAMBDA_EXX) is False

            - for other values get classic bool()
                assert get_bool(None) is False
                assert get_bool([]) is False
                assert get_bool([None, ]) is True

                assert get_bool(LAMBDA_LIST) is False
                assert get_bool(LAMBDA_LIST, [1, ]) is True

            - if on bool() exception raised - return False!
                assert get_bool(ClsBoolExx()) is False

        CREATED SPECIALLY FOR
        ---------------------
        funcs_aux.Valid.skip_link or else value/func assumed as bool result
        """
        result = cls.get_result_or_exx(source, args, kwargs)
        if TypeChecker.check__exception(result):
            return False
        else:
            try:
                return bool(result)
            except:
                return False

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def compare_doublesided(cls, obj1: Any, obj2: Any) -> bool | Exception:
        """
        GOAL
        ----
        just a direct comparing code like
            self.validate_last = self.value_last == self.VALIDATE_LINK or self.VALIDATE_LINK == self.value_last
        will not work correctly

        if any result is True - return True.
        if at least one false - return False
        if both exx - return first exx  # todo: deside return False in here!

        CREATED SPECIALLY FOR
        ---------------------
        manipulate objects which have special methods for __cmp__
        for cases when we can switch places

        BEST USAGE
        ----------
            class ClsEq:
                def __init__(self, val):
                    self.VAL = val

                def __eq__(self, other):
                    return other == self.VAL

            assert ClsEq(1) == 1
            assert 1 == ClsEq(1)

            assert compare_doublesided(1, Cls(1)) is True
            assert compare_doublesided(Cls(1), 1) is True

        example above is not clear! cause of comparison works ok if any of object has __eq__() meth even on second place!
        but i think in one case i get Exx and with switching i get correct result!!! (maybe fake! need explore!)
        """
        try:
            result12 = obj1 == obj2
            if result12:
                return True
        except Exception as exx:
            result12 = exx

        try:
            result21 = obj2 == obj1
            if result21:
                return True
        except Exception as exx:
            result21 = exx

        if False in [result12, result21]:
            return False
        else:
            return result12


# =====================================================================================================================
