import datetime as dt

import numpy as np
import pandas as pd

import thalesians.tsa.checks as checks
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.processes as proc
import thalesians.tsa.randomness as rnd

def xtimes(start, stop=None, step=None):
    checks.check_not_none(start)
    
    if step is None:
        if isinstance(start, (dt.date, dt.time, dt.datetime)) or isinstance(stop, (dt.date, dt.time, dt.datetime)):
            step = dt.timedelta(days=1)
        elif isinstance(start, float) or isinstance(stop, float):
            step = 1.
        else:
            step = 1

    resultwrap = lambda x: x

    if isinstance(start, dt.time):
        start = dt.datetime.combine(dt.datetime(1,1,1,0,0,0), start)
        resultwrap = lambda x: x.time()
    if isinstance(stop, dt.time):
        stop = dt.datetime.combine(dt.datetime(1,1,1,0,0,0), stop) if stop is not None else None
        resultwrap = lambda x: x.time()

    stepfunc = step if checks.is_callable(step) else lambda x: step
    s = stepfunc(start)
    checks.check(npu.sign(s) != 0, 'Step must be positive or negative, not zero')
    
    if stop is None:
        while True:
            yield resultwrap(start)
            start += s
            s = stepfunc(start)
    else:
        while npu.sign(start - stop) == -npu.sign(s):
            yield resultwrap(start)
            start += s
            s = stepfunc(start)

def times(start, stop=None, step=None):
    return list(xtimes(start, stop, step))

class EulerMaruyama(object):
    def __init__(self, process, initial_value=None, times=None, variates=None, time_unit=dt.timedelta(days=1), flatten=False):
        checks.check_instance(process, proc.ItoProcess)
        self.__process = process
        self.__value = npu.to_ndim_2(initial_value, ndim_1_to_col=True, copy=True) if initial_value is not None else npu.col_of(process.process_dim, 0.)
        self.__times = iter(times) if times is not None else xtimes(0., None, 1.)
        self.__variates = variates if variates is not None else rnd.multivariate_normals(ndim=process.noise_dim)
        self._time = None
        self._time_unit = time_unit
        self.__flatten = flatten

    def __next__(self):
        if self._time is None:
            self._time = next(self.__times)
        else:
            newtime = next(self.__times)
            time_delta = newtime - self._time
            if isinstance(time_delta, dt.timedelta):
                time_delta = time_delta.total_seconds() / self._time_unit.total_seconds()
            npu.col_of(self.__process.noise_dim, 0.)
            variate_delta = np.sqrt(time_delta) * npu.to_ndim_2(next(self.__variates), ndim_1_to_col=True, copy=False)
            drift = npu.to_ndim_2(self.__process.drift(self._time, self.__value), ndim_1_to_col=True, copy=False)
            diffusion = npu.to_ndim_2(self.__process.diffusion(self._time, self.__value), ndim_1_to_col=True, copy=False)
            self.__value += drift * time_delta + diffusion.dot(variate_delta)
            self._time = newtime
        v = np.copy(self.__value)
        if self.__flatten: v = v.flatten()
        return self._time, v
    
    def __iter__(self):
        return self

def run(sim, nstep=None, last_time=None):
    checks.check_at_most_one_not_none(nstep, last_time)
    ts, vs = [], []
    if nstep is not None:
        for _ in range(nstep):
            try:
                t, v = next(sim)
            except StopIteration: break
            ts.append(t)
            vs.append(v.flatten())
    elif last_time is not None:
        while True:
            try:
                t, v = next(sim)
            except StopIteration: break
            ts.append(t)
            vs.append(v.flatten())
            if t >= last_time: break
    else:
        for t, v in sim:
            ts.append(t)
            vs.append(v.flatten())
    return pd.DataFrame(data=vs, index=ts)
