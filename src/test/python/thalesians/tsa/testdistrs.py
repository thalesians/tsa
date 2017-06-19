import unittest

import numpy as np
import numpy.testing as npt

import thalesians.tsa.distrs as distrs
import thalesians.tsa.numpyutils as npu

class TestDistrs(unittest.TestCase):
    def testMultivariateNormalDistr(self):
        stdnormal1d = distrs.NormalDistr(dim=1)
        npt.assert_almost_equal(stdnormal1d.mean, 0.)
        npt.assert_almost_equal(stdnormal1d.cov, 1.)
        npt.assert_almost_equal(stdnormal1d.vol, 1.)
        
        stdnormal1d = distrs.NormalDistr(dim=2)
        npt.assert_almost_equal(stdnormal1d.mean, npu.colof(2, 0.))
        npt.assert_almost_equal(stdnormal1d.cov, np.eye(2))
        npt.assert_almost_equal(stdnormal1d.vol, np.eye(2))
        
        sd1=3.; sd2=4.; cor=-.5

        normal2d = distrs.NormalDistr(mean=[1., 2.], cov=distrs.NormalDistr.makecov2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(normal2d.mean, npu.col(1., 2.))
        npt.assert_almost_equal(normal2d.cov, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(normal2d.vol, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])

        normal2d = distrs.NormalDistr(mean=[1., 2.], vol=distrs.NormalDistr.makevol2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(normal2d.mean, npu.col(1., 2.))
        npt.assert_almost_equal(normal2d.cov, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(normal2d.vol, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])

if __name__ == '__main__':
    unittest.main()
