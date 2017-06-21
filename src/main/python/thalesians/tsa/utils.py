import datetime as dt
import itertools

import numpy as np

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

def peek(iterable, size=1):
    objs = []
    for i in range(size):
        try:
            obj = next(iterable)
        except StopIteration:
            break
        objs.append(obj)
    return objs, itertools.chain(objs, iterable)
