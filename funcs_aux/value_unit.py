from . import *
from typing import *
from object_info import ObjectInfo
from annot_attrs import *
from classes_aux import *
import re


# =====================================================================================================================
class Exx__ValueNotParsed(Exception):
    pass


class Exx__ValueUnitsIncompatible(Exception):
    pass


class UnitBase(AnnotsClsKeysAsValues):
    V: str
    A: str
    C: str


UNIT_MULTIPLIER: dict[str, float | int] = {
    "p": 10 ** (-12),
    "n": 10 ** (-9),
    "µ": 10 ** (-6),
    "m": 10 ** (-3),
    "c": 10 ** (-2),
    "d": 10 ** (-1),

    "k": 10 ** 3,
    "M": 10 ** 6,
    "G": 10 ** 9,
    "T": 10 ** 12,

    "": 10 ** 0,  # keep it last only or just delete!!!
}


# =====================================================================================================================
class Value_WithUnit(CmpInst):
    """
    used to keep separated/parse VALUE and measure UNIT and compare with any representation
    """
    VALUE: Union[int, float] = 0

    UNIT: str = ""      # final unit with multiplier
    UNIT_BASE: str = ""
    UNIT_MULTIPLIER: str = ""
    MULTIPLIER: int = 1
    SEPARATOR_OUTPUT: str = ""

    # TODO: add arithmetic/comparing magic methods like SUM/...

    def __init__(self, source: Union[int, float, str, Any] = None, unit: str = None, separator_output: str = None):
        """
        :param source:
        :param unit: use it only if not exists in source!
        :param separator_output:
        """
        if source is not None:
            self.parse(source)
        if unit is not None:
            if self.UNIT:
                msg = f"old[{self.UNIT=}] new[{unit=}]"
                raise Exx__ValueUnitsIncompatible(msg)
            self.UNIT = unit
        if separator_output is not None:
            self.SEPARATOR_OUTPUT = separator_output

    @property
    def VALUE_PURE(self) -> Union[int, float]:
        return self.VALUE * self.MULTIPLIER

    def parse(self, source: Any) -> Self | NoReturn:
        source = str(source)
        source = source.strip()
        source = source.lstrip("+")
        source = source.replace(',', ".")
        source = re.sub(r'-+\s+', '-', source)

        # WORK ---------------------------
        match = re.fullmatch(r'(-?[0-9.]+)\s*([a-zA-Z]*)', source)
        if match:
            self.VALUE = float(match[1])

            self.UNIT = match[2] or ""
        else:
            raise Exx__ValueNotParsed()

        if int(self.VALUE) == self.VALUE:
            self.VALUE = int(self.VALUE)

        # UNIT_MULTIPLIER ------------------
        for unit_multiplier, multiplier in UNIT_MULTIPLIER.items():
            if self.UNIT.startswith(unit_multiplier):
                self.UNIT_MULTIPLIER = unit_multiplier
                self.UNIT_BASE = self.UNIT.removeprefix(unit_multiplier)
                self.MULTIPLIER = multiplier
                break

        if not self.UNIT_BASE and self.UNIT:
            self.UNIT_BASE = self.UNIT

        # FINISH ---------------------------
        return self

    def __str__(self) -> str:
        return f"{self.VALUE}{self.SEPARATOR_OUTPUT}{self.UNIT}"

    def __repr__(self) -> str:
        """
        used as help
        """
        return f"{self.VALUE}'{self.UNIT}'"

    # CMP -------------------------------------------------------------------------------------------------------------
    def __cmp__(self, other) -> int | NoReturn:
        """
        do try to resolve Exceptions!!! sometimes it is ok to get it!!!

        RETURN
        ------
            1=self>other
            0=self==other
            -1=self<other
        """
        other = self.__class__(other)

        # cmp units -----------
        if self.UNIT_BASE and other.UNIT_BASE and self.UNIT_BASE != other.UNIT_BASE:
            msg = f"{self!r}/{other!r}"
            raise Exx__ValueUnitsIncompatible(msg)

        # cmp -----------
        if self.VALUE_PURE == other.VALUE_PURE:
            return 0
        elif self.VALUE_PURE > other.VALUE_PURE:
            return 1
        elif self.VALUE_PURE < other.VALUE_PURE:
            return -1


# =====================================================================================================================
