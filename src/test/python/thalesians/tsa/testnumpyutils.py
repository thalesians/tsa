import datetime as dt
import unittest

import numpy as np
import numpy.testing as npt

import thalesians.tsa.checks as checks
import thalesians.tsa.numpyutils as npu
from thalesians.tsa.numpyutils import vectorised

# In case you are interested, the numbers used in these tests come from the A000108 sequence (Catalan numbers)

class TestNumPyUtils(unittest.TestCase):
    def test_sign(self):
        self.assertEqual(npu.sign(-10), -1)
        self.assertEqual(npu.sign(0), 0)
        self.assertEqual(npu.sign(10), 1)
        self.assertEqual(npu.sign(-10.), -1.)
        self.assertEqual(npu.sign(0.), 0.)
        self.assertEqual(npu.sign(10.), 1.)
        self.assertEqual(npu.sign(dt.date(2017, 11, 7) - dt.date(2017, 11, 8)), -1.)
        self.assertEqual(npu.sign(dt.date(2017, 11, 8) - dt.date(2017, 11, 8)), 0.)
        self.assertEqual(npu.sign(dt.date(2017, 11, 8) - dt.date(2017, 11, 7)), 1.)
        self.assertEqual(npu.sign(dt.datetime(2017, 11, 8, 17, 27) - dt.datetime(2017, 11, 8, 17, 28)), -1.)
        self.assertEqual(npu.sign(dt.datetime(2017, 11, 8, 17, 28) - dt.datetime(2017, 11, 8, 17, 28)), 0.)
        self.assertEqual(npu.sign(dt.datetime(2017, 11, 8, 17, 28) - dt.datetime(2017, 11, 8, 17, 27)), 1.)
        npt.assert_almost_equal(npu.sign([-10., 0., 10.]), np.array([-1.,  0.,  1.]))
        npt.assert_almost_equal(npu.sign(np.array([
                npu.sign(dt.datetime(2017, 11, 8, 17, 27) - dt.datetime(2017, 11, 8, 17, 28)),
                npu.sign(dt.datetime(2017, 11, 8, 17, 28) - dt.datetime(2017, 11, 8, 17, 28)),
                npu.sign(dt.datetime(2017, 11, 8, 17, 28) - dt.datetime(2017, 11, 8, 17, 27))
                ])), np.array([-1.,  0.,  1.]))
        
    def test_nrow(self):
        r = npu.row(429., 5., 2., 14.)
        self.assertEqual(npu.nrow(r), 1)
        c = npu.col(429., 5., 2., 14.)
        self.assertEqual(npu.nrow(c), 4)
        m = npu.matrix_of(3, 5, 0.)
        self.assertEqual(npu.nrow(m), 3)
    
    def test_ncol(self):
        r = npu.row(429., 5., 2., 14.)
        self.assertEqual(npu.ncol(r), 4)
        c = npu.col(429., 5., 2., 14.)
        self.assertEqual(npu.ncol(c), 1)
        m = npu.matrix_of(3, 5, 0.)
        self.assertEqual(npu.ncol(m), 5)
        
    def test_is_view_of(self):
        a = np.array([[429., 5.], [2., 14.]])
        b = npu.to_ndim_1(a, copy=False)
        self.assertTrue(npu.is_view_of(b, a))
        self.assertFalse(npu.is_view_of(a, b))
        b = a.T
        self.assertTrue(npu.is_view_of(b, a))
        self.assertFalse(npu.is_view_of(a, b))
        b = npu.to_ndim_1(a, copy=True)
        self.assertFalse(npu.is_view_of(b, a))
        self.assertFalse(npu.is_view_of(a, b))
    
    def test_are_views_of_same(self):
        a = np.array([[429., 5.], [2., 14.]])
        b = npu.to_ndim_1(a, copy=False)
        self.assertTrue(npu.are_views_of_same(b, a))
        self.assertTrue(npu.are_views_of_same(a, b))
        b = a.T
        self.assertTrue(npu.are_views_of_same(b, a))
        self.assertTrue(npu.are_views_of_same(a, b))
        b = npu.to_ndim_1(a, copy=True)
        self.assertFalse(npu.are_views_of_same(b, a))
        self.assertFalse(npu.are_views_of_same(a, b))
    
    def test_to_scalar(self):
        for v in [ 429., [429.], [[429.]], np.array(429.), np.array([429.]), np.array([[429.]]) ]:
            r = npu.to_scalar(v)
            self.assertIsInstance(r, float)
            npt.assert_almost_equal(r, 429.)
        
        self.assertIsNone(npu.to_scalar(None))
            
    def test_to_ndim_1(self):
        for v in [ 429., [429.], [[429.]], np.array(429.), np.array([429.]), np.array([[429.]]) ]:
            r = npu.to_ndim_1(v)
            self.assertTrue(checks.is_numpy_array(r))
            self.assertEqual(np.shape(r), (1,))
            npt.assert_almost_equal(r, np.array([429.]))
        
        for v in [[429., 5.], [[429., 5.]], [[[429.], [5.]]], np.array([429., 5.]), np.array([[429., 5.]]), np.array([[[429.], [5.]]])]:
            r = npu.to_ndim_1(v)
            self.assertTrue(checks.is_numpy_array(r))
            self.assertEqual(np.shape(r), (2,))
            npt.assert_almost_equal(r, np.array([429., 5.]))
        
        for v in [ [429., 5., 2., 14.], [[429., 5., 2., 14.]], [[429., 5.], [2., 14.]], [[429.], [5.], [2.], [14.]], np.array([429., 5., 2., 14.]), np.array([[429., 5., 2., 14.]]), np.array([[429., 5.], [2., 14.]]), np.array([[[429.], [5.], [2.], [14.]]]) ]:
            r = npu.to_ndim_1(v)
            self.assertTrue(checks.is_numpy_array(r))
            self.assertEqual(np.shape(r), (4,))
            npt.assert_almost_equal(r, np.array([429., 5., 2., 14.]))
        
        npt.assert_equal(npu.to_ndim_1(None), np.array([None]))
    
        a = np.array([2., 14.])
        b = npu.to_ndim_1(a, copy=False)
        b[1] = 42.
        npt.assert_almost_equal(b, np.array([2., 42.]))
        npt.assert_almost_equal(a, np.array([2., 42.]))
    
        a = [2., 14.]
        b = npu.to_ndim_1(a, copy=False)
        b[1] = 42.
        npt.assert_almost_equal(b, np.array([2., 42.]))
        npt.assert_almost_equal(a, np.array([2., 14.]))

        a = [2., 14.]
        b = npu.to_ndim_1(a, copy=True)
        b[1] = 42.
        npt.assert_almost_equal(b, np.array([2., 42.]))
        npt.assert_almost_equal(a, np.array([2., 14.]))

    def test_to_ndim_2(self):
        for v in [ 429., [429.], [[429.]], np.array(429.), np.array([429.]), np.array([[429.]]) ]:
            r = npu.to_ndim_2(v)
            self.assertTrue(checks.is_numpy_array(r))
            self.assertEqual(np.shape(r), (1, 1))
            npt.assert_almost_equal(r, np.array([[429.]]))
        
        for v in [ [429., 5.], [[429., 5.]], np.array([429., 5.]), np.array([[429., 5.]]) ]:
            r = npu.to_ndim_2(v)
            self.assertTrue(checks.is_numpy_array(r))
            self.assertEqual(np.shape(r), (1, 2))
            npt.assert_almost_equal(r, np.array([[429., 5.]]))
        
        for v in [ [[429.], [5.]], np.array([[429.], [5.]]) ]:
            r = npu.to_ndim_2(v)
            self.assertTrue(checks.is_numpy_array(r))
            self.assertEqual(np.shape(r), (2, 1))
            npt.assert_almost_equal(r, np.array([[429.], [5.]]))
        
        for v in [ [429., 5., 2., 14.], [[429., 5., 2., 14.]], np.array([429., 5., 2., 14.]), np.array([[429., 5., 2., 14.]]) ]:
            r = npu.to_ndim_2(v)
            self.assertTrue(checks.is_numpy_array(r))
            self.assertEqual(np.shape(r), (1, 4))
            npt.assert_almost_equal(r, np.array([[429., 5., 2., 14.]]))
        
        for v in [ [[429., 5.], [2., 14.]], np.array([[429., 5.], [2., 14.]]) ]:
            r = npu.to_ndim_2(v)
            self.assertTrue(checks.is_numpy_array(r))
            self.assertEqual(np.shape(r), (2, 2))
            npt.assert_almost_equal(r, np.array([[429., 5.], [2., 14.]]))
        
        for v in [ [[429.], [5.], [2.], [14.]], np.array([[429.], [5.], [2.], [14.]]) ]:
            r = npu.to_ndim_2(v)
            self.assertTrue(checks.is_numpy_array(r))
            self.assertEqual(np.shape(r), (4, 1))
            npt.assert_almost_equal(r, np.array([[429.], [5.], [2.], [14.]]))
        
        npt.assert_equal(npu.to_ndim_2(None), np.array([[None]]))
        
        a = np.array([[429., 5.], [2., 14.]])
        b = npu.to_ndim_2(a, copy=False)
        b[1, 1] = 42.
        npt.assert_almost_equal(b, np.array([[429., 5.], [2., 42.]]))
        npt.assert_almost_equal(a, np.array([[429., 5.], [2., 42.]]))
    
        a = [[429., 5.], [2., 14.]]
        b = npu.to_ndim_2(a, copy=False)
        b[1, 1] = 42.
        npt.assert_almost_equal(b, np.array([[429., 5.], [2., 42.]]))
        npt.assert_almost_equal(a, np.array([[429., 5.], [2., 14.]]))

        a = np.array([[429., 5.], [2., 14.]])
        b = npu.to_ndim_2(a, copy=True)
        b[1, 1] = 42.
        npt.assert_almost_equal(b, np.array([[429., 5.], [2., 42.]]))
        npt.assert_almost_equal(a, np.array([[429., 5.], [2., 14.]]))

    def test_row(self):
        row = npu.row(1., 1., 2., 5., 14.)
        npt.assert_almost_equal(row, np.array([[1., 1., 2., 5., 14.]]))
        
    def test_col(self):
        col = npu.col(1., 1., 2., 5., 14.)
        npt.assert_almost_equal(col, np.array(([[1.], [1.], [2.], [5.], [14.]])))
        
    def test_matrix(self):
        matrix = npu.matrix(3, 429., 5., 2., 14., 42., 132.)
        npt.assert_almost_equal(matrix, np.array([[429., 5., 2.], [14., 42., 132.]]))
        
    def test_matrix_of(self):
        matrix = npu.matrix_of(2, 3, 429.)
        npt.assert_almost_equal(matrix, np.array([[429., 429., 429.], [429., 429., 429.]]))
        
    def test_row_of(self):
        row = npu.row_of(5, 429.)
        npt.assert_almost_equal(row, np.array([[429., 429., 429., 429., 429.]]))
        
    def test_col_of(self):
        col = npu.col_of(5, 429.)
        npt.assert_almost_equal(col, np.array([[429.], [429.], [429.], [429.], [429.]]))
        
    def test_ndim_1_of(self):
        ndim1 = npu.ndim_1_of(5, 429.)
        npt.assert_almost_equal(ndim1, np.array([429., 429., 429., 429., 429.]))
        
    def test_make_immutable(self):
        a = np.array([[429., 5.], [2., 14.]])
        a[1, 1] = 42.
        b = npu.make_immutable(a)
        self.assertIs(b, a)
        npt.assert_almost_equal(b[1, 1], 42.)
        with self.assertRaises(ValueError):
            b[1, 1] = 132.
        npt.assert_almost_equal(b[1, 1], 42.)
    
    def test_immutable_copy_of(self):
        a = np.array([[429., 5.], [2., 14.]])
        npt.assert_almost_equal(a, np.array([[429., 5.], [2., 14.]]))
        a[1, 1] = 42.
        npt.assert_almost_equal(a, np.array([[429., 5.], [2., 42.]]))
        b = npu.immutable_copy_of(a)
        npt.assert_almost_equal(b, np.array([[429., 5.], [2., 42.]]))
        with self.assertRaises(ValueError):
            b[1, 1] = 132.
        npt.assert_almost_equal(b, np.array([[429., 5.], [2., 42.]]))
        a[1, 1] = 132.
        npt.assert_almost_equal(b, np.array([[429., 5.], [2., 42.]]))
        
    def test_lower_to_symmetric(self):
        a = npu.matrix(3, 429., 0., 0., 5., 2., 0., 42., 1., 1.)
        b = npu.lower_to_symmetric(a)
        npt.assert_almost_equal(a, npu.matrix(3, 429., 5., 42., 5., 2., 1., 42., 1., 1.))
        npt.assert_almost_equal(b, npu.matrix(3, 429., 5., 42., 5., 2., 1., 42., 1., 1.))
        
        a = npu.matrix(3, 429., 0., 0., 5., 2., 0., 42., 1., 1.)
        b = npu.lower_to_symmetric(a, copy=True)
        npt.assert_almost_equal(a, npu.matrix(3, 429., 0., 0., 5., 2., 0., 42., 1., 1.))
        npt.assert_almost_equal(b, npu.matrix(3, 429., 5., 42., 5., 2., 1., 42., 1., 1.))        
    
    def test_upper_to_symmetric(self):
        a = npu.matrix(3, 429., 5., 42., 0., 2., 1., 0., 0., 1.)
        b = npu.upper_to_symmetric(a)
        npt.assert_almost_equal(a, npu.matrix(3, 429., 5., 42., 5., 2., 1., 42., 1., 1.))
        npt.assert_almost_equal(b, npu.matrix(3, 429., 5., 42., 5., 2., 1., 42., 1., 1.))
        
        a = npu.matrix(3, 429., 5., 42., 0., 2., 1., 0., 0., 1.)
        b = npu.upper_to_symmetric(a, copy=True)
        npt.assert_almost_equal(a, npu.matrix(3, 429., 5., 42., 0., 2., 1., 0., 0., 1.))
        npt.assert_almost_equal(b, npu.matrix(3, 429., 5., 42., 5., 2., 1., 42., 1., 1.))
        
    def test_kron(self):
        a = np.array([[  5., 1.,   14., 2., 42.],
                      [132., 2.,  429., 1.,  1.],
                      [  1., 2., 1430., 2.,  2.]])
        b = np.array([[42.,   2.],
                      [ 5.,   1.],
                      [ 5.,   2.],
                      [14., 132.]])
        c = np.kron(a, b)
        
        n = npu.nrow(a); p = npu.ncol(a)
        m = npu.nrow(b); q = npu.ncol(b)
        
        self.assertEqual(npu.nrow(c), m*n)
        self.assertEqual(npu.ncol(c), p*q)

        for i in range(n):
            for j in range(p):
                npt.assert_almost_equal(c[i*m:(i+1)*m, j*q:(j+1)*q], a[i, j] * b)

    def test_kron_sum(self):
        a = np.array([[5., 1.],
                      [2., 5.]])
        b = np.array([[ 14., 42.,  1.],
                      [132., 14.,  2.],
                      [  5.,  2., 42.]])
        c = npu.kron_sum(a, b)
        
        m = npu.nrow(a)
        self.assertEqual(npu.ncol(a), m)
        n = npu.nrow(b)
        self.assertEqual(npu.ncol(b), n)
        
        known_kron_sum = np.kron(a, np.eye(n)) + np.kron(np.eye(m), b)
        npt.assert_almost_equal(c, known_kron_sum)
        
    def test_vec_and_unvec(self):
        a = np.array([[  5., 1.,   14., 2., 42.],
                      [132., 2.,  429., 1.,  1.],
                      [  1., 2., 1430., 2.,  2.]])
        b = npu.col(5., 132., 1., 1., 2., 2., 14., 429., 1430., 2., 1., 2., 42., 1., 2.)
        npt.assert_almost_equal(npu.vec(a), b)
        npt.assert_almost_equal(npu.unvec(b, 3), a)

    def test_vectorised(self):
        func_call_count = 0

        def func(a, b):
            nonlocal func_call_count
            func_call_count += 1
            return a + b
        
        funcv_call_count = 0
        
        @vectorised
        def funcv(a, b):
            nonlocal funcv_call_count
            funcv_call_count += 1
            return a + b
        
        def solver(a, b, f):
            if npu.is_vectorised(f):
                return f(a, b)
            else:
                rc = np.shape(a)[0]
                r = np.empty((rc, 1))
                for i in range(rc):
                    r[i] = f(a[i], b[i])
                return r
            
        self.assertFalse(npu.is_vectorised(func))
        self.assertTrue(npu.is_vectorised(funcv))
        a = npu.col(14., 2., 429.)
        b = npu.col(42., 1., 5.)
        r = solver(a, b, func)
        npt.assert_almost_equal(r, np.array([[56.], [3.], [434.]]))
        self.assertEqual(func_call_count, 3)
        r = solver(a, b, funcv)
        npt.assert_almost_equal(r, np.array([[56.], [3.], [434.]]))
        self.assertEqual(funcv_call_count, 1)
        
if __name__ == '__main__':
    unittest.main()
    