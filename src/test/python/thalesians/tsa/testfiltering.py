import datetime as dt
import unittest

import numpy.testing as npt

from thalesians.tsa.distrs import NormalDistr as N
import thalesians.tsa.filtering as filtering
import thalesians.tsa.processes as proc

class TestFiltering(unittest.TestCase):
    def testkalmanfilterwithpriorpredict(self):
        t0 = dt.datetime(2014, 2, 12, 16, 18, 25, 204000)
        
        process = proc.WienerProcess.createfromcov(mean=3., cov=25.)
        
        kf = filtering.KalmanFilter(t0, statedistr=N(mean=100., cov=250.), process=process)
        
        observable = kf.createobservable(filtering.KalmanFilterObsModel.createfromcompoundobsmatrix(1.), process)
        
        t1 = t0 + dt.timedelta(hours=1)
        
        priorpredictedobs1 = observable.predict(t1)
        npt.assert_almost_equal(priorpredictedobs1.distr.mean, 100. + 3./24.)
        npt.assert_almost_equal(priorpredictedobs1.distr.cov, 250. + 25./24.)
        npt.assert_almost_equal(priorpredictedobs1.crosscov, priorpredictedobs1.distr.cov)
        
        observable.observe(t1, N(mean=100.35, cov=100.0))
        
        posteriorpredictedobs1 = observable.predict(t1)
        npt.assert_almost_equal(posteriorpredictedobs1.distr.mean, 100.28590504)
        npt.assert_almost_equal(posteriorpredictedobs1.distr.cov, 71.513353115)
        npt.assert_almost_equal(posteriorpredictedobs1.crosscov, posteriorpredictedobs1.distr.cov)
        
        t2 = t1 + dt.timedelta(hours=2)
        
        priorpredictedobs2 = observable.predict(t2)
        npt.assert_almost_equal(priorpredictedobs2.distr.mean, 100.28590504 + 2.*3./24.)
        npt.assert_almost_equal(priorpredictedobs2.distr.cov, 71.513353115 + 2.*25./24.)
        npt.assert_almost_equal(priorpredictedobs2.crosscov, priorpredictedobs2.distr.cov)
        
        observable.observe(t2, N(mean=100.35, cov=100.0))

        posteriorpredictedobs2 = observable.predict(t2)
        npt.assert_almost_equal(posteriorpredictedobs2.distr.mean, 100.45709020)
        npt.assert_almost_equal(posteriorpredictedobs2.distr.cov, 42.395213845)
        npt.assert_almost_equal(posteriorpredictedobs2.crosscov, posteriorpredictedobs2.distr.cov)
    
    def testkalmanfilterwithoutpriorpredict(self):
        t0 = dt.datetime(2014, 2, 12, 16, 18, 25, 204000)
        
        process = proc.WienerProcess.createfromcov(mean=3., cov=25.)
        
        kf = filtering.KalmanFilter(t0, statedistr=N(mean=100., cov=250.), process=process)
                
        observable = kf.createobservable(filtering.KalmanFilterObsModel.createfromcompoundobsmatrix(1.), process)
        
        t1 = t0 + dt.timedelta(hours=1)
        
        observable.observe(t1, N(mean=100.35, cov=100.0))

        posteriorpredictedobs1 = observable.predict(t1)
        npt.assert_almost_equal(posteriorpredictedobs1.distr.mean, 100.28590504)
        npt.assert_almost_equal(posteriorpredictedobs1.distr.cov, 71.513353115)
        npt.assert_almost_equal(posteriorpredictedobs1.crosscov, posteriorpredictedobs1.distr.cov)
        
        t2 = t1 + dt.timedelta(hours=2)
        
        observable.observe(t2, N(mean=100.35, cov=100.0))
        
        posteriorpredictedobs2 = observable.predict(t2)
        npt.assert_almost_equal(posteriorpredictedobs2.distr.mean, 100.45709020)
        npt.assert_almost_equal(posteriorpredictedobs2.distr.cov, 42.395213845)
        npt.assert_almost_equal(posteriorpredictedobs2.crosscov, posteriorpredictedobs2.distr.cov)

if __name__ == '__main__':
    unittest.main()
    