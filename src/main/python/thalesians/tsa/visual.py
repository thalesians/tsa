import datetime as dt

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def bar_chart_from_dict(d, fig=None, ax=None, title=None):
    if fig is None: fig = plt.figure()
    if ax is None: ax = fig.add_subplot(111)
    ax.bar(range(len(d)), d.values(), align='center')
    ax.set_xticks(range(len(d)))
    ax.set_xticklabels(d.keys(), rotation=90)
    if title is not None: ax.set_title(title)
    
def visualise_categorical_series(ser, fig=None, ax=None):
    vc = ser.value_counts()
    bar_chart_from_dict(vc, fig, ax, ser.name)
    
def visualise_categorical_iterable(it, fig=None, ax=None):
    visualise_categorical_series(pd.Series(it), fig, ax)
    
def visualise_date_series(ser, fig=None, ax=None, **kwargs):
    if fig is None: fig = plt.figure()
    if ax is None: ax = fig.add_subplot(111)
    year = lambda x: x.date().year if type(x) == dt.datetime else (x.year if x is not None else None)
    month = lambda x: x.date().month if type(x) == dt.datetime else (x.month if x is not None else None)
    ser.groupby([ser.apply(year), ser.apply(month)]).count().plot(ax=ax, kind='bar', **kwargs)
    ax.set_xlabel(ser.name)
    ax.set_ylabel('frequency')

def visualise_time_series(ser, fig=None, ax=None, **kwargs):
    if fig is None: fig = plt.figure()
    if ax is None: ax = fig.add_subplot(111)
    hour = lambda x: x.time().hour if type(x) == dt.datetime else (x.hour if x is not None else None)
    ser.groupby([ser.apply(hour)]).count().plot(ax=ax, kind='bar', **kwargs)
    ax.set_xlabel(ser.name)
    ax.set_ylabel('frequency')

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
    ax.axvline(mean + sd, color='r', linestyle='dashed')
    ax.axvline(median, color='g', label='median')
    ax.add_xlabel(ser.name)
    ax.add_legend(loc='best', fancybox=True, framealpha=.5)
    