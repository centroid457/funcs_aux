from typing import *
import pytest
from pytest import mark
from pytest_aux import *
from funcs_aux import *


# =====================================================================================================================
def test__log_lines():
    victim = ResultLogSteps("Hello")
    assert victim.LOG_LINES == []

    # SINGLE --------------------------
    victim.log_lines__add("line1")
    assert victim.LOG_LINES == ["line1"]

    # LIST --------------------------
    victim.clear()
    assert victim.LOG_LINES == []
    victim.log_lines__add([f"line{i}" for i in range(3)])
    assert victim.LOG_LINES == ["line0", "line1", "line2"]


def test__step_history():
    victim = ResultLogSteps("Hello")
    assert victim.STEP_HISTORY == []

    victim.result__apply_step(True)
    assert victim.STEP_HISTORY == [(True, True)]

    victim.result__apply_step(False)
    assert victim.STEP_HISTORY == [(True, True), (False, True)]

    victim.result__apply_step(None)
    assert victim.STEP_HISTORY == [(True, True), (False, True), (None, True)]

    victim.result__apply_step("Hello")
    assert victim.STEP_HISTORY == [(True, True), (False, True), (None, True), ("Hello", True)]

    value_validate_obj = ValueValidate(True)
    victim.result__apply_step(value_validate_obj)
    assert victim.STEP_HISTORY == [(True, True), (False, True), (None, True), ("Hello", True), (value_validate_obj, True)]

    victim.clear()
    assert victim.STEP_HISTORY == []


# =====================================================================================================================
