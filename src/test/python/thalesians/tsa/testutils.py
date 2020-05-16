import datetime as dt
import unittest

import numpy as np
import numpy.testing as npt

import thalesians.tsa.intervals as intervals
import thalesians.tsa.utils as utils

# In case you are interested, the numbers used in these tests come from the A000108 sequence (Catalan numbers).

class TestUtils(unittest.TestCase):
    def test_is_notebok(self):
        self.assertFalse(utils.is_notebook())
    
    def test_most_common(self):
        self.assertEqual(utils.most_common(['foo', 'bar', 'bar', 'foo', 'bar']), 'bar')
        self.assertEqual(utils.most_common(['foo', 'bar', 'bar', 'foo']), 'foo')
        
    def test_xbatch(self):
        self.assertSequenceEqual(list(utils.xbatch(2, range(10))),
                [range(0, 2), range(2, 4), range(4, 6), range(6, 8), range(8, 10)])
        self.assertSequenceEqual(list(utils.xbatch(3, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])),
                [['Jan', 'Feb', 'Mar'], ['Apr', 'May', 'Jun'], ['Jul', 'Aug', 'Sep'], ['Oct', 'Nov', 'Dec']])
        self.assertSequenceEqual(list(utils.xbatch(3, ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))),
                [('Jan', 'Feb', 'Mar'), ('Apr', 'May', 'Jun'), ('Jul', 'Aug', 'Sep'), ('Oct', 'Nov', 'Dec')])
        npt.assert_almost_equal(list(utils.xbatch(2, np.array(range(10)))),
                [np.array([0, 1]), np.array([2, 3]), np.array([4, 5]), np.array([6, 7]), np.array([8, 9])])
        self.assertSequenceEqual(list(utils.xbatch(2, range(10))),
                [range(0, 2), range(2, 4), range(4, 6), range(6, 8), range(8, 10)])
    
    def test_batch(self):
        self.assertSequenceEqual(utils.batch(2, range(10)),
                [range(0, 2), range(2, 4), range(4, 6), range(6, 8), range(8, 10)])
        self.assertEqual(utils.batch(3, [429, 5, 2, 14, 42, 132, 1, 1]), [[429, 5, 2], [14, 42, 132], [1, 1]])
        self.assertEqual(utils.batch(4, range(10)), [range(0, 4), range(4, 8), range(8, 10)])
    
    def test_peek(self):
        it = utils.xbatch(2, range(10))
        first_three, new_it = utils.peek(it, 3)
        self.assertSequenceEqual(first_three, [range(0, 2), range(2, 4), range(4, 6)])
        self.assertSequenceEqual(list(new_it), [range(0, 2), range(2, 4), range(4, 6), range(6, 8), range(8, 10)])
        self.assertSequenceEqual(list(it), [])
        
        it = utils.xbatch(2, range(10))
        first_three, new_it = utils.peek(it, 3)
        self.assertSequenceEqual(first_three, [range(0, 2), range(2, 4), range(4, 6)])
        self.assertSequenceEqual(list(it), [range(6, 8), range(8, 10)])
        
    def test_intervals(self):
        result = utils.intervals(start=0, end=15, delta=5, intervals_right_closed=False)
        self.assertSequenceEqual(result, [
            intervals.Interval(0, 5, left_closed=True, right_closed=False),
            intervals.Interval(5, 10, left_closed=True, right_closed=False),
            intervals.Interval(10, 15, left_closed=True, right_closed=False)])
        
        result = utils.intervals(start=0, end=15, delta=5, intervals_right_closed=True)
        self.assertSequenceEqual(result, [
            intervals.Interval(0, 5, left_closed=False, right_closed=True),
            intervals.Interval(5, 10, left_closed=False, right_closed=True),
            intervals.Interval(10, 15, left_closed=False, right_closed=True)])
        
        result = utils.intervals(start=0, end=15, delta=4, intervals_right_closed=False)
        self.assertSequenceEqual(result, [
            intervals.Interval(0, 4, left_closed=True, right_closed=False),
            intervals.Interval(4, 8, left_closed=True, right_closed=False),
            intervals.Interval(8, 12, left_closed=True, right_closed=False),
            intervals.Interval(12, 15, left_closed=True, right_closed=False)])
        
        result = utils.intervals(start=0, end=15, delta=4, intervals_right_closed=True)
        self.assertSequenceEqual(result, [
            intervals.Interval(0, 4, left_closed=False, right_closed=True),
            intervals.Interval(4, 8, left_closed=False, right_closed=True),
            intervals.Interval(8, 12, left_closed=False, right_closed=True),
            intervals.Interval(12, 15, left_closed=False, right_closed=True)])
        
        result = utils.intervals(start=dt.date(2019, 8, 31), end=dt.date(2019, 9, 15), delta=dt.timedelta(days=5), intervals_right_closed=False)
        self.assertSequenceEqual(result, [
            intervals.Interval(dt.date(2019, 8, 31), dt.date(2019, 9, 5), left_closed=True, right_closed=False),
            intervals.Interval(dt.date(2019, 9, 5), dt.date(2019, 9, 10), left_closed=True, right_closed=False),
            intervals.Interval(dt.date(2019, 9, 10), dt.date(2019, 9, 15), left_closed=True, right_closed=False)])
        
        result = utils.intervals(start=dt.date(2019, 8, 31), end=dt.date(2019, 9, 15), delta=dt.timedelta(days=5), intervals_right_closed=True)
        self.assertSequenceEqual(result, [
            intervals.Interval(dt.date(2019, 8, 31), dt.date(2019, 9, 5), left_closed=False, right_closed=True),
            intervals.Interval(dt.date(2019, 9, 5), dt.date(2019, 9, 10), left_closed=False, right_closed=True),
            intervals.Interval(dt.date(2019, 9, 10), dt.date(2019, 9, 15), left_closed=False, right_closed=True)])
        
        result = utils.intervals(start=dt.date(2019, 8, 31), end=dt.date(2019, 9, 15), delta=dt.timedelta(days=4), intervals_right_closed=False)
        self.assertSequenceEqual(result, [
            intervals.Interval(dt.date(2019, 8, 31), dt.date(2019, 9, 4), left_closed=True, right_closed=False),
            intervals.Interval(dt.date(2019, 9, 4), dt.date(2019, 9, 8), left_closed=True, right_closed=False),
            intervals.Interval(dt.date(2019, 9, 8), dt.date(2019, 9, 12), left_closed=True, right_closed=False),
            intervals.Interval(dt.date(2019, 9, 12), dt.date(2019, 9, 15), left_closed=True, right_closed=False)])
        
        result = utils.intervals(start=dt.date(2019, 8, 31), end=dt.date(2019, 9, 15), delta=dt.timedelta(days=4), intervals_right_closed=True)
        self.assertSequenceEqual(result, [
            intervals.Interval(dt.date(2019, 8, 31), dt.date(2019, 9, 4), left_closed=False, right_closed=True),
            intervals.Interval(dt.date(2019, 9, 4), dt.date(2019, 9, 8), left_closed=False, right_closed=True),
            intervals.Interval(dt.date(2019, 9, 8), dt.date(2019, 9, 12), left_closed=False, right_closed=True),
            intervals.Interval(dt.date(2019, 9, 12), dt.date(2019, 9, 15), left_closed=False, right_closed=True)])
        
        result = utils.intervals(start=dt.datetime(2019, 10, 8, 0), end=dt.datetime(2019, 10, 8, 15), delta=dt.timedelta(hours=5), intervals_right_closed=False)
        self.assertSequenceEqual(result, [
            intervals.Interval(dt.datetime(2019, 10, 8, 0), dt.datetime(2019, 10, 8, 5), left_closed=True, right_closed=False),
            intervals.Interval(dt.datetime(2019, 10, 8, 5), dt.datetime(2019, 10, 8, 10), left_closed=True, right_closed=False),
            intervals.Interval(dt.datetime(2019, 10, 8, 10), dt.datetime(2019, 10, 8, 15), left_closed=True, right_closed=False)])
        
        result = utils.intervals(start=dt.datetime(2019, 10, 8, 0), end=dt.datetime(2019, 10, 8, 15), delta=dt.timedelta(hours=5), intervals_right_closed=True)
        self.assertSequenceEqual(result, [
            intervals.Interval(dt.datetime(2019, 10, 8, 0), dt.datetime(2019, 10, 8, 5), left_closed=False, right_closed=True),
            intervals.Interval(dt.datetime(2019, 10, 8, 5), dt.datetime(2019, 10, 8, 10), left_closed=False, right_closed=True),
            intervals.Interval(dt.datetime(2019, 10, 8, 10), dt.datetime(2019, 10, 8, 15), left_closed=False, right_closed=True)])
        
        result = utils.intervals(start=dt.datetime(2019, 10, 8, 0), end=dt.datetime(2019, 10, 8, 15), delta=dt.timedelta(hours=4), intervals_right_closed=False)
        self.assertSequenceEqual(result, [
            intervals.Interval(dt.datetime(2019, 10, 8, 0), dt.datetime(2019, 10, 8, 4), left_closed=True, right_closed=False),
            intervals.Interval(dt.datetime(2019, 10, 8, 4), dt.datetime(2019, 10, 8, 8), left_closed=True, right_closed=False),
            intervals.Interval(dt.datetime(2019, 10, 8, 8), dt.datetime(2019, 10, 8, 12), left_closed=True, right_closed=False),
            intervals.Interval(dt.datetime(2019, 10, 8, 12), dt.datetime(2019, 10, 8, 15), left_closed=True, right_closed=False)])
        
        result = utils.intervals(start=dt.datetime(2019, 10, 8, 0), end=dt.datetime(2019, 10, 8, 15), delta=dt.timedelta(hours=4), intervals_right_closed=True)
        self.assertSequenceEqual(result, [
            intervals.Interval(dt.datetime(2019, 10, 8, 0), dt.datetime(2019, 10, 8, 4), left_closed=False, right_closed=True),
            intervals.Interval(dt.datetime(2019, 10, 8, 4), dt.datetime(2019, 10, 8, 8), left_closed=False, right_closed=True),
            intervals.Interval(dt.datetime(2019, 10, 8, 8), dt.datetime(2019, 10, 8, 12), left_closed=False, right_closed=True),
            intervals.Interval(dt.datetime(2019, 10, 8, 12), dt.datetime(2019, 10, 8, 15), left_closed=False, right_closed=True)])
        
    def test_bracket(self):
        data = [8, 11, 12, 13, 14, 27, 29, 37, 49, 50, 51, 79, 85]
        
        brackets, bracket_indices = utils.bracket(data, 3, 5)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(intervals.Interval(8, 13, left_closed=True), 1),
                utils.Bracket(intervals.Interval(13, 18, left_closed=True), 2),
                utils.Bracket(intervals.Interval(23, 28, left_closed=True), 4),
                utils.Bracket(intervals.Interval(28, 33, left_closed=True), 5),
                utils.Bracket(intervals.Interval(33, 38, left_closed=True), 6),
                utils.Bracket(intervals.Interval(48, 53, left_closed=True), 9),
                utils.Bracket(intervals.Interval(78, 83, left_closed=True), 15),
                utils.Bracket(intervals.Interval(83, 88, left_closed=True), 16)])
        self.assertSequenceEqual(bracket_indices, [0, 0, 0, 1, 1, 2, 3, 4, 5, 5, 5, 6, 7])
        
        brackets, bracket_indices = utils.bracket(data, 3, 5, intervals_right_closed=True)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(intervals.Interval(3, 8, right_closed=True), 0),
                utils.Bracket(intervals.Interval(8, 13, right_closed=True), 1),
                utils.Bracket(intervals.Interval(13, 18, right_closed=True), 2),
                utils.Bracket(intervals.Interval(23, 28, right_closed=True), 4),
                utils.Bracket(intervals.Interval(28, 33, right_closed=True), 5),
                utils.Bracket(intervals.Interval(33, 38, right_closed=True), 6),
                utils.Bracket(intervals.Interval(48, 53, right_closed=True), 9),
                utils.Bracket(intervals.Interval(78, 83, right_closed=True), 15),
                utils.Bracket(intervals.Interval(83, 88, right_closed=True), 16)])
        self.assertSequenceEqual(bracket_indices, [0, 1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 7, 8])
    
        brackets, bracket_indices = utils.bracket(data, 3, 5, coalesce=True)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(intervals.Interval(8, 18, left_closed=True), 1),
                utils.Bracket(intervals.Interval(23, 38, left_closed=True), 4),
                utils.Bracket(intervals.Interval(48, 53, left_closed=True), 9),
                utils.Bracket(intervals.Interval(78, 88, left_closed=True), 15)])
        self.assertSequenceEqual(bracket_indices, [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3])

        brackets, bracket_indices = utils.bracket(data, 3, 5, intervals_right_closed=True, coalesce=True)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(intervals.Interval(3, 18, right_closed=True), 0),
                utils.Bracket(intervals.Interval(23, 38, right_closed=True), 4),
                utils.Bracket(intervals.Interval(48, 53, right_closed=True), 9),
                utils.Bracket(intervals.Interval(78, 88, right_closed=True), 15)])
        self.assertSequenceEqual(bracket_indices, [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3])
        
        data = [dt.date(2017, 1, 31) + dt.timedelta(days=x) for x in [8, 11, 12, 13, 14, 27, 29, 37, 49, 50, 51, 79, 85]];
        
        brackets, bracket_indices = utils.bracket(data, dt.date(2017, 2, 3), dt.timedelta(days=5))
        self.assertSequenceEqual(brackets, [
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 8), dt.date(2017, 2, 13), left_closed=True), 1),
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 13), dt.date(2017, 2, 18), left_closed=True), 2),
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 23), dt.date(2017, 2, 28), left_closed=True), 4),
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 28), dt.date(2017, 3, 5), left_closed=True), 5),
                utils.Bracket(intervals.Interval(dt.date(2017, 3, 5), dt.date(2017, 3, 10), left_closed=True), 6),
                utils.Bracket(intervals.Interval(dt.date(2017, 3, 20), dt.date(2017, 3, 25), left_closed=True), 9),
                utils.Bracket(intervals.Interval(dt.date(2017, 4, 19), dt.date(2017, 4, 24), left_closed=True), 15),
                utils.Bracket(intervals.Interval(dt.date(2017, 4, 24), dt.date(2017, 4, 29), left_closed=True), 16)])
        self.assertSequenceEqual(bracket_indices, [0, 0, 0, 1, 1, 2, 3, 4, 5, 5, 5, 6, 7])

        brackets, bracket_indices = utils.bracket(data, dt.date(2017, 2, 3), dt.timedelta(days=5), intervals_right_closed=True)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 3), dt.date(2017, 2, 8), right_closed=True), 0),
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 8), dt.date(2017, 2, 13), right_closed=True), 1),
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 13), dt.date(2017, 2, 18), right_closed=True), 2),
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 23), dt.date(2017, 2, 28), right_closed=True), 4),
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 28), dt.date(2017, 3, 5), right_closed=True), 5),
                utils.Bracket(intervals.Interval(dt.date(2017, 3, 5), dt.date(2017, 3, 10), right_closed=True), 6),
                utils.Bracket(intervals.Interval(dt.date(2017, 3, 20), dt.date(2017, 3, 25), right_closed=True), 9),
                utils.Bracket(intervals.Interval(dt.date(2017, 4, 19), dt.date(2017, 4, 24), right_closed=True), 15),
                utils.Bracket(intervals.Interval(dt.date(2017, 4, 24), dt.date(2017, 4, 29), right_closed=True), 16)])
        self.assertSequenceEqual(bracket_indices, [0, 1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 7, 8])

        brackets, bracket_indices = utils.bracket(data, dt.date(2017, 2, 3), dt.timedelta(days=5), coalesce=True)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 8), dt.date(2017, 2, 18), left_closed=True), 1),
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 23), dt.date(2017, 3, 10), left_closed=True), 4),
                utils.Bracket(intervals.Interval(dt.date(2017, 3, 20), dt.date(2017, 3, 25), left_closed=True), 9),
                utils.Bracket(intervals.Interval(dt.date(2017, 4, 19), dt.date(2017, 4, 29), left_closed=True), 15)])
        self.assertSequenceEqual(bracket_indices, [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3])

        brackets, bracket_indices = utils.bracket(data, dt.date(2017, 2, 3), dt.timedelta(days=5), intervals_right_closed=True, coalesce=True)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 3), dt.date(2017, 2, 18), right_closed=True), 0),
                utils.Bracket(intervals.Interval(dt.date(2017, 2, 23), dt.date(2017, 3, 10), right_closed=True), 4),
                utils.Bracket(intervals.Interval(dt.date(2017, 3, 20), dt.date(2017, 3, 25), right_closed=True), 9),
                utils.Bracket(intervals.Interval(dt.date(2017, 4, 19), dt.date(2017, 4, 29), right_closed=True), 15)])
        self.assertSequenceEqual(bracket_indices, [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3])

        data = [dt.datetime(2017, 1, 31, 0, 0, 0) + dt.timedelta(minutes=x) for x in [8, 11, 12, 13, 14, 27, 29, 37, 49, 50, 51, 79, 85]];

        brackets, bracket_indices = utils.bracket(data, dt.datetime(2017, 1, 31, 0, 3, 0), dt.timedelta(minutes=5))
        self.assertSequenceEqual(brackets, [
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 8), dt.datetime(2017, 1, 31, 0, 13), left_closed=True), 1),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 13), dt.datetime(2017, 1, 31, 0, 18), left_closed=True), 2),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 23), dt.datetime(2017, 1, 31, 0, 28), left_closed=True), 4),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 28), dt.datetime(2017, 1, 31, 0, 33), left_closed=True), 5),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 33), dt.datetime(2017, 1, 31, 0, 38), left_closed=True), 6),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 48), dt.datetime(2017, 1, 31, 0, 53), left_closed=True), 9),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 1, 18), dt.datetime(2017, 1, 31, 1, 23), left_closed=True), 15),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 1, 23), dt.datetime(2017, 1, 31, 1, 28), left_closed=True), 16)])
        self.assertSequenceEqual(bracket_indices, [0, 0, 0, 1, 1, 2, 3, 4, 5, 5, 5, 6, 7])

        brackets, bracket_indices = utils.bracket(data, dt.datetime(2017, 1, 31, 0, 3, 0), dt.timedelta(minutes=5), intervals_right_closed=True)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 3), dt.datetime(2017, 1, 31, 0, 8), right_closed=True), 0),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 8), dt.datetime(2017, 1, 31, 0, 13), right_closed=True), 1),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 13), dt.datetime(2017, 1, 31, 0, 18), right_closed=True), 2),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 23), dt.datetime(2017, 1, 31, 0, 28), right_closed=True), 4),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 28), dt.datetime(2017, 1, 31, 0, 33), right_closed=True), 5),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 33), dt.datetime(2017, 1, 31, 0, 38), right_closed=True), 6),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 48), dt.datetime(2017, 1, 31, 0, 53), right_closed=True), 9),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 1, 18), dt.datetime(2017, 1, 31, 1, 23), right_closed=True), 15),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 1, 23), dt.datetime(2017, 1, 31, 1, 28), right_closed=True), 16)])
        self.assertSequenceEqual(bracket_indices, [0, 1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 7, 8])

        brackets, bracket_indices = utils.bracket(data, dt.datetime(2017, 1, 31, 0, 3, 0), dt.timedelta(minutes=5), coalesce=True)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 8), dt.datetime(2017, 1, 31, 0, 18), left_closed=True), 1),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 23), dt.datetime(2017, 1, 31, 0, 38), left_closed=True), 4),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 48), dt.datetime(2017, 1, 31, 0, 53), left_closed=True), 9),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 1, 18), dt.datetime(2017, 1, 31, 1, 28), left_closed=True), 15)])
        self.assertSequenceEqual(bracket_indices, [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3])

        brackets, bracket_indices = utils.bracket(data, dt.datetime(2017, 1, 31, 0, 3, 0), dt.timedelta(minutes=5), intervals_right_closed=True, coalesce=True)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 3), dt.datetime(2017, 1, 31, 0, 18), right_closed=True), 0),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 23), dt.datetime(2017, 1, 31, 0, 38), right_closed=True), 4),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 0, 48), dt.datetime(2017, 1, 31, 0, 53), right_closed=True), 9),
                utils.Bracket(intervals.Interval(dt.datetime(2017, 1, 31, 1, 18), dt.datetime(2017, 1, 31, 1, 28), right_closed=True), 15)])
        self.assertSequenceEqual(bracket_indices, [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3])
        
    def test_diagonal_array(self):
        a = utils.DiagonalArray(5)
        
        a[0,0] = 0
        a[1,0], a[1,1] = 10, 20
        a[2,0], a[2,1], a[2,2] = 30, 40, 50
        a[3,0], a[3,1], a[3,2], a[3,3] = 60, 70, 80, 90
        a[4,0], a[4,1], a[4,2], a[4,3], a[4,4] = 100, 110, 120, 130, 140
        
        self.assertEqual(len(a), 15)
        
        self.assertEqual(a[0,0], 0)
        self.assertEqual(a[1,0], 10)
        self.assertEqual(a[1,1], 20)
        self.assertEqual(a[2,0], 30)
        self.assertEqual(a[2,1], 40)
        self.assertEqual(a[2,2], 50)
        self.assertEqual(a[3,0], 60)
        self.assertEqual(a[3,1], 70)
        self.assertEqual(a[3,2], 80)
        self.assertEqual(a[3,3], 90)
        self.assertEqual(a[4,0], 100)
        self.assertEqual(a[4,1], 110)
        self.assertEqual(a[4,2], 120)
        self.assertEqual(a[4,3], 130)
        self.assertEqual(a[4,4], 140)
        
        self.assertEqual(a[0,0], 0)
        self.assertEqual(a[0,1], 10)
        self.assertEqual(a[1,1], 20)
        self.assertEqual(a[0,2], 30)
        self.assertEqual(a[1,2], 40)
        self.assertEqual(a[2,2], 50)
        self.assertEqual(a[0,3], 60)
        self.assertEqual(a[1,3], 70)
        self.assertEqual(a[2,3], 80)
        self.assertEqual(a[3,3], 90)
        self.assertEqual(a[0,4], 100)
        self.assertEqual(a[1,4], 110)
        self.assertEqual(a[2,4], 120)
        self.assertEqual(a[3,4], 130)
        self.assertEqual(a[4,4], 140)
        
        self.assertEqual(a._indextokey(0), (0, 0))
        self.assertEqual(a._indextokey(1), (1, 0))
        self.assertEqual(a._indextokey(2), (1, 1))
        self.assertEqual(a._indextokey(3), (2, 0))
        self.assertEqual(a._indextokey(4), (2, 1))
        self.assertEqual(a._indextokey(5), (2, 2))
        self.assertEqual(a._indextokey(6), (3, 0))
        self.assertEqual(a._indextokey(7), (3, 1))
        self.assertEqual(a._indextokey(8), (3, 2))
        self.assertEqual(a._indextokey(9), (3, 3))
        self.assertEqual(a._indextokey(10), (4, 0))
        self.assertEqual(a._indextokey(11), (4, 1))
        self.assertEqual(a._indextokey(12), (4, 2))
        self.assertEqual(a._indextokey(13), (4, 3))
        self.assertEqual(a._indextokey(14), (4, 4))

        values = []
        for v in a: values.append(v)
        self.assertSequenceEqual(tuple(a), (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140))
        
        keys = []
        for k in a.keys():
            keys.append(k)
        self.assertSequenceEqual(keys, ((0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2), (3, 3), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)))

        keys, values = [], []
        for k, v in a.items():
            keys.append(k)
            values.append(v)
        self.assertSequenceEqual(keys, ((0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2), (3, 3), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)))
        self.assertSequenceEqual(values, (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140))
        
        self.assertEqual(a.mindim(1), 1)
        self.assertEqual(a.mindim(2), 2)
        self.assertEqual(a.mindim(3), 2)
        self.assertEqual(a.mindim(4), 3)
        self.assertEqual(a.mindim(5), 3)
        self.assertEqual(a.mindim(6), 3)
        self.assertEqual(a.mindim(7), 4)
        self.assertEqual(a.mindim(8), 4)
        self.assertEqual(a.mindim(9), 4)
        self.assertEqual(a.mindim(10), 4)
        self.assertEqual(a.mindim(11), 5)
        self.assertEqual(a.mindim(12), 5)
        self.assertEqual(a.mindim(13), 5)
        self.assertEqual(a.mindim(14), 5)
        self.assertEqual(a.mindim(15), 5)

    def test_subdiagonal_array(self):
        a = utils.SubdiagonalArray(5)
        a[1,0] = 0
        a[2,0], a[2,1] = 10, 20
        a[3,0], a[3,1], a[3,2] = 30, 40, 50
        a[4,0], a[4,1], a[4,2], a[4,3] = 60, 70, 80, 90
        
        self.assertEqual(len(a), 10)
        
        self.assertEqual(a[1,0], 0)
        self.assertEqual(a[2,0], 10)
        self.assertEqual(a[2,1], 20)
        self.assertEqual(a[3,0], 30)
        self.assertEqual(a[3,1], 40)
        self.assertEqual(a[3,2], 50)
        self.assertEqual(a[4,0], 60)
        self.assertEqual(a[4,1], 70)
        self.assertEqual(a[4,2], 80)
        self.assertEqual(a[4,3], 90)
        
        self.assertEqual(a[0,1], 0)
        self.assertEqual(a[0,2], 10)
        self.assertEqual(a[1,2], 20)
        self.assertEqual(a[0,3], 30)
        self.assertEqual(a[1,3], 40)
        self.assertEqual(a[2,3], 50)
        self.assertEqual(a[0,4], 60)
        self.assertEqual(a[1,4], 70)
        self.assertEqual(a[2,4], 80)
        self.assertEqual(a[3,4], 90)
        
        self.assertEqual(a._indextokey(0), (1, 0))
        self.assertEqual(a._indextokey(1), (2, 0))
        self.assertEqual(a._indextokey(2), (2, 1))
        self.assertEqual(a._indextokey(3), (3, 0))
        self.assertEqual(a._indextokey(4), (3, 1))
        self.assertEqual(a._indextokey(5), (3, 2))
        self.assertEqual(a._indextokey(6), (4, 0))
        self.assertEqual(a._indextokey(7), (4, 1))
        self.assertEqual(a._indextokey(8), (4, 2))
        self.assertEqual(a._indextokey(9), (4, 3))
        
        values = []
        for v in a: values.append(v)
        self.assertSequenceEqual(values, (0, 10, 20, 30, 40, 50, 60, 70, 80, 90))

        keys = []
        for k in a.keys():
            keys.append(k)
        self.assertSequenceEqual(keys, ((1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (4, 3)))

        keys, values = [], []
        for k, v in a.items():
            keys.append(k)
            values.append(v)
        self.assertSequenceEqual(keys, ((1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (4, 3)))
        self.assertSequenceEqual(values, (0, 10, 20, 30, 40, 50, 60, 70, 80, 90))

        self.assertEqual(a.mindim(1), 2)
        self.assertEqual(a.mindim(2), 3)
        self.assertEqual(a.mindim(3), 3)
        self.assertEqual(a.mindim(4), 4)
        self.assertEqual(a.mindim(5), 4)
        self.assertEqual(a.mindim(6), 4)
        self.assertEqual(a.mindim(7), 5)
        self.assertEqual(a.mindim(8), 5)
        self.assertEqual(a.mindim(9), 5)
        self.assertEqual(a.mindim(10), 5)

if __name__ == '__main__':
    unittest.main()
    