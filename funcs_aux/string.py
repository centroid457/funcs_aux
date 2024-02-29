from typing import *
import json


# =====================================================================================================================
class Strings:
    SOURCE: str

    def __init__(self, source: str):
        self.SOURCE = source

    def try_convert_to__number(self, source: Optional[str] = None) -> Union[str, int, float]:
        if source is None:
            source = self.SOURCE

        try:
            source = json.loads(source)
        except:
            pass
        return source


# =====================================================================================================================
