import datetime as dt
import os
import socket
import threading
import time
import timeit
import uuid

from thalesians.tsa.strings import ToStringHelper

class Work(object):
    class Result(object):
        def __init__(self, func, args, kwargs, work_id, call_count, repeat_count, info,
                evaluation_id, result, exception, start_datetime, seconds_per_call, hostname, pid, thread_id):
            self._func = func
            self._args = args
            self._kwargs = kwargs
            self._work_id = work_id
            self._call_count = call_count
            self._repeat_count = repeat_count
            self._info = info
            self._evaluation_id = evaluation_id
            self._result = result
            self._exception = exception
            self._start_datetime = start_datetime
            self._seconds_per_call = seconds_per_call
            self._hostname = hostname
            self._pid = pid
            self._thread_id = thread_id
            self._to_string_helper_Work_Result = None
            self._str_Work_Result = None

        @property
        def work_id(self):
            return self._work_id

        @property
        def func(self):
            return self._func

        @property
        def args(self):
            return self._args

        @property
        def kwargs(self):
            return self._kwargs

        @property
        def call_count(self):
            return self._call_count

        @property
        def repeat_count(self):
            return self._repeat_count

        @property
        def info(self):
            return self._info

        @property
        def evaluation_id(self):
            return self._evaluation_id

        @property
        def result(self):
            return self._result

        @property
        def exception(self):
            return self._exception

        @property
        def start_datetime(self):
            return self._start_datetime

        @property
        def seconds_per_call(self):
            return self._seconds_per_call

        @property
        def hostname(self):
            return self._hostname

        @property
        def pid(self):
            return self._pid

        @property
        def thread_id(self):
            return self._thread_id

        def to_string_helper(self):
            if self._to_string_helper_Work_Result is None:
                self._to_string_helper_Work_Result = ToStringHelper(self) \
                        .add('work_id', self._work_id) \
                        .add('func', self._func) \
                        .add('args', self._args) \
                        .add('kwargs', self._kwargs) \
                        .add('call_count', self._call_count) \
                        .add('repeat_count', self._repeat_count) \
                        .add('info', self._info) \
                        .add('evaluation_id', self._evaluation_id) \
                        .add('result', self._result) \
                        .add('exception', self._exception) \
                        .add('start_datetime', self._start_datetime) \
                        .add('seconds_per_call', self._seconds_per_call) \
                        .add('hostname', self._hostname) \
                        .add('pid', self._pid) \
                        .add('thread_id', self._pid)
            return self._to_string_helper_Work_Result
        
        def __str__(self):
            if self._str_Work_Result is None: self._str_Work_Result = self.to_string_helper().to_string()
            return self._str_Work_Result 

        def __repr__(self):
            return str(self)

    def __init__(self, func, args=[], kwargs={}, work_id=None, call_count=1, repeat_count=1, info=None):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        if work_id is None: work_id = uuid.uuid4().hex
        self._work_id = work_id
        self._call_count = call_count
        self._repeat_count = repeat_count
        self._info = info
        self._to_string_helper_Work = None
        self._str_Work = None

    def __call__(self, *args, **kwargs):
        evaluation_id = uuid.uuid4().hex
        
        result = None
        exception = None

        def wrapped():
            nonlocal result
            nonlocal exception
            try:
                result = self._func(*self._args, **self._kwargs)
            except Exception as e:
                exception = e

        hostname = socket.gethostname()
        pid = os.getpid()
        thread_id = threading.get_ident()
        start_datetime = dt.datetime.now()
        seconds = timeit.repeat(wrapped, repeat=self._repeat_count, number=self._call_count)
        seconds_per_call = [s / self._call_count for s in seconds]

        return Work.Result(self._func, self._args, self._kwargs, self._work_id, self._call_count, self._repeat_count, self._info,
                evaluation_id, result, exception, start_datetime, seconds_per_call, hostname, pid, thread_id)

    @property
    def work_id(self):
        return self._work_id

    @property
    def func(self):
        return self._func

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def call_count(self):
        return self._call_count

    @property
    def repeat_count(self):
        return self._repeat_count

    @property
    def info(self):
        return self._info

    def to_string_helper(self):
        if self._to_string_helper_Work is None:
            self._to_string_helper_Work = ToStringHelper(self) \
                    .add('work_id', self._work_id) \
                    .add('func', self._func) \
                    .add('args', self._args) \
                    .add('kwargs', self._kwargs) \
                    .add('call_count', self._call_count) \
                    .add('repeat_count', self._repeat_count) \
                    .add('info', self._info)
        return self._to_string_helper_Work
    
    def __str__(self):
        if self._str_Work is None: self._str_Work = self.to_string_helper().to_string()
        return self._str_Work 

    def __repr__(self):
        return str(self)

