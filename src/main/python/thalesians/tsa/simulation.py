import datetime as dt

import numpy as np
import pandas as pd

import thalesians.tsa.checks as checks
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.processes as proc
import thalesians.tsa.random as rnd
import thalesians.tsa.utils as utils

def xtimes(start, stop=None, step=None):
    checks.checknotnone(start)
    
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

    stepfunc = step if checks.iscallable(step) else lambda x: step
    s = stepfunc(start)
    checks.check(utils.sign(s) != 0, 'Step must be positive or negative, not zero')
    
    if stop is None:
        while True:
            yield resultwrap(start)
            start += s
            s = stepfunc(start)
    else:
        while utils.sign(start - stop) == -utils.sign(s):
            yield resultwrap(start)
            start += s
            s = stepfunc(start)

def times(start, stop=None, step=None):
    return list(xtimes(start, stop, step))

class EulerMaruyama(object):
    def __init__(self, process, initialvalue=None, times=None, variates=None, timeunit=dt.timedelta(days=1), flatten=False):
        checks.checkinstance(process, proc.ItoProcess)
        self.__process = process
        self.__value = npu.tondim2(initialvalue, ndim1tocol=True, copy=True) if initialvalue is not None else npu.colof(process.processdim, 0.)
        self.__times = times if times is not None else xtimes(0., None, 1.)
        self.__variates = variates if variates is not None else rnd.multivatiate_normals(ndim=process.noisedim)
        self.__time = None
        self.__timeunit = timeunit
        self.__flatten = flatten

    def __next__(self):
        if self.__time is None:
            self.__time = next(self.__times)
        else:
            newtime = next(self.__times)
            timedelta = newtime - self.__time
            if isinstance(timedelta, dt.timedelta):
                timedelta = timedelta.total_seconds() / self.__timeunit.total_seconds()
            npu.colof(self.__process.noisedim, 0.)
            variatedelta = np.sqrt(timedelta) * npu.tondim2(next(self.__variates), ndim1tocol=True, copy=False)
            self.__value += self.__process.drift(self.__time, self.__value) * timedelta + self.__process.diffusion(self.__time, self.__value).dot(variatedelta)
            self.__time = newtime
        v = np.copy(self.__value)
        if self.__flatten: v = v.flatten()
        return self.__time, v
    
    def __iter__(self):
        return self

def run(sim, nstep=None, lasttime=None):
    checks.checkatmostonenotnone(nstep, lasttime)
    ts, vs = [], []
    if nstep is not None:
        for i in range(nstep):
            try:
                t, v = next(sim)
            except StopIteration: break
            ts.append(t)
            vs.append(v.flatten())
    elif lasttime is not None:
        while True:
            try:
                t, v = next(sim)
            except StopIteration: break
            ts.append(t)
            vs.append(v.flatten())
            if t >= lasttime: break
    else:
        for t, v in sim:
            ts.append(t)
            vs.append(v.flatten())
    return pd.DataFrame(data=vs, index=ts)
