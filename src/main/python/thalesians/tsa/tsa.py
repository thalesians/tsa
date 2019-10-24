import logging
import logging.config
import os
import re

import numpy as np
import pandas as pd
import pandas.plotting

import thalesians.tsa.checks as checks

class DataSet(object):
    class DataSubset(object):
        class InputAndOutput(object):
            def __init__(self, input_df, output_df, output_base_df):
                self.__input_df = input_df
                self.__output_df = output_df
                self.__output_base_df = output_base_df
            
            @property
            def input(self):
                return self.__input_df
            
            @property
            def output(self):
                return self.__output_df
            
            @property
            def output_base(self):
                return self.__output_base_df
            
        def __init__(self, input_df, output_df, output_base_df, purpose, split_purposes, split_starts_inclusive, split_ends_exclusive):
            self.__input_df = input_df
            self.__output_df = output_df
            self.__output_base_df = output_base_df
            self.__purpose = purpose
            self.__split_purposes = split_purposes
            self.__split_starts_inclusive = split_starts_inclusive
            self.__split_ends_exclusive = split_ends_exclusive
        
        def __getitem__(self, index):
            j = [i for i, x in enumerate(self.__split_purposes) if x == self.__purpose][index]
            return DataSet.DataSubset.InputAndOutput(
                    self.__input_df.iloc[self.__split_starts_inclusive[j]:self.__split_ends_exclusive[j]],
                    self.__output_df.iloc[self.__split_starts_inclusive[j]:self.__split_ends_exclusive[j]],
                    self.__output_base_df.iloc[self.__split_starts_inclusive[j]:self.__split_ends_exclusive[j]])
        
        def __len__(self):
            return len([i for i, x in enumerate(self.__split_purposes) if x == self.__purpose])
    
    def __init__(self, df):
        self.__input_df = df.copy()
        self.__output_df = None
        self.__output_base_df = None
        self.__original_columns = tuple(df.columns)
        self.__is_split = False
        self.__split_purposes = None
        self.__split_starts_inclusive = None
        self.__split_ends_exclusive = None
        self.__truncate_from_above = 0
        self.__truncate_from_below = 0
    
    @property
    def original_columns(self):
        return self.__original_columns
    
    def add_derived_column(self, name, func):
        result = self.__input_df.apply(func, axis=1)
        self.__input_df[name] = result
        
    def remove_input_column(self, column):
        del self.__input_df[column]
    
    def add_diff(self, column=None, prefix='diff(', suffix=')', exclude_column_re=None, include_column_re=None):
        logger = logging.getLogger()
        if column is None: column = self.__input_df.columns
        if not checks.is_iterable_not_string(column): column = [column]
        if exclude_column_re is not None: exclude_column_re = re.compile(exclude_column_re)
        if include_column_re is not None: include_column_re = re.compile(include_column_re)
        for c in column:
            if include_column_re is not None and not include_column_re.match(c):
                logger.info('- Excluding column due to include_column_re: %s' % c)
                continue
            if exclude_column_re is not None and exclude_column_re.match(c):
                logger.info('- Excluding column due to exclude_column_re: %s' % c)
                continue
            new_column_name = prefix + c + suffix
            logger.info('- Adding new diff column: %s' % new_column_name)
            self.__input_df[new_column_name] = self.__input_df[c].diff()
            try:
                self.__truncate_from_above = max(self.__truncate_from_above, list(self.__input_df[new_column_name].isnull().values).index(False))
            except ValueError:
                self.__truncate_from_above = max(self.__truncate_from_above, len(self.__input_df))
    
    def add_lag(self, lag, column=None, prefix='lag(${LAG},', suffix=')', exclude_column_re=None, include_column_re=None):
        logger = logging.getLogger()
        checks.check_not_none(lag)
        if not checks.is_iterable(lag): lag = [lag]
        if column is None: column = self.__input_df.columns
        if not checks.is_iterable_not_string(column): column = [column]
        if exclude_column_re is not None: exclude_column_re = re.compile(exclude_column_re)
        if include_column_re is not None: include_column_re = re.compile(include_column_re)
        for c in column:
            if include_column_re is not None and not include_column_re.match(c):
                logger.info('- Excluding column due to include_column_re: %s' % c)
                continue
            if exclude_column_re is not None and exclude_column_re.match(c):
                logger.info('- Excluding column due to exclude_column_re: %s' % c)
                continue
            for l in lag:
                c_prefix = prefix.replace('${LAG}', str(l))
                c_suffix = suffix.replace('${LAG}', str(l))
                new_column_name = c_prefix + c + c_suffix
                logger.info('- Adding new lag column: %s' % new_column_name)
                self.__input_df[new_column_name] = self.__input_df[c].shift(l)
                try:
                    self.__truncate_from_above = max(self.__truncate_from_above, list(self.__input_df[new_column_name].isnull().values).index(False))
                except ValueError:
                    self.__truncate_from_above = max(self.__truncate_from_above, len(self.__input_df))

    def add_ma(self, window, column=None, prefix='ma(${WINDOW},', suffix=')', exclude_column_re=None, include_column_re=None):
        logger = logging.getLogger()
        checks.check_not_none(window)
        if not checks.is_iterable(window): window = [window]
        if column is None: column = self.__input_df.columns
        if not checks.is_iterable_not_string(column): column = [column]
        if exclude_column_re is not None: exclude_column_re = re.compile(exclude_column_re)
        if include_column_re is not None: include_column_re = re.compile(include_column_re)
        for c in column:
            if include_column_re is not None and not include_column_re.match(c):
                logger.info('- Excluding column due to include_column_re: %s' % c)
                continue
            if exclude_column_re is not None and exclude_column_re.match(c):
                logger.info('- Excluding column due to exclude_column_re: %s' % c)
                continue
            for w in window:
                c_prefix = prefix.replace('${WINDOW}', str(w))
                c_suffix = suffix.replace('${WINDOW}', str(w))
                new_column_name = c_prefix + c + c_suffix
                logger.info('- Adding new MA column: %s' % new_column_name)
                self.__input_df[new_column_name] = self.__input_df[c].rolling(window=w, center=False).mean()
                try:
                    self.__truncate_from_above = max(self.__truncate_from_above, list(self.__input_df[new_column_name].isnull().values).index(False))
                except ValueError:
                    self.__truncate_from_above = max(self.__truncate_from_above, len(self.__input_df))

    def add_ln(self, column=None, prefix='ln(', suffix=')', exclude_column_re=None, include_column_re=None, exclude_columns_with_negative_values=True):
        logger = logging.getLogger()
        if column is None: column = self.__input_df.columns
        if not checks.is_iterable_not_string(column): column = [column]
        if exclude_column_re is not None: exclude_column_re = re.compile(exclude_column_re)
        if include_column_re is not None: include_column_re = re.compile(include_column_re)
        for c in column:
            if include_column_re is not None and not include_column_re.match(c):
                logger.info('- Excluding column due to include_column_re: %s' % c)
                continue
            if exclude_column_re is not None and exclude_column_re.match(c):
                logger.info('- Excluding column due to exclude_column_re: %s' % c)
                continue
            if exclude_columns_with_negative_values and any(self.__input_df[c] < 0.):
                logger.info('- Excluding column since it contains negative values: %s' % c)
                continue
            new_column_name = prefix + c + suffix
            logger.info('- Adding new ln column: %s' % new_column_name)
            self.__input_df[new_column_name] = self.__input_df[c].apply(np.log)
            
    def set_output(self, column, forecast_horizon=0, remove_from_input=None, difference_from_present=False):
        assert column is not None
        assert forecast_horizon is not None
        if not checks.is_iterable(forecast_horizon): forecast_horizon = [forecast_horizon]
        for fh in forecast_horizon: assert fh >= 0
        if remove_from_input is None:
            remove_from_input = not all(forecast_horizon)
        if difference_from_present:
            self.__output_df = pd.concat([self.__input_df[column].shift(-fh) - self.__input_df[column] for fh in forecast_horizon], axis=1)
        else:
            self.__output_df = pd.concat([self.__input_df[column].shift(-fh) for fh in forecast_horizon], axis=1)
        self.__output_df.columns = ['forecast(' + str(fh) + ',' + column + ')' if fh > 0 else column for fh in forecast_horizon]
        self.__output_base_df = self.__input_df[column].to_frame()
        if remove_from_input:
            del self.__input_df[column]
        self.__truncate_from_below = max(forecast_horizon)

    @property    
    def input_dim(self):
        return np.shape(self.__input_df)[1]
    
    @property
    def output_dim(self):
        return np.shape(self.__output_df)[1]
    
    @property
    def input_all(self):
        return self.__input_df
    
    @property
    def output_all(self):
        return self.__output_df
    
    @property
    def output_base_all(self):
        return self.__output_base_df
        
    @property
    def input_working(self):
        return self.__input_df.iloc[self.__truncate_from_above:len(self.__input_df) - self.__truncate_from_below]
    
    @property
    def output_working(self):
        return None if self.__output_df is None else self.__output_df.iloc[self.__truncate_from_above:len(self.__input_df) - self.__truncate_from_below]
    
    @property
    def output_base_working(self):
        return None if self.__output_base_df is None else self.__output_base_df.iloc[self.__truncate_from_above:len(self.__input_df) - self.__truncate_from_below]
    
    @property
    def is_split(self):
        return self.__is_split
    
    def split(self, purpose=('training', 'validation', 'test'), fraction=(.5, .25, .25)):
        logger = logging.getLogger()
        
        if not checks.is_iterable_not_string(purpose): purpose = [purpose]
        if not checks.is_iterable(fraction): fraction = [fraction]

        split_purposes = []
        split_starts_inclusive = []
        split_ends_exclusive = []
        
        count_remaining = len(self.input_working)
        fraction_done = 0.
        count_done = 0
        for p, f in zip(purpose, fraction):
            assert p in ('training', 'validation', 'test')
            split_purposes.append(p)
            next_count = int(count_remaining * f / (1. - fraction_done))
            split_starts_inclusive.append(count_done)
            count_done += next_count
            split_ends_exclusive.append(count_done)
            count_remaining -= next_count
            fraction_done += f
            
            logger.info('A %s set: [%d, %d)' % (split_purposes[-1], split_starts_inclusive[-1], split_ends_exclusive[-1]))
        
        self.__is_split = True
        self.__split_purposes = tuple(split_purposes)
        self.__split_starts_inclusive = tuple(split_starts_inclusive)
        self.__split_ends_exclusive = tuple(split_ends_exclusive)

    @property    
    def training_set(self):
        assert self.__is_split
        return DataSet.DataSubset(self.input_working, self.output_working, self.output_base_working, 'training', self.__split_purposes, self.__split_starts_inclusive, self.__split_ends_exclusive)
    
    @property
    def validation_set(self):
        assert self.__is_split
        return DataSet.DataSubset(self.input_working, self.output_working, self.output_base_working, 'validation', self.__split_purposes, self.__split_starts_inclusive, self.__split_ends_exclusive)
    
    @property
    def test_set(self):
        assert self.__is_split
        return DataSet.DataSubset(self.input_working, self.output_working, self.output_base_working, 'test', self.__split_purposes, self.__split_starts_inclusive, self.__split_ends_exclusive)
    
    @property
    def all_training_sets(self):
        assert self.__is_split
        return DataSet.DataSubset.InputAndOutput(
                pd.concat([self.input_working[s:e] for (p, s, e) in zip(self.__split_purposes, self.__split_starts_inclusive, self.__split_ends_exclusive) if p == 'training']),
                pd.concat([self.output_working[s:e] for (p, s, e) in zip(self.__split_purposes, self.__split_starts_inclusive, self.__split_ends_exclusive) if p == 'training']),
                pd.concat([self.output_base_working[s:e] for (p, s, e) in zip(self.__split_purposes, self.__split_starts_inclusive, self.__split_ends_exclusive) if p == 'training']))
    
    @property
    def all_validation_sets(self):
        assert self.__is_split
        return DataSet.DataSubset.InputAndOutput(
                pd.concat([self.input_working[s:e] for (p, s, e) in zip(self.__split_purposes, self.__split_starts_inclusive, self.__split_ends_exclusive) if p == 'validation']),
                pd.concat([self.output_working[s:e] for (p, s, e) in zip(self.__split_purposes, self.__split_starts_inclusive, self.__split_ends_exclusive) if p == 'validation']),
                pd.concat([self.output_base_working[s:e] for (p, s, e) in zip(self.__split_purposes, self.__split_starts_inclusive, self.__split_ends_exclusive) if p == 'validation']))
    
    @property
    def all_test_sets(self):
        assert self.__is_split
        return DataSet.DataSubset.InputAndOutput(
                pd.concat([self.input_working[s:e] for (p, s, e) in zip(self.__split_purposes, self.__split_starts_inclusive, self.__split_ends_exclusive) if p == 'test']),
                pd.concat([self.output_working[s:e] for (p, s, e) in zip(self.__split_purposes, self.__split_starts_inclusive, self.__split_ends_exclusive) if p == 'test']),
                pd.concat([self.output_base_working[s:e] for (p, s, e) in zip(self.__split_purposes, self.__split_starts_inclusive, self.__split_ends_exclusive) if p == 'test']))
    
    def __len__(self):
        return len(self.__input_df)
    
    def __repr__(self):
        return repr(self.__input_df)
    
    def __str__(self):
        return str(self.__input_df)
    
