import datetime as dt
import unittest

import numpy as np
import numpy.testing as npt

import thalesians.tsa.utils as utils

# In case you are interested, the numbers used in these tests come from the A000108 sequence (Catalan numbers).

class TestUtils(unittest.TestCase):
    def test_sign(self):
        self.assertEqual(utils.sign(-10), -1)
        self.assertEqual(utils.sign(0), 0)
        self.assertEqual(utils.sign(10), 1)
        self.assertEqual(utils.sign(-10.), -1.)
        self.assertEqual(utils.sign(0.), 0.)
        self.assertEqual(utils.sign(10.), 1.)
        self.assertEqual(utils.sign(dt.date(2017, 11, 7) - dt.date(2017, 11, 8)), -1.)
        self.assertEqual(utils.sign(dt.date(2017, 11, 8) - dt.date(2017, 11, 8)), 0.)
        self.assertEqual(utils.sign(dt.date(2017, 11, 8) - dt.date(2017, 11, 7)), 1.)
        self.assertEqual(utils.sign(dt.datetime(2017, 11, 8, 17, 27) - dt.datetime(2017, 11, 8, 17, 28)), -1.)
        self.assertEqual(utils.sign(dt.datetime(2017, 11, 8, 17, 28) - dt.datetime(2017, 11, 8, 17, 28)), 0.)
        self.assertEqual(utils.sign(dt.datetime(2017, 11, 8, 17, 28) - dt.datetime(2017, 11, 8, 17, 27)), 1.)
        npt.assert_almost_equal(utils.sign([-10., 0., 10.]), np.array([-1.,  0.,  1.]))
        npt.assert_almost_equal(utils.sign(np.array([
                utils.sign(dt.datetime(2017, 11, 8, 17, 27) - dt.datetime(2017, 11, 8, 17, 28)),
                utils.sign(dt.datetime(2017, 11, 8, 17, 28) - dt.datetime(2017, 11, 8, 17, 28)),
                utils.sign(dt.datetime(2017, 11, 8, 17, 28) - dt.datetime(2017, 11, 8, 17, 27))
                ])), np.array([-1.,  0.,  1.]))
        
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
                utils.Bracket(utils.Interval(8, 13, left_closed=True), 1),
                utils.Bracket(utils.Interval(13, 18, left_closed=True), 2),
                utils.Bracket(utils.Interval(23, 28, left_closed=True), 4),
                utils.Bracket(utils.Interval(28, 33, left_closed=True), 5),
                utils.Bracket(utils.Interval(33, 38, left_closed=True), 6),
                utils.Bracket(utils.Interval(48, 53, left_closed=True), 9),
                utils.Bracket(utils.Interval(78, 83, left_closed=True), 15),
                utils.Bracket(utils.Interval(83, 88, left_closed=True), 16)])
        self.assertSequenceEqual(bracket_indices, [0, 0, 0, 1, 1, 2, 3, 4, 5, 5, 5, 6, 7])
        
        brackets, bracket_indices = utils.bracket(data, 3, 5, intervals_right_closed=True)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(utils.Interval(3, 8, right_closed=True), 0),
                utils.Bracket(utils.Interval(8, 13, right_closed=True), 1),
                utils.Bracket(utils.Interval(13, 18, right_closed=True), 2),
                utils.Bracket(utils.Interval(23, 28, right_closed=True), 4),
                utils.Bracket(utils.Interval(28, 33, right_closed=True), 5),
                utils.Bracket(utils.Interval(33, 38, right_closed=True), 6),
                utils.Bracket(utils.Interval(48, 53, right_closed=True), 9),
                utils.Bracket(utils.Interval(78, 83, right_closed=True), 15),
                utils.Bracket(utils.Interval(83, 88, right_closed=True), 16)])
        self.assertSequenceEqual(bracket_indices, [0, 1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 7, 8])
    
        brackets, bracket_indices = utils.bracket(data, 3, 5, coalesce=True)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(utils.Interval(8, 18, left_closed=True), 1),
                utils.Bracket(utils.Interval(23, 38, left_closed=True), 4),
                utils.Bracket(utils.Interval(48, 53, left_closed=True), 9),
                utils.Bracket(utils.Interval(78, 88, left_closed=True), 15)])
        self.assertSequenceEqual(bracket_indices, [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3])

        brackets, bracket_indices = utils.bracket(data, 3, 5, intervals_right_closed=True, coalesce=True)
        self.assertSequenceEqual(brackets, [
                utils.Bracket(utils.Interval(3, 18, right_closed=True), 0),
                utils.Bracket(utils.Interval(23, 38, right_closed=True), 4),
                utils.Bracket(utils.Interval(48, 53, right_closed=True), 9),
                utils.Bracket(utils.Interval(78, 88, right_closed=True), 15)])
        self.assertSequenceEqual(bracket_indices, [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3])
