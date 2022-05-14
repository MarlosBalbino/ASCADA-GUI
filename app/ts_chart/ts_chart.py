from queue import Queue, LifoQueue
from PySide6.QtWidgets import QVBoxLayout, QFrame
from .chart_controller import ChartController
from .chart_view import ChartVew
from .options import Options

from app import logDebug


class TSChart(QFrame):

    def __init__(self,
                 ts_data,
                 ts_info,
                 initial_time_range_sz=5,
                 initial_vertical_range=(0, 5),
                 title="Sines"):
        """

        :param ts_info: Um dicionário no formato:
        {
            ts_id_1: {'lb': Time_Series_1_label, 'color': color},
            ts_id_2: {'lb': Time_Series_2_label, 'color': color}
        }
        :param ts_data: Um dicionário no formato:
        {
            ts_id_1: {time, values},
            ts_id_2: {time, values},
            ...
        }
        :param initial_time_range_sz:
        :param initial_vertical_range:
        :param title:
        """
        super().__init__()

        chart_lines_queue = Queue()
        chart_time_range_queue = LifoQueue()
        options_queue = Queue()

        self.chart_view = ChartVew(chart_lines_queue, chart_time_range_queue, options_queue,
                                   ts_info, title=title, initial_value_range=initial_vertical_range)

        self.chart_controller = ChartController(ts_data, chart_lines_queue,
                                                chart_time_range_queue, options_queue,
                                                initial_time_range_sz)

        # Options
        self.options = Options(ts_info, self.chart_controller.range_min_value_handler,
                               self.chart_controller.range_max_value_handler,
                               initial_vertical_range, self.chart_controller.slider_enable_handler,
                               self.chart_controller.time_range_sz_handler,
                               self.chart_controller.slider_scroll_handler,
                               self.chart_controller.ts_enable_handler,
                               self.chart_controller.ts_target_handler,
                               self.chart_controller.ts_labels_handler)

        v_layout = QVBoxLayout(self)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)
        v_layout.addWidget(self.chart_view)
        v_layout.addWidget(self.options)

    def update_chart(self):
        self.chart_view.update_chart()

    def __del__(self):
        self.chart_controller.stop()
