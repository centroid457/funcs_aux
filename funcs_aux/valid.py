from typing import *
import time
# from funcs_aux import *
from object_info import *
from funcs_aux import args__ensure_tuple, TYPE__ARGS, TYPE__KWARGS, ArgsEmpty

from .value_variants import ValueVariants


# =====================================================================================================================
TYPE__EXCEPTION = Union[Exception, Type[Exception]]
TYPE__SOURCE_LINK = Union[Any, TYPE__EXCEPTION, Callable[[...], Any | NoReturn]]
TYPE__VALIDATE_LINK = Union[bool, Any, TYPE__EXCEPTION, Callable[[Any, ...], bool | NoReturn]]
TYPE__BOOL_LINK = Union[bool, Any, TYPE__EXCEPTION, Callable[[...], bool | NoReturn]]


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

    3. VALIDATE
    if final value - it will be compared directly by compare_doublesided.
    So be careful about True (as default) and apply LAMBDA_BOOL(VALUE) if you need bool(val) comparing!

    BEST USAGE
    ----------

    WHY NOT: 1?
    -----------

    WHY NOT: 2?
    -----------
    """

    NAME: str = ""      # TODO: realise access to Valid from Chains!
    COMMENT: str = ""

    SKIP_LINK: TYPE__BOOL_LINK = None
    VALUE_LINK: TYPE__SOURCE_LINK
    VALIDATE_LINK: TYPE__VALIDATE_LINK = True

    ARGS__VALUE: TYPE__ARGS = ()
    ARGS__VALIDATE: TYPE__ARGS = ()
    KWARGS__VALUE: TYPE__KWARGS = None
    KWARGS__VALIDATE: TYPE__KWARGS = None

    # TODO: apply name from source!!! if not passed
    STR_PATTERN: str = ("{0.__class__.__name__}(validate_last_bool={0.validate_last_bool},validate_last={0.validate_last},\n"
                        "...VALUE_LINK={0.VALUE_LINK},ARGS__VALUE={0.ARGS__VALUE},KWARGS__VALUE={0.KWARGS__VALUE},value_last={0.value_last},\n"
                        "...VALIDATE_LINK={0.VALIDATE_LINK},ARGS__VALIDATE={0.ARGS__VALIDATE},KWARGS__VALIDATE={0.KWARGS__VALIDATE},\n"
                        "...skip_last={0.skip_last},NAME={0.NAME},finished={0.finished},timestamp_last={0.timestamp_last})")

    # RESULT ACTUAL ------------------------------
    timestamp_last: float | None = None
    skip_last: bool = False
    finished: bool | None = None
    value_last: Any | Exception = None
    validate_last: None | bool | Exception = True   # decide using only bool???
    log_lines: list[str] = None

    # CHAINS -------------------------------------
    CHAIN__CUM: bool = True
    CHAIN__FAIL_STOP: bool = True

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
            result = bool(self)
        return result

    def __init__(
            self,
            value_link: TYPE__SOURCE_LINK,
            validate_link: Optional[TYPE__VALIDATE_LINK] = None,
            skip_link: Optional[TYPE__BOOL_LINK] = None,

            args__value: TYPE__ARGS = (),
            args__validate: TYPE__ARGS = (),

            kwargs__value: TYPE__KWARGS = None,
            kwargs__validate: TYPE__KWARGS = None,

            name: Optional[str] = None,
            comment: Optional[str] = None,

            chain__cum: Optional[bool] = None,
            chain__fail_stop: Optional[bool] = None,
    ):
        self.clear()

        self.VALUE_LINK = value_link

        if validate_link is not None:
            self.VALIDATE_LINK = validate_link
        if skip_link is not None:
            self.SKIP_LINK = skip_link

        # ARGS/KWARGS --------------------------------
        self.ARGS__VALUE = args__ensure_tuple(args__value)
        self.ARGS__VALIDATE = args__ensure_tuple(args__validate)

        self.KWARGS__VALUE = kwargs__value or {}
        self.KWARGS__VALIDATE = kwargs__validate or {}

        # INFO ---------------------------------------
        if name:
            self.NAME = name
        if comment:
            self.COMMENT = comment

        # CHAINS -------------------------------------
        if chain__cum is not None:
            self.CHAIN__CUM = chain__cum
        if chain__fail_stop is not None:
            self.CHAIN__FAIL_STOP = chain__fail_stop

    def run__if_not_finished(self) -> bool:
        if not self.finished:
            return self.run()
        else:
            return bool(self)

    def clear(self):
        self.timestamp_last = None
        self.skip_last = False
        self.finished = None
        self.value_last = None
        self.validate_last = True
        self.log_lines = []

    def run(self) -> bool:
        """
        CONSTRAINTS
        -----------
        careful about 1 comparing (assert 0 == False, assert 1 == True, assert 2 != True)
        """
        self.clear()
        self.timestamp_last = time.time()

        # SKIP ---------------------
        self.skip_last = self.get_bool(self.SKIP_LINK)

        if not self.skip_last:
            # WORK =======================
            self.finished = False

            # VALUE ---------------------
            self.value_last = self.get_result_or_exx(self.VALUE_LINK, args=self.ARGS__VALUE, kwargs=self.KWARGS__VALUE)

            # TODO: maybe add ArgsKwargs but it is too complicated! add only in critical obligatory situation!
            # if TypeChecker.check__callable_func_meth_inst(self.VALUE_LINK):
            #     self.VALUE_ACTUAL = self.VALUE_LINK(*self.ARGS, **self.KWARGS)
            # else:
            #     self.VALUE_ACTUAL = self.VALUE_LINK

            # VALIDATE ------------------
            if isinstance(self.value_last, Exception) and not TypeChecker.check__exception(self.VALIDATE_LINK):
                self.validate_last = False

            elif TypeChecker.check__exception(self.VALIDATE_LINK):
                self.validate_last = TypeChecker.check__nested__by_cls_or_inst(self.value_last, self.VALIDATE_LINK)

            elif TypeChecker.check__callable_func_meth_inst(self.VALIDATE_LINK):
                args_validate = (self.value_last, *self.ARGS__VALIDATE)
                self.validate_last = self.get_result_or_exx(self.VALIDATE_LINK, args=args_validate, kwargs=self.KWARGS__VALIDATE)

                # elif self.VALIDATE_LINK is True:
                #     # self.validate_last = self.get_result_or_exx(lambda: self.VALIDATE_LINK(self.value_last))
                #     # dont use it!

            elif isinstance(self.VALIDATE_LINK, ValueVariants):
                self.validate_last = self.value_last in self.VALIDATE_LINK
            else:
                self.validate_last = self.compare_doublesided(self.value_last, self.VALIDATE_LINK)

            self.finished = True
            # ============================

        # FINISH ---------------------
        return bool(self)

    @property
    def validate_last_bool(self) -> bool:
        return bool(self)

    def __bool__(self) -> bool:
        return self.validate_last is True   # dont use validate_last_bool!

    def __str__(self) -> str:
        # main ---------------
        result_str = self.STR_PATTERN.format(self)

        # log ----------------
        for index, line in enumerate(self.log_lines):
            result_str += "\n" + f"{index}:".rjust(5, '_') + line

        return result_str

    def __repr__(self) -> str:
        return str(self)

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_result_or_exx(cls, source: Any | Callable[..., Any], args: TYPE__ARGS = None, kwargs: TYPE__KWARGS = None) -> Any | Exception:
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

        if TypeChecker.check__callable_func_meth_inst(source):
            try:
                result = source(*args, **kwargs)
            except Exception as exx:
                result = exx
        else:
            result = source
        return result

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_bool(cls, source: Any | Callable[..., Any], args: TYPE__ARGS = None, kwargs: TYPE__KWARGS = None) -> bool:
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

        try:
            result3 = obj2 is obj1
            if result3:
                return True
        except Exception as exx:
            result3 = exx
            pass

        if False in [result12, result21]:
            return False
        else:
            return result12

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
class ValidFailStop(Valid):
    """
    just a derivative
    """
    CHAIN__FAIL_STOP = True


class ValidFailContinue(Valid):
    """
    just a derivative
    """
    CHAIN__FAIL_STOP = False


class ValidNoCum(Valid):
    """
    just a derivative

    you can use it as a stub in chains
    """
    CHAIN__CUM = False


# =====================================================================================================================
TYPE__CHAINS = list[Union[Valid, 'ValidChains', Any]]      # all Any will be converted to Valid!


# =====================================================================================================================
class ValidChains(Valid):
    """
    GOAL
    ----

    CREATED SPECIALLY FOR
    ---------------------

    CONSTRAINTS
    -----------

    BEST USAGE
    ----------
    val_chains = ValidChains(
        chains=[
            True,
            1+1 == 2,
            Valid(2),
            Valid(3, chain_cum=False),
            ValidChains([Valid(21), Valid(22)], chain_cum=False),
        ]
    )

    result = val_chains.run()

    WHY NOT: 1?
    -----------

    WHY NOT: 2?
    -----------
    """
    _CHAINS: TYPE__CHAINS

    def __init__(self, chains: TYPE__CHAINS, **kwargs):
        super().__init__(value_link=None, **kwargs)
        self._CHAINS = chains

    def __len__(self) -> int:
        return len(self._CHAINS)

    def __iter__(self):
        return iter(self._CHAINS)

    def run(self) -> bool:
        self.clear()
        self.timestamp_last = time.time()

        # SKIP ---------------------
        self.skip_last = self.get_bool(self.SKIP_LINK)

        if not self.skip_last:
            # WORK =======================
            self.finished = False
            self.log_lines.append(f"(START) len={len(self)}/timestamp={self.timestamp_last}")

            # init self.validate_last if None -----------
            if self.validate_last is None:
                self.validate_last = True

            # ITER -----------
            for index, step in enumerate(self):
                if not isinstance(step, (Valid, ValidChains)):
                    step = Valid(step)

                step_result = step.run()
                self.log_lines.append(str(step))

                if not step.skip_last:
                    if step.CHAIN__CUM:
                        self.validate_last &= step_result
                    if step.CHAIN__FAIL_STOP and not step_result:
                        self.log_lines.append(f"(FAIL STOP) [result={bool(self)}]{index=}/len={len(self)}")
                        break
            # ITER -----------

            self.log_lines.append(f"(FINISH) [result={bool(self)}]/len={len(self)}")
            self.finished = True
            # ============================

        return bool(self)


# =====================================================================================================================
if __name__ == "__main__":
    victim = ValidChains([Valid(True), Valid(False)])
    print(victim)
    print()

    victim.run()
    print(victim)


# =====================================================================================================================
