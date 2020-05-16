import collections as col
import copy
import itertools
import math
import operator

import thalesians.tsa.intervals

# Based on an answer by Gustavo Bezerra on Stack Overflow
# https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
def is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            # Jupyter notebook or qtconsole
            return True
        elif shell == 'TerminalInteractiveShell':
            # Terminal running IPython
            return False
        else:
            # Other type (?)
            return False
    except NameError:
        # Probably a standard Python interpreter
        return False

def sequence_eq(sequence1, sequence2):
    """
    Compares two sequences.

    Parameters
    ----------
    sequence1 : sequence
        The first sequence.
    sequence2 : sequence
        The second sequence.

    Returns
    -------
    bool
        `True` iff `sequence1` equals `sequence2`, otherwise `False`.
    """
    return len(sequence1) == len(sequence2) and all(map(operator.eq, sequence1, sequence2))

def cmp(x, y):
    return (x > y) - (x < y)

def most_common(iterable):
    """
    >>> most_common(['foo', 'bar', 'bar', 'foo', 'bar'])
    'bar'
    >>> most_common(['foo', 'bar', 'bar', 'foo'])
    'foo'
    >>> most_common(['foo', 'bar'])
    'foo'
    """
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

def xconst(value):
    while True: yield value

def xbatch(size, iterable):
    """
    >>> list(xbatch(2, range(10)))
    [range(0, 2), range(2, 4), range(4, 6), range(6, 8), range(8, 10)]
    >>> list(xbatch(3, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']))
    [['Jan', 'Feb', 'Mar'], ['Apr', 'May', 'Jun'], ['Jul', 'Aug', 'Sep'], ['Oct', 'Nov', 'Dec']]
    >>> list(xbatch(3, ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')))
    [('Jan', 'Feb', 'Mar'), ('Apr', 'May', 'Jun'), ('Jul', 'Aug', 'Sep'), ('Oct', 'Nov', 'Dec')]
    >>> import numpy as np
    >>> list(xbatch(2, np.array(range(10))))
    [array([0, 1]), array([2, 3]), array([4, 5]), array([6, 7]), array([8, 9])]
    >>> list(xbatch(2, range(10)))
    [range(0, 2), range(2, 4), range(4, 6), range(6, 8), range(8, 10)]
    """
    l = len(iterable)
    for i in range(0, l, size):
        yield iterable[i:min(i + size, l)]

def batch(size, iterable):
    """
    >>> batch(2, range(10))
    [range(0, 2), range(2, 4), range(4, 6), range(6, 8), range(8, 10)]
    >>> batch(3, [429, 5, 2, 14, 42, 132, 1, 1])
    [[429, 5, 2], [14, 42, 132], [1, 1]]
    >>> batch(4, range(10))
    [range(0, 4), range(4, 8), range(8, 10)]
    """
    return list(xbatch(size, iterable))

def peek(iterable, size=1):
    """
    >>> it = xbatch(2, range(10))
    >>> first_three, new_it = peek(it, 3)
    >>> first_three
    [range(0, 2), range(2, 4), range(4, 6)]
    >>> list(new_it)
    [range(0, 2), range(2, 4), range(4, 6), range(6, 8), range(8, 10)]
    >>> list(it)
    []
        
    >>> it = xbatch(2, range(10))
    >>> first_three, new_it = peek(it, 3)
    >>> first_three
    [range(0, 2), range(2, 4), range(4, 6)]
    >>> list(it)
    [range(6, 8), range(8, 10)]
    """
    objs = []
    for _ in range(size):
        try:
            obj = next(iterable)
        except StopIteration:
            break
        objs.append(obj)
    return objs, itertools.chain(objs, iterable)

