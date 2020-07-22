import collections as col
import copy
import uuid

import thalesians.tsa.checks as checks
import thalesians.tsa.evaluation as evaluation
from thalesians.tsa.strings import ToStringHelper
import thalesians.tsa.utils as utils

def _param_names_and_values_to_args_and_kwargs(param_names, param_values):
    args = []
    kwargs = col.OrderedDict()
    for pn, pv in zip(param_names, param_values):
        if checks.is_int(pn):
            utils.pad_on_right(args, pn + 1, padding=None, in_place=True)
            args[pn] = pv
        else:
            kwargs[pn] = pv
    return args, kwargs

def _evaluate(func, param_ranges, param_names, param_value_indices,
        optimization_id, work_id, call_count, repeat_count, evaluator,
        pype):
    param_values = [param_ranges[pn][param_value_indices[i]] for i, pn in enumerate(param_names)]
    args, kwargs = _param_names_and_values_to_args_and_kwargs(param_names, param_values)
    info = {
            'param_ranges': param_ranges,
            'param_names': param_names,
            'param_value_indices': param_value_indices,
            'optimization_id': optimization_id,
            'work_id': work_id
        }
    status = evaluation.evaluate(func, args, kwargs,
            work_id=work_id, call_count=call_count, repeat_count=repeat_count, evaluator=evaluator,
            info=info)
    if pype is not None: pype.send(status)
    return status

class GridSearchResult(object):
    def __init__(self, param_ranges, optimization_id, evaluation_statuses):
        self._param_ranges = param_ranges
        self._optimization_id = optimization_id
        self._evaluation_statuses = evaluation_statuses

    @property
    def param_ranges(self):
        return self._param_ranges

    @property
    def optimization_id(self):
        return self._optimization_id

    @property
    def evaluation_statuses(self):
        return self._evaluation_statuses

    def to_string_helper(self):
        return ToStringHelper(self) \
                    .add('param_ranges', self._param_ranges) \
                    .add('optimization_id', self._optimization_id) \
                    .add('evaluation_statuses', self._evaluation_statuses)
    
    def __str__(self):
        return self.to_string_helper().to_string()

    def __repr__(self):
        return str(self)

def grid_search(func, param_ranges,
        optimization_id=None, work_id=None, call_count=1, repeat_count=1, evaluator=None,
        pype=None):
    param_ranges = copy.copy(param_ranges)
    if optimization_id is None: optimization_id = uuid.uuid4().hex
    if work_id is None: work_id = optimization_id
    if not checks.is_callable(work_id):
        last_index = 0
        def work_id_callable():
            nonlocal last_index
            last_index += 1
            return last_index
        work_id = work_id_callable

    param_names = list(param_ranges)
    param_value_indices = [0] * len(param_names)

    evaluation_statuses = []

    status = _evaluate(func, param_ranges, param_names, copy.copy(param_value_indices),
            optimization_id=optimization_id, work_id=work_id(),
            call_count=call_count, repeat_count=repeat_count,
            evaluator=evaluator,
            pype=pype)
    evaluation_statuses.append(status)

    while True:
        altered_param = False
        for param_index in range(len(param_names) - 1, -1, -1):
            if param_value_indices[param_index] < len(param_ranges[param_names[param_index]]) - 1:
                param_value_indices[param_index] += 1
                altered_param = True
                for param_index1 in range(param_index + 1, len(param_names)):
                    param_value_indices[param_index1] = 0

                status = _evaluate(func, param_ranges, param_names, copy.copy(param_value_indices),
                        optimization_id=optimization_id, work_id=work_id(),
                        call_count=call_count, repeat_count=repeat_count,
                        evaluator=evaluator,
                        pype=pype)
                evaluation_statuses.append(status)

                break
        if not altered_param: break

    return GridSearchResult(
            param_ranges=param_ranges,
            optimization_id=optimization_id,
            evaluation_statuses=evaluation_statuses)
