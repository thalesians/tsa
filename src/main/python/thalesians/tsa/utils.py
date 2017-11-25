import collections as col
import copy
import itertools
import operator

import thalesians.tsa.intervals as intervals

def most_common(iterable):
    sorted_iterable = sorted((x, i) for i, x in enumerate(iterable))
    groups = itertools.groupby(sorted_iterable, key=operator.itemgetter(0))
    def _auxfun(g):
        _, it = g
        count = 0
        min_index = len(iterable)
        for _, where in it:
            count += 1
            min_index = min(min_index, where)
        return count, -min_index
    return max(groups, key=_auxfun)[0]

def prepend(collection, to_prepend, in_place=False):
    if not in_place: collection = copy.copy(collection)
    collection[0:0] = to_prepend
    return collection

def _pad_on_left_with_callable(collection, new_len, padding=None):
    return prepend(collection, [padding() for _ in range(new_len - len(collection))], in_place=True)

def _pad_on_left_with_noncallable(collection, new_len, padding=None):
    return prepend(collection, [padding for _ in range(new_len - len(collection))], in_place=True)

def pad_on_left(collection, new_len, padding=None, in_place=False):
    if not in_place: collection = copy.copy(collection)
    if hasattr(padding, '__call__') or isinstance(padding, col.Callable):
        return _pad_on_left_with_callable(collection, new_len, padding)
    else:
        return _pad_on_left_with_noncallable(collection, new_len, padding)

def _pad_on_right_with_callable(collection, new_len, padding=None):
    collection.extend([padding() for _ in range(new_len - len(collection))])
    return collection

def _pad_on_right_with_noncallable(collection, new_len, padding=None):
    collection.extend([padding for _ in range(new_len - len(collection))])
    return collection

def pad_on_right(collection, new_len, padding=None, in_place=False):
    if not in_place: collection = copy.copy(collection)
    if hasattr(padding, '__call__') or isinstance(padding, col.Callable):
        return _pad_on_right_with_callable(collection, new_len, padding)
    else:
        return _pad_on_right_with_noncallable(collection, new_len, padding)

def trim_on_left(collection, new_len, in_place=False):
    if not in_place: collection = copy.copy(collection)
    del collection[:max(len(collection) - new_len, 0)]
    return collection

def trim_on_right(collection, new_len, in_place=False):
    if not in_place: collection = copy.copy(collection)
    del collection[new_len:]
    return collection

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

class Bracket(object):
    def __init__(self, interval, interval_offset):
        self.interval = interval
        self.interval_offset = interval_offset
        self._str_Bracket = None
        
    def __eq__(self, other):
        return self.interval == other.interval and self.interval_offset == other.interval_offset
        
    def __str__(self):
        if self._str_Bracket is None:
            self._str_Bracket = '{' + str(self.interval) + ', ' + str(self.interval_offset) + '}'
        return self._str_Bracket
    
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
