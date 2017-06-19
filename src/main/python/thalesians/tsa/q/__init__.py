import sys

# In Python 2.6 and below sys.version_info is not a named tuple. The following check works across versions:
if sys.version_info[0] >= 3:
    from thalesians.tsa.q.q3 import *
else:
    from thalesians.tsa.q.q2 import *