def intervals(start, end, delta, intervals_right_closed=False):
    """
    >>> intervals(start=0, end=15, delta=5, intervals_right_closed=False)
    [[0, 5), [5, 10), [10, 15)]
    
    >>> intervals(start=0, end=15, delta=5, intervals_right_closed=True)
    [(0, 5], (5, 10], (10, 15]]
    
    >>> intervals(start=0, end=15, delta=4, intervals_right_closed=False)
    [[0, 4), [4, 8), [8, 12), [12, 15)]
    
    >>> intervals(start=0, end=15, delta=4, intervals_right_closed=True)
    [(0, 4], (4, 8], (8, 12], (12, 15]]
    
    >>> import datetime as dt
    >>> intervals(start=dt.date(2019, 8, 31), end=dt.date(2019, 9, 15), delta=dt.timedelta(days=5), intervals_right_closed=False)
    [[2019-08-31, 2019-09-05), [2019-09-05, 2019-09-10), [2019-09-10, 2019-09-15)]
    
    >>> intervals(start=dt.date(2019, 8, 31), end=dt.date(2019, 9, 15), delta=dt.timedelta(days=5), intervals_right_closed=True)
    [(2019-08-31, 2019-09-05], (2019-09-05, 2019-09-10], (2019-09-10, 2019-09-15]]
    
    >>> intervals(start=dt.date(2019, 8, 31), end=dt.date(2019, 9, 15), delta=dt.timedelta(days=4), intervals_right_closed=False)
    [[2019-08-31, 2019-09-04), [2019-09-04, 2019-09-08), [2019-09-08, 2019-09-12), [2019-09-12, 2019-09-15)]
    
    >>> intervals(start=dt.date(2019, 8, 31), end=dt.date(2019, 9, 15), delta=dt.timedelta(days=4), intervals_right_closed=True)
    [(2019-08-31, 2019-09-04], (2019-09-04, 2019-09-08], (2019-09-08, 2019-09-12], (2019-09-12, 2019-09-15]]
    
    >>> intervals(start=dt.datetime(2019, 10, 8, 0), end=dt.datetime(2019, 10, 8, 15), delta=dt.timedelta(hours=5), intervals_right_closed=False)
    [[2019-10-08 00:00:00, 2019-10-08 05:00:00), [2019-10-08 05:00:00, 2019-10-08 10:00:00), [2019-10-08 10:00:00, 2019-10-08 15:00:00)]
    
    >>> intervals(start=dt.datetime(2019, 10, 8, 0), end=dt.datetime(2019, 10, 8, 15), delta=dt.timedelta(hours=5), intervals_right_closed=True)
    [(2019-10-08 00:00:00, 2019-10-08 05:00:00], (2019-10-08 05:00:00, 2019-10-08 10:00:00], (2019-10-08 10:00:00, 2019-10-08 15:00:00]]
    
    >>> intervals(start=dt.datetime(2019, 10, 8, 0), end=dt.datetime(2019, 10, 8, 15), delta=dt.timedelta(hours=4), intervals_right_closed=False)
    [[2019-10-08 00:00:00, 2019-10-08 04:00:00), [2019-10-08 04:00:00, 2019-10-08 08:00:00), [2019-10-08 08:00:00, 2019-10-08 12:00:00), [2019-10-08 12:00:00, 2019-10-08 15:00:00)]
    
    >>> intervals(start=dt.datetime(2019, 10, 8, 0), end=dt.datetime(2019, 10, 8, 15), delta=dt.timedelta(hours=4), intervals_right_closed=True)
    [(2019-10-08 00:00:00, 2019-10-08 04:00:00], (2019-10-08 04:00:00, 2019-10-08 08:00:00], (2019-10-08 08:00:00, 2019-10-08 12:00:00], (2019-10-08 12:00:00, 2019-10-08 15:00:00]]
    """
    result = []
    interval_start, interval_end = None, None
    while True:
        interval_start = start if interval_end is None else interval_end
        interval_end = min(end, interval_start + delta)
        result.append(thalesians.tsa.intervals.Interval(
            interval_start, interval_end,
            not intervals_right_closed, intervals_right_closed))
        if interval_end == end: break
    return result

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
    """
    >>> data = [8, 11, 12, 13, 14, 27, 29, 37, 49, 50, 51, 79, 85]
    
    >>> brackets, bracket_indices = bracket(data, 3, 5)
    >>> brackets
    [{[8, 13), 1}, {[13, 18), 2}, {[23, 28), 4}, {[28, 33), 5}, {[33, 38), 6}, {[48, 53), 9}, {[78, 83), 15}, {[83, 88), 16}]
    >>> bracket_indices
    [0, 0, 0, 1, 1, 2, 3, 4, 5, 5, 5, 6, 7]
    
    >>> brackets, bracket_indices = bracket(data, 3, 5, intervals_right_closed=True)
    >>> brackets
    [{(3, 8], 0}, {(8, 13], 1}, {(13, 18], 2}, {(23, 28], 4}, {(28, 33], 5}, {(33, 38], 6}, {(48, 53], 9}, {(78, 83], 15}, {(83, 88], 16}]
    >>> bracket_indices
    [0, 1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 7, 8]

    >>> brackets, bracket_indices = bracket(data, 3, 5, coalesce=True)
    >>> brackets
    [{[8, 18), 1}, {[23, 38), 4}, {[48, 53), 9}, {[78, 88), 15}]
    >>> bracket_indices
    [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3]

    >>> brackets, bracket_indices = bracket(data, 3, 5, intervals_right_closed=True, coalesce=True)
    >>> brackets
    [{(3, 18], 0}, {(23, 38], 4}, {(48, 53], 9}, {(78, 88], 15}]
    >>> bracket_indices
    [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3]
    
    >>> import datetime as dt
    >>> data = [dt.date(2017, 1, 31) + dt.timedelta(days=x) for x in [8, 11, 12, 13, 14, 27, 29, 37, 49, 50, 51, 79, 85]];
    
    >>> brackets, bracket_indices = bracket(data, dt.date(2017, 2, 3), dt.timedelta(days=5))
    >>> brackets
    [{[2017-02-08, 2017-02-13), 1}, {[2017-02-13, 2017-02-18), 2}, {[2017-02-23, 2017-02-28), 4}, {[2017-02-28, 2017-03-05), 5}, {[2017-03-05, 2017-03-10), 6}, {[2017-03-20, 2017-03-25), 9}, {[2017-04-19, 2017-04-24), 15}, {[2017-04-24, 2017-04-29), 16}]
    >>> bracket_indices
    [0, 0, 0, 1, 1, 2, 3, 4, 5, 5, 5, 6, 7]

    >>> brackets, bracket_indices = bracket(data, dt.date(2017, 2, 3), dt.timedelta(days=5), intervals_right_closed=True)
    >>> brackets
    [{(2017-02-03, 2017-02-08], 0}, {(2017-02-08, 2017-02-13], 1}, {(2017-02-13, 2017-02-18], 2}, {(2017-02-23, 2017-02-28], 4}, {(2017-02-28, 2017-03-05], 5}, {(2017-03-05, 2017-03-10], 6}, {(2017-03-20, 2017-03-25], 9}, {(2017-04-19, 2017-04-24], 15}, {(2017-04-24, 2017-04-29], 16}]
    >>> bracket_indices
    [0, 1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 7, 8]

    >>> brackets, bracket_indices = bracket(data, dt.date(2017, 2, 3), dt.timedelta(days=5), coalesce=True)
    >>> brackets
    [{[2017-02-08, 2017-02-18), 1}, {[2017-02-23, 2017-03-10), 4}, {[2017-03-20, 2017-03-25), 9}, {[2017-04-19, 2017-04-29), 15}]
    >>> bracket_indices
    [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3]

    >>> brackets, bracket_indices = bracket(data, dt.date(2017, 2, 3), dt.timedelta(days=5), intervals_right_closed=True, coalesce=True)
    >>> brackets
    [{(2017-02-03, 2017-02-18], 0}, {(2017-02-23, 2017-03-10], 4}, {(2017-03-20, 2017-03-25], 9}, {(2017-04-19, 2017-04-29], 15}]
    >>> bracket_indices
    [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3]

    >>> data = [dt.datetime(2017, 1, 31, 0, 0, 0) + dt.timedelta(minutes=x) for x in [8, 11, 12, 13, 14, 27, 29, 37, 49, 50, 51, 79, 85]];

    >>> brackets, bracket_indices = bracket(data, dt.datetime(2017, 1, 31, 0, 3, 0), dt.timedelta(minutes=5))
    >>> brackets
    [{[2017-01-31 00:08:00, 2017-01-31 00:13:00), 1}, {[2017-01-31 00:13:00, 2017-01-31 00:18:00), 2}, {[2017-01-31 00:23:00, 2017-01-31 00:28:00), 4}, {[2017-01-31 00:28:00, 2017-01-31 00:33:00), 5}, {[2017-01-31 00:33:00, 2017-01-31 00:38:00), 6}, {[2017-01-31 00:48:00, 2017-01-31 00:53:00), 9}, {[2017-01-31 01:18:00, 2017-01-31 01:23:00), 15}, {[2017-01-31 01:23:00, 2017-01-31 01:28:00), 16}]
    >>> bracket_indices
    [0, 0, 0, 1, 1, 2, 3, 4, 5, 5, 5, 6, 7]

    >>> brackets, bracket_indices = bracket(data, dt.datetime(2017, 1, 31, 0, 3, 0), dt.timedelta(minutes=5), intervals_right_closed=True)
    >>> brackets
    [{(2017-01-31 00:03:00, 2017-01-31 00:08:00], 0}, {(2017-01-31 00:08:00, 2017-01-31 00:13:00], 1}, {(2017-01-31 00:13:00, 2017-01-31 00:18:00], 2}, {(2017-01-31 00:23:00, 2017-01-31 00:28:00], 4}, {(2017-01-31 00:28:00, 2017-01-31 00:33:00], 5}, {(2017-01-31 00:33:00, 2017-01-31 00:38:00], 6}, {(2017-01-31 00:48:00, 2017-01-31 00:53:00], 9}, {(2017-01-31 01:18:00, 2017-01-31 01:23:00], 15}, {(2017-01-31 01:23:00, 2017-01-31 01:28:00], 16}]
    >>> bracket_indices
    [0, 1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 7, 8]

    >>> brackets, bracket_indices = bracket(data, dt.datetime(2017, 1, 31, 0, 3, 0), dt.timedelta(minutes=5), coalesce=True)
    >>> brackets
    [{[2017-01-31 00:08:00, 2017-01-31 00:18:00), 1}, {[2017-01-31 00:23:00, 2017-01-31 00:38:00), 4}, {[2017-01-31 00:48:00, 2017-01-31 00:53:00), 9}, {[2017-01-31 01:18:00, 2017-01-31 01:28:00), 15}]
    >>> bracket_indices
    [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3]

    >>> brackets, bracket_indices = bracket(data, dt.datetime(2017, 1, 31, 0, 3, 0), dt.timedelta(minutes=5), intervals_right_closed=True, coalesce=True)
    >>> brackets
    [{(2017-01-31 00:03:00, 2017-01-31 00:18:00], 0}, {(2017-01-31 00:23:00, 2017-01-31 00:38:00], 4}, {(2017-01-31 00:48:00, 2017-01-31 00:53:00], 9}, {(2017-01-31 01:18:00, 2017-01-31 01:28:00], 15}]
    >>> bracket_indices
    [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3]
    """
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
                    Bracket(thalesians.tsa.intervals.Interval(interval_left,
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

class FlatStoredArray(object):
    def __init__(self, *args):
        self.__count = self._getcount(*args)
        self._data = [None] * self.__count
    
    def _getcount(self):
        raise NotImplementedError('Pure virtual method')
    
    def _keytoindex(self, key):
        raise NotImplementedError('Pure virtual method')
    
    def _indextokey(self, index):
        raise NotImplementedError('Pure virtual method')

    def __getitem__(self, key):
        return self._data[self._keytoindex(key)]
    
    def __setitem__(self, key, value):
        self._data[self._keytoindex(key)] = value
        
    def __len__(self):
        return self.__count
    
    def __str__(self):
        return str(self._data)
    
    def __repr__(self):
        return repr(self._data)
    
    def setall(self, iterable):
        for i, v in enumerate(iterable):
            if i >= self.__count: break
            self._data[i] = v
            
    class __Iterator(object):
        def __init__(self, data):
            self._data = data
            self.__idx = 0
            
        def __iter__(self):
            return self
            
        def __next__(self):
            if self.__idx < len(self._data):
                v = self._data[self.__idx]
                self.__idx += 1
                return v
            raise StopIteration()

    def __iter__(self):
        return FlatStoredArray.__Iterator(self._data)
    
    class __KeysIterator(object):
        def __init__(self, collection):
            self.__collection = collection
            self.__idx = 0
            
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.__idx < len(self.__collection):
                k = self.__collection._indextokey(self.__idx)
                self.__idx += 1
                return k
            raise StopIteration()
        
    def keys(self):
        return FlatStoredArray.__KeysIterator(self)

    class __ItemsIterator(object):
        def __init__(self, data, collection):
            self.__data = data
            self.__collection = collection
            self.__idx = 0
            
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.__idx < len(self.__data):
                k = self.__collection._indextokey(self.__idx)
                v = self.__data[self.__idx]
                self.__idx += 1
                return k, v
            raise StopIteration()
        
    def items(self):
        return FlatStoredArray.__ItemsIterator(self._data, self)
    
class DiagonalArray(FlatStoredArray):
    """
    >>> a = DiagonalArray(5)
    
    >>> a[0,0] = 0
    >>> a[1,0], a[1,1] = 10, 20
    >>> a[2,0], a[2,1], a[2,2] = 30, 40, 50
    >>> a[3,0], a[3,1], a[3,2], a[3,3] = 60, 70, 80, 90
    >>> a[4,0], a[4,1], a[4,2], a[4,3], a[4,4] = 100, 110, 120, 130, 140
    
    >>> len(a)
    15
    
    >>> a[0,0]
    0
    >>> a[1,0]
    10
    >>> a[1,1]
    20
    >>> a[2,0]
    30
    >>> a[2,1]
    40
    >>> a[2,2]
    50
    >>> a[3,0]
    60
    >>> a[3,1]
    70
    >>> a[3,2]
    80
    >>> a[3,3]
    90
    >>> a[4,0]
    100
    >>> a[4,1]
    110
    >>> a[4,2]
    120
    >>> a[4,3]
    130
    >>> a[4,4]
    140
    
    >>> a[0,0]
    0
    >>> a[0,1]
    10
    >>> a[1,1]
    20
    >>> a[0,2]
    30
    >>> a[1,2]
    40
    >>> a[2,2]
    50
    >>> a[0,3]
    60
    >>> a[1,3]
    70
    >>> a[2,3]
    80
    >>> a[3,3]
    90
    >>> a[0,4]
    100
    >>> a[1,4]
    110
    >>> a[2,4]
    120
    >>> a[3,4]
    130
    >>> a[4,4]
    140
    
    >>> a._indextokey(0)
    (0, 0)
    >>> a._indextokey(1)
    (1, 0)
    >>> a._indextokey(2)
    (1, 1)
    >>> a._indextokey(3)
    (2, 0)
    >>> a._indextokey(4)
    (2, 1)
    >>> a._indextokey(5)
    (2, 2)
    >>> a._indextokey(6)
    (3, 0)
    >>> a._indextokey(7)
    (3, 1)
    >>> a._indextokey(8)
    (3, 2)
    >>> a._indextokey(9)
    (3, 3)
    >>> a._indextokey(10)
    (4, 0)
    >>> a._indextokey(11)
    (4, 1)
    >>> a._indextokey(12)
    (4, 2)
    >>> a._indextokey(13)
    (4, 3)
    >>> a._indextokey(14)
    (4, 4)

    >>> values = []
    >>> for v in a: values.append(v)
    >>> tuple(a)
    (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140)
    
    >>> keys = []
    >>> for k in a.keys(): keys.append(k)
    >>> keys
    [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2), (3, 3), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]

    >>> keys, values = [], []
    >>> for k, v in a.items():
    ...     keys.append(k)
    ...     values.append(v)
    >>> keys
    [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2), (3, 3), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    >>> values
    [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
    
    >>> a.mindim(1)
    1
    >>> a.mindim(2)
    2
    >>> a.mindim(3)
    2
    >>> a.mindim(4)
    3
    >>> a.mindim(5)
    3
    >>> a.mindim(6)
    3
    >>> a.mindim(7)
    4
    >>> a.mindim(8)
    4
    >>> a.mindim(9)
    4
    >>> a.mindim(10)
    4
    >>> a.mindim(11)
    5
    >>> a.mindim(12)
    5
    >>> a.mindim(13)
    5
    >>> a.mindim(14)
    5
    >>> a.mindim(15)
    5
    """
    def __init__(self, dim):
        super(DiagonalArray, self).__init__(dim)
        self.__dim = dim
        
    @property
    def dim(self): return self.__dim
    
    @classmethod
    def _getcount(cls, dim):
        return (dim*dim + dim) // 2
    
    @classmethod
    def _keytoindex(cls, key):
        i, j = key[0], key[1]
        if i < j: i, j = j, i
        return (i*i + i) // 2 + j
    
    @classmethod
    def _indextokey(self, index):
        i = int(math.sqrt(2*index))
        n = (i*i + i) // 2
        j = index - n
        if j < 0:
            i -= 1
            n = (i*i + i) // 2
            j = index - n
        return i, j
    
    @classmethod
    def mindim(cls, count):
        dim = int(math.sqrt(2*count))
        if cls._getcount(dim) < count:
            dim += 1
        return dim
    
    @classmethod
    def create(cls, obj):
        if isinstance(obj, DiagonalArray):
            res = DiagonalArray(obj.dim)
            res.setall(obj)
        elif isinstance(obj, SubdiagonalArray):
            res = DiagonalArray(obj.dim)
            for k, v in obj.items():
                self[k] = v
        else:
            res = DiagonalArray(cls.mindim(len(obj)))
            res.setall(obj)
        return res
    
    def tonumpyarray(self, fill=None, symmetric=False):
        import numpy as np
        if fill is None: fill = np.NAN
        res = np.empty((self.__dim, self.__dim))
        idx = 0
        for i in range(self.__dim):
            for j in range(i+1):
                res[i,j] = self._data[idx]
                if symmetric: res[j,i] = res[i,j]
                idx += 1
            if not symmetric: res[i,i+1:self.__dim] = fill
        return res
        
class SubdiagonalArray(FlatStoredArray):
    """
    >>> a = SubdiagonalArray(5)
    >>> a[1,0] = 0
    >>> a[2,0], a[2,1] = 10, 20
    >>> a[3,0], a[3,1], a[3,2] = 30, 40, 50
    >>> a[4,0], a[4,1], a[4,2], a[4,3] = 60, 70, 80, 90
    
    >>> len(a)
    10
    
    >>> a[1,0]
    0
    >>> a[2,0]
    10
    >>> a[2,1]
    20
    >>> a[3,0]
    30
    >>> a[3,1]
    40
    >>> a[3,2]
    50
    >>> a[4,0]
    60
    >>> a[4,1]
    70
    >>> a[4,2]
    80
    >>> a[4,3]
    90
    
    >>> a[0,1]
    0
    >>> a[0,2]
    10
    >>> a[1,2]
    20
    >>> a[0,3]
    30
    >>> a[1,3]
    40
    >>> a[2,3]
    50
    >>> a[0,4]
    60
    >>> a[1,4]
    70
    >>> a[2,4]
    80
    >>> a[3,4]
    90
    
    >>> a._indextokey(0)
    (1, 0)
    >>> a._indextokey(1)
    (2, 0)
    >>> a._indextokey(2)
    (2, 1)
    >>> a._indextokey(3)
    (3, 0)
    >>> a._indextokey(4)
    (3, 1)
    >>> a._indextokey(5)
    (3, 2)
    >>> a._indextokey(6)
    (4, 0)
    >>> a._indextokey(7)
    (4, 1)
    >>> a._indextokey(8)
    (4, 2)
    >>> a._indextokey(9)
    (4, 3)
    
    >>> values = []
    >>> for v in a: values.append(v)
    >>> values
    [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

    >>> keys = []
    >>> for k in a.keys(): keys.append(k)
    >>> keys
    [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (4, 3)]

    >>> keys, values = [], []
    >>> for k, v in a.items():
    ...     keys.append(k)
    ...     values.append(v)
    >>> keys
    [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (4, 3)]
    >>> values
    [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

    >>> a.mindim(1)
    2
    >>> a.mindim(2)
    3
    >>> a.mindim(3)
    3
    >>> a.mindim(4)
    4
    >>> a.mindim(5)
    4
    >>> a.mindim(6)
    4
    >>> a.mindim(7)
    5
    >>> a.mindim(8)
    5
    >>> a.mindim(9)
    5
    >>> a.mindim(10)
    5
    """
    def __init__(self, dim):
        super(SubdiagonalArray, self).__init__(dim)
        self.__dim = dim
        
    @property
    def dim(self): return self.__dim
    
    @classmethod
    def _getcount(cls, dim):
        return (dim*dim - dim) // 2
        
    @classmethod
    def _keytoindex(cls, key):
        i, j = key[0], key[1]
        if i < j: i, j = j, i
        return (i*i - i) // 2 + j

    @classmethod
    def _indextokey(cls, index):
        i = int(math.sqrt(2*index)) + 1
        n = (i*i - i) // 2
        j = index - n
        if j < 0:
            i -= 1
            n = (i*i - i) // 2
            j = index - n
        return i, j
    
    @classmethod
    def mindim(cls, count):
        dim = int(math.sqrt(2*count)) + 1
        if cls._getcount(dim) < count:
            dim += 1
        return dim
    
    @classmethod
    def create(cls, obj):
        if isinstance(obj, SubdiagonalArray):
            res = SubdiagonalArray(obj.dim)
            res.setall(obj)
        elif isinstance(obj, DiagonalArray):
            res = SubdiagonalArray(obj.dim)
            for k, v in obj.items():
                if k[0] != k[1]: self[k] = v
        else:
            res = SubdiagonalArray(cls.mindim(len(obj)))
            res.setall(obj)
        return res

    def tonumpyarray(self, fill=None, symmetric=False):
        import numpy as np
        if fill is None: fill = np.NAN
        res = np.empty((self.__dim, self.__dim))
        idx = 0
        for i in range(self.__dim):
            for j in range(i):
                res[i,j] = self._data[idx]
                if symmetric: res[j,i] = res[i,j]
                idx += 1
            res[i,i] = fill
            if not symmetric: res[i,i+1:self.__dim] = fill
        return res

def _test():
    import doctest
    doctest.testmod(verbose=True)

if __name__ == '__main__':
    _test()
