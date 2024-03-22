from funcs_aux import ResultValue, ResultFunc, ResultExpect_Step, ResultExpect_Chain


# =====================================================================================================================
class Test__ResultValue:
    # @classmethod
    # def setup_class(cls):
    #     # cls.Victim = ResultFunc
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__1(self):
        assert ResultValue(123)() == 123

        assert ResultValue(123).RESULT_VALUE == 123
        assert ResultValue([123]).RESULT_VALUE == [123]
        assert ResultValue({123}).RESULT_VALUE == {123}
        assert ResultValue({123: 123}).RESULT_VALUE == {123: 123}


# =====================================================================================================================
class Test__ResultFunc:
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
        self.Victim = ResultFunc

        pass

    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__bool(self):

        victim = self.Victim(func=bool)

        assert victim.FUNC == bool
        assert victim.ARGS == ()
        assert victim.KWARGS == {}

        assert victim.RESULT__VALUE is None
        assert victim.RESULT__EXX is None
        assert victim.RESULT__CORRECT is True

        # ------------------------------
        victim(0)

        assert victim.FUNC == bool
        assert victim.ARGS == (0, )
        assert victim.KWARGS == {}

        assert victim.RESULT__VALUE is False
        assert victim.RESULT__EXX is None
        assert victim.RESULT__CORRECT is True

        # ------------------------------
        victim(1)

        assert victim.FUNC == bool
        assert victim.ARGS == (1, )
        assert victim.KWARGS == {}

        assert victim.RESULT__VALUE is True
        assert victim.RESULT__EXX is None
        assert victim.RESULT__CORRECT is True

        # ------------------------------
        victim(0, 1)

        assert victim.FUNC == bool
        assert victim.ARGS == (0, 1, )
        assert victim.KWARGS == {}

        assert victim.RESULT__VALUE is None
        assert victim.RESULT__EXX is not None
        assert victim.RESULT__CORRECT is False

    def test__RUN_ON_INIT(self):
        victim = self.Victim(func=bool, args=(0,1), run_on_init=False)

        assert victim.FUNC == bool
        assert victim.ARGS == (0, 1)
        assert victim.KWARGS == {}

        assert victim.RESULT__VALUE is None
        assert victim.RESULT__EXX is None
        assert victim.RESULT__CORRECT is True

        # ------------------------------
        victim = self.Victim(func=bool, args=(0,1), run_on_init=True)

        assert victim.FUNC == bool
        assert victim.ARGS == (0, 1)
        assert victim.KWARGS == {}

        assert victim.RESULT__VALUE is None
        assert victim.RESULT__EXX is not None
        assert victim.RESULT__CORRECT is False


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
