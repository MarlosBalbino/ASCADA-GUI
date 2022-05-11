from PySide6.QtWidgets import QMainWindow
from wave_source import WaveSource
from ts_chart import TSChart
from queue import Queue
from ts_chart import Colors
from random import randint


class MainWindow(QMainWindow):

    def __init__(self, title="TSChart Testing"):
        super().__init__()

        chart_title = 'Sines'
        frame_rate = 60
        sampling_rate = 256
        color_max_i = len(Colors.Favorites.get_list()) - 1
        color_list = Colors.Favorites.get_list()
        id_label_color_list = [
            {'id': 1, 'lb': 'Time Series 1', 'color': color_list[randint(0, color_max_i)]},
            {'id': 2, 'lb': 'Time Series 2', 'color': color_list[randint(0, color_max_i)]},
        ]
        # id_label_color_list = [
        #     {'id': 1, 'lb': 'Time Series 1', 'color': Colors.Favorites.blue},
        #     {'id': 2, 'lb': 'Time Series 2', 'color': Colors.Favorites.darkgreen},
        # ]

        self.waves_queue = Queue()
        self.waves = [
            WaveSource(self.waves_queue, wave_id=id_label_color_list[0]['id'],
                       sampling_rate=sampling_rate, frame_rate=frame_rate, offset=1.5,
                       wave_frequency_hz=1, delay_rate=0.1),
            WaveSource(self.waves_queue, wave_id=id_label_color_list[1]['id'],
                       sampling_rate=sampling_rate, frame_rate=frame_rate, offset=3.5,
                       wave_frequency_hz=1.5)
        ]

        self.ts_chart = TSChart(id_label_color_list, frame_rate=frame_rate, initial_time_range_sz=5,
                                title=chart_title)

        self.setCentralWidget(self.ts_chart)
        self.setWindowTitle(title)
        available_geometry = self.screen().availableGeometry()
        height = available_geometry.height() * 2/4
        width = available_geometry.width() * 2/4
        self.resize(width, height)
        self.show()

    def closeEvent(self, event):
        self.ts_chart.stop()
        for wave in self.waves:
            wave.stop()
        event.accept()
