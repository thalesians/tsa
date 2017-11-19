import datetime as dt
import itertools
import operator

import numpy as np

import thalesians.tsa.intervals as intervals

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
    for _ in range(size):
        try:
            obj = next(iterable)
        except StopIteration:
            break
        objs.append(obj)
    return objs, itertools.chain(objs, iterable)

class Bracket:
    def __init__(self, interval, interval_offset):
        self.interval = interval
        self.interval_offset = interval_offset
        
    def __eq__(self, other):
        return self.interval == other.interval and self.interval_offset == other.interval_offset
        
    def __str__(self):
        return '{' + str(self.interval) + ', ' + str(self.interval_offset) + '}'
    
    def __repr__(self):
        return str(self)

def bracket(iterable, origin, interval_size, already_sorted=False, intervals_right_closed=False, coalesce=False):
    if not already_sorted:
        sorted_indices, iterable = zip(*sorted([(i, v) for i, v in enumerate(iterable)], key=operator.itemgetter(1)))
    
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
                    Bracket(intervals.Interval(interval_left,
                                     interval_right,
                                     not intervals_right_closed,
                                     intervals_right_closed),
                            interval_offset))
            
        bracket_indices.append(len(brackets) - 1)
        
    if not already_sorted:
        new_bracket_indices = [None] * len(bracket_indices)
        for i in range(len(bracket_indices)):
            new_bracket_indices[sorted_indices[i]] = bracket_indices[i]
        bracket_indices = new_bracket_indices
    
    return brackets, bracket_indices
