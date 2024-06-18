from . import *

from typing import *
import time
import re
import logging
import datetime

from object_info import *


# =====================================================================================================================
class Cmp:
    """
    TEMPLATE FOR APPLYING COMPARISON WITH SELF INSTANCE
    """
    __eq__ = lambda self, other: self.__cmp__(other) == 0
    __ne__ = lambda self, other: self.__cmp__(other) != 0
    __lt__ = lambda self, other: self.__cmp__(other) < 0
    __gt__ = lambda self, other: self.__cmp__(other) > 0
    __le__ = lambda self, other: self.__cmp__(other) <= 0
    __ge__ = lambda self, other: self.__cmp__(other) >= 0

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
        raise NotImplemented()

    # -----------------------------------------------------------------------------------------------------------------
    # def __eq__(self, other):
    #     return self.__cmp__(other) == 0
    #
    # def __ne__(self, other):
    #     return self.__cmp__(other) != 0
    #
    # def __lt__(self, other):
    #     return self.__cmp__(other) < 0
    #
    # def __gt__(self, other):
    #     return self.__cmp__(other) > 0
    #
    # def __le__(self, other):
    #     return self.__cmp__(other) <= 0
    #
    # def __ge__(self, other):
    #     return self.__cmp__(other) >= 0


# =====================================================================================================================
