from time import time
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtGui import QBrush, QPen
from PySide6.QtCore import Slot, QTimer, QThread
from .constants import OptionsKeys


class ChartVew(QChartView):
    def __init__(self,
                 lines_data_queue,
                 time_range_queue,
                 options_queue,
                 id_label_color_list,
                 frame_rate,
                 title='Sines',
                 xlabel='Time [s]',
                 ylabel='Value [p.u.]',
                 line_width=2,
                 initial_time_range=(-5, 0),
                 initial_value_range=(0, 5)):

        self.lines_data_queue = lines_data_queue
        self.time_range_queue = time_range_queue
        self.options_queue = options_queue

        self.chart = QChart()
        self.chart.setContentsMargins(0, 0, 0, 0)
        self.chart.setWindowFrameMargins(0, 0, 0, 0)
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.lines_data = {}
        self.lines = {}
        for id_label_color in id_label_color_list:
            line = QLineSeries()
            line.append([])
            line.setName(id_label_color['lb'])
            line.setPen(QPen(QBrush(id_label_color['color']), line_width))
            line.setUseOpenGL(True)
            self.lines[id_label_color['id']] = line
            self.lines_data[id_label_color['id']] = []

        foo_line = QLineSeries()
        self.chart.addSeries(foo_line)
        self.chart.createDefaultAxes()
        self._axis_x, self._axis_y = self.chart.axes()
        self.chart.removeSeries(foo_line)
        self._axis_x.setRange(*initial_time_range)
        self._axis_x.setLabelFormat("%.2f")
        self._axis_x.setTitleText(xlabel)
        self.left = 0
        self.right = 60
        self._axis_y.setRange(*initial_value_range)
        self._axis_y.setLabelFormat("%.2f")
        self._axis_y.setTitleText(ylabel)
        self.chart.legend().hide()
        self.chart.setTitle(title)

        super().__init__(self.chart)
        self.setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)

        self.timer = QTimer(self)
        self.timer.setInterval(round(1/frame_rate*1000))
        self.timer.timeout.connect(self.update_chart)
        self.timer.start()
        self.frame_instant = time()
        self.frame_periods = []

        self.options_handlers = {
            OptionsKeys.value_range: self.value_range_handler,
            OptionsKeys.ts_labels: self.ts_labels_handler,
            OptionsKeys.ts_enable: self.ts_enable_handler
        }

    @Slot()
    def update_chart(self):
        old_frame_instant, self.frame_instant = self.frame_instant, time()
        self.frame_periods.append(self.frame_instant - old_frame_instant)
        if len(self.frame_periods) >= 100:
            # print(f'Frame rate: {1/statistics.mean(self.frame_periods):.2f} fps.')
            self.frame_periods = []

        id_data = {}
        while not self.lines_data_queue.empty():
            line_id, line_data = self.lines_data_queue.get()
            id_data[line_id] = line_data
        for line_id, line_data in id_data.items():
            self.lines[line_id].replace(line_data)

        if not self.time_range_queue.empty():
            left, right = self.time_range_queue.get()
            self._axis_x.setRange(left, right)
            while not self.time_range_queue.empty():
                self.time_range_queue.get()

        while not self.options_queue.empty():
            option = self.options_queue.get()
            self.options_handlers[option['key']](option['value'])

    def value_range_handler(self, value):
        self._axis_y.setRange(*value)

    def ts_labels_handler(self, enable):
        if enable: self.chart.legend().show()
        else: self.chart.legend().hide()

    def ts_enable_handler(self, value):
        ts_id, enable = value.values()
        line = self.lines[ts_id]
        if enable:
            self.chart.addSeries(line)
            self.chart.setAxisX(self._axis_x, line)
            self.chart.setAxisY(self._axis_y, line)
        else: self.chart.removeSeries(line)
