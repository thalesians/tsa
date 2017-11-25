import numpy as np

import thalesians.tsa.checks as checks
import thalesians.tsa.filtering as filtering
import thalesians.tsa.visual

class StatePlot(thalesians.tsa.visual.LivePlot):    
    def __init__(self, fig=None, ax=None, filter_name=None, is_posterior=False, plot_true_values=True,
                 state_indices=None, state_labels=None,
                 observable_names=None, obs_indices=None, obs_labels=None,
                 *args, **kwargs):
        super().__init__(fig, ax, *args, **kwargs)

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

        self._filter_name = filter_name
        self._is_posterior = is_posterior
        self._plot_true_values = plot_true_values
        
        self._state_indices = state_indices
        self._state_labels = state_labels
        self._observable_names = observable_names
        self._obs_indices = obs_indices
        self._obs_labels = obs_labels
        
        self._state_mean_plot_indices = []
        self._state_mean_minus_sd_plot_indices = []
        self._state_mean_plus_sd_plot_indices = []
        self._true_value_plot_indices = []
        self._obs_plot_indices = []
        
        self._state_and_true_value_plots_inited = False
        self._obs_plots_inited = False
        
        if self._state_indices is not None:
            self._init_state_and_true_value_plots()
        
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
        self.ax.legend(loc='upper right')
        
    def _init_state_and_true_value_plots_info(self, value):
        if self._state_indices is None:
            self._state_indices = tuple(range(np.size(value)))
        if self._state_labels is None:
            self._state_labels = tuple([('state %d' % i) for i in self._state_indices])
        
    def _init_state_and_true_value_plots(self):
        for state_label in self._state_labels:
            self._state_mean_plot_indices.append(len(self.ax.lines))
            self.ax.plot([], [], color='blue', linestyle='solid', label=state_label)
            self._state_mean_minus_sd_plot_indices.append(len(self.ax.lines))
            self.ax.plot([], [], color='blue', linestyle='dashed', label='%s +/- sd' % state_label)
            self._state_mean_plus_sd_plot_indices.append(len(self.ax.lines))
            self.ax.plot([], [], color='blue', linestyle='dashed')
            if self._plot_true_values:
                self._true_value_plot_indices.append(len(self.ax.lines))
                self.ax.plot([], [], color='red', linestyle='solid', label='%s true value' % state_label)
        self._post_init_plots()
        self._state_and_true_value_plots_inited = True
        
    def _init_obs_plots_info(self, obs):
        if not obs.observable_name in self._actual_observable_names:
            for i in range(np.size(obs.distr.mean)):
                self._actual_observable_names.append(obs.observable_name)
                self._actual_obs_indices.append(i)
        
    def _init_obs_plots(self):
        for i in range(len(self._obs_plot_indices), len(self._actual_observable_names)):
            self._obs_plot_indices.append(len(self.ax.lines))
            self.ax.plot([], [], color='red', marker='x', linestyle='None', label=self._actual_obs_labels[i])
        self._post_init_plots()
    
    def _append_filter_state(self, filter_state):
        if not self._state_and_true_value_plots_inited:
            self._init_state_and_true_value_plots_info(filter_state.state_distr.mean)
            self._init_state_and_true_value_plots()
            
        for i in self._state_indices:
            mean = filter_state.state_distr.mean[i]
            sd = np.sqrt(filter_state.state_distr.cov[i,i])
            self.append(filter_state.time, mean, self._state_mean_plot_indices[i], refresh=False)
            self.append(filter_state.time, mean - sd, self._state_mean_minus_sd_plot_indices[i], refresh=False)
            self.append(filter_state.time, mean + sd, self._state_mean_plus_sd_plot_indices[i], refresh=False)
        
        self.refresh()
        
    def _append_true_value(self, true_value):
        if not self._state_and_true_value_plots_inited:
            self._init_state_and_true_value_plots_info(true_value.value)
            self._init_state_and_true_value_plots()
    
        for i in self._state_indices:
            self.append(true_value.time, true_value.value[i], self._true_value_plot_indices[i], refresh=False)
            
        self.refresh()

    def _append_obs(self, obs):
        if not self._obs_plots_inited:
            self._init_obs_plots_info(obs)
            self._init_obs_plots()
            
        for i, (observable_name, obs_index) in enumerate(zip(self._actual_observable_names, self._actual_obs_indices)):
            if obs.observable_name == observable_name:
                self.append(obs.time, obs.distr.mean[obs_index], self._obs_plot_indices[i], refresh=False)
                
        self.refresh()
        
    def append_filter_object(self, obj, raise_value_error=False):
        if self._filter_name is None or self._filter_name == obj.filter_name:
            if checks.is_instance(obj, filtering.FilterState):
                if self._is_posterior == obj.is_posterior: self._append_filter_state(obj)
            elif checks.is_instance(obj, filtering.TrueValue) and self._plot_true_values:
                self._append_true_value(obj)
            elif checks.is_instance(obj, filtering.Obs) and not checks.is_instance(obj. filtering.PredictedObs):
                self._append_obs(obj)
            elif raise_value_error: raise ValueError('Unable to process a filter object: %s' % str(obj))
        
class ErrorPlot(thalesians.tsa.visual.LivePlot):
    def __init__(self, fig=None, ax=None):
        super().__init__(fig, ax)
        
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
        