from typing import NamedTuple, Any


# =====================================================================================================================
class ResultSucceed(NamedTuple):
    """
    main idea - solve NONE-value ambiguity
    by simple way

    USAGE:
    ------
    def func(a, b) -> Optional(ResultSucceed):
        if a in b:
            return ResultSucceed(a)
        else:
            return

    result = func("None", [None, ])
    assert result is None

    result = func(None, [None, ])
    assert result == ResultSucceed(None)

    if result:
        print(result.VALUE)
        print(result())
    """
    VALUE: Any

    def __call__(self, *args, **kwargs) -> Any:
        return self.VALUE


# =====================================================================================================================
