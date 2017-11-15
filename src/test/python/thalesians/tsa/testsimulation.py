import collections
import datetime as dt
import unittest

import numpy as np
import numpy.testing as npt
import pandas as pd
import pandas.util.testing as pdt

import thalesians.tsa.numpyutils as npu
import thalesians.tsa.simulation as sim
import thalesians.tsa.processes as proc
import thalesians.tsa.random as rnd

class TestSimulation(unittest.TestCase):
    def test_xtimes(self):
        self.assertIsInstance(sim.xtimes(-5, 5, step=2), collections.Iterator)
        self.assertTrue(issubclass(collections.Iterator, collections.Iterable))
        self.assertIsInstance(sim.xtimes(-5, 5, step=2), collections.Iterable)
        
        self.assertEqual(list(sim.xtimes(-5, 5, step=2)), [-5, -3, -1, 1, 3])
        self.assertEqual(list(sim.xtimes(-5, 5, step=3)), [-5, -2, 1, 4])
        self.assertEqual(list(sim.xtimes(5, -5, step=-2)), [5, 3, 1, -1, -3])
        self.assertEqual(list(sim.xtimes(5, -5, step=-3)), [5, 2, -1, -4])
        
        self.assertEqual(list(sim.xtimes(-5., 5., step=2.5)), [-5.0, -2.5, 0.0, 2.5])
        self.assertEqual(list(sim.xtimes(-5., 5., step=3.25)), [-5.0, -1.75, 1.5, 4.75])
        self.assertEqual(list(sim.xtimes(5., -5., step=-2.5)), [5.0, 2.5, 0.0, -2.5])
        self.assertEqual(list(sim.xtimes(5., -5., step=-3.25)), [5.0, 1.75, -1.5, -4.75])

        self.assertEqual(
                list(sim.xtimes(dt.datetime(2017, 5, 5), dt.datetime(2017, 5, 10), dt.timedelta(days=1))),
                [dt.datetime(2017, 5, 5),  dt.datetime(2017, 5, 6),  dt.datetime(2017, 5, 7),  dt.datetime(2017, 5, 8),  dt.datetime(2017, 5, 9)])
        self.assertEqual(
                list(sim.xtimes(dt.datetime(2017, 5, 10), dt.datetime(2017, 5, 5), dt.timedelta(days=-1))),
                [dt.datetime(2017, 5, 10), dt.datetime(2017, 5, 9), dt.datetime(2017, 5, 8), dt.datetime(2017, 5, 7), dt.datetime(2017, 5, 6)])
        self.assertEqual(
                list(sim.xtimes(dt.datetime(2017, 5, 5, 8), dt.datetime(2017, 5, 5, 12), dt.timedelta(minutes=30))),
                [dt.datetime(2017, 5, 5, 8), dt.datetime(2017, 5, 5, 8, 30), dt.datetime(2017, 5, 5, 9), dt.datetime(2017, 5, 5, 9, 30),
                 dt.datetime(2017, 5, 5, 10), dt.datetime(2017, 5, 5, 10, 30), dt.datetime(2017, 5, 5, 11), dt.datetime(2017, 5, 5, 11, 30)])
        self.assertEqual(
                list(sim.xtimes(dt.datetime(2017, 5, 5, 12), dt.datetime(2017, 5, 5, 8), dt.timedelta(minutes=-30))),
                [dt.datetime(2017, 5, 5, 12), dt.datetime(2017, 5, 5, 11, 30), dt.datetime(2017, 5, 5, 11), dt.datetime(2017, 5, 5, 10, 30),
                 dt.datetime(2017, 5, 5, 10), dt.datetime(2017, 5, 5, 9, 30), dt.datetime(2017, 5, 5, 9), dt.datetime(2017, 5, 5, 8, 30)])
        self.assertEqual(
                list(sim.xtimes(dt.datetime(2017, 5, 5, 8), dt.datetime(2017, 5, 5, 8, 0, 1), dt.timedelta(milliseconds=100))),
                [dt.datetime(2017, 5, 5, 8), dt.datetime(2017, 5, 5, 8, 0, 0, 100000), dt.datetime(2017, 5, 5, 8, 0, 0, 200000),
                 dt.datetime(2017, 5, 5, 8, 0, 0, 300000), dt.datetime(2017, 5, 5, 8, 0, 0, 400000), dt.datetime(2017, 5, 5, 8, 0, 0, 500000),
                 dt.datetime(2017, 5, 5, 8, 0, 0, 600000), dt.datetime(2017, 5, 5, 8, 0, 0, 700000), dt.datetime(2017, 5, 5, 8, 0, 0, 800000),
                 dt.datetime(2017, 5, 5, 8, 0, 0, 900000)])
        
        self.assertEqual(
                list(sim.xtimes(dt.date(2017, 5, 5), dt.date(2017, 5, 10), dt.timedelta(days=1))),
                [dt.date(2017, 5, 5), dt.date(2017, 5, 6), dt.date(2017, 5, 7), dt.date(2017, 5, 8), dt.date(2017, 5, 9)])
        self.assertEqual(
                list(sim.xtimes(dt.date(2017, 5, 10), dt.date(2017, 5, 5), dt.timedelta(days=-1))),
                [dt.date(2017, 5, 10), dt.date(2017, 5, 9), dt.date(2017, 5, 8), dt.date(2017, 5, 7), dt.date(2017, 5, 6)])
        
        self.assertEqual(
                list(sim.xtimes(dt.time(8), dt.time(12), dt.timedelta(minutes=30))),
                [dt.time(8, 0), dt.time(8, 30), dt.time(9, 0), dt.time(9, 30), dt.time(10, 0), dt.time(10, 30), dt.time(11, 0), dt.time(11, 30)])
        self.assertEqual(
                list(sim.xtimes(dt.time(12), dt.time(8), dt.timedelta(minutes=-30))),
                [dt.time(12, 0), dt.time(11, 30), dt.time(11, 0), dt.time(10, 30), dt.time(10, 0), dt.time(9, 30), dt.time(9, 0), dt.time(8, 30)])
            
        # Since end is set to None, we have a potentially infinite iteration
        ts = sim.xtimes(dt.datetime(2017, 5, 10), None, dt.timedelta(days=1))
        self.assertEqual(dt.datetime(2017, 5, 10), next(ts))
        self.assertEqual(dt.datetime(2017, 5, 11), next(ts))
        self.assertEqual(dt.datetime(2017, 5, 12), next(ts))
        ts = sim.xtimes(dt.date(2017, 5, 10), None, dt.timedelta(days=-1))
        self.assertEqual(dt.date(2017, 5, 10), next(ts))
        self.assertEqual(dt.date(2017, 5, 9), next(ts))
        self.assertEqual(dt.date(2017, 5, 8), next(ts))

    def test_xtimes_random_step(self):
        rnd.random_state(np.random.RandomState(seed=42), force=True)

        npt.assert_almost_equal(list(sim.xtimes(-5., 5., step=lambda x: rnd.exponential(2.5))),
                [-5., -3.8268298, 3.6984738])
        npt.assert_almost_equal(list(sim.xtimes(-5., 5., step=lambda x: rnd.exponential(3.25))),
                [-5.0, -4.448719170997375, -3.897531222274908, -3.703055224296696, 2.833445085263108])
        npt.assert_almost_equal(list(sim.xtimes(5., -5., step=lambda x: -rnd.exponential(2.5))),
                [5.0, 4.9480017300021535, -3.8108919578936264])
        npt.assert_almost_equal(list(sim.xtimes(5., -5., step=lambda x: -rnd.exponential(3.25))),
                [5.0, 4.347793286563594, 3.689306162358759, 2.5103565416122082, 0.09259109131443122, -1.7454043757216628, -2.8641291015219728])
        
        self.assertEqual(
                list(sim.xtimes(dt.datetime(2017, 5, 5), dt.datetime(2017, 5, 10), lambda x: rnd.exponential(dt.timedelta(days=1)))),
                [dt.datetime(2017, 5, 5), dt.datetime(2017, 5, 5, 8, 17, 32, 540237), dt.datetime(2017, 5, 5, 19, 14, 34, 891891),
                 dt.datetime(2017, 5, 6, 9, 51, 26, 848922), dt.datetime(2017, 5, 7, 22, 46, 4, 520275), dt.datetime(2017, 5, 8, 4, 6, 48, 898763),
                 dt.datetime(2017, 5, 8, 21, 26, 32, 217758), dt.datetime(2017, 5, 9, 18, 58, 56, 625679), dt.datetime(2017, 5, 9, 20, 7, 26, 142298)])
        self.assertEqual(
                list(sim.xtimes(dt.datetime(2017, 5, 10), dt.datetime(2017, 5, 5), lambda x: -rnd.exponential(dt.timedelta(days=1)))),
                [dt.datetime(2017, 5, 10), dt.datetime(2017, 5, 9, 22, 23, 8, 396372), dt.datetime(2017, 5, 6, 23, 1, 1, 771013)])
        self.assertEqual(
                list(sim.xtimes(dt.datetime(2017, 5, 5, 8), dt.datetime(2017, 5, 5, 12), lambda x: rnd.exponential(dt.timedelta(minutes=30)))),
                [dt.datetime(2017, 5, 5, 8), dt.datetime(2017, 5, 5, 8, 10, 53, 918148), dt.datetime(2017, 5, 5, 8, 13, 58, 917315),
                 dt.datetime(2017, 5, 5, 8, 48, 33, 868689), dt.datetime(2017, 5, 5, 9, 5, 58, 32206), dt.datetime(2017, 5, 5, 9, 9, 52, 306227),
                 dt.datetime(2017, 5, 5, 9, 30, 22, 691238), dt.datetime(2017, 5, 5, 9, 31, 25, 679937), dt.datetime(2017, 5, 5, 10, 43, 26, 441134),
                 dt.datetime(2017, 5, 5, 10, 52, 25, 465132), dt.datetime(2017, 5, 5, 11, 25, 0, 725569), dt.datetime(2017, 5, 5, 11, 36, 13, 109416),
                 dt.datetime(2017, 5, 5, 11, 58, 14, 509029)])
        self.assertEqual(
                list(sim.xtimes(dt.datetime(2017, 5, 5, 12), dt.datetime(2017, 5, 5, 8), lambda x: -rnd.exponential(dt.timedelta(minutes=30)))),
                [dt.datetime(2017, 5, 5, 12), dt.datetime(2017, 5, 5, 10, 15, 12, 947161), dt.datetime(2017, 5, 5, 9, 30, 26, 905482),
                 dt.datetime(2017, 5, 5, 8, 6, 17, 735527)])
        self.assertEqual(
                list(sim.xtimes(dt.datetime(2017, 5, 5, 8), dt.datetime(2017, 5, 5, 8, 0, 1), lambda x: rnd.exponential(dt.timedelta(milliseconds=100)))),
                [dt.datetime(2017, 5, 5, 8), dt.datetime(2017, 5, 5, 8, 0, 0, 254944), dt.datetime(2017, 5, 5, 8, 0, 0, 264210),
                 dt.datetime(2017, 5, 5, 8, 0, 0, 286023), dt.datetime(2017, 5, 5, 8, 0, 0, 290651), dt.datetime(2017, 5, 5, 8, 0, 0, 330004),
                 dt.datetime(2017, 5, 5, 8, 0, 0, 379217), dt.datetime(2017, 5, 5, 8, 0, 0, 410873), dt.datetime(2017, 5, 5, 8, 0, 0, 587329),
                 dt.datetime(2017, 5, 5, 8, 0, 0, 631452), dt.datetime(2017, 5, 5, 8, 0, 0, 664432), dt.datetime(2017, 5, 5, 8, 0, 0, 742673),
                 dt.datetime(2017, 5, 5, 8, 0, 0, 757863), dt.datetime(2017, 5, 5, 8, 0, 0, 919911), dt.datetime(2017, 5, 5, 8, 0, 0, 927659)])

        self.assertEqual(
                list(sim.xtimes(dt.date(2017, 5, 5), dt.date(2017, 5, 10), lambda x: rnd.exponential(dt.timedelta(days=1)))),
                [dt.date(2017, 5, 5), dt.date(2017, 5, 5), dt.date(2017, 5, 5), dt.date(2017, 5, 6), dt.date(2017, 5, 7), dt.date(2017, 5, 8),
                 dt.date(2017, 5, 9), dt.date(2017, 5, 9), dt.date(2017, 5, 9), dt.date(2017, 5, 9)])
        self.assertEqual(
                list(sim.xtimes(dt.date(2017, 5, 10), dt.date(2017, 5, 5), lambda x: -rnd.exponential(dt.timedelta(days=1)))),
                [dt.date(2017, 5, 10), dt.date(2017, 5, 9), dt.date(2017, 5, 8), dt.date(2017, 5, 7), dt.date(2017, 5, 6)])
        
        self.assertEqual(
                list(sim.xtimes(dt.time(8), dt.time(12), lambda x: rnd.exponential(dt.timedelta(minutes=30)))),
                [dt.time(8), dt.time(9, 5, 28, 53442), dt.time(9, 24, 38, 372482), dt.time(9, 28, 27, 642791), dt.time(10, 5, 56, 70211),
                 dt.time(10, 48, 50, 777167), dt.time(11, 13, 33, 774658), dt.time(11, 57, 46, 776598)])
        self.assertEqual(
                list(sim.xtimes(dt.time(12), dt.time(8), lambda x: -rnd.exponential(dt.timedelta(minutes=30)))),
                [dt.time(12), dt.time(11, 43, 15, 934451), dt.time(11, 42, 29, 588458), dt.time(11, 39, 4, 87075), dt.time(11, 38, 6, 606449),
                 dt.time(11, 7, 45, 493257), dt.time(10, 56, 26, 179181), dt.time(10, 35, 7, 392262), dt.time(9, 23, 41, 114308), dt.time(9, 15, 4, 984427),
                 dt.time(8, 59, 14, 76872), dt.time(8, 16, 58, 328406), dt.time(8, 9, 10, 679124), dt.time(8, 6, 46, 491423)])
            
        # Since end is set to None, we have a potentially infinite iteration
        ts = sim.xtimes(dt.datetime(2017, 5, 10), None, lambda x: rnd.exponential(dt.timedelta(days=1)))
        self.assertEqual(dt.datetime(2017, 5, 10), next(ts))
        self.assertEqual(dt.datetime(2017, 5, 12, 15, 43, 7, 687420), next(ts))
        self.assertEqual(dt.datetime(2017, 5, 14, 7, 20, 24, 331174), next(ts))
        ts = sim.xtimes(dt.date(2017, 5, 10), None, lambda x: -rnd.exponential(dt.timedelta(days=1)))
        self.assertEqual(dt.date(2017, 5, 10), next(ts))
        self.assertEqual(dt.date(2017, 5, 7), next(ts))
        self.assertEqual(dt.date(2017, 5, 5), next(ts))
        
    def test_euler_maruyama(self):
        rnd.random_state(np.random.RandomState(seed=42), force=True)

        W = proc.WienerProcess.create_2d(mean1=-.5, mean2=3., sd1=3., sd2=4., cor=.5)
        em = sim.EulerMaruyama(process=W)
        
        t, v = next(em)
        npt.assert_almost_equal(t, 0.)
        npt.assert_almost_equal(v, npu.col(0.0, 0.0))

        t, v = next(em)
        npt.assert_almost_equal(t, 1.)
        npt.assert_almost_equal(v, npu.col(0.9901425, 3.5144667))
        
    def test_run(self):
        rnd.random_state(np.random.RandomState(seed=42), force=True)

        W = proc.WienerProcess.create_2d(mean1=.25, mean2=.5, sd1=3., sd2=4., cor=.5)
        em = sim.EulerMaruyama(process=W)
        
        df = sim.run(em, nstep=10)
        pdt.assert_frame_equal(df, pd.DataFrame(data=[
                [0.000000, 0.000000],
                [1.740142, 1.014467],
                [3.933208, 8.085774],
                [3.480748, 7.306393],
                [8.468386, 13.623291],
                [7.309963, 15.063825],
                [6.169710, 13.023654],
                [7.145597, 7.379782],
                [2.220843, 2.482125],
                [-0.567650, 2.045047]],
                index=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]))
        
if __name__ == '__main__':
    unittest.main()
    