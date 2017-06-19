import sys

if __debug__:
    MIN_PRECONDITION_LEVEL = 1
    MIN_POSTCONDITION_LEVEL = 1
    MIN_CHECK_LEVEL = 1
else:
    MIN_PRECONDITION_LEVEL = sys.maxsize
    MIN_POSTCONDITION_LEVEL = sys.maxsize
    MIN_CHECK_LEVEL = sys.maxsize

try:
    from local_settings import *
except ImportError:
    pass
