from time import sleep
from queue import Queue, LifoQueue
from PySide6.QtWidgets import QVBoxLayout, QFrame
from .chart_controller import ChartController
from .chart_view import ChartVew
from .options import Options


class TSChart(QFrame):

    def __init__(self,
                 id_label_color_list,
                 waves_queue,
                 frame_rate=60,
                 time_range_sz=5,
                 title="Sines"):
        super().__init__()

        chart_lines_queue = Queue()
        chart_time_range_queue = LifoQueue()
        options_queue = Queue()

        self.chart_view = ChartVew(chart_lines_queue,
                                   chart_time_range_queue,
                                   options_queue,
                                   id_label_color_list,
                                   frame_rate,
                                   title=title)

        self.chart_controller = ChartController(waves_queue, chart_lines_queue,
                                                chart_time_range_queue, options_queue,
                                                time_range_sz)

        # Options
        initial_vertical_range = (0, 5)
        self.options = Options(id_label_color_list,
                               self.chart_controller.range_min_value_handler,
                               self.chart_controller.range_max_value_handler,
                               initial_vertical_range,
                               self.chart_controller.slider_enable_handler,
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

    def stop(self):
        self.chart_view.stop()
        sleep(0.5)
        self.chart_controller.stop()
        sleep(0.5)