import itertools
import time
import warnings

import numpy as np
import matplotlib.colors
import matplotlib.pyplot as plt

import thalesians.tsa.checks as checks
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.utils as utils

def _aggregate(aggregate_func, data, empty_aggregate):
    if empty_aggregate != 'none':
        return npu.apply(lambda x: empty_aggregate if len(x) == 0 else aggregate_func(x), data)
    else:
        return npu.apply(aggregate_func, data)

def visualize_grid_search(grid_search_result,
        aggregate_func=np.nanmean, empty_aggregate='none',
        fig=None, title=None,
        refresh_until_ready=False):
    if fig is None: fig = plt.figure()

    if title is None: title = grid_search_result.optimization_id
    fig.suptitle(title)

    param_names = list(grid_search_result.param_ranges.keys())

    subplots = {}
    heatmaps = {}
    datas = {}

    for i1 in range(len(param_names)):
        param_name1 = param_names[i1]
        param_values1 = grid_search_result.param_ranges[param_name1]
        for i2 in range(i1):
            param_name2 = param_names[i2]
            param_values2 = grid_search_result.param_ranges[param_name2]
            data = np.empty((len(param_values1), len(param_values2)), dtype=object)
            for i in range(np.size(data)): data.flat[i] = []
            datas[(i1, i2)] = data

            ax = fig.add_subplot(len(param_names) - 1, len(param_names) - 1, (i1 - 1) * (len(param_names) - 1) + i2 + 1)
            subplots[(i1, i2)] = ax
            
            initial_data = _aggregate(aggregate_func, datas[(i1, i2)], empty_aggregate)

            heatmaps[(i1, i2)] = ax.matshow(npu.apply(aggregate_func, initial_data), cmap='coolwarm')

            if i2 == i1 - 1:
                ax.set_xticklabels([np.nan] + [0. if x == 1e-06 else x for x in param_values2], fontsize=6, rotation='vertical', verticalalignment='bottom')
                ax.xaxis.set_ticks_position('top')
                ax.set_yticklabels([np.nan] + [0. if x == 1e-06 else x for x in param_values1], fontsize=6)
                ax.yaxis.set_ticks_position('right')
            else:
                ax.set_xticks([])
                ax.set_yticks([])
            if i1 == len(param_names) - 1: ax.set_xlabel(param_name2)
            if i2 == 0: ax.set_ylabel(param_name1)

    while True:
        all_ready = True
        for status in grid_search_result.evaluation_statuses:
            if not status.ready: all_ready = False
            else:
                checks.check(utils.sequence_eq(param_names, status.work.info['param_names']))
                param_value_index_combinations = itertools.combinations(range(len(param_names)), 2)
                param_value_index_combinations = [(i2, i1) for (i1, i2) in param_value_index_combinations if i1 != i2]
                for i1, i2 in param_value_index_combinations:
                    param_value_index1 = status.work.info['param_value_indices'][i1]
                    param_value_index2 = status.work.info['param_value_indices'][i2]
                    if status.result.exception is not None:
                        result = np.nan
                    elif status.result.result is None:
                        result = np.nan
                    else:
                        result = status.result.result
                    datas[(i1, i2)][param_value_index1, param_value_index2].append(result)
        for i1 in range(len(param_names)):
            for i2 in range(i1):
                new_data = _aggregate(aggregate_func, datas[(i1, i2)], empty_aggregate)
                heatmaps[(i1, i2)].set_data(new_data)
                heatmaps[(i1, i2)].autoscale()
        if (not refresh_until_ready) or all_ready: break
        else:
            fig.canvas.draw()
            time.sleep(1)

    return fig
