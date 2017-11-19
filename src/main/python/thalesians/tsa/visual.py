import datetime as dt

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import thalesians.tsa.conversions as conv
import thalesians.tsa.pandasutils as pdutils

def bar_chart_from_dict(d, fig=None, ax=None, title=None):
    if fig is None: fig = plt.figure()
    if ax is None: ax = fig.add_subplot(111)
    ax.bar(range(len(d)), d.values, align='center')
    ax.set_xticks(range(len(d)))
    ax.set_xticklabels(d.keys(), rotation=90)
    if title is not None: ax.set_title(title)
    
def visualise_categorical_series(ser, fig=None, ax=None):
    vc = ser.value_counts()
    bar_chart_from_dict(vc, fig, ax, ser.name)
    
def visualise_categorical_iterable(it, name=None, fig=None, ax=None):
    visualise_categorical_series(pd.Series(it, name=name), fig, ax)
    
def visualise_date_series(ser, fig=None, ax=None, **kwargs):
    if fig is None: fig = plt.figure()
    if ax is None: ax = fig.add_subplot(111)
    year = lambda x: x.date().year if type(x) == dt.datetime else (x.year if x is not None else None)
    month = lambda x: x.date().month if type(x) == dt.datetime else (x.month if x is not None else None)
    ser.groupby([ser.apply(year), ser.apply(month)]).count().plot(ax=ax, kind='bar', **kwargs)
    ax.set_xlabel(ser.name)
    ax.set_ylabel('frequency')

def visualise_date_iterable(it, name=None, fig=None, ax=None, **kwargs):
    visualise_date_series(pd.Series(it, name=name), fig, ax, **kwargs)
    
def visualise_time_series(ser, fig=None, ax=None, **kwargs):
    if fig is None: fig = plt.figure()
    if ax is None: ax = fig.add_subplot(111)
    hour = lambda x: x.time().hour if type(x) == dt.datetime else (x.hour if x is not None else None)
    ser.groupby([ser.apply(hour)]).count().plot(ax=ax, kind='bar', **kwargs)
    ax.set_xlabel(ser.name)
    ax.set_ylabel('frequency')

def visualise_time_iterable(it, name=None, fig=None, ax=None, **kwargs):
    visualise_time_series(pd.Series(it, name=name), fig, ax, **kwargs)
    
def visualise_float_series(ser, fig=None, ax=None, **kwargs):
    if fig is None: fig = plt.figure()
    if ax is None: ax = fig.add_subplot(111)
    if 'alpha' not in kwargs: kwargs['alpha'] = .75
    ser = ser.dropna()
    ax.hist(ser, **kwargs)
    mean = np.mean(ser)
    sd = np.sqrt(np.var(ser))
    median = np.median(ser)
    ax.axvline(mean, color='r', label='mean')
    ax.axvline(mean + sd, color='r', linestyle='dashed', label='mean +/- sd')
    ax.axvline(mean - sd, color='r', linestyle='dashed')
    ax.axvline(median, color='g', label='median')
    ax.set_xlabel(ser.name)
    ax.legend(loc='best', fancybox=True, framealpha=.5)
    
def visualise_df_categorical_columns(df, categorical_columns=None):
    if categorical_columns is None:
        categorical_columns = pdutils.detect_df_categorical_columns(df)
    for c in categorical_columns:
        visualise_categorical_series(df[c])

def visualise_df_int_columns(df, int_columns=None):
    if int_columns is None:    
        int_columns = pdutils.get_df_int_columns(df)
    for c in int_columns:
        visualise_float_series(df[c])
        
def visualise_df_float_columns(df, float_columns=None):
    if float_columns is None:    
        float_columns = pdutils.get_df_float_columns(df)
    for c in float_columns:
        visualise_float_series(df[c])
        
def visualise_df_date_columns(df, date_columns=None):
    if date_columns is None:    
        date_columns = pdutils.get_df_date_columns(df)
    for c in date_columns:
        visualise_date_series(df[c])
        
def visualise_df_time_columns(df, time_columns=None):
    if time_columns is None:
        time_columns = pdutils.get_df_time_columns(df)
    for c in time_columns:
        visualise_time_series(df[c])
        
def visualise_df_datetime_columns(df, datetime_columns=None):
    if datetime_columns is None:
        datetime_columns = pdutils.get_df_datetime_columns(df)
    for c in datetime_columns:
        visualise_date_iterable([conv.to_python_datetime(x).date() for x in df[c].values], name='%s.date' % c)
        visualise_time_iterable([conv.to_python_datetime(x).time() for x in df[c].values], name='%s.time' % c)

def visualise_df(df):
    visualise_df_categorical_columns(df)
    visualise_df_int_columns(df)
    visualise_df_float_columns(df)
    visualise_df_date_columns(df)
    visualise_df_time_columns(df)
    visualise_df_datetime_columns(df)
    