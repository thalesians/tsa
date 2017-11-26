import unittest

import numpy as np
import numpy.testing as npt

import thalesians.tsa.stats as stats
import thalesians.tsa.utils as utils

class TestStats(unittest.TestCase):
    def test_cor_to_cov(self):
        cors = utils.SubdiagonalArray.create((-.25, -.5, .3))
        vars = (4., 3., 5.)  # @ReservedAssignment
        covs = stats.cor_to_cov(cors, vars)
        known_good_covs = np.array([
                [ 4.        , -0.8660254, -2.23606798],
                [-0.8660254 ,  3.       ,  1.161895  ],
                [-2.23606798,  1.161895 ,  5.        ]
            ])
        npt.assert_almost_equal(covs, known_good_covs)
            
if __name__ == '__main__':
    unittest.main()
    