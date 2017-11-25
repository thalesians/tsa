import numpy as np

import thalesians.tsa.checks as checks
import thalesians.tsa.filtering as filtering
import thalesians.tsa.stats as stats
import thalesians.tsa.visual

_default_state_colours = ['#95c3e8', '#89b4d6', '#769ab8', '#3e5161', '#242f38', '#c3b9c2', '#88898c', '#736966', '#595047', '#2b1a0b']
_default_true_value_colours = ['#60617f', '#8f91bf', '#bfc2ff', '#303040', '#acaee5', '#405173', '#8a9cbf', '#a9b9d9', '#402924', '#8c6c6c']
_default_obs_colours = ['#900c3f', '#c70039', '#ff5733', '#907163', '#379683', '#5d001e', '#e3e2df', '#e3afbc', '#9a1750', '#ee4c7c']

class FilteringPlot(thalesians.tsa.visual.LivePlot):
    def __init__(self, fig, ax, title, filter_name,
                 process_prior_filter_states, process_posterior_filter_states, process_true_values, process_obs_results,
                 state_indices=None, state_labels=None, observable_names=None, obs_indices=None, obs_labels=None,
                 state_colours=_default_state_colours, true_value_colours=_default_true_value_colours,
                 obs_colours=_default_obs_colours,
                 *args, **kwargs):
        super().__init__(fig, ax, *args, **kwargs)
        
        self._process_prior_filter_states = process_prior_filter_states
        self._process_posterior_filter_states = process_posterior_filter_states
        self._process_true_values = process_true_values
        self._process_obs_results = process_obs_results

        if state_indices is not None:
            if not checks.is_iterable(state_indices): state_indices = (state_indices,)
            else: state_indices = tuple(state_indices)
        if state_labels is not None:
            if not checks.is_iterable(state_labels): state_labels = (state_labels,)
            else: state_labels = tuple(state_labels)
        checks.is_same_len_or_none(state_indices, state_labels)

        if observable_names is not None:
            checks.check_not_none(obs_indices)
            if not checks.is_iterable(observable_names): observable_names = (observable_names,)
            else: observable_names = tuple(observable_names)
        if obs_indices is not None:
            checks.check_not_none(observable_names)
            if not checks.is_iterable(obs_indices): obs_indices = (obs_indices,)
            else: obs_indices = tuple(obs_indices)
        if obs_labels is not None:
            if not checks.is_iterable(obs_labels): obs_labels = (obs_labels,)
            else: obs_labels = tuple(obs_labels)
        checks.is_same_len_or_none(observable_names, obs_indices, obs_labels)

        self._title = title
        
        self._filter_name = filter_name
        
        self._state_indices = state_indices
        self._state_labels = state_labels
        self._observable_names = observable_names
        self._obs_indices = obs_indices
        self._obs_labels = obs_labels
        
        self._state_colours = state_colours
        self._true_value_colours = true_value_colours
        self._obs_colours = obs_colours

        self._state_and_true_value_plots_inited = False
        self._obs_plots_inited = False
        
        if self._state_indices is not None:
            self._init_state_and_true_value_plots()
        
        self._inited_obs_index_count = 0
        
        if self._observable_names is not None:
            if self._obs_labels is None:
                self._obs_labels = []
                for observable_name, obs_index in zip(self._observable_names, self._obs_indices):
                    if self._observable_names.count(observable_name) == 1:
                        self._obs_labels.append(observable_name)
                    else:
                        self._obs_labels.append('%s %d' % (observable_name, obs_index))
                self._obs_labels = tuple(self._obs_labels)
            self._actual_observable_names = self._observable_names
            self._actual_obs_indices = self._obs_indices
            self._actual_obs_labels = self._obs_labels
            self._init_obs_plots()
            self._obs_plots_inited = True
        else:
            self._actual_observable_names = []
            self._actual_obs_indices = []
            self._actual_obs_labels = []
        
    def _post_init_plots(self):
        if len(self.ax.lines) > 0: self.ax.legend(loc='upper right')
        self.ax.set_title(self._title)
        
    def _init_state_and_true_value_plots_info(self, value):
        if self._state_indices is None:
            self._state_indices = tuple(range(np.size(value)))
        if self._state_labels is None:
            self._state_labels = tuple([('state %d' % i) for i in self._state_indices])
        
    def _init_state_and_true_value_plots(self):
        for plot_offset, (state_index, state_label) in enumerate(zip(self._state_indices, self._state_labels)):
            state_colour = None if self._state_colours is None else self._state_colours[plot_offset % len(self._state_colours)]
            true_value_colour = None if self._true_value_colours is None else self._true_value_colours[plot_offset % len(self._true_value_colours)]
            self._init_state_and_true_value_plots_for_state_index(plot_offset, state_index, state_label, state_colour, true_value_colour)
        self._post_init_plots()
        self._state_and_true_value_plots_inited = True
        
    def _init_state_and_true_value_plots_for_state_index(self, plot_offset, state_index, state_label, state_colour, true_value_colour):
        raise NotImplementedError

    def _init_obs_plots_info(self, obs):
        if not obs.observable_name in self._actual_observable_names:
            for i in range(np.size(obs.distr.mean)):
                self._actual_observable_names.append(obs.observable_name)
                self._actual_obs_indices.append(i)
                self._actual_obs_labels.append('%s %d' % (obs.observable_name, i))
        
    def _init_obs_plots(self):
        for plot_offset in range(self._inited_obs_index_count, len(self._actual_observable_names)):
            obs_colour = None if self._obs_colours is None else self._obs_colours[plot_offset % len(self._obs_colours)]
            self._init_obs_plots_for_obs_index(plot_offset, self._actual_observable_names[plot_offset], self._actual_obs_indices[plot_offset], self._actual_obs_labels[plot_offset], obs_colour)
        self._inited_obs_index_count = len(self._actual_observable_names)
        self._post_init_plots()
        
    def _init_obs_plots_for_obs_index(self, plot_offset, observable_name, obs_index, obs_label, obs_colour):
        raise NotImplementedError
    
    def _process_filter_state(self, filter_state):
        if not self._state_and_true_value_plots_inited:
            self._init_state_and_true_value_plots_info(filter_state.state_distr.mean)
            self._init_state_and_true_value_plots()
            
        for plot_offset, state_index in enumerate(self._state_indices):
            self._process_filter_state_for_state_index(filter_state, plot_offset, state_index)
        
        self.refresh()
        
    def _process_filter_state_for_state_index(self, filter_state, plot_offset, state_index):
        raise NotImplementedError
        
    def _process_true_value(self, true_value):
        if not self._state_and_true_value_plots_inited:
            self._init_state_and_true_value_plots_info(true_value.value)
            self._init_state_and_true_value_plots()
    
        for plot_offset, state_index in enumerate(self._state_indices):
            self._process_true_value_for_state_index(true_value, plot_offset, state_index)
            
        self.refresh()
        
    def _process_true_value_for_state_index(self, true_value, plot_offset, state_index):
        raise NotImplementedError

    def _process_obs_result(self, obs_result):
        obs = obs_result.obs        

        if not self._obs_plots_inited:
            self._init_obs_plots_info(obs)
            self._init_obs_plots()
            
        for plot_offset, (observable_name, obs_index) in enumerate(zip(self._actual_observable_names, self._actual_obs_indices)):
            if obs.observable_name == observable_name:
                self._process_obs_result_for_obs_index(obs_result, plot_offset, observable_name, obs_index)
                
        self.refresh()
        
    def _process_obs_result_for_obs_index(self, obs_result, plot_offset, observable_name, obs_index):
        obs = obs_result.obs        
        self.append(obs.time, obs.distr.mean[obs_index], self._obs_plot_indices[plot_offset], refresh=False)
        
    def process_filter_object(self, obj, raise_value_error=False):
        if self._filter_name is None or self._filter_name == obj.filter_name:
            if checks.is_instance(obj, filtering.FilterState):
                if self._process_prior_filter_states and (not obj.is_posterior):
                    self._process_filter_state(obj)
                elif self._process_posterior_filter_states and obj.is_posterior:
                    self._process_filter_state(obj)
            elif checks.is_instance(obj, filtering.TrueValue) and self._process_true_values:
                self._process_true_value(obj)
            elif checks.is_instance(obj, filtering.ObsResult) and self._process_obs_results:
                self._process_obs_result(obj)
            elif raise_value_error: raise ValueError('Unable to process a filter object: %s' % str(obj))

