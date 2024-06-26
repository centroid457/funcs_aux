from typing import *


# =====================================================================================================================
def LAMBDA_TRUE(*args, **kwargs) -> bool:
    return True


def LAMBDA_FALSE(*args, **kwargs) -> bool:
    return False


def LAMBDA_NONE(*args, **kwargs) -> None:
    return None


def LAMBDA_EXX(*args, **kwargs) -> NoReturn:
    raise Exception("LAMBDA_EXX")


# =====================================================================================================================
