from funcs_aux import ResultSucceedSimple, ResultFull


# =====================================================================================================================
def test__ResultSucceed():
    assert ResultSucceedSimple(123)() == 123

    assert ResultSucceedSimple(123).VALUE == 123
    assert ResultSucceedSimple([123]).VALUE == [123]
    assert ResultSucceedSimple({123}).VALUE == {123}
    assert ResultSucceedSimple({123: 123}).VALUE == {123: 123}


# =====================================================================================================================
class Test__ResultFull:
    # @classmethod
    # def setup_class(cls):
    #     # cls.Victim = ResultFull
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    def setup_method(self, method):
        self.Victim = ResultFull

        pass

    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__bool(self):

        victim = self.Victim(func=bool)

        assert victim.FUNC == bool
        assert victim.ARGS == ()
        assert victim.KWARGS == {}

        assert victim.RESULT_VALUE is None
        assert victim.RESULT_EXX is None
        assert victim.RESULT_OK is True

        # ------------------------------
        victim(0)

        assert victim.FUNC == bool
        assert victim.ARGS == (0, )
        assert victim.KWARGS == {}

        assert victim.RESULT_VALUE is False
        assert victim.RESULT_EXX is None
        assert victim.RESULT_OK is True

        # ------------------------------
        victim(1)

        assert victim.FUNC == bool
        assert victim.ARGS == (1, )
        assert victim.KWARGS == {}

        assert victim.RESULT_VALUE is True
        assert victim.RESULT_EXX is None
        assert victim.RESULT_OK is True

        # ------------------------------
        victim(0, 1)

        assert victim.FUNC == bool
        assert victim.ARGS == (0, 1, )
        assert victim.KWARGS == {}

        assert victim.RESULT_VALUE is None
        assert victim.RESULT_EXX is not None
        assert victim.RESULT_OK is False

    def test__RUN_ON_INIT(self):
        victim = self.Victim(func=bool, args=(0,1), run_on_init=False)

        assert victim.FUNC == bool
        assert victim.ARGS == (0, 1)
        assert victim.KWARGS == {}

        assert victim.RESULT_VALUE is None
        assert victim.RESULT_EXX is None
        assert victim.RESULT_OK is True

        # ------------------------------
        victim = self.Victim(func=bool, args=(0,1), run_on_init=True)

        assert victim.FUNC == bool
        assert victim.ARGS == (0, 1)
        assert victim.KWARGS == {}

        assert victim.RESULT_VALUE is None
        assert victim.RESULT_EXX is not None
        assert victim.RESULT_OK is False


# =====================================================================================================================