class CurrentThreadEvaluator(object):
    class Status(object):
        def __init__(self, work, result):
            self._work = work
            self._result = result

        def add_callback(self, callback):
            # Call callback immediately:
            callback(self)

        @property
        def ready(self):
            return True

        @property
        def work(self):
            return self._work

        @property
        def result(self):
            return self._result

        def __str__(self):
            return ToStringHelper(self) \
                    .add('ready', self.ready) \
                    .add('work', self.work) \
                    .add('result', self.result) \
                    .to_string()

        def __repr__(self):
            return str(self)

    def __init__(self):
        pass

    def evaluate(self, work):
        result = work()
        return __class__.Status(work, result)

class MultiprocessingEvaluator(object):
    class Status(object):
        def __init__(self, work, apply_result):
            self._work = work
            self._apply_result = apply_result
            self._callbacks = []
            def wait_to_call_callbacks():
                while not self._apply_result.ready():
                    time.sleep(0.1)
                for c in self._callbacks: c(self)
            t = threading.Thread(target=wait_to_call_callbacks)
            t.start()            

        def add_callback(self, callback):
            self._callbacks.append(callback)
            
        def _callback(self):
            for c in self._callbacks: c(self)

        @property
        def ready(self):
            return self._apply_result.ready()

        @property
        def work(self):
            return self._work

        @property
        def result(self):
            return self._apply_result.get() if self.ready else None

        def __str__(self):
            return ToStringHelper(self) \
                    .add('ready', self.ready) \
                    .add('work', self.work) \
                    .add('result', self.result) \
                    .to_string()

        def __repr__(self):
            return str(self)

    def __init__(self, pool=None):
        import multiprocessing as mp
        if pool is None: pool = mp.Pool(5)
        self._pool = pool

    def evaluate(self, work):
        result = self._pool.apply_async(work, [None])
        return __class__.Status(work, result)

class IPyParallelEvaluator(object):
    class Status(object):
        def __init__(self, work, async_result):
            self._work = work
            self._async_result = async_result

        def add_callback(self, callback):
            def wrapped(async_result):
                callback(self)
            self._async_result.add_done_callback(wrapped)

        @property
        def ready(self):
            return self._async_result.ready()

        @property
        def work(self):
            return self._work

        @property
        def result(self):
            return self._async_result.get()[0] if self.ready else None

        def __str__(self):
            return ToStringHelper(self) \
                    .add('ready', self.ready) \
                    .add('work', self.work) \
                    .add('result', self.result) \
                    .to_string()

        def __repr__(self):
            return str(self)

    def __init__(self, client=None, profile=None):
        import ipyparallel as ipp
        if client is None:
            if profile is None: profile = 'mycluster'
            client = ipp.Client(profile=profile)
        self._client = client
        self._client[:].use_cloudpickle()
        self._view = client.load_balanced_view()

    def evaluate(self, work):
        result = self._view.map(work, [None])
        return __class__.Status(work, result)

def evaluate(func, args=[], kwargs={}, work_id=None, call_count=1, repeat_count=1, info=None, evaluator=None):
    if evaluator is None: evaluator = CurrentThreadEvaluator()
    work = Work(func=func, args=args, kwargs=kwargs,
            work_id=work_id, call_count=call_count, repeat_count=repeat_count, info=info)
    return evaluator.evaluate(work)