"""
                                     
    data = [dt.date(2017, 1, 31) + dt.timedelta(days=x) for x in [8, 11, 12, 13, 14, 27, 29, 37, 49, 50, 51, 79, 85]];

    utils.bracket(data, dt.date(2017, 2, 3), dt.timedelta(days=5))
    
    ([{[2017-02-08, 2017-02-13), 1},
  {[2017-02-13, 2017-02-18), 2},
  {[2017-02-23, 2017-02-28), 4},
  {[2017-02-28, 2017-03-05), 5},
  {[2017-03-05, 2017-03-10), 6},
  {[2017-03-20, 2017-03-25), 9},
  {[2017-04-19, 2017-04-24), 15},
  {[2017-04-24, 2017-04-29), 16}],
 [0, 0, 0, 1, 1, 2, 3, 4, 5, 5, 5, 6, 7])
    
    utils.bracket(data, dt.date(2017, 2, 3), dt.timedelta(days=5), intervals_right_closed=True)
    
    ([{(2017-02-03, 2017-02-08], 0},
  {(2017-02-08, 2017-02-13], 1},
  {(2017-02-13, 2017-02-18], 2},
  {(2017-02-23, 2017-02-28], 4},
  {(2017-02-28, 2017-03-05], 5},
  {(2017-03-05, 2017-03-10], 6},
  {(2017-03-20, 2017-03-25], 9},
  {(2017-04-19, 2017-04-24], 15},
  {(2017-04-24, 2017-04-29], 16}],
 [0, 1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 7, 8])
    
    utils.bracket(data, dt.date(2017, 2, 3), dt.timedelta(days=5), coalesce=True)
    
    ([{[2017-02-08, 2017-02-18), 1},
  {[2017-02-23, 2017-03-10), 4},
  {[2017-03-20, 2017-03-25), 9},
  {[2017-04-19, 2017-04-29), 15}],
 [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3])
    
    utils.bracket(data, dt.date(2017, 2, 3), dt.timedelta(days=5), intervals_right_closed=True, coalesce=True)
    
    ([{(2017-02-03, 2017-02-18], 0},
  {(2017-02-23, 2017-03-10], 4},
  {(2017-03-20, 2017-03-25], 9},
  {(2017-04-19, 2017-04-29], 15}],
 [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3])
    
    data = [dt.datetime(2017, 1, 31, 0, 0, 0) + dt.timedelta(minutes=x) for x in [8, 11, 12, 13, 14, 27, 29, 37, 49, 50, 51, 79, 85]];

    [datetime.datetime(2017, 1, 31, 0, 8),
 datetime.datetime(2017, 1, 31, 0, 11),
 datetime.datetime(2017, 1, 31, 0, 12),
 datetime.datetime(2017, 1, 31, 0, 13),
 datetime.datetime(2017, 1, 31, 0, 14),
 datetime.datetime(2017, 1, 31, 0, 27),
 datetime.datetime(2017, 1, 31, 0, 29),
 datetime.datetime(2017, 1, 31, 0, 37),
 datetime.datetime(2017, 1, 31, 0, 49),
 datetime.datetime(2017, 1, 31, 0, 50),
 datetime.datetime(2017, 1, 31, 0, 51),
 datetime.datetime(2017, 1, 31, 1, 19),
 datetime.datetime(2017, 1, 31, 1, 25)]
    
    utils.bracket(data, dt.datetime(2017, 1, 31, 0, 3, 0), dt.timedelta(minutes=5))
    
    ([{[2017-01-31 00:08:00, 2017-01-31 00:13:00), 1},
  {[2017-01-31 00:13:00, 2017-01-31 00:18:00), 2},
  {[2017-01-31 00:23:00, 2017-01-31 00:28:00), 4},
  {[2017-01-31 00:28:00, 2017-01-31 00:33:00), 5},
  {[2017-01-31 00:33:00, 2017-01-31 00:38:00), 6},
  {[2017-01-31 00:48:00, 2017-01-31 00:53:00), 9},
  {[2017-01-31 01:18:00, 2017-01-31 01:23:00), 15},
  {[2017-01-31 01:23:00, 2017-01-31 01:28:00), 16}],
 [0, 0, 0, 1, 1, 2, 3, 4, 5, 5, 5, 6, 7])
    
    utils.bracket(data, dt.datetime(2017, 1, 31, 0, 3, 0), dt.timedelta(minutes=5), intervals_right_closed=True)
    
    ([{(2017-01-31 00:03:00, 2017-01-31 00:08:00], 0},
  {(2017-01-31 00:08:00, 2017-01-31 00:13:00], 1},
  {(2017-01-31 00:13:00, 2017-01-31 00:18:00], 2},
  {(2017-01-31 00:23:00, 2017-01-31 00:28:00], 4},
  {(2017-01-31 00:28:00, 2017-01-31 00:33:00], 5},
  {(2017-01-31 00:33:00, 2017-01-31 00:38:00], 6},
  {(2017-01-31 00:48:00, 2017-01-31 00:53:00], 9},
  {(2017-01-31 01:18:00, 2017-01-31 01:23:00], 15},
  {(2017-01-31 01:23:00, 2017-01-31 01:28:00], 16}],
 [0, 1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 7, 8])
    
    utils.bracket(data, dt.datetime(2017, 1, 31, 0, 3, 0), dt.timedelta(minutes=5), coalesce=True)
    
    ([{[2017-01-31 00:08:00, 2017-01-31 00:18:00), 1},
  {[2017-01-31 00:23:00, 2017-01-31 00:38:00), 4},
  {[2017-01-31 00:48:00, 2017-01-31 00:53:00), 9},
  {[2017-01-31 01:18:00, 2017-01-31 01:28:00), 15}],
 [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3])
    
    utils.bracket(data, dt.datetime(2017, 1, 31, 0, 3, 0), dt.timedelta(minutes=5), intervals_right_closed=True, coalesce=True)
    
    ([{(2017-01-31 00:03:00, 2017-01-31 00:18:00], 0},
  {(2017-01-31 00:23:00, 2017-01-31 00:38:00], 4},
  {(2017-01-31 00:48:00, 2017-01-31 00:53:00], 9},
  {(2017-01-31 01:18:00, 2017-01-31 01:28:00], 15}],
 [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3])
 """
        
if __name__ == '__main__':
    unittest.main()
    