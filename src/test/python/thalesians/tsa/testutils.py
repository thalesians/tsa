import datetime as dt
import unittest

import numpy as np
import numpy.testing as npt

import thalesians.tsa.intervals as intervals
import thalesians.tsa.utils as utils

# In case you are interested, the numbers used in these tests come from the A000108 sequence (Catalan numbers).

class TestUtils(unittest.TestCase):
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
        
if __name__ == '__main__':
    unittest.main()
    