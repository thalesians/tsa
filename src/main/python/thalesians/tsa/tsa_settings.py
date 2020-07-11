"""
`thalesians.tsa.tsa_settings`
=============================

This module configures the Time Series Analysis (TSA) library.

If a module named `local_tsa_settings` appears on the Python path, the settings contained in that module override the
settings from this module.

This module defines the following settings:

* `MIN_CHECK_LEVEL`: The minimum check level to check. Checks with level less than this value will be skipped and not
  checked. Defaults to 1 if `__debug__` is `True`, otherwise `sys.maxsize`.
* `MIN_PRECONDITION_LEVEL`: The minimum precondition level to check. Preconditions with level less than this value will
  be skipped and not checked. Defaults to 1 if `__debug__` is `True`, otherwise `sys.maxsize`. 
* `MIN_POSTCONDITION_LEVEL`: The minimum postcondition level to check. Postconditions with level less than this value
  will be skipped and not checked. Defaults to 1 if `__debug__` is `True`, otherwise `sys.maxsize`.
"""

import sys

# The __debug__ constant is True if Python was not started with an -O option.
if __debug__:
    MIN_CHECK_LEVEL = 1
    MIN_PRECONDITION_LEVEL = 1
    MIN_POSTCONDITION_LEVEL = 1
else:
    MIN_CHECK_LEVEL = sys.maxsize
    MIN_PRECONDITION_LEVEL = sys.maxsize
    MIN_POSTCONDITION_LEVEL = sys.maxsize

try:
    from local_tsa_settings import *
except ImportError:
    pass
