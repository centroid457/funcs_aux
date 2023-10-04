import pathlib
from typing import *
import numpy as np


# =====================================================================================================================


# =====================================================================================================================
def array_2d_get_compact_str(
        array: np.ndarray,
        interpreter: Optional[Dict[Any, Any]] = None,
        separate_rows: Optional[int] = None,
        wrap: Optional[bool] = None,
        use_rows_num: Optional[bool] = None
) -> str:
    """

    :param array:
    :param interpreter: dictionary to change some elements
    :param separate_rows: add blank line on step
    :param wrap: add additional strings before and after data
    :param use_rows_num: add row num in
    :return:
    """
    interpreter = interpreter or {}
    count_rows = len(array)
    count_columns = len(array[0])
    row_pos = 0
    result: str = ""

    if wrap:
        if use_rows_num:
            result += " " * 3
        result += "=" * count_columns + "\n"

    for row in array:
        row_pos += 1
        if separate_rows and row_pos > 1 and (row_pos - 1) % separate_rows == 0:
            result += f"\n"

        if use_rows_num:
            result += f"{row_pos:3} "
        for value in row:
            replaced = interpreter.get(value)
            if replaced is not None:
                value = replaced
            result += f"{value}"

        # result += f"\n"
        if row_pos != count_rows:
            result += f"\n"

    if wrap:
        result += "\n"
        if use_rows_num:
            result += " " * 3
        result += "=" * count_columns

    return result


# =====================================================================================================================
