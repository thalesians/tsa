import collections as col
import datetime as dt

import numpy as np
import pandas as pd

import thalesians.tsa.checks as checks
import thalesians.tsa.conversions as conv

eq = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) == value)
    
lt = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) < value)
    
gt = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) > value)
    
leq = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) <= value)
    
geq = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) >= value)
    
isin = lambda column, values, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)).isin(values))

def apply_predicates(df, predicates):
    for p in predicates:
        if p is not None: df = df[p(df)]
    return df

def apply_funs(df, funs):
    for f in funs:
        if f is not None: df = f(df)
    return df

def load_df_from_zipped_csv(path, predicates=[], pre_funs=[], post_funs=[], **kwargs):
    if 'iterator' not in kwargs: kwargs['iterator'] = True
    if 'chunksize' not in kwargs: kwargs['chunksize'] = 10000
    if 'compression' not in kwargs: kwargs['compression'] = 'zip'
    if 'header' not in kwargs: kwargs['header'] = 0
    if 'dtype' not in kwargs: kwargs['dtype'] = str
    if 'keep_default_na' not in kwargs: kwargs['keep_default_na'] = False
    it = pd.read_csv(path, **kwargs)
    df = pd.concat([apply_funs(apply_predicates(apply_funs(chunk, pre_funs), predicates), post_funs) for chunk in it])
    # Since we are reading the data chunk by chunk and then concatenating the resulting data frames, the indices may not
    # be unique. We correct this by replacing them:
    df.index = range(len(df))
    return df

def detect_df_column_types(df, none_values=conv.default_none_values, min_success_rate=conv.default_min_success_rate,
                           convert=False, in_place=False, return_df=False):
    if convert and (not in_place): return_df = True
    if not in_place: df = df.copy()
    types = {}
    for c in df.columns:
        if df[c].dtype != object:
            types[c] = df[c].dtype
            continue
        
        if len(df) == 0 or not checks.is_string(df[c].values[0]):
            types[c] = object
            continue
        
        float_results, float_success_count, _ = conv.strs_to_float(df[c].values, none_values=none_values,
                none_result=float('nan'), raise_value_error=False, return_extra_info=True,
                min_success_rate=min_success_rate)
        if float_results is not None and float_success_count > 0:
            int_results, int_success_count, _ = conv.strs_to_int(df[c].values, none_values=none_values,
                    none_result=None, min_success_rate=min_success_rate,
                    raise_value_error=False, return_extra_info=True)
            if float_success_count > int_success_count:
                types[c] = float
                if convert: df[c] = float_results
            else:
                types[c] = int
                if convert: df[c] = int_results
            continue        
        
        datetime_results = conv.strs_to_datetime(df[c].values, none_values=none_values, none_result=None,
                                                 raise_value_error=False, return_extra_info=False,
                                                 min_success_rate=min_success_rate)
        if datetime_results is not None:
            types[c] = dt.datetime
            if convert: df[c] = datetime_results
            continue
        
        date_results = conv.strs_to_date(df[c].values, none_values=none_values, none_result=None,
                                         raise_value_error=False, return_extra_info=False,
                                         min_success_rate=min_success_rate)
        if date_results is not None:
            types[c] = dt.date
            if convert: df[c] = date_results
            continue
        
        time_results = conv.strs_to_time(df[c].values, none_values=none_values, none_result=None,
                                         raise_value_error=False, return_extra_info=False,
                                         min_success_rate=min_success_rate)
        if time_results is not None:
            types[c] = dt.time
            if convert: df[c] = time_results
            continue
        
        types[c] = type(df[c].values[0]) if len(df) > 0 else None        
    
    return (types, df) if return_df else types

def convert_df_columns(df, conversions, in_place=False):
    if not in_place: df = df.copy()
    conversion_columns = set(conversions.keys())
    unfamiliar_columns = conversion_columns.difference(df.columns)
    assert len(unfamiliar_columns) == 0, 'Unfamiliar columns: %s' % str(unfamiliar_columns)
    for column, conversion in conversions.items():
        df[column] = df[column].apply(conversion)
    return df

def detect_df_categorical_columns(df):
    categorical_columns = []
    for c in df.columns:
        distinct_element_count = len(set(df[c]))
        if distinct_element_count <= 100 and distinct_element_count <= 0.1 * len(df):
            categorical_columns.append(c)
    return categorical_columns

def get_column_types(df):
    column_types = col.OrderedDict()
    if len(df) > 0:
        for c in df.columns:
            if df[c].dtype == object:
                non_none_values = [x for x in df[c].values if x is not None]
                column_types[c] = type(df[c].values[0]) if len(non_none_values) > 0 else object
            else:
                if checks.is_instance(df[c].values[0], np.datetime64):
                    column_types[c] = np.datetime64
                else:
                    column_types[c] = df[c].dtype
    return column_types

def get_df_columns_of_type(df, types):
    columns = []
    if len(df) > 0:
        for c in df.columns:
            non_none_values = [x for x in df[c].values if x is not None]
            if len(non_none_values) > 0 and checks.is_instance(df[c].values[0], types):
                columns.append(c)
    return columns

def get_df_int_columns(df):
    return get_df_columns_of_type(df, (int, np.int64))

def get_df_float_columns(df):
    return get_df_columns_of_type(df, (float, np.float64))

def get_df_time_columns(df):
    return get_df_columns_of_type(df, dt.time)

def get_df_date_columns(df):
    return get_df_columns_of_type(df, dt.date)

def get_df_datetime_columns(df):
    return get_df_columns_of_type(df, (dt.datetime, np.datetime64))

def combine_date_time(df, date_column, time_column):
    return df[[date_column, time_column]].apply(lambda x: dt.datetime.combine(x[0], x[1]), axis=1)
