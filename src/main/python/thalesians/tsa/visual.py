import datetime as dt
import time

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import thalesians.tsa.checks as checks
import thalesians.tsa.conversions as conv
import thalesians.tsa.pandasutils as pdutils
import thalesians.tsa.utils as utils

def get_figure_and_axes(fig, ax):
    if checks.is_callable(fig): fig = fig()
    elif fig is None: fig = plt.figure()
    
    if checks.is_callable(ax): ax = ax(fig)
    elif ax is None: ax = fig.add_subplot(111)
    
    return fig, ax

default_xticklabels_rotation = 45

def rotate_xticklabels(ax, rotation=default_xticklabels_rotation):
    for label in ax.get_xticklabels():
        label.set_rotation(rotation)
        
def bar_chart_from_dict(d, fig=None, ax=None, title=None):
    fig, ax = get_figure_and_axes(fig, ax)
    ax.bar(range(len(d)), d.values, align='center')
    ax.set_xticks(range(len(d)))
    ax.set_xticklabels(d.keys(), rotation=default_xticklabels_rotation)
    if title is not None: ax.set_title(title)
    return fig, ax
    
def visualise_categorical_series(ser, fig=None, ax=None):
    vc = ser.value_counts()
    bar_chart_from_dict(vc, fig, ax, ser.name)
    
def visualise_categorical_iterable(it, name=None, fig=None, ax=None):
    visualise_categorical_series(pd.Series(it, name=name), fig, ax)
    
def visualise_date_series(ser, fig=None, ax=None, **kwargs):
    fig, ax = get_figure_and_axes(fig, ax)
    year = lambda x: x.date().year if type(x) == dt.datetime else (x.year if x is not None else None)
    month = lambda x: x.date().month if type(x) == dt.datetime else (x.month if x is not None else None)
    ser.groupby([ser.apply(year), ser.apply(month)]).count().plot(ax=ax, kind='bar', **kwargs)
    ax.set_xlabel(ser.name)
    ax.set_ylabel('frequency')
    return fig, ax

def visualise_date_iterable(it, name=None, fig=None, ax=None, **kwargs):
    visualise_date_series(pd.Series(it, name=name), fig, ax, **kwargs)
    
def visualise_time_series(ser, fig=None, ax=None, **kwargs):
    fig, ax = get_figure_and_axes(fig, ax)
    hour = lambda x: x.time().hour if type(x) == dt.datetime else (x.hour if x is not None else None)
    ser.groupby([ser.apply(hour)]).count().plot(ax=ax, kind='bar', **kwargs)
    ax.set_xlabel(ser.name)
    ax.set_ylabel('frequency')
    return fig, ax

def visualise_time_iterable(it, name=None, fig=None, ax=None, **kwargs):
    visualise_time_series(pd.Series(it, name=name), fig, ax, **kwargs)
    
def visualise_float_series(ser, fig=None, ax=None, **kwargs):
    fig, ax = get_figure_and_axes(fig, ax)
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
    return fig, ax
    
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

def visualise_sized_point_series(time_ser, value_ser, size_ser, scaling=None, fig=None, ax=None, **kwargs):
    if 'alpha' not in kwargs: kwargs['alpha'] = .3
    
    if scaling is None: scaling = lambda x: x
    elif not checks.is_callable(scaling): scaling = lambda x: scaling * x

    if time_ser is None: time_ser = value_ser.index
    time_ser, value_ser, size_ser = [conv.to_plottable_value(x) for x in (time_ser, value_ser, size_ser)]
    value_ser = conv.to_plottable_value(value_ser)
    size_ser = conv.to_plottable_value(size_ser)

    fig, ax = get_figure_and_axes(fig, ax)
    if len(value_ser) > 0:
        ax.scatter(
            time_ser,
            value_ser,
            s=[scaling(x) for x in size_ser],
            **kwargs)
        rotate_xticklabels(ax)

    return fig, ax

def visualise_df_sized_point_series(df, time_column, value_column, size_column, scaling=None, fig=None, ax=None, **kwargs):
    return visualise_sized_point_series(df[time_column], df[value_column], df[size_column], scaling, fig, ax, **kwargs)

