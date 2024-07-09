from . import *
from typing import *
from object_info import ObjectInfo
from annot_attrs import *
from classes_aux import *
import re


# =====================================================================================================================
class Value_NotPassed:
    """
    resolve not passed parameters in case of None VALUE!

    special object used as VALUE to show that parameter was not passed!
    dont pass it directly! keep it only as default parameter in class and in methods instead of None Value!
    it used only in special cases! not always even in one method!!!
    """
    pass
    # @classmethod
    # def __str__(self):
    #     return ""     # it used as direct Class! without any instantiation!


TYPE__VALUE_NOT_PASSED = Type[Value_NotPassed]


# =====================================================================================================================
