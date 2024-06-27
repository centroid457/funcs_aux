from typing import *
import pytest
from pytest_aux import *

from funcs_aux import *


# =====================================================================================================================
pass


# =====================================================================================================================
class Test__ResultExpect_Step:
    # @classmethod
    # def setup_class(cls):
    #     # cls.Victim = ResultFunc
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    def setup_method(self, method):
        self.Victim = ResultExpect_Step
        pass

    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__bool_1(self):
        victim = self.Victim(bool)

        assert victim.VALUE == bool
        assert victim.ARGS == ()
        assert victim.KWARGS == {}

        assert victim.STEP__RESULT is None
        assert victim.STEP__EXX is None

        # ------------------------------
        victim(1)
        assert victim.VALUE == bool
        assert victim.ARGS == (1, )
        assert victim.KWARGS == {}

        assert victim.STEP__RESULT is True
        assert victim.STEP__EXX is None

        # ------------------------------
        victim.VALUE_EXPECTED = False
        victim.run()
        assert victim.VALUE == bool
        assert victim.ARGS == (1, )
        assert victim.KWARGS == {}

        assert victim.STEP__RESULT is False
        assert victim.STEP__EXX is None


# =====================================================================================================================
class Test__ResultExpect_Chain:
    # @classmethod
    # def setup_class(cls):
    #     # cls.Victim = ResultFunc
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    def setup_method(self, method):
        self.Victim = ResultExpect_Chain
        pass

    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__1(self):
        chain = [
            ResultExpect_Step(bool, value_expected=False, use_result=True, chain__stop_on_fail=True),
        ]
        victim = self.Victim(chain)

        assert victim.ARGS == ()
        assert victim.KWARGS == {}

        assert victim.STEP__RESULT is None
        assert victim.STEP__EXX is None

        # ------------------------------
        victim.run()

        assert victim.ARGS == ()
        assert victim.KWARGS == {}

        assert victim.STEP__RESULT is True
        assert victim.STEP__EXX is None

        # ------------------------------
        victim.run(1)

        assert victim.ARGS == (1, )
        assert victim.KWARGS == {}

        assert victim.STEP__RESULT is False
        assert victim.STEP__EXX is None

    def test__single(self):
        chain = [
            ResultExpect_Step(bool, value_expected=False, use_result=True, chain__stop_on_fail=True),
        ]
        victim = self.Victim(chain)

        # ------------------------------
        victim.run()

        assert victim.STEP__RESULT is True
        assert victim.STEP__EXX is None

        chain = [
            ResultExpect_Step(bool, value_expected=True, use_result=True, chain__stop_on_fail=True),
        ]
        victim = self.Victim(chain)

        # ------------------------------
        victim.run()

        assert victim.STEP__RESULT is False
        assert victim.STEP__EXX is None

        chain = [
            ResultExpect_Step(bool, value_expected=True, use_result=False, chain__stop_on_fail=False),
        ]
        victim = self.Victim(chain)

        # ------------------------------
        victim.run()

        assert victim.STEP__RESULT is True
        assert victim.STEP__EXX is None

    def test__double__first_fail(self):
        chain = [
            ResultExpect_Step(bool, value_expected=True, use_result=True, chain__stop_on_fail=True),
            ResultExpect_Step(bool, value_expected=False, use_result=True, chain__stop_on_fail=True),
        ]
        victim = self.Victim(chain)

        # ------------------------------
        victim.run()

        assert victim.STEP__RESULT is False
        assert victim.STEP__EXX is None

        chain = [
            ResultExpect_Step(bool, value_expected=True, use_result=True, chain__stop_on_fail=False),
            ResultExpect_Step(bool, value_expected=False, use_result=True, chain__stop_on_fail=True),
        ]
        victim = self.Victim(chain)

        # ------------------------------
        victim.run()

        assert victim.STEP__RESULT is False
        assert victim.STEP__EXX is None

        chain = [
            ResultExpect_Step(bool, value_expected=True, use_result=False, chain__stop_on_fail=False),
            ResultExpect_Step(bool, value_expected=False, use_result=True, chain__stop_on_fail=True),
        ]
        victim = self.Victim(chain)

        # ------------------------------
        victim.run()

        assert victim.STEP__RESULT is True
        assert victim.STEP__EXX is None

    # -----------------------------------------------------------------------------------------------------------------
    def test__finished(self):
        victim = self.Victim([])
        assert victim.STEP__FINISHED is None
        victim.run()
        assert victim.STEP__FINISHED is True

    @pytest.mark.parametrize(
        argnames="chains, _EXPECTED",
        argvalues=[
            ((), -1),
            ((True, ), 0),
            ((False,), 0),
            ((False, False), 1),
            ((True, True), 1),

            ((True, True, True), 2),
            ((ResultExpect_Step(False, chain__stop_on_fail=False), True, True), 2),
            ((ResultExpect_Step(False, chain__stop_on_fail=True), True, True), 0),
        ]
    )
    def test__step_index(self, chains, _EXPECTED):
        victim = self.Victim(chains)
        victim.run()
        func_link = victim.STEP__INDEX
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="chains, _EXPECTED",
        argvalues=[
            ((), 0),
            ((True,), 1),
            ((False,), 1),
            ((False, False), 2),
            ((True, True), 2),
        ]
    )
    def test__step_count(self, chains, _EXPECTED):
        victim = self.Victim(chains)
        func_link = victim.CHAINS_COUNT
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="chains, _EXPECTED",
        argvalues=[
            ((), True),
            ((True, ), True),
            ((lambda: True, ), True),

            ((False,), False),
            ((lambda: False,), False),

            ((None,), False),

            ((1,), True),
            ((0,), False),

            ((True, False,), False),
            ((False, True), False),

            ((lambda: False,), False),
            ((lambda: False,), False),

            ((True, lambda: False,), False),
            ((lambda: False, True), False),

            ((False, ResultExpect_Step(True)), False),
            ((True, ResultExpect_Step(True)), True),
            ((True, ResultExpect_Step(False)), False),
        ]
    )
    def test__result(self, chains, _EXPECTED):
        func_link = self.Victim(chains).run
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="chains, _EXPECTED",
        argvalues=[
            ((ResultExpect_Step(False, skip_if=None), ), False),
            ((ResultExpect_Step(False, skip_if=False), ), False),
            ((ResultExpect_Step(False, skip_if=True), ), True),
            ((ResultExpect_Step(False, skip_if=lambda: True), ), True),
            ((ResultExpect_Step(False, skip_if=lambda: False), ), False),

            ((ResultExpect_Step(lambda: False, skip_if=lambda: False), ), False),
            ((ResultExpect_Step(LAMBDA_EXX, skip_if=False), ), False),
            ((ResultExpect_Step(LAMBDA_EXX, skip_if=True), ), True),
        ]
    )
    def test__skip_if(self, chains, _EXPECTED):
        func_link = self.Victim(chains).run
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    @pytest.mark.parametrize(
        argnames="chains, _EXPECTED",
        argvalues=[
            # ((ResultExpect_Step(False, use_result=None), ), True),
            ((ResultExpect_Step(False, use_result=False), ), True),
            ((ResultExpect_Step(False, use_result=True), ), False),
        ]
    )
    def test__use_result(self, chains, _EXPECTED):
        func_link = self.Victim(chains).run
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


# =====================================================================================================================