class LivePlot(object):
    _figure_refresh_times = {}
    
    def __init__(self, fig=None, ax=None, keep_last_points=None, min_refresh_interval=None,
                 pad_left=None, pad_right=None, pad_bottom=None, pad_top=None,
                 update_xlim=True, update_ylim=True,
                 never_shrink_xlim_left=False, never_shrink_xlim_right=False,
                 never_shrink_ylim_bottom=False, never_shrink_ylim_top=False):
        self._fig, self._ax = get_figure_and_axes(fig, ax)
        self._keep_last_points = keep_last_points
        self._xs, self._ys = [], []
        self._minx, self._maxx, self._miny, self._maxy = [], [], [], []
        if checks.is_timedelta(min_refresh_interval): min_refresh_interval = min_refresh_interval.total_seconds()
        self._min_refresh_interval = min_refresh_interval
        self._pad_left = pad_left
        self._pad_right = pad_right
        self._pad_bottom = pad_bottom
        self._pad_top = pad_top
        self._update_xlim = update_xlim
        self._update_ylim = update_ylim
        self._never_shrink_xlim_left = never_shrink_xlim_left
        self._never_shrink_xlim_right = never_shrink_xlim_right
        self._never_shrink_ylim_bottom = never_shrink_ylim_bottom
        self._never_shrink_ylim_top = never_shrink_ylim_top
        
    @property
    def fig(self):
        return self._fig
    
    @property
    def ax(self):
        return self._ax
        
    def refresh(self, force=False):
        current_time = time.monotonic()        
        if (not force) and self._min_refresh_interval is not None:
            if id(self._fig) in LivePlot._figure_refresh_times:
                last_refresh_time = LivePlot._figure_refresh_times[id(self._fig)]
                if current_time - last_refresh_time < self._min_refresh_interval: return        
        self._fig.canvas.draw()
        LivePlot._figure_refresh_times[id(self._fig)] = current_time
        
    def _append(self, x, y, plot_index):
        for col in [self._xs, self._ys]:
            utils.pad_on_right(col, plot_index + 1, padding=lambda: [], in_place=True)
        for col in [self._minx, self._maxx, self._miny, self._maxy]:
            utils.pad_on_right(col, plot_index + 1, padding=None, in_place=True)
        if self._keep_last_points is not None and len(self._xs[plot_index]) >= self._keep_last_points:
            utils.trim_on_left(self._xs[plot_index], self._keep_last_points - 1, in_place=True)
            utils.trim_on_left(self._ys[plot_index], self._keep_last_points - 1, in_place=True)
            self._minx[plot_index] = np.min(self._xs[plot_index])
            self._maxx[plot_index] = np.max(self._xs[plot_index])
            self._miny[plot_index] = np.min(self._ys[plot_index])
            self._maxy[plot_index] = np.max(self._ys[plot_index])
        self._xs[plot_index].append(x)
        self._ys[plot_index].append(y)
        self._minx[plot_index] = x if self._minx[plot_index] is None else np.min([x, self._minx[plot_index]])
        self._maxx[plot_index] = x if self._maxx[plot_index] is None else np.max([x, self._maxx[plot_index]])
        self._miny[plot_index] = y if self._miny[plot_index] is None else np.min([y, self._miny[plot_index]])
        self._maxy[plot_index] = y if self._maxy[plot_index] is None else np.max([y, self._maxy[plot_index]])
        self._ax.lines[plot_index].set_data(self._xs[plot_index], self._ys[plot_index])
    
    def _fix_lim_if_broken(self, lim):
        if lim[0] == lim[1]:
            if lim[0] == 0: lim[0] = -1; lim[1] = 1
            else: lim[0] -= 0.1 * lim[0]; lim[1] += 0.1 * lim[1]
            
    def _update_lim(self):
        if self._update_xlim:
            minxs = [x for x in self._minx if (x is not None and not np.isnan(x))]
            maxxs = [x for x in self._maxx if (x is not None and not np.isnan(x))]
            new_xlim = [
                np.min(minxs) if len(minxs) > 0 else np.nan,
                np.max(maxxs) if len(maxxs) > 0 else np.nan
                ]
            if self._pad_left is not None: new_xlim[0] -= self._pad_left
            if self._pad_right is not None: new_xlim[1] += self._pad_right
            if self._never_shrink_xlim_left: new_xlim[0] = np.min([new_xlim[0], self._ax.get_xlim()[0]])
            if self._never_shrink_xlim_right: new_xlim[1] = np.max([new_xlim[1], self._ax.get_xlim()[1]])
            self._fix_lim_if_broken(new_xlim)
            self._ax.set_xlim(new_xlim)

        if self._update_ylim:
            minys = [y for y in self._miny if (y is not None and not np.isnan(y))]
            maxys = [y for y in self._maxy if (y is not None and not np.isnan(y))]
            new_ylim = [
                np.min(minys) if len(minys) > 0 else np.nan,
                np.max(maxys) if len(maxys) > 0 else np.nan
                ]
            if self._pad_bottom is not None: new_ylim[0] -= self._pad_bottom
            if self._pad_top is not None: new_ylim[1] += self._pad_top
            if self._never_shrink_ylim_bottom: new_ylim[0] = np.min([new_ylim[0], self._ax.get_ylim()[0]])
            if self._never_shrink_ylim_top: new_ylim[1] = np.max([new_ylim[1], self._ax.get_ylim()[1]])
            self._fix_lim_if_broken(new_ylim)
            self._ax.set_ylim(new_ylim)

    def append(self, x, y, plot_index=None, refresh=True):
        x = np.array(x)
        y = np.array(y)

        if plot_index is not None:
            self._append(x, y, plot_index)
        else:
            for i in range(len(self._ax.lines)):
                self._append(x[i] if np.size(x) > 1 else x, y[i] if np.size(y) > 1 else y, i)
                
        self._update_lim()        
        
        if refresh: self.refresh()
        