from typing import Any, Callable, NoReturn

from object_info import TypeChecker

from funcs_aux import TYPE__ARGS, TYPE__KWARGS


# =====================================================================================================================
class ValidAux:
    """
    Try to keep all validating funcs in separated place
    """
    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_result(
            cls,
            source: Any | Callable[..., Any],
            args: TYPE__ARGS = None,
            kwargs: TYPE__KWARGS = None,
    ) -> Any | NoReturn:
        """
        GOAL
        ----
        get generic common expected for any python code result - simple calculate or raise!
        because of get_result_or_exx is not enough!

        CREATED SPECIALLY FOR
        ---------------------
        GetattrPrefixInst
        """
        args = args or []
        kwargs = kwargs or {}

        if TypeChecker.check__callable_func_meth_inst(source):
            result = source(*args, **kwargs)
        else:
            result = source
        return result

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_result_or_exx(
            cls,
            source: Any | Callable[..., Any],
            args: TYPE__ARGS = None,
            kwargs: TYPE__KWARGS = None,
    ) -> Any | Exception:
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
        try:
            result = cls.get_result(source=source, args=args, kwargs=kwargs)
        except Exception as exx:
            result = exx
        return result

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_bool(
            cls,
            source: Any | Callable[..., Any],
            args: TYPE__ARGS = None,
            kwargs: TYPE__KWARGS = None,
    ) -> bool:
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
        try:
            result = cls.get_result(source, args, kwargs)
            if TypeChecker.check__exception(result):
                return False
            return bool(result)
        except:
            return False

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def compare_doublesided(cls, obj1: Any, obj2: Any, return_bool: bool = None) -> bool | Exception:
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

        try:
            result3 = obj2 is obj1
            if result3:
                return True
        except Exception as exx:
            result3 = exx
            pass

        if False in [result12, result21] or return_bool:
            return False
        else:
            return result12

    @classmethod
    def compare_doublesided__bool(cls, obj1: Any, obj2: Any) -> bool:
        """
        CREATED SPECIALLY FOR
        ---------------------
        Valid.value_validate
        """
        return cls.compare_doublesided(obj1, obj2, return_bool=True)

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def ltgt(source: Any, low: Any | None = None, high: Any | None = None) -> bool | Exception:
        """
        NOTE
        ----
        1. important to keep source at first place!
        """
        result = True
        if low is not None:
            result &= source > low
        if high is not None:
            result &= source < high
        return result

    @staticmethod
    def ltge(source: Any, low: Any | None = None, high: Any | None = None) -> bool | Exception:
        result = True
        if low is not None:
            result &= source > low
        if high is not None:
            result &= source <= high
        return result

    @staticmethod
    def legt(source: Any, low: Any | None = None, high: Any | None = None) -> bool | Exception:
        result = True
        if low is not None:
            result &= source >= low
        if high is not None:
            result &= source < high
        return result

    @staticmethod
    def lege(source: Any, low: Any | None = None, high: Any | None = None) -> bool | Exception:
        result = True
        if low is not None:
            result &= source >= low
        if high is not None:
            result &= source <= high
        return result


# =====================================================================================================================
