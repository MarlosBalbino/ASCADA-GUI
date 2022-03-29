from ctypes import alignment
from copy import deepcopy

from gui.widgets.py_push_button import PyPushButton
from gui.widgets.my_widgets import ChartWindow, MyScrollBar

from numpy import spacing
from qt_core import *

from app.noised_wave import NoisedWave
from app.ts_chart import TSChart
from queue import Queue
from app.ts_chart import Colors
from random import randint

class UI_application_page_3(object):
    
    object_list = []

    def setupUi(self, application_pages: QStackedWidget):
        if not application_pages.objectName():
            application_pages.setObjectName(u"application_pages")

        # PAGE
        self.page = QWidget()

        # PAGE LAYOUT
        self.page_layout = QVBoxLayout(self.page)
        self.page_layout.setContentsMargins(0,0,0,0)

        # SCROLL AREA
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("border: none")
        self.scroll_area.setWidgetResizable(True)

        # CREATE CUSTOM SCROLL BAR
        self.scroll_bar = MyScrollBar()

        # SET CUSTOM SCROLL BAR
        self.scroll_area.setVerticalScrollBar(self.scroll_bar)

        # ADD SCROLL AREA TO PAGE LAYOUT
        self.page_layout.addWidget(self.scroll_area)

        # CONTENTS AREA
        self.contents_area = QWidget()
        self.contents_area_layout = QVBoxLayout(self.contents_area)
        self.contents_area_layout.setContentsMargins(10,10,5,10)
        
        # CONTENTS FRAME
        self.contents_frame = QFrame()
        # self.contents_frame.setStyleSheet("background-color: blue")
        self.contents_frame.setMinimumWidth(500)
        self.contents_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # CONTENTS FRAME LAYOUT
        self.contents_frame_layout = QVBoxLayout(self.contents_frame)
        self.contents_frame_layout.setContentsMargins(0,0,0,0)
        self.contents_frame_layout.setSpacing(10)

        # CENTRAL FRAME (MAIN WORKING AREA FRAME)
        self.central_frame = QFrame()
        self.central_frame.setStyleSheet("background-color: red")

        # CENTRAL FRAME LAYOUT
        self.central_frame_layout = QVBoxLayout(self.central_frame)
        self.central_frame_layout.setContentsMargins(0,0,0,0)
        self.central_frame_layout.setSpacing(5)

        # BOTTOM FRAME
        self.bottom_frame = QFrame()
        # self.bottom_frame.setStyleSheet("background-color: green")
        self.bottom_frame.setMaximumHeight(40)

        # BOTTOM FRAME LAYOUT
        self.bottom_frame_layout = QHBoxLayout(self.bottom_frame)
        self.bottom_frame_layout.setContentsMargins(0,0,0,0)
        self.bottom_frame_layout.setSpacing(0)

        # Spacer
        self.spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Add btn frame
        self.add_btn_frame = QFrame()
        self.add_btn_frame.setStyleSheet("background-color: purple")
        self.add_btn_frame.setMaximumHeight(40)
        self.add_btn_frame.setMaximumWidth(120)

        # Add btn layout
        self.add_btn_layout = QHBoxLayout(self.add_btn_frame)
        self.add_btn_layout.setContentsMargins(0,0,0,0)
        self.add_btn_layout.setSpacing(0)

        # Add widget btn
        self.add_widget_btn = PyPushButton(
            text="",
            icon_path="cil-add-2",
            minimum_width=120
        )

        # Add btn to layout
        self.add_btn_layout.addWidget(self.add_widget_btn)
        
        # ADD WIDGETS TO BOTTOM FRAME LAYOUT
        self.bottom_frame_layout.addSpacerItem(self.spacer)
        self.bottom_frame_layout.addWidget(self.add_btn_frame)
        self.bottom_frame_layout.addSpacerItem(self.spacer)

        # ADD WIDGETS TO CONTENTS FRAME
        self.contents_frame_layout.addWidget(self.central_frame)
        self.contents_frame_layout.addSpacerItem(self.spacer)
        self.contents_frame_layout.addWidget(self.bottom_frame)

        # ADD CONTENTS FRAME TO CONTENTS AREA
        self.contents_area_layout.addWidget(self.contents_frame)

        # ACTIVATE CONTENTS AREA INSIDE SCROLL AREA
        self.scroll_area.setWidget(self.contents_area)
        application_pages.addWidget(self.page)

        # CLICK EVENT
        self.add_widget_btn.clicked.connect(self.add_widget)

    def add_widget(self):
        
        chart_window = ChartWindow(height=550)
        
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
            NoisedWave(self.waves_queue,
                       frame_rate=frame_rate,
                       sampling_rate=sampling_rate,
                       offset=1.5,
                       wave_id=id_label_color_list[0]['id'],
                       f=1,
                       delay_rate=0.1),
            NoisedWave(self.waves_queue,
                       frame_rate=frame_rate,
                       sampling_rate=sampling_rate,
                       offset=3.5,
                       wave_id=id_label_color_list[1]['id'],
                       f=1.5)
        ]

        self.ts_chart = TSChart(id_label_color_list,
                                self.waves_queue,
                                frame_rate=frame_rate,
                                time_range_sz=5,
                                title=chart_title)

        chart_window.add_widget(self.ts_chart)


        self.object_list.append(chart_window)
        self.central_frame_layout.addWidget(chart_window)
        self.scroll_area.verticalScrollBar().rangeChanged.connect(lambda: scroll_down())

        def scroll_down():
            self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()
            )

        chart_window.btn.clicked.connect(lambda: remove_widget())

        def remove_widget():
            index = self.object_list.index(chart_window)
            print(index)
            self.object_list[index].deleteLater()
            self.object_list.remove(chart_window)

        