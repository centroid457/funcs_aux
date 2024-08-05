from typing import *
from object_info import ObjectInfo, TypeChecker


# =====================================================================================================================
"""
HOW to work with ARGS in your funcs
---------------------
usually and maybe often when we passing ARGS it assumed as we will pass tuple/list or direct value

"""


# =====================================================================================================================
class Default:
    """
    GOAL
    ----
    use in funcs as explicitly define for not passed params!

    USAGE
    -----
    1. AUTO_WORK (preferred)
        when get Default instance - call it to get source value!
        if get Default class - get None as value!

        def func(source = Default(1)):
            if isinstance(source, Default):
                source = source()

    2. MANUAL_WORK (not preferred)
        you can apply inside func

        def func(source = Default):
            if source == Default:
                source = 1
    """
    __SOURCE: Any

    def __init__(self, source: Any = None):
        self.__SOURCE = source

    def __call__(self, *args, **kwargs) -> Any:
        return self.__SOURCE


# ---------------------------------------------------------------------------------------------------------------------
TYPE__DEFAULT = Type[Default] | Default


# =====================================================================================================================
class ArgsEmpty(Default):
    """
    THIS IS JUST A PARTIAL CASE FOR ARGS Default

    DEPRECATE ???
    ---------
    USE DIRECTLY THE CONSTANT VALUE ()!!!
    its clear and

    GOAL
    ----
    explicit pass
    resolve not passed parameters in case of None VALUE!

    special object used as VALUE to show that parameter was not passed!
    dont pass it directly! keep it only as default parameter in class and in methods instead of None Value!
    it used only in special cases! not always even in one method!!!
    """
    def __init__(self, source: Any = ()):
        super().__init__(source)

    # # NOTE: this is not nesessory!!! and even need not to use for sure!
    # @classmethod
    # def __str__(cls):
    #     return "()"
    #
    # @classmethod
    # def __repr__(cls):
    #     return str(cls)
    #
    # @classmethod
    # def __len__(cls):
    #     return 0
    #
    # @classmethod
    # def __bool__(cls):
    #     return False
    #
    # @classmethod
    # def __iter__(cls):
    #     yield from ()


# ---------------------------------------------------------------------------------------------------------------------
TYPE__ARGS_EMPTY = Type[ArgsEmpty] | ArgsEmpty


# =====================================================================================================================
TYPE__ARGS = Union[tuple, Any, None, TYPE__ARGS_EMPTY, TYPE__DEFAULT]
TYPE__KWARGS = Optional[dict[str, Any]]


# =====================================================================================================================
def args__ensure_tuple(args: TYPE__ARGS = ()) -> tuple:
    """
    GOAL
    ----
    used in methods which handle with *args/args (like in funcs_aux.Valid)
    when we want to apply singular value without tuple

    CREATED SPECIALLY FOR
    ---------------------
    Valid
    but can be used in any funcs!

    USAGE
    -----
        def func1(*args):
            args = args__ensure_tuple(args)

        def func2(link: Callable, args):
            args = args__ensure_tuple(args)
            result = link(*args)

    :param args:
        NONE - is equivalent to SingleElement! so None -> (None, )
        any elementaryCollection - will convert to tuple!
        for others (classes/instances/irerables/generators/...) will assumed as single Object!!! and applied in tuple!!!

        unpacked iterables/generators - if need unpack it manually!!! its not difficult and so clear!
        elementary collection would unpack!
    """
    # APPLY DEFAULT --------------------------
    if args == Default or args == ArgsEmpty:
        args = ()
    elif isinstance(args, Default):
        args = args()

    # ENSURE TUPLE --------------------------
    if not TypeChecker.check__elementary_collection(args):
        result = (args, )
    else:
        result = tuple(args)
    return result


# =====================================================================================================================
if __name__ == '__main__':
    pass
    # CLS ----------------
    print(ArgsEmpty)    # <class '__main__.ArgsEmpty'>
    print(str(ArgsEmpty))   # <class '__main__.ArgsEmpty'>
    # print(len(ArgsEmpty))   #TypeError: object of type 'type' has no len()
    # print(list(ArgsEmpty))  #TypeError: 'type' object is not iterable
    print()

    # INST ---------------
    victim = ArgsEmpty()
    print(victim)
    print(str(victim))
    print(repr(victim))
    print(bool(victim))
    print(len(victim))
    print(list(victim))


# =====================================================================================================================
