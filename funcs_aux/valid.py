from typing import *
import time
# from funcs_aux import *
from object_info import *

from .args import TYPE__ARGS, TYPE__KWARGS
from .valid_aux import ValidAux
from .ensure import args__ensure_tuple
from .value_explicit import ValueNotExist, TYPE__VALUE_NOT_PASSED


# =====================================================================================================================
TYPE__EXCEPTION = Union[Exception, Type[Exception]]
TYPE__SOURCE_LINK = Union[Any, TYPE__EXCEPTION, Callable[[...], Any | NoReturn], TYPE__VALUE_NOT_PASSED]
TYPE__VALIDATE_LINK = Union[bool, Any, TYPE__EXCEPTION, Callable[[Any, ...], bool | NoReturn]]
TYPE__BOOL_LINK = Union[bool, Any, TYPE__EXCEPTION, Callable[[...], bool | NoReturn]]


# =====================================================================================================================
class Valid(ValidAux):
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
    VALIDATE_RETRY: int = 0

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

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def validate_last_bool(self) -> bool:
        return bool(self)

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
            value_link: TYPE__SOURCE_LINK = ValueNotExist,
            validate_link: Optional[TYPE__VALIDATE_LINK] = None,
            validate_retry: Optional[int] = None,
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
        """

        :param value_link: None - for cmp by eq/ne! other types - for direct usage
        :param validate_link:
        :param skip_link:
        :param args__value:
        :param args__validate:
        :param kwargs__value:
        :param kwargs__validate:
        :param name:
        :param comment:
        :param chain__cum:
        :param chain__fail_stop:
        """
        self.clear()

        self.VALUE_LINK = value_link

        if validate_link is not None:
            self.VALIDATE_LINK = validate_link
        if validate_retry is not None:
            self.VALIDATE_RETRY = validate_retry
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

    def run(self, _value_link: Any = ValueNotExist) -> bool:
        """
        CONSTRAINTS
        -----------
        careful about 1 comparing (assert 0 == False, assert 1 == True, assert 2 != True)

        :param _value_link: BE CAREFUL created specially for value_link=ValueNotExist on init
        """
        if _value_link == ValueNotExist:
            _value_link = self.VALUE_LINK

        self.clear()
        self.timestamp_last = time.time()

        # SKIP ---------------------
        self.skip_last = self.get_bool(self.SKIP_LINK)

        if not self.skip_last:
            retry_count = 0
            # WORK =======================
            self.finished = False

            while True:
                self.clear()
                self.timestamp_last = time.time()

                # VALUE ---------------------
                self.value_last = self.get_result_or_exx(_value_link, args=self.ARGS__VALUE, kwargs=self.KWARGS__VALUE)

                # VALIDATE ------------------
                if isinstance(self.value_last, Exception) and not TypeChecker.check__exception(self.VALIDATE_LINK):
                    self.validate_last = False

                elif TypeChecker.check__exception(self.VALIDATE_LINK):
                    self.validate_last = TypeChecker.check__nested__by_cls_or_inst(self.value_last, self.VALIDATE_LINK)

                elif TypeChecker.check__callable_func_meth_inst(self.VALIDATE_LINK):
                    args_validate = (self.value_last, *self.ARGS__VALIDATE)
                    self.validate_last = self.get_result_or_exx(self.VALIDATE_LINK, args=args_validate, kwargs=self.KWARGS__VALIDATE)

                else:
                    self.validate_last = self.compare_doublesided(self.value_last, self.VALIDATE_LINK)

                # FINISH retry
                if not self.VALIDATE_RETRY or retry_count == self.VALIDATE_RETRY or self.validate_last_bool:
                    break
                else:
                    retry_count += 1

            self.finished = True
            # ============================

        # FINISH final ---------------------
        return bool(self)

    # def validate(self, _value_link: Any = ValueNotExist) -> bool:

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
    def __eq__(self, other) -> bool:
        """
        GOAL
        ----
        use created object (with not defined value_link=None) as validator by EQ/NE inline methods!

        USAGE
        -----
        assert 1.0 >= 1
        assert float("1.0") >= 1
        assert "1.0" == Valid(validate_link=lambda x: float(x) >= 1)

        SPECIALY CREATED FOR
        --------------------
        test uart devises by schema!

        assert "220.0V" == ValueUnit(...)
        assert "OFF" == ValueVariant("OFF", ["OFF", "ON"])
        assert "1.0" == Valid(validate_link=lambda x: float(x) >= 1)

        ValidTypeFloat = Valid(validate_link=lambda x: isinstance(x, float))
        assert "1.0" != ValidTypeFloat()
        assert 1.0 == ValidTypeFloat()
        """
        if self.VALUE_LINK == ValueNotExist:
            return self.run(other)
        else:
            # todo: maybe its not so good here/need ref? - seems OK!
            return self.run__if_not_finished() == other


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
                    if step.CHAIN__CUM and step.CHAIN__FAIL_STOP and not step_result:
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
