import pytest
from pytest_aux import *

from funcs_aux import *


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

        assert victim.STEP__SKIPPED is None
        assert victim.STEP__FINISHED is None
        assert victim.STEP__RESULT is None
        assert victim.STEP__EXX is None

        # ------------------------------
        victim(1)
        assert victim.VALUE == bool
        assert victim.ARGS == (1, )
        assert victim.KWARGS == {}

        assert victim.STEP__SKIPPED is None
        assert victim.STEP__FINISHED is True
        assert victim.STEP__RESULT is True
        assert victim.STEP__EXX is None

        # ------------------------------
        victim.VALUE_EXPECTED = False
        victim.run()
        assert victim.VALUE == bool
        assert victim.ARGS == (1, )
        assert victim.KWARGS == {}

        assert victim.STEP__SKIPPED is None
        assert victim.STEP__FINISHED is True
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

        assert victim.STEP__FINISHED is None
        assert victim.STEP__RESULT is None
        assert victim.STEP__EXX is None

        # ------------------------------
        victim.run()

        assert victim.ARGS == ()
        assert victim.KWARGS == {}

        assert victim.STEP__FINISHED is True
        assert victim.STEP__RESULT is True
        assert victim.STEP__EXX is None
        assert victim.STEP__INDEX == 0
        assert victim.CHAINS_COUNT == 1

        # ------------------------------
        victim.run(1)

        assert victim.ARGS == (1, )
        assert victim.KWARGS == {}

        assert victim.STEP__FINISHED is True
        assert victim.STEP__RESULT is False
        assert victim.STEP__EXX is None
        assert victim.STEP__INDEX == 0
        assert victim.CHAINS_COUNT == 1

    def test__single(self):
        chain = [
            ResultExpect_Step(bool, value_expected=False, use_result=True, chain__stop_on_fail=True),
        ]
        victim = self.Victim(chain)

        # ------------------------------
        victim.run()

        assert victim.STEP__FINISHED is True
        assert victim.STEP__RESULT is True
        assert victim.STEP__EXX is None
        assert victim.STEP__INDEX == 0
        assert victim.CHAINS_COUNT == 1

        chain = [
            ResultExpect_Step(bool, value_expected=True, use_result=True, chain__stop_on_fail=True),
        ]
        victim = self.Victim(chain)

        # ------------------------------
        victim.run()

        assert victim.STEP__FINISHED is True
        assert victim.STEP__RESULT is False
        assert victim.STEP__EXX is None
        assert victim.STEP__INDEX == 0
        assert victim.CHAINS_COUNT == 1

        chain = [
            ResultExpect_Step(bool, value_expected=True, use_result=False, chain__stop_on_fail=False),
        ]
        victim = self.Victim(chain)

        # ------------------------------
        victim.run()

        assert victim.STEP__FINISHED is True
        assert victim.STEP__RESULT is True
        assert victim.STEP__EXX is None
        assert victim.STEP__INDEX == 0
        assert victim.CHAINS_COUNT == 1

    def test__double__first_fail(self):
        chain = [
            ResultExpect_Step(bool, value_expected=True, use_result=True, chain__stop_on_fail=True),
            ResultExpect_Step(bool, value_expected=False, use_result=True, chain__stop_on_fail=True),
        ]
        victim = self.Victim(chain)

        # ------------------------------
        victim.run()

        assert victim.STEP__FINISHED is True
        assert victim.STEP__RESULT is False
        assert victim.STEP__EXX is None
        assert victim.STEP__INDEX == 0
        assert victim.CHAINS_COUNT == 2

        chain = [
            ResultExpect_Step(bool, value_expected=True, use_result=True, chain__stop_on_fail=False),
            ResultExpect_Step(bool, value_expected=False, use_result=True, chain__stop_on_fail=True),
        ]
        victim = self.Victim(chain)

        # ------------------------------
        victim.run()

        assert victim.STEP__FINISHED is True
        assert victim.STEP__RESULT is False
        assert victim.STEP__EXX is None
        assert victim.STEP__INDEX == 1
        assert victim.CHAINS_COUNT == 2

        chain = [
            ResultExpect_Step(bool, value_expected=True, use_result=False, chain__stop_on_fail=False),
            ResultExpect_Step(bool, value_expected=False, use_result=True, chain__stop_on_fail=True),
        ]
        victim = self.Victim(chain)

        # ------------------------------
        victim.run()

        assert victim.STEP__FINISHED is True
        assert victim.STEP__RESULT is True
        assert victim.STEP__EXX is None
        assert victim.STEP__INDEX == 1
        assert victim.CHAINS_COUNT == 2

    def test__empty(self):
        victim = self.Victim([])
        victim.run()
        assert victim.STEP__FINISHED is True
        assert victim.STEP__RESULT is True
        assert victim.STEP__EXX is None
        assert victim.STEP__INDEX == -1
        assert victim.CHAINS_COUNT == 0

    # ------------------------------------------------------
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
        ]
    )
    def test__steps(self, chains, _EXPECTED):
        func_link = self.Victim(chains).run
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # def test__skip_if(self):
    #     victim = self.Victim([])
    #     victim.run()
    #     assert victim.STEP__FINISHED is True
    #     assert victim.STEP__RESULT is True
    #     assert victim.STEP__EXX is None
    #     assert victim.STEP__INDEX == -1
    #     assert victim.CHAINS_COUNT == 0


# =====================================================================================================================
