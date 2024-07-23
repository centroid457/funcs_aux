# DON'T DELETE!
# useful to start smth without pytest and not to run in main script!


from funcs_aux import *
from pytest_aux import *


result = ResultCum()
result.result__apply_step(True)
result.result__apply_step(True, msg="line2")
result.result__apply_step(ValueValidate(True))
result.result__apply_step(ValueValidate(LAMBDA_TRUE), msg="extraLine")

print(result)