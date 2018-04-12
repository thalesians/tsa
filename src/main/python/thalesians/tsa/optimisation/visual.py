import itertools
import warnings

import numpy as np
import matplotlib.colors
import matplotlib.pyplot as plt

import thalesians.tsa.checks as checks
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.utils as utils

def visualise_grid_search(grid_search_output, aggregate_function=np.nanmean, fig=None, title=None):
    if fig is None: fig = plt.figure()

    if title is None: title = grid_search_output.optimisation_id

    param_names = list(grid_search_output.param_ranges.keys())

    subplots = {}
    heatmaps = {}
    datas = {}

    for i1 in range(len(param_names)):
        param_name1 = param_names[i1]
        param_values1 = grid_search_output.param_ranges[param_name1]
        for i2 in range(i1):
            param_name2 = param_names[i2]
            param_values2 = grid_search_output.param_ranges[param_name2]
            data = np.empty((len(param_values1), len(param_values2)), dtype=object)
            for i in range(np.size(data)): data.flat[i] = []
            datas[(i1, i2)] = data

            ax = fig.add_subplot(len(param_names) - 1, len(param_names) - 1, (i1 - 1) * (len(param_names) - 1) + i2 + 1)
            subplots[(i1, i2)] = ax
            initial_data = np.empty((len(param_values1), len(param_values2)))
            heatmaps[(i1, i2)] = ax.matshow(npu.apply(np.nanmean, initial_data), cmap='coolwarm')

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

    for status in grid_search_output.evaluation_statuses:
        if status.ready:
            checks.check(utils.sequence_eq(param_names, status.work.info['param_names']))
            param_value_index_combinations = itertools.combinations(range(len(param_names)), 2)
            param_value_index_combinations = [(i2, i1) for (i1, i2) in param_value_index_combinations if i1 != i2]
            for i1, i2 in param_value_index_combinations:
                param_value_index1 = status.work.info['param_value_indices'][i1]
                param_value_index2 = status.work.info['param_value_indices'][i2]
                datas[(i1, i2)][param_value_index1, param_value_index2].append(status.result.result)
                new_data = npu.apply(np.nanmean, datas[(i1, i2)])
                heatmaps[(i1, i2)].set_data(new_data)
                heatmaps[(i1, i2)].autoscale()

    fig.suptitle(title)

    return fig
