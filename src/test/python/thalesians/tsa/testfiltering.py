import datetime as dt
import unittest

import numpy as np
import numpy.testing as npt

from thalesians.tsa.distrs import NormalDistr as N
import thalesians.tsa.filtering as filtering
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.processes as proc

class TestFiltering(unittest.TestCase):
    def test_kalman_filter_with_prior_predict(self):
        t0 = dt.datetime(2017, 5, 12, 16, 18, 25, 204000)
        
        process = proc.WienerProcess.create_from_cov(mean=3., cov=25.)
        
        kf = filtering.KalmanFilter(t0, state_distr=N(mean=100., cov=250.), process=process)
        
        observable = kf.create_observable(filtering.KalmanFilterObsModel.create(1.), process)
        
        t1 = t0 + dt.timedelta(hours=1)
        
        prior_predicted_obs1 = observable.predict(t1)
        npt.assert_almost_equal(prior_predicted_obs1.distr.mean, 100. + 3./24.)
        npt.assert_almost_equal(prior_predicted_obs1.distr.cov, 250. + 25./24.)
        npt.assert_almost_equal(prior_predicted_obs1.cross_cov, prior_predicted_obs1.distr.cov)
        
        observable.observe(t1, N(mean=100.35, cov=100.0))
        
        posterior_predicted_obs1 = observable.predict(t1)
        npt.assert_almost_equal(posterior_predicted_obs1.distr.mean, 100.28590504)
        npt.assert_almost_equal(posterior_predicted_obs1.distr.cov, 71.513353115)
        npt.assert_almost_equal(posterior_predicted_obs1.cross_cov, posterior_predicted_obs1.distr.cov)
        
        t2 = t1 + dt.timedelta(hours=2)
        
        prior_predicted_obs2 = observable.predict(t2)
        npt.assert_almost_equal(prior_predicted_obs2.distr.mean, 100.28590504 + 2.*3./24.)
        npt.assert_almost_equal(prior_predicted_obs2.distr.cov, 71.513353115 + 2.*25./24.)
        npt.assert_almost_equal(prior_predicted_obs2.cross_cov, prior_predicted_obs2.distr.cov)
        
        observable.observe(t2, N(mean=100.35, cov=100.0))

        posterior_predicted_obs2 = observable.predict(t2)
        npt.assert_almost_equal(posterior_predicted_obs2.distr.mean, 100.45709020)
        npt.assert_almost_equal(posterior_predicted_obs2.distr.cov, 42.395213845)
        npt.assert_almost_equal(posterior_predicted_obs2.cross_cov, posterior_predicted_obs2.distr.cov)
    
    def test_kalman_filter_without_prior_predict(self):
        t0 = dt.datetime(2017, 5, 12, 16, 18, 25, 204000)
        
        process = proc.WienerProcess.create_from_cov(mean=3., cov=25.)
        
        kf = filtering.KalmanFilter(t0, state_distr=N(mean=100., cov=250.), process=process)
                
        observable = kf.create_observable(filtering.KalmanFilterObsModel.create(1.), process)
        
        t1 = t0 + dt.timedelta(hours=1)
        
        observable.observe(t1, N(mean=100.35, cov=100.0))

        posterior_predicted_obs1 = observable.predict(t1)
        npt.assert_almost_equal(posterior_predicted_obs1.distr.mean, 100.28590504)
        npt.assert_almost_equal(posterior_predicted_obs1.distr.cov, 71.513353115)
        npt.assert_almost_equal(posterior_predicted_obs1.cross_cov, posterior_predicted_obs1.distr.cov)
        
        t2 = t1 + dt.timedelta(hours=2)
        
        observable.observe(t2, N(mean=100.35, cov=100.0))
        
        posterior_predicted_obs2 = observable.predict(t2)
        npt.assert_almost_equal(posterior_predicted_obs2.distr.mean, 100.45709020)
        npt.assert_almost_equal(posterior_predicted_obs2.distr.cov, 42.395213845)
        npt.assert_almost_equal(posterior_predicted_obs2.cross_cov, posterior_predicted_obs2.distr.cov)
        
    def testkalmanfilterwithlowvarianceobs(self):
        t0 = dt.datetime(2017, 5, 12, 16, 18, 25, 204000)
        
        process = proc.WienerProcess.create_from_cov(mean=3., cov=25.)
        
        kf = filtering.KalmanFilter(t0, state_distr=N(mean=100., cov=250.), process=process)
        
        observable = kf.create_observable(filtering.KalmanFilterObsModel.create(1.), process)
        
        t1 = t0 + dt.timedelta(hours=1)
        
        observable.observe(t1, N(mean=200., cov=0.0))
        
        posterior_predicted_obs1 = observable.predict(t1)
        npt.assert_almost_equal(posterior_predicted_obs1.distr.mean, 200.0)
        npt.assert_almost_equal(posterior_predicted_obs1.distr.cov, 2.8421709430404007E-14)
        npt.assert_almost_equal(posterior_predicted_obs1.cross_cov, posterior_predicted_obs1.distr.cov)
        
    def testkalmanfiltermultid(self):
        t0 = dt.datetime(2017, 5, 12, 16, 18, 25, 204000)
        
        process1 = proc.WienerProcess.create_from_cov(mean=3., cov=25.)
        process2 = proc.WienerProcess.create_from_cov(mean=[1., 4.], cov=[[36.0, -9.0], [-9.0, 25.0]])
        
        kf = filtering.KalmanFilter(t0, state_distr=N(mean=[100.0, 120.0, 130.0], cov=[[250.0, 0.0, 0.0], [0.0, 360.0, 0.0], [0.0,   0.0, 250.0]]), process=(process1, process2))
        
        state_observable = kf.create_observable(filtering.KalmanFilterObsModel.create(1.0, np.eye(2)), process1, process2)
        coord0_observable = kf.create_observable(filtering.KalmanFilterObsModel.create(1.), process1)
        coord1_observable = kf.create_observable(filtering.KalmanFilterObsModel.create(npu.row(1., 0.)), process2)
        coord2_observable = kf.create_observable(filtering.KalmanFilterObsModel.create(npu.row(0., 1.)), process2)
        sum_observable = kf.create_observable(filtering.KalmanFilterObsModel.create(npu.row(1., 1., 1.)), process1, process2)
        lin_comb_observable = kf.create_observable(filtering.KalmanFilterObsModel.create(npu.row(2., 0., -3.)), process1, process2)
        
        t1 = t0 + dt.timedelta(hours=1)
        
        predicted_obs1_prior = state_observable.predict(t1)
        npt.assert_almost_equal(predicted_obs1_prior.distr.mean, npu.col(100.0 + 3.0/24.0, 120.0 + 1.0/24.0, 130.0 + 4.0/24.0))
        npt.assert_almost_equal(predicted_obs1_prior.distr.cov, [[250.0 + 25.0/24.0, 0.0, 0.0], [0.0, 360.0 + 36.0/24.0, -9.0/24.0], [0.0, -9.0/24.0, 250 + 25.0/24.0]])
        npt.assert_almost_equal(predicted_obs1_prior.cross_cov, predicted_obs1_prior.distr.cov)
        
        state_observable.observe(t1, N(mean=[100.35, 121.0, 135.0], cov=[[100.0, 0.0, 0.0], [0.0, 400.0, 0.0], [0.0, 0.0, 100.0]]))
        
        predicted_obs1_posterior = state_observable.predict(t1)
        npt.assert_almost_equal(predicted_obs1_posterior.distr.mean, npu.col(100.285905044, 120.493895183, 133.623010239))
        npt.assert_almost_equal(predicted_obs1_posterior.distr.cov, [[71.513353115, 0.0, 0.0], [0.0, 189.888267669, -0.056112925], [0.0, -0.056112925, 71.513338130]])
        npt.assert_almost_equal(predicted_obs1_posterior.cross_cov, predicted_obs1_posterior.distr.cov)
        
        predicted_obs1_0 = coord0_observable.predict(t1)
        npt.assert_almost_equal(predicted_obs1_0.distr.mean, 100.285905044)
        npt.assert_almost_equal(predicted_obs1_0.distr.cov, 71.513353115)
        npt.assert_almost_equal(predicted_obs1_0.cross_cov, npu.row(71.513353115, 0.0, 0.0))
        
        predicted_obs1_1 = coord1_observable.predict(t1)
        npt.assert_almost_equal(predicted_obs1_1.distr.mean, 120.493895183)
        npt.assert_almost_equal(predicted_obs1_1.distr.cov, 189.888267669)
        npt.assert_almost_equal(predicted_obs1_1.cross_cov, npu.row(0.0, 189.888267669, -0.056112925))

        predicted_obs1_2 = coord2_observable.predict(t1)
        npt.assert_almost_equal(predicted_obs1_2.distr.mean, 133.623010239)
        npt.assert_almost_equal(predicted_obs1_2.distr.cov, 71.513338130)
        npt.assert_almost_equal(predicted_obs1_2.cross_cov, npu.row(0.0, -0.056112925, 71.513338130))

        predicted_obs1_sum = sum_observable.predict(t1)
        npt.assert_almost_equal(predicted_obs1_sum.distr.mean, 354.402810466)
        npt.assert_almost_equal(predicted_obs1_sum.distr.cov, 332.802733064)
        npt.assert_almost_equal(predicted_obs1_sum.cross_cov, npu.row(71.513353115, 189.832154744, 71.457225204))

        predicted_obs1_lin_comb = lin_comb_observable.predict(t1)
        npt.assert_almost_equal(predicted_obs1_lin_comb.distr.mean, -200.297220628)
        npt.assert_almost_equal(predicted_obs1_lin_comb.distr.cov, 929.673455633)
        npt.assert_almost_equal(predicted_obs1_lin_comb.cross_cov, npu.row(143.026706231, 0.168338776, -214.540014390))
        
        t2 = t1 + dt.timedelta(minutes=30)
        
        coord1_observable.observe(t2, N(mean=125.25, cov=4.))
        
        predicted_obs2_1 = coord1_observable.predict(t2)
        npt.assert_almost_equal(predicted_obs2_1.distr.mean, 125.152685704)
        npt.assert_almost_equal(predicted_obs2_1.distr.cov, 3.917796226)
        npt.assert_almost_equal(predicted_obs2_1.cross_cov, npu.row(0.0, 3.917796226, -0.005006475))

        t3 = t2 + dt.timedelta(minutes=30)
        
        predicted_obs3_prior_sum = sum_observable.predict(t3)
        npt.assert_almost_equal(predicted_obs3_prior_sum.distr.mean, 359.368174232)
        npt.assert_almost_equal(predicted_obs3_prior_sum.distr.cov, 149.392502944)
        npt.assert_almost_equal(predicted_obs3_prior_sum.cross_cov, npu.row(72.555019782, 4.475289751, 72.36219341))
        
        predicted_obs3_prior0 = coord0_observable.predict(t3)
        npt.assert_almost_equal(predicted_obs3_prior0.distr.mean, 100.410905044)
        npt.assert_almost_equal(predicted_obs3_prior0.distr.cov, 72.555019782)
        npt.assert_almost_equal(predicted_obs3_prior0.cross_cov, npu.row(72.555019782, 0.0, 0.0))
        predicted_obs3_prior1 = coord1_observable.predict(t3)
        npt.assert_almost_equal(predicted_obs3_prior1.distr.mean, 125.173519037)
        npt.assert_almost_equal(predicted_obs3_prior1.distr.cov, 4.667796226)
        npt.assert_almost_equal(predicted_obs3_prior1.cross_cov, npu.row(0.0, 4.667796226, -0.192506475))
        predicted_obs3_prior2 = coord2_observable.predict(t3)
        npt.assert_almost_equal(predicted_obs3_prior2.distr.mean, 133.783750150)
        npt.assert_almost_equal(predicted_obs3_prior2.distr.cov, 72.554699886)
        npt.assert_almost_equal(predicted_obs3_prior2.cross_cov, npu.row(0.0, -0.192506475, 72.554699886))
        
        sum_observable.observe(t3, N(mean=365.00, cov=9.))
        
        predicted_obs3_posterior_sum = sum_observable.predict(t3)
        npt.assert_almost_equal(predicted_obs3_posterior_sum.distr.mean, 364.679994753)
        npt.assert_almost_equal(predicted_obs3_posterior_sum.distr.cov, 8.488612159)
        npt.assert_almost_equal(predicted_obs3_posterior_sum.cross_cov, npu.row(4.122639429, 0.254289862, 4.111682867))
        predicted_obs3_posterior0 = coord0_observable.predict(t3)
        npt.assert_almost_equal(predicted_obs3_posterior0.distr.mean, 102.990681374)
        npt.assert_almost_equal(predicted_obs3_posterior0.distr.cov, 39.319665849)
        npt.assert_almost_equal(predicted_obs3_posterior0.cross_cov, npu.row(39.319665849, 0.0, 0.0))
        predicted_obs3_posterior1 = coord1_observable.predict(t3)
        npt.assert_almost_equal(predicted_obs3_posterior1.distr.mean, 125.332643059)
        npt.assert_almost_equal(predicted_obs3_posterior1.distr.cov, 4.541349469)
        npt.assert_almost_equal(predicted_obs3_posterior1.cross_cov, npu.row(0.0, 4.541349469, -2.237058941))
        predicted_obs3_posterior2 = coord2_observable.predict(t3)
        npt.assert_almost_equal(predicted_obs3_posterior2.distr.mean, 136.356670319)
        npt.assert_almost_equal(predicted_obs3_posterior2.distr.cov, 39.495767563)
        npt.assert_almost_equal(predicted_obs3_posterior2.cross_cov, npu.row(0.0, -2.237058941, 39.495767563))
        
if __name__ == '__main__':
    unittest.main()
    