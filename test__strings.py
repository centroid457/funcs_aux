from funcs_aux import *
from funcs_aux import ResultSucceedSimple


# =====================================================================================================================
class Test__1:
    @classmethod
    def setup_class(cls):
        cls.victim = Strings().try_convert_to__elementary
        pass

    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__same_value(self):
        assert self.victim(None) is None
        assert self.victim(0) == 0
        assert self.victim([]) == []
        assert self.victim({1: 1}) == {1: 1}

    def test__none(self):
        # single
        assert self.victim(None) is None
        assert self.victim("None") is None
        assert self.victim("null") is None

        # collects
        assert self.victim([None]) == [None]
        assert self.victim("[None]") == [None]
        assert self.victim("[null]") == [None]

        # assert self.victim("['None',]") == ['None']
        # assert self.victim("['null']") == ['None']

    def test__bool(self):
        # TODO: APPLY USUALL VALUES FOR NULL/FALSE/TRUE

        assert self.victim(True) is True
        assert self.victim(False) is False

        assert self.victim("True") == "True"
        assert self.victim("False") == "False"

        assert self.victim("true") is True
        assert self.victim("false") is False

    def test__numbs(self):
        assert self.victim("000") == "000"
        assert self.victim("01") == "01"

        assert self.victim(0) == 0
        assert self.victim("0") == 0
        assert self.victim("10") == 10

        assert self.victim("1.0") == 1.0
        assert self.victim("1.000") == 1.0

    def test__iters(self):
        assert self.victim("[]") == []

    def test__dicts(self):
        # INcorrect
        assert self.victim("{1: 1}") != {1: 1}      # FIXME: for dicts - use only string keys even for numbs!
        assert self.victim("{'1': 1}") != {1: 1}    # FIXME: for dicts - use only double quotes!

        # correct
        assert self.victim('{"1": 1}') == {"1": 1}


# =====================================================================================================================
