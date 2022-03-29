from threading import Thread
from PySide6.QtCore import QPointF
from .constants import OptionsKeys


class ChartController:

    def __init__(self,
                 ts_queue,
                 chart_lines_queue,
                 chart_time_range_queue,
                 options_queue,
                 time_range_sz):
        super().__init__()

        self.ts_queue = ts_queue
        self.chart_lines_queue = chart_lines_queue
        self.chart_time_range_queue = chart_time_range_queue
        self.options_queue = options_queue
        self.ts_data = {}

        self.value_range = [0, 5]
        self.options_queue.put({'key': OptionsKeys.value_range, 'value': self.value_range})

        self.is_slider_enabled = False
        self.time_range_sz = time_range_sz
        self.slider_value = 0

        self.ts_enabled_list = []
        self.ts_target_id = None

        self.thread = Thread(target=self._run)
        self.keep_running = False
        self.run()

    def run(self):
        self.keep_running = True
        self.thread.start()

    def _run(self):
        while self.keep_running:
            xdata, ydata, ts_id = self.ts_queue.get()
            if ts_id not in self.ts_data.keys(): self.ts_data[ts_id] = {'x': [], 'y': []}
            ts_data = self.ts_data[ts_id]
            ts_data['x'].extend(xdata)
            ts_data['y'].extend(ydata)

            if not self.is_slider_enabled:
                self.handle_last_ts_data(ts_id)

    def handle_last_ts_data(self, ts_id):
        if self.ts_target_id is None: return
        max_time = self.ts_data[self.ts_target_id]['x'][-1] + 0.01 * self.time_range_sz
        min_time = max_time - self.time_range_sz
        self.update_chart(ts_id, min_time, max_time)

    def update_chart(self, ts_id, min_time, max_time):
        if ts_id not in self.ts_enabled_list: return
        ts_data = self.ts_data[ts_id]
        min_index, max_index = self.get_index_range(ts_data, min_time, max_time)
        to_plot = [QPointF(ts_data['x'][i], ts_data['y'][i]) for i in range(min_index, max_index)]
        self.chart_lines_queue.put((ts_id, to_plot))
        if ts_id == self.ts_target_id:
            self.chart_time_range_queue.put((min_time, max_time))

    def slider_scroll_handler(self, value):
        self.slider_value = value
        if self.ts_target_id is None: return
        t = self.ts_data[self.ts_target_id]['x']
        max_time = (t[-1] - t[0]) * value / 100 + 0.01*self.time_range_sz
        min_time = max_time - self.time_range_sz
        for ts_id, ts_data in self.ts_data.items():
            self.update_chart(ts_id, min_time, max_time)

    def ts_enable_handler(self, ts_id, enable):
        if enable:
            self.ts_enabled_list.append(ts_id)
            if self.is_slider_enabled:
                self.slider_scroll_handler(self.slider_value)
            else:
                self.handle_last_ts_data(ts_id)
        else:
            if ts_id in self.ts_enabled_list: self.ts_enabled_list.remove(ts_id)
            self.chart_lines_queue.put((ts_id, []))
        self.options_queue.put({'key': OptionsKeys.ts_enable, 'value': {'id': ts_id, 'en': enable}})

    def ts_target_handler(self, ts_id, enable):
        self.ts_target_id = ts_id if enable else None

    @staticmethod
    def get_index_range(ts_data, min_time, max_time):
        t = ts_data['x']
        sampling_rate = len(t) / (t[-1] - t[0])
        min_index = round(sampling_rate * (min_time - t[0]))
        if not min_index <= len(t): min_index = len(t)
        if min_index < 0: min_index = 0
        max_index = round(sampling_rate * (max_time - t[0]))
        if not max_index <= len(t): max_index = len(t)
        if max_index < 0: max_index = 0
        return min_index, max_index

    def time_range_sz_handler(self, value):
        self.time_range_sz = value

    def stop(self):
        self.keep_running = False

    def range_min_value_handler(self, value):
        self.value_range[0] = value
        self.options_queue.put({'key': OptionsKeys.value_range, 'value': self.value_range})

    def range_max_value_handler(self, value):
        self.value_range[1] = value
        self.options_queue.put({'key': OptionsKeys.value_range, 'value': self.value_range})

    def slider_enable_handler(self, is_enabled):
        self.is_slider_enabled = is_enabled

    def ts_labels_handler(self, enable):
        self.options_queue.put({'key': OptionsKeys.ts_labels, 'value': enable})
