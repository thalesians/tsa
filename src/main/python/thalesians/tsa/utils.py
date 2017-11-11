import collections as col
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

class Interval:
    def __init__(self, left, right, left_closed=False, right_closed=False):
        self._left = left
        self._right = right
        self._left_closed = left_closed
        self._right_closed = right_closed
        
    @property
    def left(self):
        return self._left
        
    @property
    def right(self):
        return self._right
        
    def replace_left(self, new_left, new_left_closed=None):
        if new_left_closed is None: new_left_closed = self._left_closed
        return Interval(new_left, self._right, new_left_closed, self._right_closed)
    
    def replace_right(self, new_right, new_right_closed=None):
        if new_right_closed is None: new_right_closed = self._right_closed
        return Interval(self._left, new_right, self._left_closed, new_right_closed)
    
    def __str__(self):
        return ('[' if self._left_closed else '(') + \
                str(self._left) + ', ' + str(self._right) + \
                (']' if self._right_closed else ')')
                
    def __repr__(self):
        return str(self)
    
class Bracket:
    def __init__(self, interval, interval_offset):
        self.interval = interval
        self.interval_offset = interval_offset
        
    def __str__(self):
        return '{' + str(self.interval) + ', ' + str(self.interval_offset) + '}'
    
    def __repr__(self):
        return str(self)

def bracket(iterable, origin, interval_size, already_sorted=False, intervals_right_closed=False, coalesce=False):
    if not already_sorted:
        iterable = sorted(iterable)
    
    brackets = []
    bracket_indices = []
    
    interval_offset = None
    interval_left = None
    interval_right = None
    
    for x in iterable:
        if interval_offset is None or x - interval_left >= interval_size:
            new_interval_offset = (x - origin) // interval_size
            new_interval_left = origin + new_interval_offset * interval_size
            
            if intervals_right_closed and x == new_interval_left:
                new_interval_offset -= 1
                new_interval_left -= interval_size
            
            if coalesce and (interval_offset is not None) and (new_interval_left <= brackets[-1].interval.right):
                interval_right = new_interval_left + interval_size
                brackets[-1].interval = brackets[-1].interval.replace_right(interval_right)
            elif interval_offset is None or new_interval_offset != interval_offset:
                interval_offset = new_interval_offset
                interval_left = new_interval_left
                interval_right = interval_left + interval_size
                brackets.append(
                    Bracket(Interval(interval_left,
                                     interval_right,
                                     not intervals_right_closed,
                                     intervals_right_closed),
                            interval_offset))
            
        bracket_indices.append(len(brackets) - 1)
    
    return brackets, bracket_indices
