import unittest

import numpy as np
import numpy.testing as npt

import thalesians.tsa.distrs as distrs
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.stats as stats

class TestDistrs(unittest.TestCase):
    def test_multivariate_normal_distr(self):
        std_normal_1d = distrs.NormalDistr(dim=1)
        npt.assert_almost_equal(std_normal_1d.mean, 0.)
        npt.assert_almost_equal(std_normal_1d.cov, 1.)
        npt.assert_almost_equal(std_normal_1d.vol, 1.)
        
        std_normal_1d = distrs.NormalDistr(dim=2)
        npt.assert_almost_equal(std_normal_1d.mean, npu.col_of(2, 0.))
        npt.assert_almost_equal(std_normal_1d.cov, np.eye(2))
        npt.assert_almost_equal(std_normal_1d.vol, np.eye(2))
        
        sd1=3.; sd2=4.; cor=-.5

        normal_2d = distrs.NormalDistr(mean=[1., 2.], cov=stats.make_cov_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(normal_2d.mean, npu.col(1., 2.))
        npt.assert_almost_equal(normal_2d.cov, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(normal_2d.vol, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])

        normal_2d = distrs.NormalDistr(mean=[1., 2.], vol=stats.make_vol_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(normal_2d.mean, npu.col(1., 2.))
        npt.assert_almost_equal(normal_2d.cov, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(normal_2d.vol, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])

if __name__ == '__main__':
    unittest.main()
