import unittest

import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal

import thalesians.tsa.tsa as tsa

#import thalesians.tsa.distrs as distrs
#import thalesians.tsa.numpyutils as npu
#import thalesians.tsa.stats as stats
#from blaze.compute.tests.test_comprehensive import df

class TestTSA(unittest.TestCase):
    def test_data_set(self):
        df = pd.DataFrame({
            'col1': [10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200.],
            'col2': [100., 200., 300., 400., 500., 600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700., 1800., 1900., 2000.]
        },
            columns=['col1', 'col2'],
            index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
        )
        
        df
        
        ds = tsa.DataSet(df)
        
        self.assertSequenceEqual(ds.original_columns, ['col1', 'col2'])
        
        ds.add_derived_column('sum', lambda x: x['col1'] + x['col2'])
        
        self.assertSequenceEqual(ds.original_columns, ['col1', 'col2'])
        
        ds.add_diff()
        
        expected = pd.DataFrame(
                {
                    'col1': [10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200.],
                    'col2': [100., 200., 300., 400., 500., 600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700., 1800., 1900., 2000.],
                    'sum': [110., 220., 330., 440., 550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200.],
                    'diff(col1)': [np.nan, 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'diff(col2)': [np.nan, 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100.],
                    'diff(sum)': [np.nan, 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)'],
                index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
            )
        assert_frame_equal(ds.input_all, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200.],
                    'col2': [200., 300., 400., 500., 600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700., 1800., 1900., 2000.],
                    'sum': [220., 330., 440., 550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200.],
                    'diff(col1)': [10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'diff(col2)': [100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100.],
                    'diff(sum)': [110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)'],
                index=['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
            )
        assert_frame_equal(ds.input_working, expected)
        
        self.assertIsNone(ds.output_all)
        
        self.assertIsNone(ds.output_working)
        
        ds.add_output('sum', forecast_horizon=[1, 3])
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [220., 330., 440., 550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200., np.nan],
                    'forecast(3,sum)': [440., 550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200., np.nan, np.nan, np.nan]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
            )
        assert_frame_equal(ds.output_all, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [330., 440., 550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980.],
                    'forecast(3,sum)': [550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.output_working, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170.],
                    'col2': [200., 300., 400., 500., 600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700.],
                    'sum': [220., 330., 440., 550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870.],
                    'diff(col1)': [10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'diff(col2)': [100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100.],
                    'diff(sum)': [110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)'],
                index=['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.input_working, expected)
        
        ds.add_lag([1, 2, 3], include_column_re='diff\(col1\)')
        
        expected = pd.DataFrame(
                {
                    'col1': [10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200.],
                    'col2': [100., 200., 300., 400., 500., 600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700., 1800., 1900., 2000.],
                    'sum': [110., 220., 330., 440., 550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200.],
                    'diff(col1)': [np.nan, 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'diff(col2)': [np.nan, 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100.],
                    'diff(sum)': [np.nan, 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110.],
                    'lag(1,diff(col1))': [np.nan, np.nan, 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'lag(2,diff(col1))': [np.nan, np.nan, np.nan, 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'lag(3,diff(col1))': [np.nan, np.nan, np.nan, np.nan, 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))'],
                index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
            )
        assert_frame_equal(ds.input_all, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170.],
                    'col2': [500., 600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700.],
                    'sum': [550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870.],
                    'diff(col1)': [10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'diff(col2)': [100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100.],
                    'diff(sum)': [110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))'],
                index=['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.input_working, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [220., 330., 440., 550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200., np.nan],
                    'forecast(3,sum)': [440., 550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200., np.nan, np.nan, np.nan]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
            )
        assert_frame_equal(ds.output_all, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980.],
                    'forecast(3,sum)': [880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.output_working, expected)
        
        ds.add_ma([1, 2, 3], include_column_re='col1|col2')
        
        expected = pd.DataFrame(
                {
                    'col1': [10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200.],
                    'col2': [100., 200., 300., 400., 500., 600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700., 1800., 1900., 2000.],
                    'sum': [110., 220., 330., 440., 550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200.],
                    'diff(col1)': [np.nan, 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'diff(col2)': [np.nan, 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100.],
                    'diff(sum)': [np.nan, 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110.],
                    'lag(1,diff(col1))': [np.nan, np.nan, 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'lag(2,diff(col1))': [np.nan, np.nan, np.nan, 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'lag(3,diff(col1))': [np.nan, np.nan, np.nan, np.nan, 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'ma(1,col1)': [10., 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190., 200.],
                    'ma(2,col1)': [np.nan, 15., 25., 35., 45., 55., 65., 75., 85., 95., 105., 115., 125., 135., 145., 155., 165., 175., 185., 195.],
                    'ma(3,col1)': [np.nan, np.nan, 20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180., 190.],
                    'ma(1,col2)': [100., 200., 300., 400., 500., 600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700., 1800., 1900., 2000.],
                    'ma(2,col2)': [np.nan, 150., 250., 350., 450., 550., 650., 750., 850., 950., 1050., 1150., 1250., 1350., 1450., 1550., 1650., 1750., 1850., 1950.],
                    'ma(3,col2)': [np.nan, np.nan, 200., 300., 400., 500., 600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700., 1800., 1900.]
                },                    
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
            )
        assert_frame_equal(ds.input_all, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170.],
                    'col2': [500., 600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700.],
                    'sum': [550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870.],
                    'diff(col1)': [10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'diff(col2)': [100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100.],
                    'diff(sum)': [110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10., 10.],
                    'ma(1,col1)': [50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170.],
                    'ma(2,col1)': [45., 55., 65., 75., 85., 95., 105., 115., 125., 135., 145., 155., 165.],
                    'ma(3,col1)': [40., 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160.],
                    'ma(1,col2)': [500., 600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700.],
                    'ma(2,col2)': [450., 550., 650., 750., 850., 950., 1050., 1150., 1250., 1350., 1450., 1550., 1650.],
                    'ma(3,col2)': [400., 500., 600., 700., 800., 900., 1000., 1100., 1200., 1300., 1400., 1500., 1600.]
                },                    
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.input_working, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [220., 330., 440., 550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200., np.nan],
                    'forecast(3,sum)': [440., 550., 660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200., np.nan, np.nan, np.nan]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
            )
        assert_frame_equal(ds.output_all, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [660., 770., 880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980.],
                    'forecast(3,sum)': [880., 990., 1100., 1210., 1320., 1430., 1540., 1650., 1760., 1870., 1980., 2090., 2200.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.output_working, expected)
        
        ds.split(purpose=['training', 'validation', 'test'], fraction=[.5, .25, .25])
        
        expected = pd.DataFrame(
                {
                    'col1': [50., 60., 70., 80., 90., 100.],
                    'col2': [500., 600., 700., 800., 900., 1000.],
                    'sum': [550., 660., 770., 880., 990., 1100.],
                    'diff(col1)': [10., 10., 10., 10., 10., 10.],
                    'diff(col2)': [100., 100., 100., 100., 100., 100.],
                    'diff(sum)': [110., 110., 110., 110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10., 10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10., 10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10., 10., 10., 10.],
                    'ma(1,col1)': [50., 60., 70., 80., 90., 100.],
                    'ma(2,col1)': [45., 55., 65., 75., 85., 95.],
                    'ma(3,col1)': [40., 50., 60., 70., 80., 90.],
                    'ma(1,col2)': [500., 600., 700., 800., 900., 1000.],
                    'ma(2,col2)': [450., 550., 650., 750., 850., 950.],
                    'ma(3,col2)': [400., 500., 600., 700., 800., 900.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['E', 'F', 'G', 'H', 'I', 'J']
            )
        assert_frame_equal(ds.training_set[0].input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [660., 770., 880., 990., 1100., 1210.],
                    'forecast(3,sum)': [880., 990., 1100., 1210., 1320., 1430.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['E', 'F', 'G', 'H', 'I', 'J']
            )
        assert_frame_equal(ds.training_set[0].output, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [110., 120., 130.],
                    'col2': [1100., 1200., 1300.],
                    'sum': [1210., 1320., 1430.],
                    'diff(col1)': [10., 10., 10.],
                    'diff(col2)': [100., 100., 100.],
                    'diff(sum)': [110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10.],
                    'ma(1,col1)': [110., 120., 130.],
                    'ma(2,col1)': [105., 115., 125.],
                    'ma(3,col1)': [100., 110., 120.],
                    'ma(1,col2)': [1100., 1200., 1300.],
                    'ma(2,col2)': [1050., 1150., 1250.],
                    'ma(3,col2)': [1000., 1100., 1200.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['K', 'L', 'M']
            )
        assert_frame_equal(ds.validation_set[0].input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [1320., 1430., 1540.],
                    'forecast(3,sum)': [1540., 1650., 1760.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['K', 'L', 'M']
            )
        assert_frame_equal(ds.validation_set[0].output, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [140., 150., 160., 170.],
                    'col2': [1400., 1500., 1600., 1700.],
                    'sum': [1540., 1650., 1760., 1870.],
                    'diff(col1)': [10., 10., 10., 10.],
                    'diff(col2)': [100., 100., 100., 100.],
                    'diff(sum)': [110., 110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10., 10.],
                    'ma(1,col1)': [140., 150., 160., 170.],
                    'ma(2,col1)': [135., 145., 155., 165.],
                    'ma(3,col1)': [130., 140., 150., 160.],
                    'ma(1,col2)': [1400., 1500., 1600., 1700.],
                    'ma(2,col2)': [1350., 1450., 1550., 1650.],
                    'ma(3,col2)': [1300., 1400., 1500., 1600.]
                },                    
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.test_set[0].input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [1650., 1760., 1870., 1980.],
                    'forecast(3,sum)': [1870., 1980., 2090., 2200.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.test_set[0].output, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [50., 60., 70., 80., 90., 100.],
                    'col2': [500., 600., 700., 800., 900., 1000.],
                    'sum': [550., 660., 770., 880., 990., 1100.],
                    'diff(col1)': [10., 10., 10., 10., 10., 10.],
                    'diff(col2)': [100., 100., 100., 100., 100., 100.],
                    'diff(sum)': [110., 110., 110., 110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10., 10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10., 10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10., 10., 10., 10.],
                    'ma(1,col1)': [50., 60., 70., 80., 90., 100.],
                    'ma(2,col1)': [45., 55., 65., 75., 85., 95.],
                    'ma(3,col1)': [40., 50., 60., 70., 80., 90.],
                    'ma(1,col2)': [500., 600., 700., 800., 900., 1000.],
                    'ma(2,col2)': [450., 550., 650., 750., 850., 950.],
                    'ma(3,col2)': [400., 500., 600., 700., 800., 900.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['E', 'F', 'G', 'H', 'I', 'J']
            )
        assert_frame_equal(ds.all_training_sets.input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [660., 770., 880., 990., 1100., 1210.],
                    'forecast(3,sum)': [880., 990., 1100., 1210., 1320., 1430.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['E', 'F', 'G', 'H', 'I', 'J']
            )
        assert_frame_equal(ds.all_training_sets.output, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [110., 120., 130.],
                    'col2': [1100., 1200., 1300.],
                    'sum': [1210., 1320., 1430.],
                    'diff(col1)': [10., 10., 10.],
                    'diff(col2)': [100., 100., 100.],
                    'diff(sum)': [110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10.],
                    'ma(1,col1)': [110., 120., 130.],
                    'ma(2,col1)': [105., 115., 125.],
                    'ma(3,col1)': [100., 110., 120.],
                    'ma(1,col2)': [1100., 1200., 1300.],
                    'ma(2,col2)': [1050., 1150., 1250.],
                    'ma(3,col2)': [1000., 1100., 1200.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['K', 'L', 'M']
            )
        assert_frame_equal(ds.all_validation_sets.input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [1320., 1430., 1540.],
                    'forecast(3,sum)': [1540., 1650., 1760.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['K', 'L', 'M']
            )
        assert_frame_equal(ds.all_validation_sets.output, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [140., 150., 160., 170.],
                    'col2': [1400., 1500., 1600., 1700.],
                    'sum': [1540., 1650., 1760., 1870.],
                    'diff(col1)': [10., 10., 10., 10.],
                    'diff(col2)': [100., 100., 100., 100.],
                    'diff(sum)': [110., 110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10., 10.],
                    'ma(1,col1)': [140., 150., 160., 170.],
                    'ma(2,col1)': [135., 145., 155., 165.],
                    'ma(3,col1)': [130., 140., 150., 160.],
                    'ma(1,col2)': [1400., 1500., 1600., 1700.],
                    'ma(2,col2)': [1350., 1450., 1550., 1650.],
                    'ma(3,col2)': [1300., 1400., 1500., 1600.]
                },                    
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.all_test_sets.input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [1650., 1760., 1870., 1980.],
                    'forecast(3,sum)': [1870., 1980., 2090., 2200.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.all_test_sets.output, expected)
        
        ds.split(purpose=['training', 'validation', 'validation', 'test'], fraction=[.25, .25, .25, .25])
        
        expected = pd.DataFrame(
                {
                    'col1': [50., 60., 70.],
                    'col2': [500., 600., 700.],
                    'sum': [550., 660., 770.],
                    'diff(col1)': [10., 10., 10.],
                    'diff(col2)': [100., 100., 100.],
                    'diff(sum)': [110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10.],
                    'ma(1,col1)': [50., 60., 70.],
                    'ma(2,col1)': [45., 55., 65.],
                    'ma(3,col1)': [40., 50., 60.],
                    'ma(1,col2)': [500., 600., 700.],
                    'ma(2,col2)': [450., 550., 650.],
                    'ma(3,col2)': [400., 500., 600.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['E', 'F', 'G']
            )
        assert_frame_equal(ds.training_set[0].input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [660., 770., 880.],
                    'forecast(3,sum)': [880., 990., 1100.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['E', 'F', 'G']
            )
        assert_frame_equal(ds.training_set[0].output, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [80., 90., 100.],
                    'col2': [800., 900., 1000.],
                    'sum': [880., 990., 1100.],
                    'diff(col1)': [10., 10., 10.],
                    'diff(col2)': [100., 100., 100.],
                    'diff(sum)': [110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10.],
                    'ma(1,col1)': [80., 90., 100.],
                    'ma(2,col1)': [75., 85., 95.],
                    'ma(3,col1)': [70., 80., 90.],
                    'ma(1,col2)': [800., 900., 1000.],
                    'ma(2,col2)': [750., 850., 950.],
                    'ma(3,col2)': [700., 800., 900.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['H', 'I', 'J']
            )
        assert_frame_equal(ds.validation_set[0].input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [990., 1100., 1210.],
                    'forecast(3,sum)': [1210., 1320., 1430.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['H', 'I', 'J']
            )
        assert_frame_equal(ds.validation_set[0].output, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [110., 120., 130.],
                    'col2': [1100., 1200., 1300.],
                    'sum': [1210., 1320., 1430.],
                    'diff(col1)': [10., 10., 10.],
                    'diff(col2)': [100., 100., 100.],
                    'diff(sum)': [110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10.],
                    'ma(1,col1)': [110., 120., 130.],
                    'ma(2,col1)': [105., 115., 125.],
                    'ma(3,col1)': [100., 110., 120.],
                    'ma(1,col2)': [1100., 1200., 1300.],
                    'ma(2,col2)': [1050., 1150., 1250.],
                    'ma(3,col2)': [1000., 1100., 1200.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['K', 'L', 'M']
            )
        assert_frame_equal(ds.validation_set[1].input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [1320., 1430., 1540.],
                    'forecast(3,sum)': [1540., 1650., 1760.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['K', 'L', 'M']
            )
        assert_frame_equal(ds.validation_set[1].output, expected)
                
        expected = pd.DataFrame(
                {
                    'col1': [140., 150., 160., 170.],
                    'col2': [1400., 1500., 1600., 1700.],
                    'sum': [1540., 1650., 1760., 1870.],
                    'diff(col1)': [10., 10., 10., 10.],
                    'diff(col2)': [100., 100., 100., 100.],
                    'diff(sum)': [110., 110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10., 10.],
                    'ma(1,col1)': [140., 150., 160., 170.],
                    'ma(2,col1)': [135., 145., 155., 165.],
                    'ma(3,col1)': [130., 140., 150., 160.],
                    'ma(1,col2)': [1400., 1500., 1600., 1700.],
                    'ma(2,col2)': [1350., 1450., 1550., 1650.],
                    'ma(3,col2)': [1300., 1400., 1500., 1600.]
                },                    
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.test_set[0].input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [1650., 1760., 1870., 1980.],
                    'forecast(3,sum)': [1870., 1980., 2090., 2200.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.test_set[0].output, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [50., 60., 70.],
                    'col2': [500., 600., 700.],
                    'sum': [550., 660., 770.],
                    'diff(col1)': [10., 10., 10.],
                    'diff(col2)': [100., 100., 100.],
                    'diff(sum)': [110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10.],
                    'ma(1,col1)': [50., 60., 70.],
                    'ma(2,col1)': [45., 55., 65.],
                    'ma(3,col1)': [40., 50., 60.],
                    'ma(1,col2)': [500., 600., 700.],
                    'ma(2,col2)': [450., 550., 650.],
                    'ma(3,col2)': [400., 500., 600.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['E', 'F', 'G']
            )
        assert_frame_equal(ds.all_training_sets.input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [660., 770., 880.],
                    'forecast(3,sum)': [880., 990., 1100.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['E', 'F', 'G']
            )
        assert_frame_equal(ds.all_training_sets.output, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [80., 90., 100., 110., 120., 130.],
                    'col2': [800., 900., 1000., 1100., 1200., 1300.],
                    'sum': [880., 990., 1100., 1210., 1320., 1430.],
                    'diff(col1)': [10., 10., 10., 10., 10., 10.],
                    'diff(col2)': [100., 100., 100., 100., 100., 100.],
                    'diff(sum)': [110., 110., 110., 110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10., 10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10., 10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10., 10., 10., 10.],
                    'ma(1,col1)': [80., 90., 100., 110., 120., 130.],
                    'ma(2,col1)': [75., 85., 95., 105., 115., 125.],
                    'ma(3,col1)': [70., 80., 90., 100., 110., 120.],
                    'ma(1,col2)': [800., 900., 1000., 1100., 1200., 1300.],
                    'ma(2,col2)': [750., 850., 950., 1050., 1150., 1250.],
                    'ma(3,col2)': [700., 800., 900., 1000., 1100., 1200.]
                },
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['H', 'I', 'J', 'K', 'L', 'M']
            )
        assert_frame_equal(ds.all_validation_sets.input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [990., 1100., 1210., 1320., 1430., 1540.],
                    'forecast(3,sum)': [1210., 1320., 1430., 1540., 1650., 1760.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['H', 'I', 'J', 'K', 'L', 'M']
            )
        assert_frame_equal(ds.all_validation_sets.output, expected)
        
        expected = pd.DataFrame(
                {
                    'col1': [140., 150., 160., 170.],
                    'col2': [1400., 1500., 1600., 1700.],
                    'sum': [1540., 1650., 1760., 1870.],
                    'diff(col1)': [10., 10., 10., 10.],
                    'diff(col2)': [100., 100., 100., 100.],
                    'diff(sum)': [110., 110., 110., 110.],
                    'lag(1,diff(col1))': [10., 10., 10., 10.],
                    'lag(2,diff(col1))': [10., 10., 10., 10.],
                    'lag(3,diff(col1))': [10., 10., 10., 10.],
                    'ma(1,col1)': [140., 150., 160., 170.],
                    'ma(2,col1)': [135., 145., 155., 165.],
                    'ma(3,col1)': [130., 140., 150., 160.],
                    'ma(1,col2)': [1400., 1500., 1600., 1700.],
                    'ma(2,col2)': [1350., 1450., 1550., 1650.],
                    'ma(3,col2)': [1300., 1400., 1500., 1600.]
                },                    
                columns=['col1', 'col2', 'sum', 'diff(col1)', 'diff(col2)', 'diff(sum)', 'lag(1,diff(col1))', 'lag(2,diff(col1))', 'lag(3,diff(col1))', 'ma(1,col1)', 'ma(2,col1)', 'ma(3,col1)', 'ma(1,col2)', 'ma(2,col2)', 'ma(3,col2)'],
                index=['N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.all_test_sets.input, expected)
        
        expected = pd.DataFrame(
                {
                    'forecast(1,sum)': [1650., 1760., 1870., 1980.],
                    'forecast(3,sum)': [1870., 1980., 2090., 2200.]
                },
                columns=['forecast(1,sum)', 'forecast(3,sum)'],
                index=['N', 'O', 'P', 'Q']
            )
        assert_frame_equal(ds.all_test_sets.output, expected)        

if __name__ == '__main__':
    unittest.main()
