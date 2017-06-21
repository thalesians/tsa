import datetime as dt
import unittest

import numpy as np
import numpy.testing as npt

from thalesians.tsa.distrs import NormalDistr as N
import thalesians.tsa.filtering as filtering
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.processes as proc

class TestFiltering(unittest.TestCase):
    def testkalmanfilterwithpriorpredict(self):
        t0 = dt.datetime(2014, 2, 12, 16, 18, 25, 204000)
        
        process = proc.WienerProcess.createfromcov(mean=3., cov=25.)
        
        kf = filtering.KalmanFilter(t0, statedistr=N(mean=100., cov=250.), process=process)
        
        observable = kf.createobservable(filtering.KalmanFilterObsModel.create(1.), process)
        
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
                
        observable = kf.createobservable(filtering.KalmanFilterObsModel.create(1.), process)
        
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
        
    def testkalmanfilterwithlowvarianceobs(self):
        t0 = dt.datetime(2014, 2, 12, 16, 18, 25, 204000)
        
        process = proc.WienerProcess.createfromcov(mean=3., cov=25.)
        
        kf = filtering.KalmanFilter(t0, statedistr=N(mean=100., cov=250.), process=process)
        
        observable = kf.createobservable(filtering.KalmanFilterObsModel.create(1.), process)
        
        t1 = t0 + dt.timedelta(hours=1)
        
        observable.observe(t1, N(mean=200., cov=0.0))
        
        posteriorpredictedobs1 = observable.predict(t1)
        npt.assert_almost_equal(posteriorpredictedobs1.distr.mean, 200.0)
        npt.assert_almost_equal(posteriorpredictedobs1.distr.cov, 2.8421709430404007E-14)
        npt.assert_almost_equal(posteriorpredictedobs1.crosscov, posteriorpredictedobs1.distr.cov)
        
    def testkalmanfiltermultid(self):
        t0 = dt.datetime(2014, 2, 12, 16, 18, 25, 204000)
        
        process1 = proc.WienerProcess.createfromcov(mean=3., cov=25.)
        process2 = proc.WienerProcess.createfromcov(mean=[1., 4.], cov=[[36.0, -9.0], [-9.0, 25.0]])
        
        kf = filtering.KalmanFilter(t0, statedistr=N(mean=[100.0, 120.0, 130.0], cov=[[250.0, 0.0, 0.0], [0.0, 360.0, 0.0], [0.0,   0.0, 250.0]]), process=(process1, process2))
        
        stateobservable = kf.createobservable(filtering.KalmanFilterObsModel.create(1.0, np.eye(2)), process1, process2)
        coord0observable = kf.createobservable(filtering.KalmanFilterObsModel.create(1.), process1)
        coord1observable = kf.createobservable(filtering.KalmanFilterObsModel.create(npu.row(1., 0.)), process2)
        coord2observable = kf.createobservable(filtering.KalmanFilterObsModel.create(npu.row(0., 1.)), process2)
        sumobservable = kf.createobservable(filtering.KalmanFilterObsModel.create(npu.row(1., 1., 1.)), process1, process2)
        lincombobservable = kf.createobservable(filtering.KalmanFilterObsModel.create(npu.row(2., 0., -3.)), process1, process2)
        
        t1 = t0 + dt.timedelta(hours=1)
        
        predictedobs1_prior = stateobservable.predict(t1)
        npt.assert_almost_equal(predictedobs1_prior.distr.mean, npu.col(100.0 + 3.0/24.0, 120.0 + 1.0/24.0, 130.0 + 4.0/24.0))
        npt.assert_almost_equal(predictedobs1_prior.distr.cov, [[250.0 + 25.0/24.0,  0.0, 0.0], [0.0, 360.0 + 36.0/24.0, -9.0/24.0], [0.0, -9.0/24.0, 250 + 25.0/24.0]])
        npt.assert_almost_equal(predictedobs1_prior.crosscov, predictedobs1_prior.distr.cov)

if __name__ == '__main__':
    unittest.main()
    