from numbers import Number
from typing import Callable

from PySide6.QtCore import QObject, Slot


class ChartController(QObject):

    def __init__(self, update_plot_handler: Callable):
        super().__init__()
        self.update_plot_handler = update_plot_handler
        self.t_max = None
        self.t_sz = 5
        self.ts_enabled_list = []

    def build_chart_data(self, ts_data):
        """
        Receives a ts dada packet on format {1: (t, x), 2: (t, x), ..., n: (t, x)} and 
        returns a data packet to be ploted in the same format.

        :data: ex.: {1: (t, x), 2: (t, x), ..., n: (t, x)}
        """
        chart_data = {}
        for id, (t, x) in ts_data.items():
            if id not in self.ts_enabled_list:
                chart_data[id] = [], []
                continue
            if len(t) < 2:
                continue
            
            if self.t_max is None:
                t_max = t[-1]
            else:
                t_max = self.t_max/100 * (t[-1] - t[0]) + t[0]

            i_min, i_max = self._get_index_range(t, t_max, self.t_sz)
            chart_data[id] = t[i_min:i_max+1], x[i_min:i_max+1]

        return chart_data

    def _get_index_range(self, t, t_max, t_sz):
        if t[-1] == t[0]:
            return 0, -1
        sampling_rate = (len(t)-1) / (t[-1] - t[0])
        min_index = round(sampling_rate * (t_max-t_sz - t[0]))
        if not min_index <= len(t):
            min_index = len(t)
        if min_index < 0:
            min_index = 0
        max_index = round(sampling_rate * (t_max - t[0]))
        if not max_index <= len(t):
            max_index = len(t)
        if max_index < 0:
            max_index = 0
        return min_index, max_index

    def update_plot(self, data_to_plot):
        self.update_plot_handler(data_to_plot)

    @Slot(Number)
    def t_sz_changed(self, t_sz):
        self.t_sz = t_sz

    @Slot(Number)
    def t_max_changed(self, t_max):
        self.t_max = t_max

    @Slot(int, bool)
    def ts_enable_changed(self, ts_id, enabled):
        if enabled:
            if ts_id not in self.ts_enabled_list:
                self.ts_enabled_list.append(ts_id)
        else:
            self.ts_enabled_list.remove(ts_id)