def to_lstm_input(input, timesteps):
    input_values = input.values if isinstance(input, pd.DataFrame) else input
    result = np.empty((np.shape(input_values)[0] - timesteps + 1, timesteps, np.shape(input_values)[1]))
    for i in range(np.shape(input_values)[0] - timesteps + 1):
        result[i,:,:] = input_values[i:i+timesteps,:]
    return result

def to_lstm_output(output, timesteps):
    output_values = output.values if isinstance(output, pd.DataFrame) else output
    return output_values[timesteps - 1:,:]

def __init_logging():
    module_dir = os.path.dirname(os.path.abspath(__file__))
    logging_config_file_name = 'tsa-logging.cfg'
    default_config_file_path = os.path.join(module_dir, '..', 'resources', logging_config_file_name)
    config_file_path = os.getenv('TSA_LOGGING_CONFIG', default_config_file_path)
    if not os.path.exists(config_file_path):
        config_file_path = os.path.join(module_dir, '..', '..', 'config', logging_config_file_name)
    if os.path.exists(config_file_path):
        logging.config.fileConfig(config_file_path)
    else:
        logging.basicConfig()

__version__ = '1.0.0'

__init_logging()
logger = logging.getLogger()
logger.info('Initialising TSA version %s' % __version__)

logger.info('Registering Pandas Matplotlib converters')
pandas.plotting.register_matplotlib_converters()
