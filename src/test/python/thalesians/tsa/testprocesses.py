import unittest

import numpy as np
import numpy.testing as npt

import thalesians.tsa.distrs as distrs
import thalesians.tsa.processes as proc

class TestProcesses(unittest.TestCase):
    def test_ito_process(self):
        p = proc.ItoProcess()
        self.assertEqual(str(p), 'ItoProcess(process_dim=1, noise_dim=1)')
        
    def test_wiener_process(self):
        p = proc.WienerProcess(3., 5.)
        self.assertEqual(str(p), 'WienerProcess(process_dim=1, noise_dim=1, mean=[[ 3.]], vol=[[ 5.]])')
        
        sd1 = 3.; sd2 = 4.; cor = .5
        vol = np.array([[sd1, 0.], [cor * sd2, np.sqrt(1. - cor*cor) * sd2]])
        npt.assert_almost_equal(distrs.NormalDistr.make_vol_2d(sd1, sd2, cor), vol)
        cov = np.array([[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(distrs.NormalDistr.make_vol_from_cov(cov), vol)
        
    def test_ornstein_uhlenbeck_process(self):
        p = proc.OrnsteinUhlenbeckProcess(3., 3., 5.)
        self.assertEqual(str(p), 'OrnsteinUhlenbeckProcess(process_dim=1, noise_dim=1, transition=[[ 3.]], mean=[[ 3.]], vol=[[ 5.]])')

if __name__ == '__main__':
    unittest.main()
    