class StatePlot(FilteringPlot):
    def __init__(self, fig=None, ax=None, title=None, filter_name=None, is_posterior=False, plot_true_values=True,
                 state_indices=None, state_labels=None,
                 observable_names=None, obs_indices=None, obs_labels=None,
                 state_colours=_default_state_colours,
                 true_value_colours=_default_true_value_colours,
                 obs_colours=_default_obs_colours, 
                 *args, **kwargs):
        if title is None: title = 'posterior state' if is_posterior else 'prior state'
        
        super().__init__(fig=fig, ax=ax, title=title, filter_name=filter_name,
                process_prior_filter_states=not is_posterior, process_posterior_filter_states=is_posterior,
                process_true_values=plot_true_values, process_obs_results=True,
                state_indices=state_indices, state_labels=state_labels,
                observable_names=observable_names, obs_indices=obs_indices, obs_labels=obs_labels,
                state_colours=state_colours, true_value_colours=true_value_colours, obs_colours=obs_colours,
                *args, **kwargs)

        self._state_mean_plot_indices = []
        self._state_mean_minus_sd_plot_indices = []
        self._state_mean_plus_sd_plot_indices = []
        self._true_value_plot_indices = []
        self._obs_plot_indices = []
        
    def _init_state_and_true_value_plots_for_state_index(self, plot_offset, state_index, state_label, state_colour, true_value_colour):
        self._state_mean_plot_indices.append(len(self.ax.lines))
        self.ax.plot([], [], color=state_colour, linestyle='solid', label=state_label)
        self._state_mean_minus_sd_plot_indices.append(len(self.ax.lines))
        self.ax.plot([], [], color=state_colour, linestyle='dashed', label='%s +/- sd' % state_label)
        self._state_mean_plus_sd_plot_indices.append(len(self.ax.lines))
        self.ax.plot([], [], color=state_colour, linestyle='dashed')
        if self._process_true_values:
            self._true_value_plot_indices.append(len(self.ax.lines))
            self.ax.plot([], [], color=true_value_colour, linestyle='solid', label='%s true value' % state_label)
        
    def _init_obs_plots_for_obs_index(self, plot_offset, observable_name, obs_index, obs_label, obs_colour):
        self._obs_plot_indices.append(len(self.ax.lines))
        self.ax.plot([], [], color=obs_colour, marker='x', linestyle='None', label=obs_label)
    
    def _process_filter_state_for_state_index(self, filter_state, plot_offset, state_index):
        mean = filter_state.state_distr.mean[state_index]
        sd = np.sqrt(filter_state.state_distr.cov[state_index, state_index])
        self.append(filter_state.time, mean, self._state_mean_plot_indices[plot_offset], refresh=False)
        self.append(filter_state.time, mean - sd, self._state_mean_minus_sd_plot_indices[plot_offset], refresh=False)
        self.append(filter_state.time, mean + sd, self._state_mean_plus_sd_plot_indices[plot_offset], refresh=False)
        
    def _process_true_value_for_state_index(self, true_value, plot_offset, state_index):
        self.append(true_value.time, true_value.value[state_index], self._true_value_plot_indices[plot_offset], refresh=False)

    def _process_obs_result_for_obs_index(self, obs_result, plot_offset, observable_name, obs_index):
        obs = obs_result.obs
        self.append(obs.time, obs.distr.mean[obs_index], self._obs_plot_indices[plot_offset], refresh=False)
        
