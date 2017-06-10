import unittest

import numpy as np
import numpy.testing as npt

import tsa.processes as proc

class TestProcesses(unittest.TestCase):
    def testItoProcess(self):
        p = proc.ItoProcess()
        self.assertEqual(str(p), 'ItoProcess(processdim=1, noisedim=1)')
        
    def testWienerProcess(self):
        p = proc.WienerProcess(3., 5.)
        self.assertEqual(str(p), 'WienerProcess(processdim=1, noisedim=1, mean=[[ 3.]], vol=[[ 5.]])')
        
        sd1 = 3.; sd2 = 4.; cor = .5
        vol = np.array([[sd1, 0.], [cor * sd2, np.sqrt(1. - cor*cor) * sd2]])
        npt.assert_almost_equal(proc.WienerProcess.makevol2d(sd1, sd2, cor), vol)
        cov = np.array([[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(proc.WienerProcess.makevolfromcov(cov), vol)
        
    def testOrnsteinUhlenbeckProcess(self):
        p = proc.OrnsteinUhlenbeckProcess(3., 3., 5.)
        self.assertEqual(str(p), 'OrnsteinUhlenbeckProcess(processdim=1, noisedim=1, transition=[[ 3.]], mean=[[ 3.]], vol=[[ 5.]])')

if __name__ == '__main__':
    unittest.main()
    