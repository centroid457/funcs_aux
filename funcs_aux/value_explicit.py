from typing import *
from enum import Enum


# =====================================================================================================================
# TODO: use as ValueExplicit and VariantsExplicit(*args)
class Explicit:
    """
    GOAL
    ----
    1. solve NONE-VALUE as ambiguity by simple way
    2. show/pass explicitly the EXACT VALUE like None/[]/()

    RULES (when apply as funcResult)
    -----
    return object if you get final result!
    return None if there are any errors withing execution

    OLD ---- WHY: NamedTuple
    ----------------
    cause of we need to be able to compare different objects by values.
    maybe we need just add __eq__ method instead of it!!!

    USAGE
    -----
    to get exact value - just CALL instance! dont use VALUE access by attribute!

        from funcs_aux import *

        def func(a, b) -> Optional[Explicit]:
            if a in b:
                return Explicit(a)
            else:
                return

        result = func("None", [None, ])
        assert result is None

        result = func(None, [None, ])
        assert result == Explicit(None)

        if result:
            print(result())         # None
    """
    __VALUE: Any   # dont use VALUE access by attribute

    def __init__(self, source: Any = None):
        self.__VALUE = source

    def __call__(self, *args, **kwargs) -> Any:
        return self.__VALUE

    def __str__(self):
        return f"{self.__class__.__name__}({self.__VALUE})"

    # -----------------------------------------------------------------------------------------------------------------
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__VALUE == other()
        else:
            return self.__VALUE == other


# =====================================================================================================================
class Default(Explicit):
    """
    GOAL
    ----
    just a derivative for Explicit!
    use in funcs as explicitly define for not passed params!

    USAGE
    -----
    1. AUTO_WORK (preferred)
        when get Default instance - call it to get source value!
        if get Default class - get None as value!

        def func(source = Default(1)):
            if isinstance(source, Default):
                source = source()

    2. MANUAL_WORK (not preferred)
        you can apply inside func

        def func(source = Default):
            if source == Default:
                source = 1
    """
    pass


# =====================================================================================================================
class ValueNotExist:
    """
    DEPRECATE???
    ---------
    use direct ArgsEmpty???

    GOAL
    ----
    it is different from Default!
    there is no value!
    used when we need to change logic with not passed value!

    SPECIALLY CREATED FOR
    ---------------------
    Valid as universal validation object under cmp other objects!

    USAGE
    -----
    class Cls:
        def __init__(self, value: Any | Type[ValueNotExist] | ValueNotExist = ValueNotExist):
            self.value = value

        def __eq__(self, other):
            if self.value is ValueNotExist:
                return other is True
                # or
                return self.__class__(other).run()
            else:
                return other == self.value

        def run(self):
            return bool(self.value)

    SAME AS
    -------
    args.ArgsEmpty but single and really not defined
    """
    pass


# =====================================================================================================================
TYPE__EXPLICIT = Type[Explicit] | Explicit
TYPE__DEFAULT = Type[Default] | Default
TYPE__VALUE_NOT_PASSED = Type[ValueNotExist] | ValueNotExist


# =====================================================================================================================
