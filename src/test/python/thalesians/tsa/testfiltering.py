import datetime as dt
import unittest

import thalesians.tsa.distrs as distrs
import thalesians.tsa.filtering as filtering
import thalesians.tsa.processes as proc

class TestFiltering(unittest.TestCase):
    def testkalmanfilterwithpriorpredict(self):
        t0 = dt.datetime(2014, 2, 12, 16, 18, 25, 204000)
        
        process = proc.WienerProcess.createfromcov(mean=3., cov=25.)
        
        kf = filtering.KalmanFilter(t0, statedistr=distrs.NormalDistr(mean=100., cov=250.), process=process)
        
        observable = kf.createobservable(filtering.KalmanFilterObsModel.createfromcompoundobsmatrix(1.), process)
        
        t1 = t0 + dt.timedelta(hours=1)
        
        predictedobs1 = observable.predict(t1)
    
if __name__ == '__main__':
    unittest.main()
    