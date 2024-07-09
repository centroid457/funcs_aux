from . import *
from typing import *
from object_info import ObjectInfo
from annot_attrs import *
from classes_aux import *
import re


# =====================================================================================================================
class Exx__ValueNotInVariants(Exception):
    pass


class Exx__VariantsIncompatible(Exception):     # TODO: seems need to deprecate it! it is not important!
    pass


class Value_FromVariants:
    """
    used to keep separated VALUE and measure unit
    """
    # TODO: combine with Value_WithUnit - just add ACCEPTABLE(*VARIANTS) and rename UNIT just as SUFFIX!

    # SETTINGS -----------------------
    CASE_INSENSITIVE: bool = True
    VARIANTS: list[Any] = None
    VALUE_DEFAULT: Any = Value_NotPassed

    # DATA ---------------------------
    __value: Any = Value_NotPassed

    def __init__(self, value: Union[str, Any] = Value_NotPassed, variants: list[Union[str, Any]] = None, case_insensitive: bool = None):
        """
        :param value: None mean NotSelected/NotSet!
            if you need set None - use string VALUE in any case! 'None'/NONE/none
        """
        # FIXME: need think about None VALUE!
        # settings ---------------
        if case_insensitive is not None:
            self.CASE_INSENSITIVE = case_insensitive
        if variants is not None:
            self.VARIANTS = variants

        # work ---------------
        self._variants_validate()

        if value != Value_NotPassed:
            self.VALUE_DEFAULT = value
            self.VALUE = value

    def __str__(self) -> str:
        return f"{self.VALUE}"

    def __repr__(self) -> str:
        """
        used as help
        """
        return f"{self.VALUE}{self.VARIANTS}"

    def __eq__(self, other):
        if isinstance(other, Value_FromVariants):
            other = other.VALUE

        # todo: decide is it correct using comparing by str()??? by now i think it is good enough! but maybe add it as parameter
        if self.CASE_INSENSITIVE:
            return (self.VALUE == other) or (str(self.VALUE).lower() == str(other).lower())
        else:
            return (self.VALUE == other) or (str(self.VALUE) == str(other))

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self.VARIANTS)

    def __iter__(self):
        yield from self.VARIANTS

    def __contains__(self, item):
        """
        used to check compatibility
        """
        for variant in self.VARIANTS:
            if self.CASE_INSENSITIVE:
                result = str(variant).lower() == str(item).lower()
            else:
                result = str(variant) == str(item)
            if result:
                return True

        return False

    def _variants_validate(self) -> Optional[NoReturn]:
        if self.CASE_INSENSITIVE:
            real_len = len(set(map(lambda item: str(item).lower(), self.VARIANTS)))
        else:
            real_len = len(set(self.VARIANTS))

        result = real_len == len(self.VARIANTS)
        if not result:
            raise Exx__VariantsIncompatible()

    @property
    def VALUE(self) -> Any:
        return self.__value

    @VALUE.setter
    def VALUE(self, value: Any) -> Optional[NoReturn]:
        for variant in self.VARIANTS:
            if self.CASE_INSENSITIVE:
                result = str(variant).lower() == str(value).lower()
            else:
                result = str(variant) == str(value)
            if result:
                self.__value = variant
                return

        raise Exx__ValueNotInVariants()

    def reset(self) -> None:
        """
        set VALUE into default only if default is exists!
        """
        if self.VALUE_DEFAULT != Value_NotPassed:
            self.VALUE = self.VALUE_DEFAULT


# =====================================================================================================================
