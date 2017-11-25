import unittest

import thalesians.tsa.stats as stats
import thalesians.tsa.utils as utils

class TestStats(unittest.TestCase):
    def test_cor2cov(self):
        cors = utils.SubdiagonalArray.create((-.25, -.5, .3))
        vars = (4., 3., 5.)  # @ReservedAssignment
        covs = stats.cor_to_cov(cors, vars)
        print(cors)
        print(covs)
            
if __name__ == '__main__':
    unittest.main()
    