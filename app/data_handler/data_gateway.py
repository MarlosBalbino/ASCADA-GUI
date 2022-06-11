import numpy as np
from time import time

from PySide6.QtCore import QObject, Signal, Slot, QRunnable, QThreadPool, QThread

from ts_chart import TsChart
from ts_chart import ChartController

class DataGatewaySignals(QObject):
    update_charts = Signal(dict)


class DataGateway(QRunnable):

    def __init__(self):
        super().__init__()
        self.next_chart_id = 1
        self.ts_info = {
            1: {'legend': 'TimeSeries-1', 'color': (100, 200, 230)},
            2: {'legend': 'TimeSeries-2', 'color': (250, 200, 150)}
        }
        self.ts_data = {
            1: ([0], [0]),
            2: ([10], [0])
        }
        self.params = {
            1: {'f': 2*np.pi/2, 'step': 4e-3, 'frm_n': 25},
            2: {'f': 2*np.pi/3, 'step': 4.1e-3, 'frm_n': 25}
        }
        self.update_freq = 30       # Flushes the icomming data and updates the plots "update_freq" times per second

        self.controllers = {}
        self._signals = DataGatewaySignals()
        self._signals.update_charts.connect(self._update_charts)

        self.keep = None
        self.thread_pool = QThreadPool()
        self.thread_pool.start(self)

    def run(self):
        self.keep = True
        while self.keep:
            t0 = time()

            self._flush_data_streaming()

            # build data and update charts
            data_to_plot = {}
            for chart_id, controller in self.controllers.items():
                data_to_plot[chart_id] = controller.build_chart_data(self.ts_data)
            self._signals.update_charts.emit(data_to_plot)

            processing_time = time() - t0
            if processing_time < 1/self.update_freq:
                QThread.msleep(round((1/self.update_freq - processing_time) * 1000))
            else:
                print(
                    f"Data processing took too long: {processing_time}s."
                    f"Max expected: {1/self.update_freq}s."
                )

    def _flush_data_streaming(self):
        """
        It is a mock for data streaming.
        """
        for id, (t, x) in self.ts_data.items():
            f, step, frm_n = self.params[id].values()
            new_t = np.linspace(t[-1]+step, t[-1]+step + step*frm_n, frm_n)
            new_x = np.sin(f*new_t)
            t.extend(new_t)
            x.extend(new_x)

    @Slot(dict)
    def _update_charts(self, data_to_plot):
        for chart_id, chart_data in data_to_plot.items():
            self.controllers[chart_id].update_plot(chart_data)

    @Slot()
    def get_new_chart(self):
        chart = TsChart(self.next_chart_id, self.ts_info)        
        controller = ChartController(chart.update_lines)

        chart.t_sz_changed.connect(controller.t_sz_changed)
        chart.t_max_changed.connect(controller.t_max_changed)
        chart.ts_enable_changed.connect(controller.ts_enable_changed)
        chart.closing.connect(self._detach_chart)
        self.controllers[self.next_chart_id] = controller

        self.next_chart_id += 1

        return chart

    @Slot(int)
    def _detach_chart(self, chart_id):
        self.controllers.pop(chart_id)

    @Slot()
    def stop(self):
        self.keep = False
