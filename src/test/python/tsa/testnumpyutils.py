import unittest

import numpy as np
import numpy.testing as npt

import tsa.numpyutils as npu
from tsa.numpyutils import vectorised

# In case you are interested, the numbers used in these tests come from the A000108 sequence (Catalan numbers)

class TestNumPyUtils(unittest.TestCase):
    def testnrow(self):
        r = npu.row(429., 5., 2., 14.)
        self.assertEqual(npu.nrow(r), 1)
        c = npu.col(429., 5., 2., 14.)
        self.assertEqual(npu.nrow(c), 4)
        m = npu.matrixof(3, 5, 0.)
        self.assertEqual(npu.nrow(m), 3)
    
    def testncol(self):
        r = npu.row(429., 5., 2., 14.)
        self.assertEqual(npu.ncol(r), 4)
        c = npu.col(429., 5., 2., 14.)
        self.assertEqual(npu.ncol(c), 1)
        m = npu.matrixof(3, 5, 0.)
        self.assertEqual(npu.ncol(m), 5)
        
    def testisviewof(self):
        a = np.array([[429., 5.], [2., 14.]])
        b = npu.tondim1(a, copy=False)
        self.assertTrue(npu.isviewof(b, a))
        self.assertFalse(npu.isviewof(a, b))
        b = a.T
        self.assertTrue(npu.isviewof(b, a))
        self.assertFalse(npu.isviewof(a, b))
        b = npu.tondim1(a, copy=True)
        self.assertFalse(npu.isviewof(b, a))
        self.assertFalse(npu.isviewof(a, b))
    
    def testareviewsofsame(self):
        a = np.array([[429., 5.], [2., 14.]])
        b = npu.tondim1(a, copy=False)
        self.assertTrue(npu.areviewsofsame(b, a))
        self.assertTrue(npu.areviewsofsame(a, b))
        b = a.T
        self.assertTrue(npu.areviewsofsame(b, a))
        self.assertTrue(npu.areviewsofsame(a, b))
        b = npu.tondim1(a, copy=True)
        self.assertFalse(npu.areviewsofsame(b, a))
        self.assertFalse(npu.areviewsofsame(a, b))
    
    def testtoscalar(self):
        for v in [ 429., [429.], [[429.]], np.array(429.), np.array([429.]), np.array([[429.]]) ]:
            r = npu.toscalar(v)
            self.assertIsInstance(r, float)
            npt.assert_almost_equal(r, 429.)
        
        self.assertIsNone(npu.toscalar(None))
            
    def testtondim1(self):
        for v in [ 429., [429.], [[429.]], np.array(429.), np.array([429.]), np.array([[429.]]) ]:
            r = npu.tondim1(v)
            self.assertIsInstance(r, np.ndarray)
            self.assertEqual(np.shape(r), (1,))
            npt.assert_almost_equal(r, np.array([429.]))
        
        for v in [[429., 5.], [[429., 5.]], [[[429.], [5.]]], np.array([429., 5.]), np.array([[429., 5.]]), np.array([[[429.], [5.]]])]:
            r = npu.tondim1(v)
            self.assertIsInstance(r, np.ndarray)
            self.assertEqual(np.shape(r), (2,))
            npt.assert_almost_equal(r, np.array([429., 5.]))
        
        for v in [ [429., 5., 2., 14.], [[429., 5., 2., 14.]], [[429., 5.], [2., 14.]], [[429.], [5.], [2.], [14.]], np.array([429., 5., 2., 14.]), np.array([[429., 5., 2., 14.]]), np.array([[429., 5.], [2., 14.]]), np.array([[[429.], [5.], [2.], [14.]]]) ]:
            r = npu.tondim1(v)
            self.assertIsInstance(r, np.ndarray)
            self.assertEqual(np.shape(r), (4,))
            npt.assert_almost_equal(r, np.array([429., 5., 2., 14.]))
        
        npt.assert_equal(npu.tondim1(None), np.array([None]))
    
        a = np.array([2., 14.])
        b = npu.tondim1(a, copy=False)
        b[1] = 42.
        npt.assert_almost_equal(b, np.array([2., 42.]))
        npt.assert_almost_equal(a, np.array([2., 42.]))
    
        a = [2., 14.]
        b = npu.tondim1(a, copy=False)
        b[1] = 42.
        npt.assert_almost_equal(b, np.array([2., 42.]))
        npt.assert_almost_equal(a, np.array([2., 14.]))

        a = [2., 14.]
        b = npu.tondim1(a, copy=True)
        b[1] = 42.
        npt.assert_almost_equal(b, np.array([2., 42.]))
        npt.assert_almost_equal(a, np.array([2., 14.]))

    def testtondim2(self):
        for v in [ 429., [429.], [[429.]], np.array(429.), np.array([429.]), np.array([[429.]]) ]:
            r = npu.tondim2(v)
            self.assertIsInstance(r, np.ndarray)
            self.assertEqual(np.shape(r), (1, 1))
            npt.assert_almost_equal(r, np.array([[429.]]))
        
        for v in [ [429., 5.], [[429., 5.]], np.array([429., 5.]), np.array([[429., 5.]]) ]:
            r = npu.tondim2(v)
            self.assertIsInstance(r, np.ndarray)
            self.assertEqual(np.shape(r), (1, 2))
            npt.assert_almost_equal(r, np.array([[429., 5.]]))
        
        for v in [ [[429.], [5.]], np.array([[429.], [5.]]) ]:
            r = npu.tondim2(v)
            self.assertIsInstance(r, np.ndarray)
            self.assertEqual(np.shape(r), (2, 1))
            npt.assert_almost_equal(r, np.array([[429.], [5.]]))
        
        for v in [ [429., 5., 2., 14.], [[429., 5., 2., 14.]], np.array([429., 5., 2., 14.]), np.array([[429., 5., 2., 14.]]) ]:
            r = npu.tondim2(v)
            self.assertIsInstance(r, np.ndarray)
            self.assertEqual(np.shape(r), (1, 4))
            npt.assert_almost_equal(r, np.array([[429., 5., 2., 14.]]))
        
        for v in [ [[429., 5.], [2., 14.]], np.array([[429., 5.], [2., 14.]]) ]:
            r = npu.tondim2(v)
            self.assertIsInstance(r, np.ndarray)
            self.assertEqual(np.shape(r), (2, 2))
            npt.assert_almost_equal(r, np.array([[429., 5.], [2., 14.]]))
        
        for v in [ [[429.], [5.], [2.], [14.]], np.array([[429.], [5.], [2.], [14.]]) ]:
            r = npu.tondim2(v)
            self.assertIsInstance(r, np.ndarray)
            self.assertEqual(np.shape(r), (4, 1))
            npt.assert_almost_equal(r, np.array([[429.], [5.], [2.], [14.]]))
        
        npt.assert_equal(npu.tondim2(None), np.array([[None]]))
        
        a = np.array([[429., 5.], [2., 14.]])
        b = npu.tondim2(a, copy=False)
        b[1, 1] = 42.
        npt.assert_almost_equal(b, np.array([[429., 5.], [2., 42.]]))
        npt.assert_almost_equal(a, np.array([[429., 5.], [2., 42.]]))
    
        a = [[429., 5.], [2., 14.]]
        b = npu.tondim2(a, copy=False)
        b[1, 1] = 42.
        npt.assert_almost_equal(b, np.array([[429., 5.], [2., 42.]]))
        npt.assert_almost_equal(a, np.array([[429., 5.], [2., 14.]]))

        a = np.array([[429., 5.], [2., 14.]])
        b = npu.tondim2(a, copy=True)
        b[1, 1] = 42.
        npt.assert_almost_equal(b, np.array([[429., 5.], [2., 42.]]))
        npt.assert_almost_equal(a, np.array([[429., 5.], [2., 14.]]))

    def testrow(self):
        row = npu.row(1., 1., 2., 5., 14.)
        npt.assert_almost_equal(row, np.array([[1., 1., 2., 5., 14.]]))
        
    def testcol(self):
        col = npu.col(1., 1., 2., 5., 14.)
        npt.assert_almost_equal(col, np.array(([[1.], [1.], [2.], [5.], [14.]])))
        
    def testmatrix(self):
        matrix = npu.matrix(3, 429., 5., 2., 14., 42., 132.)
        npt.assert_almost_equal(matrix, np.array([[429., 5., 2.], [14., 42., 132.]]))
        
    def testmatrixof(self):
        matrix = npu.matrixof(2, 3, 429.)
        npt.assert_almost_equal(matrix, np.array([[429., 429., 429.], [429., 429., 429.]]))
        
    def testrowof(self):
        row = npu.rowof(5, 429.)
        npt.assert_almost_equal(row, np.array([[429., 429., 429., 429., 429.]]))
        
    def testcolof(self):
        col = npu.colof(5, 429.)
        npt.assert_almost_equal(col, np.array([[429.], [429.], [429.], [429.], [429.]]))
        
    def testndim1of(self):
        ndim1 = npu.ndim1of(5, 429.)
        npt.assert_almost_equal(ndim1, np.array([429., 429., 429., 429., 429.]))
        
    def testmakeimmutable(self):
        a = np.array([[429., 5.], [2., 14.]])
        a[1, 1] = 42.
        b = npu.makeimmutable(a)
        self.assertIs(b, a)
        npt.assert_almost_equal(b[1, 1], 42.)
        with self.assertRaises(ValueError):
            b[1, 1] = 132.
        npt.assert_almost_equal(b[1, 1], 42.)
    
    def testimmutablecopyof(self):
        a = np.array([[429., 5.], [2., 14.]])
        npt.assert_almost_equal(a, np.array([[429., 5.], [2., 14.]]))
        a[1, 1] = 42.
        npt.assert_almost_equal(a, np.array([[429., 5.], [2., 42.]]))
        b = npu.immutablecopyof(a)
        npt.assert_almost_equal(b, np.array([[429., 5.], [2., 42.]]))
        with self.assertRaises(ValueError):
            b[1, 1] = 132.
        npt.assert_almost_equal(b, np.array([[429., 5.], [2., 42.]]))
        a[1, 1] = 132.
        npt.assert_almost_equal(b, np.array([[429., 5.], [2., 42.]]))
        
    def testlowertosymmetric(self):
        a = npu.matrix(3, 429., 0., 0., 5., 2., 0., 42., 1., 1.)
        b = npu.lowertosymmetric(a)
        npt.assert_almost_equal(a, npu.matrix(3, 429., 5., 42., 5., 2., 1., 42., 1., 1.))
        npt.assert_almost_equal(b, npu.matrix(3, 429., 5., 42., 5., 2., 1., 42., 1., 1.))
        
        a = npu.matrix(3, 429., 0., 0., 5., 2., 0., 42., 1., 1.)
        b = npu.lowertosymmetric(a, copy=True)
        npt.assert_almost_equal(a, npu.matrix(3, 429., 0., 0., 5., 2., 0., 42., 1., 1.))
        npt.assert_almost_equal(b, npu.matrix(3, 429., 5., 42., 5., 2., 1., 42., 1., 1.))        
    
    def testuppertosymmetric(self):
        a = npu.matrix(3, 429., 5., 42., 0., 2., 1., 0., 0., 1.)
        b = npu.uppertosymmetric(a)
        npt.assert_almost_equal(a, npu.matrix(3, 429., 5., 42., 5., 2., 1., 42., 1., 1.))
        npt.assert_almost_equal(b, npu.matrix(3, 429., 5., 42., 5., 2., 1., 42., 1., 1.))
        
        a = npu.matrix(3, 429., 5., 42., 0., 2., 1., 0., 0., 1.)
        b = npu.uppertosymmetric(a, copy=True)
        npt.assert_almost_equal(a, npu.matrix(3, 429., 5., 42., 0., 2., 1., 0., 0., 1.))
        npt.assert_almost_equal(b, npu.matrix(3, 429., 5., 42., 5., 2., 1., 42., 1., 1.))
        
    def testkron(self):
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

    def testkronsum(self):
        a = np.array([[5., 1.],
                      [2., 5.]])
        b = np.array([[ 14., 42.,  1.],
                      [132., 14.,  2.],
                      [  5.,  2., 42.]])
        c = npu.kronsum(a, b)
        
        m = npu.nrow(a)
        self.assertEqual(npu.ncol(a), m)
        n = npu.nrow(b)
        self.assertEqual(npu.ncol(b), n)
        
        knownkronsum = np.kron(a, np.eye(n)) + np.kron(np.eye(m), b)
        npt.assert_almost_equal(c, knownkronsum)
        
    def testvecandunvec(self):
        a = np.array([[  5., 1.,   14., 2., 42.],
                      [132., 2.,  429., 1.,  1.],
                      [  1., 2., 1430., 2.,  2.]])
        b = npu.col(5., 132., 1., 1., 2., 2., 14., 429., 1430., 2., 1., 2., 42., 1., 2.)
        npt.assert_almost_equal(npu.vec(a), b)
        npt.assert_almost_equal(npu.unvec(b, 3), a)

    def testvectorised(self):
        funccallcount = 0

        def func(a, b):
            nonlocal funccallcount
            funccallcount += 1
            return a + b
        
        funcvcallcount = 0
        
        @vectorised
        def funcv(a, b):
            nonlocal funcvcallcount
            funcvcallcount += 1
            return a + b
        
        def solver(a, b, f):
            if npu.isvectorised(f):
                return f(a, b)
            else:
                rc = np.shape(a)[0]
                r = np.empty((rc, 1))
                for i in range(rc):
                    r[i] = f(a[i], b[i])
                return r
            
        self.assertFalse(npu.isvectorised(func))
        self.assertTrue(npu.isvectorised(funcv))
        a = npu.col(14., 2., 429.)
        b = npu.col(42., 1., 5.)
        r = solver(a, b, func)
        npt.assert_almost_equal(r, np.array([[56.], [3.], [434.]]))
        self.assertEqual(funccallcount, 3)
        r = solver(a, b, funcv)
        npt.assert_almost_equal(r, np.array([[56.], [3.], [434.]]))
        self.assertEqual(funcvcallcount, 1)
        
if __name__ == '__main__':
    unittest.main()
    