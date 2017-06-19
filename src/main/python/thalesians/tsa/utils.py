import collections
import datetime as dt

import numpy as np

def iscallable(arg):
    return hasattr(arg, '__call__') or isinstance(arg, collections.Callable)

def sign(arg):
    if isinstance(arg, dt.timedelta):
        arg = arg.total_seconds()
    elif isinstance(arg, np.ndarray) and arg.dtype == object and np.size(arg) > 0 and isinstance(arg.item(0), dt.timedelta):
        arg = np.vectorize(lambda x: x.total_seconds())(arg)
    return np.sign(arg)

def xbatch(size, iterable):
    l = len(iterable)
    for i in range(0, l, size):
        yield iterable[i:min(i + size, l)]

def batch(size, iterable):
    return list(xbatch(size, iterable))
