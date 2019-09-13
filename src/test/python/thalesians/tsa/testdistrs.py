import unittest

import numpy as np
import numpy.testing as npt

import thalesians.tsa.distrs as distrs
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.random as rnd
import thalesians.tsa.stats as stats

class TestDistrs(unittest.TestCase):
    def test_wide_sense_distr(self):
        std_wide_sense_1d = distrs.WideSenseDistr(dim=1)
        npt.assert_almost_equal(std_wide_sense_1d.mean, 0.)
        npt.assert_almost_equal(std_wide_sense_1d.cov, 1.)
        npt.assert_almost_equal(std_wide_sense_1d.vol, 1.)
        
        with self.assertRaises(NotImplementedError):
            std_wide_sense_1d.sample()
        
        std_wide_sense_2d = distrs.WideSenseDistr(dim=2)
        npt.assert_almost_equal(std_wide_sense_2d.mean, npu.col_of(2, 0.))
        npt.assert_almost_equal(std_wide_sense_2d.cov, np.eye(2))
        npt.assert_almost_equal(std_wide_sense_2d.vol, np.eye(2))
        
        with self.assertRaises(NotImplementedError):
            std_wide_sense_2d.sample()
        
        sd1=3.; sd2=4.; cor=-.5

        wide_sense_2d = distrs.WideSenseDistr(mean=[1., 2.], cov=stats.make_cov_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(wide_sense_2d.mean, npu.col(1., 2.))
        npt.assert_almost_equal(wide_sense_2d.cov, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(wide_sense_2d.vol, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])
        
        with self.assertRaises(NotImplementedError):
            wide_sense_2d.sample()

        wide_sense_2d = distrs.WideSenseDistr(mean=[1., 2.], vol=stats.make_vol_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(wide_sense_2d.mean, npu.col(1., 2.))
        npt.assert_almost_equal(wide_sense_2d.cov, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(wide_sense_2d.vol, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])
        
        with self.assertRaises(NotImplementedError):
            wide_sense_2d.sample()
    
    def test_normal_distr(self):
        rnd.random_state(np.random.RandomState(seed=42), force=True)

        std_normal_1d = distrs.NormalDistr(dim=1)
        npt.assert_almost_equal(std_normal_1d.mean, 0.)
        npt.assert_almost_equal(std_normal_1d.cov, 1.)
        npt.assert_almost_equal(std_normal_1d.vol, 1.)
        
        sample = std_normal_1d.sample()
        self.assertEqual(np.shape(sample), (1, 1))
        npt.assert_almost_equal(sample, [[ 0.49671415]])
        
        sample = std_normal_1d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 1))
        npt.assert_almost_equal(sample, [
                [-0.1382643 ],
                [ 0.64768854],
                [ 1.52302986],
                [-0.23415337],
                [-0.23413696],
                [ 1.57921282],
                [ 0.76743473],
                [-0.46947439],
                [ 0.54256004],
                [-0.46341769]])
        
        std_normal_2d = distrs.NormalDistr(dim=2)
        npt.assert_almost_equal(std_normal_2d.mean, npu.col_of(2, 0.))
        npt.assert_almost_equal(std_normal_2d.cov, np.eye(2))
        npt.assert_almost_equal(std_normal_2d.vol, np.eye(2))
        
        sample = std_normal_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [-0.46572975,  0.24196227],
                [-1.91328024, -1.72491783],
                [-0.56228753, -1.01283112],
                [ 0.31424733, -0.90802408],
                [-1.4123037 ,  1.46564877],
                [-0.2257763 ,  0.0675282 ],
                [-1.42474819, -0.54438272],
                [ 0.11092259, -1.15099358],
                [ 0.37569802, -0.60063869],
                [-0.29169375, -0.60170661]])

        sd1=3.; sd2=4.; cor=-.5

        normal_2d = distrs.NormalDistr(mean=[1., 2.], cov=stats.make_cov_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(normal_2d.mean, npu.col(1., 2.))
        npt.assert_almost_equal(normal_2d.cov, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(normal_2d.vol, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])

        sample = normal_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [-3.09581812,  9.06710684],
                [ 5.00400357, -1.07912958],
                [ 4.10821238, -2.42324481],
                [ 2.58989516, -7.05256838],
                [ 2.07671635,  3.61955714],
                [ 0.38728403,  2.5195548 ],
                [-1.36010204, -0.88681309],
                [ 1.63968707, -1.29329703],
                [-0.61960168,  6.44566548],
                [ 5.53451941, -4.36131646]])

        normal_2d = distrs.NormalDistr(mean=[1., 2.], vol=stats.make_vol_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(normal_2d.mean, npu.col(1., 2.))
        npt.assert_almost_equal(normal_2d.cov, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(normal_2d.vol, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])

        sample = normal_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [ 0.4624506 , -0.26705979],
                [ 1.76344545,  5.54913479],
                [-2.76038957,  4.57609973],
                [ 2.35608833,  1.20642031],
                [-2.1218454 ,  5.16796697],
                [-0.85307657, -0.00850715],
                [ 5.28771297, -1.62048489],
                [-2.12592264,  7.1016208 ],
                [-0.46508111,  6.26189296],
                [ 3.15543223, -0.04269231]])
        
    def test_dirac_delta_distr(self):
        std_dirac_delta_1d = distrs.DiracDeltaDistr(dim=1)
        npt.assert_almost_equal(std_dirac_delta_1d.mean, 0.)
        npt.assert_almost_equal(std_dirac_delta_1d.cov, 0.)
        npt.assert_almost_equal(std_dirac_delta_1d.vol, 0.)
        
        sample = std_dirac_delta_1d.sample()
        self.assertEqual(np.shape(sample), (1, 1))
        npt.assert_almost_equal(sample, [[ 0. ]])
        
        sample = std_dirac_delta_1d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 1))
        npt.assert_almost_equal(sample, [
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.]])
        
        std_dirac_delta_2d = distrs.DiracDeltaDistr(dim=2)
        npt.assert_almost_equal(std_dirac_delta_2d.mean, npu.col_of(2, 0.))
        npt.assert_almost_equal(std_dirac_delta_2d.cov, np.zeros((2, 2)))
        npt.assert_almost_equal(std_dirac_delta_2d.vol, np.zeros((2, 2)))
        
        sample = std_dirac_delta_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.]])

        dirac_delta_2d = distrs.DiracDeltaDistr(mean=[1., 2.], dim=2)
        npt.assert_almost_equal(dirac_delta_2d.mean, [[1.], [2.]])
        npt.assert_almost_equal(dirac_delta_2d.cov, np.zeros((2, 2)))
        npt.assert_almost_equal(dirac_delta_2d.vol, np.zeros((2, 2)))
        
        sample = dirac_delta_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.]])
    
    def test_log_normal_distr(self):
        rnd.random_state(np.random.RandomState(seed=42), force=True)

        std_log_normal_1d = distrs.LogNormalDistr(dim=1)
        npt.assert_almost_equal(std_log_normal_1d.mean, [[ 1.6487213]])
        npt.assert_almost_equal(std_log_normal_1d.cov, [[ 4.6707743]])
        npt.assert_almost_equal(std_log_normal_1d.vol, [[ 2.1611974]])
        
        sample = std_log_normal_1d.sample(size=1)
        self.assertEqual(np.shape(sample), (1, 1))
        npt.assert_almost_equal(sample, [[ 1.6433127]])
        
        sample = std_log_normal_1d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 1))
        npt.assert_almost_equal(sample, [
                [ 0.87086849],
                [ 1.91111824],
                [ 4.58609939],
                [ 0.79124045],
                [ 0.79125344],
                [ 4.85113557],
                [ 2.15423297],
                [ 0.62533086],
                [ 1.72040554],
                [ 0.62912979]])
        
        std_log_normal_2d = distrs.LogNormalDistr(dim=2)
        npt.assert_almost_equal(std_log_normal_2d.mean, [
                [ 1.6487213],
                [ 1.6487213]])
        npt.assert_almost_equal(std_log_normal_2d.cov, [
                [ 4.6707743,  0.       ],
                [ 0.       ,  4.6707743]])
        npt.assert_almost_equal(std_log_normal_2d.vol, [
                [ 2.1611974,  0.       ],
                [ 0.       ,  2.1611974]])
        
        sample = std_log_normal_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [ 0.62767689,  1.27374614],
                [ 0.14759544,  0.17818769],
                [ 0.5699039 ,  0.36318929],
                [ 1.36922835,  0.40332037],
                [ 0.2435815 ,  4.33035173],
                [ 0.79789657,  1.06986043],
                [ 0.24056903,  0.58019982],
                [ 1.11730841,  0.31632232],
                [ 1.45600738,  0.54846123],
                [ 0.74699727,  0.54787583]])

        sd1=.4; sd2=.4; cor=-.5

        log_normal_2d = distrs.LogNormalDistr(mean_of_log=[1., 1.3], cov_of_log=stats.make_cov_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(log_normal_2d.mean_of_log, npu.col(1., 1.3))
        npt.assert_almost_equal(log_normal_2d.cov_of_log, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(log_normal_2d.vol_of_log, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])
        npt.assert_almost_equal(log_normal_2d.mean, [[ 2.9446796], [ 3.9749016]])
        npt.assert_almost_equal(log_normal_2d.cov, [[ 1.5045366, -0.8999087], [-0.8999087,  2.7414445]])
        npt.assert_almost_equal(log_normal_2d.vol, [[ 1.2265956,  0.       ], [-0.7336637,  1.484312 ]])

        sample = log_normal_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [ 1.42711164,  6.95143797],
                [ 4.62238496,  2.99848502],
                [ 4.32618186,  2.50643161],
                [ 4.10913455,  1.42691268],
                [ 2.94320341,  4.55346303],
                [ 2.50304159,  3.80468825],
                [ 2.24476532,  2.45957906],
                [ 3.18112082,  2.60781028],
                [ 2.01884543,  5.66848303],
                [ 5.34174201,  2.12565878]])

        log_normal_2d = distrs.LogNormalDistr(mean_of_log=[1., 1.3], vol_of_log=stats.make_vol_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(log_normal_2d.mean_of_log, npu.col(1., 1.3))
        npt.assert_almost_equal(log_normal_2d.cov_of_log, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(log_normal_2d.vol_of_log, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])
        npt.assert_almost_equal(log_normal_2d.mean, npu.col(2.9446796, 3.9749016))
        npt.assert_almost_equal(log_normal_2d.cov, [[ 1.5045366, -0.8999087], [-0.8999087,  2.7414445]])
        npt.assert_almost_equal(log_normal_2d.vol, [[ 1.2265956,  0.       ], [-0.7336637,  1.484312 ]])

        sample = log_normal_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [ 2.71288329,  2.80448293],
                [ 2.70285608,  5.57387658],
                [ 1.66454464,  4.28346127],
                [ 3.23285936,  3.52238521],
                [ 1.76160691,  4.67441442],
                [ 2.32343609,  2.75776026],
                [ 4.8398479 ,  2.85230385],
                [ 1.67494888,  5.78583855],
                [ 2.06409776,  5.58431178],
                [ 3.6537541 ,  3.15441508]])

    def test_empirical_distr(self):
        rnd.random_state(np.random.RandomState(seed=42), force=True)
        
        trivial_empirical_1d = distrs.EmpiricalDistr(particles=[[0.]], weights=[1.])
        self.assertEqual(trivial_empirical_1d.particle_count, 1)
        self.assertEqual(trivial_empirical_1d.dim, 1)
        npt.assert_almost_equal(trivial_empirical_1d.particles, np.array([[0.]]))
        npt.assert_almost_equal(trivial_empirical_1d.particle(0), np.array([[0.]]))
        npt.assert_almost_equal(trivial_empirical_1d.weights, np.array([[1.]]))
        npt.assert_almost_equal(trivial_empirical_1d.weight(0), 1.)
        npt.assert_almost_equal(trivial_empirical_1d.normalised_weights, np.array([[1.]]))
        npt.assert_almost_equal(trivial_empirical_1d.normalised_weight(0), 1.)
        self.assertEqual(trivial_empirical_1d.weight_sum, 1.)
        self.assertEqual(trivial_empirical_1d.mean, 0.)
        self.assertEqual(trivial_empirical_1d.var_n, 0.)
        npt.assert_almost_equal(trivial_empirical_1d.var_n_minus_1, np.nan)
        self.assertEqual(trivial_empirical_1d.var, 0.)
        self.assertEqual(trivial_empirical_1d.cov_n, 0.)
        npt.assert_almost_equal(trivial_empirical_1d.cov_n_minus_1, np.nan)
        self.assertEqual(trivial_empirical_1d.cov, 0.)
        with self.assertRaises(np.linalg.LinAlgError):  # Matrix is not positive definite
            trivial_empirical_1d.vol_n
        with self.assertRaises(np.linalg.LinAlgError):  # Matrix is not positive definite
            trivial_empirical_1d.vol_n_minus_1
        with self.assertRaises(np.linalg.LinAlgError):  # Matrix is not positive definite
            trivial_empirical_1d.vol

        simple_empirical_1d = distrs.EmpiricalDistr(particles=[[-1.], [1.]], weights=[.5, .5])
        self.assertEqual(simple_empirical_1d.particle_count, 2)
        self.assertEqual(simple_empirical_1d.dim, 1)
        npt.assert_almost_equal(simple_empirical_1d.particles, np.array([[-1.], [1.]]))
        npt.assert_almost_equal(simple_empirical_1d.particle(0), np.array([[-1.]]))
        npt.assert_almost_equal(simple_empirical_1d.weights, np.array([[.5], [.5]]))
        npt.assert_almost_equal(simple_empirical_1d.weight(0), .5)
        npt.assert_almost_equal(simple_empirical_1d.normalised_weights, np.array([[.5], [.5]]))
        npt.assert_almost_equal(simple_empirical_1d.normalised_weight(0), .5)
        self.assertEqual(simple_empirical_1d.weight_sum, 1.)
        self.assertEqual(simple_empirical_1d.mean, 0.)
        self.assertEqual(simple_empirical_1d.var_n, 1.)
        # "n minus 1" (unbiased) stats don't make sense as we are not using "repeat"-type weights, meaning that each
        # weight represents the number of occurrences of one observation:
        npt.assert_almost_equal(simple_empirical_1d.var_n_minus_1, np.inf)
        self.assertEqual(simple_empirical_1d.cov_n, 1.)
        # "n minus 1" (unbiased) stats don't make sense as we are not using "repeat"-type weights, meaning that each
        # weight represents the number of occurrences of one observation:
        npt.assert_almost_equal(simple_empirical_1d.cov_n_minus_1, np.inf)
        self.assertEqual(simple_empirical_1d.cov, 1.)
        self.assertEqual(simple_empirical_1d.vol_n, 1.)
        # "n minus 1" (unbiased) stats don't make sense as we are not using "repeat"-type weights, meaning that each
        # weight represents the number of occurrences of one observation:
        self.assertEqual(simple_empirical_1d.vol_n_minus_1, np.inf)
        self.assertEqual(simple_empirical_1d.vol, 1.)

        # The weights can be specified as a one-dimensional array...
        simple_empirical_1d = distrs.EmpiricalDistr(particles=[[-1.], [1.]], weights=[.5, .5])
        self.assertEqual(simple_empirical_1d.particle_count, 2)
        self.assertEqual(simple_empirical_1d.dim, 1)
        npt.assert_almost_equal(simple_empirical_1d.particles, np.array([[-1.], [1.]]))
        # ...but they come back as a (two-dimensional) column vector:
        npt.assert_almost_equal(simple_empirical_1d.weights, np.array([[.5], [.5]]))

        # ...alternatively, the weights can be specified as a (two-dimensional) column vector:
        simple_empirical_1d = distrs.EmpiricalDistr(particles=[[-1.], [1.]], weights=[[.5], [.5]])
        self.assertEqual(simple_empirical_1d.particle_count, 2)
        self.assertEqual(simple_empirical_1d.dim, 1)
        npt.assert_almost_equal(simple_empirical_1d.particles, np.array([[-1.], [1.]]))
        # ...they always come back as a (two-dimensional) column vector:
        npt.assert_almost_equal(simple_empirical_1d.weights, np.array([[.5], [.5]]))

        # If the particles are specified as a one-dimensional array, they are interpreted as...
        simple_empirical_1d = distrs.EmpiricalDistr(particles=[-1., 1.], weights=[.5, .5])
        self.assertEqual(simple_empirical_1d.particle_count, 2)
        self.assertEqual(simple_empirical_1d.dim, 1)
        # ...multiple one-dimensional particles (each row corresponds to a particle, each column to a dimension):
        npt.assert_almost_equal(simple_empirical_1d.particles, np.array([[-1.], [1.]]))
        npt.assert_almost_equal(simple_empirical_1d.weights, np.array([[.5], [.5]]))

        # Now we shall be using "repeat"-type weights:
        repeat_empirical_1d = distrs.EmpiricalDistr(particles=[[-1.], [1.]], weights=[2., 1.])
        self.assertEqual(repeat_empirical_1d.particle_count, 2)
        self.assertEqual(repeat_empirical_1d.dim, 1)
        npt.assert_almost_equal(repeat_empirical_1d.particles, np.array([[-1.], [1.]]))
        npt.assert_almost_equal(repeat_empirical_1d.particle(0), np.array([[-1.]]))
        npt.assert_almost_equal(repeat_empirical_1d.weights, np.array([[2.], [1.]]))
        npt.assert_almost_equal(repeat_empirical_1d.weight(0), 2.)
        npt.assert_almost_equal(repeat_empirical_1d.normalised_weights, np.array([[ 0.6666667], [ 0.3333333]]))
        npt.assert_almost_equal(repeat_empirical_1d.normalised_weight(0), 0.6666667)
        self.assertEqual(repeat_empirical_1d.weight_sum, 3.)
        npt.assert_almost_equal(repeat_empirical_1d.mean, -0.33333333)
        npt.assert_almost_equal(repeat_empirical_1d.var_n, 0.88888889)
        npt.assert_almost_equal(repeat_empirical_1d.var_n_minus_1, 1.3333333)
        npt.assert_almost_equal(repeat_empirical_1d.cov_n, 0.88888889)
        npt.assert_almost_equal(repeat_empirical_1d.cov_n_minus_1, 1.3333333)
        npt.assert_almost_equal(repeat_empirical_1d.cov, 0.88888889)
        npt.assert_almost_equal(repeat_empirical_1d.vol_n, 0.94280904)
        npt.assert_almost_equal(repeat_empirical_1d.vol_n_minus_1, 1.15470054)
        npt.assert_almost_equal(repeat_empirical_1d.vol, 0.94280904)

        # Now we shall be using "repeat"-type weights. There are three two-dimensional particles:
        repeat_empirical_2d = distrs.EmpiricalDistr(particles=[[-2., 2.], [0., 0.], [1., -1.]], weights=[2., 1., 1.])
        self.assertEqual(repeat_empirical_2d.particle_count, 3)
        self.assertEqual(repeat_empirical_2d.dim, 2)
        npt.assert_almost_equal(repeat_empirical_2d.particles, np.array([[-2., 2.], [0., 0.], [1., -1.]]))
        npt.assert_almost_equal(repeat_empirical_2d.particle(0), np.array([[-2.], [2.]]))
        npt.assert_almost_equal(repeat_empirical_2d.weights, np.array([[2.], [1.], [1.]]))
        npt.assert_almost_equal(repeat_empirical_2d.weight(0), 2.)
        npt.assert_almost_equal(repeat_empirical_2d.normalised_weights, np.array([[ 0.5 ], [ 0.25], [ 0.25]]))
        npt.assert_almost_equal(repeat_empirical_2d.normalised_weight(0), .5)
        self.assertEqual(repeat_empirical_2d.weight_sum, 4.)
        npt.assert_almost_equal(repeat_empirical_2d.mean, [[-0.75], [ 0.75]])
        npt.assert_almost_equal(repeat_empirical_2d.var_n, [[ 1.6875], [ 1.6875]])
        npt.assert_almost_equal(repeat_empirical_2d.var_n_minus_1, [[ 2.25], [ 2.25]])
        npt.assert_almost_equal(repeat_empirical_2d.cov_n, [[ 1.6875, -1.6875], [-1.6875,  1.6875]])
        npt.assert_almost_equal(repeat_empirical_2d.cov_n_minus_1, [[ 2.25, -2.25], [-2.25,  2.25]])
        npt.assert_almost_equal(repeat_empirical_2d.cov, [[ 1.6875, -1.6875], [-1.6875,  1.6875]])
        with self.assertRaises(np.linalg.LinAlgError):  # Matrix is not positive definite
            repeat_empirical_2d.vol_n
        with self.assertRaises(np.linalg.LinAlgError):  # Matrix is not positive definite
            repeat_empirical_2d.vol_n_minus_1
        with self.assertRaises(np.linalg.LinAlgError):  # Matrix is not positive definite
            repeat_empirical_2d.vol
        
        normal_distr = distrs.NormalDistr(mean=[10., 100.], cov=[[4., -3.], [-3., 9.]])
        particles = normal_distr.sample(size=100)
        approx_normal_empirical_2d = distrs.EmpiricalDistr(particles=particles, weights=np.ones((100,)))
        self.assertEqual(approx_normal_empirical_2d.particle_count, 100)
        self.assertEqual(approx_normal_empirical_2d.dim, 2)
        npt.assert_almost_equal(approx_normal_empirical_2d.particles, particles)
        npt.assert_almost_equal(approx_normal_empirical_2d.particle(0), npu.col(*particles[0]))
        npt.assert_almost_equal(approx_normal_empirical_2d.weights, npu.col(*np.ones((100,))))
        npt.assert_almost_equal(approx_normal_empirical_2d.weight(0), 1.)
        npt.assert_almost_equal(approx_normal_empirical_2d.normalised_weights, npu.col(*np.ones((100,))) / 100.)
        npt.assert_almost_equal(approx_normal_empirical_2d.normalised_weight(0), .01)
        self.assertEqual(approx_normal_empirical_2d.weight_sum, 100.)
        npt.assert_almost_equal(approx_normal_empirical_2d.mean, [[ 10.2077457], [ 99.6856645]])
        npt.assert_almost_equal(approx_normal_empirical_2d.var_n, [[ 3.3516275], [ 6.7649298]])
        npt.assert_almost_equal(approx_normal_empirical_2d.var_n_minus_1, [[ 3.3854823], [ 6.8332624]])
        npt.assert_almost_equal(approx_normal_empirical_2d.cov_n, [[ 3.3516275, -1.8258307], [-1.8258307,  6.7649298]])
        npt.assert_almost_equal(approx_normal_empirical_2d.cov_n_minus_1, [[ 3.3854823, -1.8442735], [-1.8442735,  6.8332624]])
        npt.assert_almost_equal(approx_normal_empirical_2d.cov, [[ 3.3516275, -1.8258307], [-1.8258307,  6.7649298]])
        npt.assert_almost_equal(approx_normal_empirical_2d.vol_n, [[ 1.8307451,  0.       ], [-0.9973157,  2.4021431]])
        npt.assert_almost_equal(approx_normal_empirical_2d.vol_n_minus_1, [[ 1.839968 ,  0.       ], [-1.00234  ,  2.4142446]])
        npt.assert_almost_equal(approx_normal_empirical_2d.vol, [[ 1.8307451,  0.       ], [-0.9973157,  2.4021431]])

        # Using more particles more faithfully approximates the mean and covariance of the normal distribution:
        normal_distr = distrs.NormalDistr(mean=[10., 100.], cov=[[4., -3.], [-3., 9.]])
        particles = normal_distr.sample(size=100000)
        approx_normal_empirical_2d = distrs.EmpiricalDistr(particles=particles, weights=np.ones((100000,)))
        self.assertEqual(approx_normal_empirical_2d.particle_count, 100000)
        self.assertEqual(approx_normal_empirical_2d.dim, 2)
        npt.assert_almost_equal(approx_normal_empirical_2d.particles, particles)
        npt.assert_almost_equal(approx_normal_empirical_2d.particle(0), npu.col(*particles[0]))
        npt.assert_almost_equal(approx_normal_empirical_2d.weights, npu.col(*np.ones((100000,))))
        npt.assert_almost_equal(approx_normal_empirical_2d.weight(0), 1.)
        npt.assert_almost_equal(approx_normal_empirical_2d.normalised_weights, npu.col(*np.ones((100000,))) / 100000.)
        npt.assert_almost_equal(approx_normal_empirical_2d.normalised_weight(0), .00001)
        self.assertEqual(approx_normal_empirical_2d.weight_sum, 100000.)
        npt.assert_almost_equal(approx_normal_empirical_2d.mean, [[ 9.9863195], [ 100.0145412]])
        npt.assert_almost_equal(approx_normal_empirical_2d.var_n, [[ 3.9901799], [ 9.0390325]])
        npt.assert_almost_equal(approx_normal_empirical_2d.var_n_minus_1, [[ 3.9902198], [ 9.0391229]])
        npt.assert_almost_equal(approx_normal_empirical_2d.cov_n, [[ 3.9901799, -3.0120428], [-3.0120428,  9.0390325]])
        npt.assert_almost_equal(approx_normal_empirical_2d.cov_n_minus_1, [[ 3.9902198, -3.0120729], [-3.0120729,  9.0391229]])
        npt.assert_almost_equal(approx_normal_empirical_2d.cov, [[ 3.9901799, -3.0120428], [-3.0120428,  9.0390325]])
        npt.assert_almost_equal(approx_normal_empirical_2d.vol_n, [[ 1.9975435,  0.       ], [-1.5078735,  2.6010287]])
        npt.assert_almost_equal(approx_normal_empirical_2d.vol_n_minus_1, [[ 1.9975535,  0.       ], [-1.507881 ,  2.6010417]])
        npt.assert_almost_equal(approx_normal_empirical_2d.vol, [[ 1.9975435,  0.       ], [-1.5078735,  2.6010287]])
        
    def test_multinomial_resample(self):
        rnd.random_state(np.random.RandomState(seed=42), force=True)
        
        normal_distr = distrs.NormalDistr(mean=[10., 100.], cov=[[4., -3.], [-3., 9.]])
        particles = normal_distr.sample(size=100000)
        approx_normal_empirical_2d = distrs.EmpiricalDistr(particles=particles, weights=np.ones((100000,)))
        self.assertEqual(approx_normal_empirical_2d.particle_count, 100000)
        self.assertEqual(approx_normal_empirical_2d.dim, 2)
        npt.assert_almost_equal(approx_normal_empirical_2d.particles, particles)
        npt.assert_almost_equal(approx_normal_empirical_2d.particle(0), npu.col(*particles[0]))
        npt.assert_almost_equal(approx_normal_empirical_2d.weights, npu.col(*np.ones((100000,))))
        npt.assert_almost_equal(approx_normal_empirical_2d.weight(0), 1.)
        npt.assert_almost_equal(approx_normal_empirical_2d.normalised_weights, npu.col(*np.ones((100000,))) / 100000.)
        npt.assert_almost_equal(approx_normal_empirical_2d.normalised_weight(0), .00001)
        self.assertEqual(approx_normal_empirical_2d.weight_sum, 100000.)
        npt.assert_almost_equal(approx_normal_empirical_2d.mean, [[   9.9866994], [ 100.0141095]])
        npt.assert_almost_equal(approx_normal_empirical_2d.var_n, [[ 3.9902435], [ 9.0362717]])
        npt.assert_almost_equal(approx_normal_empirical_2d.var_n_minus_1, [[ 3.9902834], [ 9.036362 ]])
        npt.assert_almost_equal(approx_normal_empirical_2d.cov_n, [[ 3.9902435, -3.011222 ], [-3.011222 ,  9.0362717]])
        npt.assert_almost_equal(approx_normal_empirical_2d.cov_n_minus_1, [[ 3.9902834, -3.0112521], [-3.0112521,  9.036362 ]])
        npt.assert_almost_equal(approx_normal_empirical_2d.cov, [[ 3.9902435, -3.011222 ], [-3.011222 ,  9.0362717]])
        npt.assert_almost_equal(approx_normal_empirical_2d.vol_n, [[ 1.9975594,  0.       ], [-1.5074505,  2.6007431]])
        npt.assert_almost_equal(approx_normal_empirical_2d.vol_n_minus_1, [[ 1.9975694,  0.       ], [-1.5074581,  2.6007561]])
        npt.assert_almost_equal(approx_normal_empirical_2d.vol, [[ 1.9975594,  0.       ], [-1.5074505,  2.6007431]])
        
        rnd.random_state(np.random.RandomState(seed=43), force=True)

        resampled_approx_normal_empirical_2d = distrs.multinomial_resample(approx_normal_empirical_2d)
        self.assertEqual(resampled_approx_normal_empirical_2d.particle_count, 100000)
        self.assertEqual(resampled_approx_normal_empirical_2d.dim, 2)
        # The resampled particles should ("almost certainly") be different from the original ones:
        self.assertFalse(np.sum(resampled_approx_normal_empirical_2d.particles) == np.sum(particles))
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.particle(0), npu.col(*particles[1]))
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.weights, npu.col(*np.ones((100000,))))
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.weight(0), 1.)
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.normalised_weights, npu.col(*np.ones((100000,))) / 100000.)
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.normalised_weight(0), .00001)
        self.assertEqual(resampled_approx_normal_empirical_2d.weight_sum, 100000.)
        # But the stats should be pretty close to those of the original empirical distribution, though not to seven
        # decimal places:
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.mean, [[   9.9866994], [ 100.0141095]], decimal=1)
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.var_n, [[ 3.9902435], [ 9.0362717]], decimal=1)
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.var_n_minus_1, [[ 3.9902834], [ 9.036362 ]], decimal=1)
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.cov_n, [[ 3.9902435, -3.011222 ], [-3.011222 ,  9.0362717]], decimal=1)
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.cov_n_minus_1, [[ 3.9902834, -3.0112521], [-3.0112521,  9.036362 ]], decimal=1)
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.cov, [[ 3.9902435, -3.011222 ], [-3.011222 ,  9.0362717]], decimal=1)
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.vol_n, [[ 1.9975594,  0.       ], [-1.5074505,  2.6007431]], decimal=1)
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.vol_n_minus_1, [[ 1.9975694,  0.       ], [-1.5074581,  2.6007561]], decimal=1)
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d.vol, [[ 1.9975594,  0.       ], [-1.5074505,  2.6007431]], decimal=1)
        
        rnd.random_state(np.random.RandomState(seed=43), force=True)
        
        resampled_approx_normal_empirical_2d_particles = approx_normal_empirical_2d.sample(size=100000)
        npt.assert_almost_equal(resampled_approx_normal_empirical_2d_particles, resampled_approx_normal_empirical_2d.particles)

        subsampled_approx_normal_empirical_2d = distrs.multinomial_resample(approx_normal_empirical_2d, target_particle_count=40000)
        self.assertEqual(subsampled_approx_normal_empirical_2d.particle_count, 40000)
        self.assertEqual(subsampled_approx_normal_empirical_2d.dim, 2)
        # The resampled particles should ("almost certainly") be different from the original ones:
        self.assertFalse(np.sum(subsampled_approx_normal_empirical_2d.particles) == np.sum(particles))
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.particle(0), npu.col(*particles[1]))
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.weights, npu.col(*np.ones((40000,))))
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.weight(0), 1.)
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.normalised_weights, npu.col(*np.ones((40000,))) / 40000.)
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.normalised_weight(0), .000025)
        self.assertEqual(subsampled_approx_normal_empirical_2d.weight_sum, 40000.)
        # But the stats should be pretty close to those of the original empirical distribution, though not to seven
        # decimal places:
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.mean, [[   9.9866994], [ 100.0141095]], decimal=1)
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.var_n, [[ 3.9902435], [ 9.0362717]], decimal=1)
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.var_n_minus_1, [[ 3.9902834], [ 9.036362 ]], decimal=1)
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.cov_n, [[ 3.9902435, -3.011222 ], [-3.011222 ,  9.0362717]], decimal=1)
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.cov_n_minus_1, [[ 3.9902834, -3.0112521], [-3.0112521,  9.036362 ]], decimal=1)
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.cov, [[ 3.9902435, -3.011222 ], [-3.011222 ,  9.0362717]], decimal=1)
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.vol_n, [[ 1.9975594,  0.       ], [-1.5074505,  2.6007431]], decimal=1)
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.vol_n_minus_1, [[ 1.9975694,  0.       ], [-1.5074581,  2.6007561]], decimal=1)
        npt.assert_almost_equal(subsampled_approx_normal_empirical_2d.vol, [[ 1.9975594,  0.       ], [-1.5074505,  2.6007431]], decimal=1)

        supersampled_approx_normal_empirical_2d = distrs.multinomial_resample(approx_normal_empirical_2d, target_particle_count=300000)
        self.assertEqual(supersampled_approx_normal_empirical_2d.particle_count, 300000)
        self.assertEqual(supersampled_approx_normal_empirical_2d.dim, 2)
        # The resampled particles should ("almost certainly") be different from the original ones:
        self.assertFalse(np.sum(supersampled_approx_normal_empirical_2d.particles) == np.sum(particles))
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.particle(0), npu.col(*particles[0]))
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.weights, npu.col(*np.ones((300000,))))
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.weight(0), 1.)
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.normalised_weights, npu.col(*np.ones((300000,))) / 300000.)
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.normalised_weight(0), 3.3333333333333333e-06)
        self.assertEqual(supersampled_approx_normal_empirical_2d.weight_sum, 300000.)
        # But the stats should be pretty close to those of the original empirical distribution, though not to seven
        # decimal places:
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.mean, [[   9.9866994], [ 100.0141095]], decimal=1)
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.var_n, [[ 3.9902435], [ 9.0362717]], decimal=1)
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.var_n_minus_1, [[ 3.9902834], [ 9.036362 ]], decimal=1)
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.cov_n, [[ 3.9902435, -3.011222 ], [-3.011222 ,  9.0362717]], decimal=1)
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.cov_n_minus_1, [[ 3.9902834, -3.0112521], [-3.0112521,  9.036362 ]], decimal=1)
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.cov, [[ 3.9902435, -3.011222 ], [-3.011222 ,  9.0362717]], decimal=1)
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.vol_n, [[ 1.9975594,  0.       ], [-1.5074505,  2.6007431]], decimal=1)
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.vol_n_minus_1, [[ 1.9975694,  0.       ], [-1.5074581,  2.6007561]], decimal=1)
        npt.assert_almost_equal(supersampled_approx_normal_empirical_2d.vol, [[ 1.9975594,  0.       ], [-1.5074505,  2.6007431]], decimal=1)

if __name__ == '__main__':
    unittest.main()