class ErrorPlot(FilteringPlot):
    def __init__(self, fig=None, ax=None, title=None, filter_name=None, is_posterior=False, rmse=False,
                 state_indices=None, state_labels=None,
                 state_colours=_default_state_colours,
                 *args, **kwargs):
        if title is None:
            if rmse:
                title = 'posterior rmse' if is_posterior else 'prior rmse'
            else:
                title = 'posterior error' if is_posterior else 'prior error'

        super().__init__(fig=fig, ax=ax, title=title, filter_name=filter_name,
                process_prior_filter_states=not is_posterior, process_posterior_filter_states=is_posterior,
                process_true_values=True, process_obs_results=False,
                state_indices=state_indices, state_labels=state_labels,
                observable_names=[], obs_indices=[], obs_labels=[],
                state_colours=state_colours, true_value_colours=None, obs_colours=None,
                *args, **kwargs)
        
        self._rms_calculator = stats.OnlineMeanAndVarCalculator() if rmse else None 

        self._last_true_value = None
        
        self._state_error_plot_indices = []
        
    def _init_state_and_true_value_plots_for_state_index(self, plot_offset, state_index, state_label, state_colour, true_value_colour):
        self._state_error_plot_indices.append(len(self.ax.lines))
        self.ax.plot([], [], color=state_colour, linestyle='solid', label=state_label)
        
    def _process_filter_state_for_state_index(self, filter_state, plot_offset, state_index):
        if self._last_true_value is not None and self._last_true_value.time == filter_state.time:
            error = self._last_true_value.value[state_index] - filter_state.state_distr.mean[state_index]
            if self._rms_calculator is not None:
                self._rms_calculator.add(error)
                error = self._rms_calculator.rms
            self.append(filter_state.time, error, self._state_error_plot_indices[plot_offset], refresh=False)
        
    def _process_true_value_for_state_index(self, true_value, plot_offset, state_index):
        if self._last_true_value is not true_value: self._last_true_value = true_value
        
class RMSEPlot(thalesians.tsa.visual.LivePlot):
    def __init__(self, fig=None, ax=None):
        super().__init__(fig, ax)
        
class ObservationPlot(thalesians.tsa.visual.LivePlot):
    def __init__(self, fig=None, ax=None):
        super().__init__(fig, ax)
        
class InnovationPlot(thalesians.tsa.visual.LivePlot):
    def __init__(self, fig=None, ax=None):
        super().__init__(fig, ax)
        
class InnovationQQPlot(thalesians.tsa.visual.LivePlot):
    def __init__(self, fig=None, ax=None):
        super().__init__(fig, ax)
        
class CUSUMPlot(thalesians.tsa.visual.LivePlot):
    def __init__(self, fig=None, ax=None):
        super().__init__(fig, ax)
        
class GainPlot(thalesians.tsa.visual.LivePlot):
    def __init__(self, fig=None, ax=None):
        super().__init__(fig, ax)
        
class LogLikelihoodPlot(thalesians.tsa.visual.LivePlot):
    def __init__(self, fig=None, ax=None):
        super().__init__(fig, ax)
        
class EffectiveSampleSizePlot(thalesians.tsa.visual.LivePlot):
    def __init__(self, fig=None, ax=None):
        super().__init__(fig, ax)
