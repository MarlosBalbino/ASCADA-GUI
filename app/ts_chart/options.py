from PySide6.QtWidgets import QFrame, QLabel, QDoubleSpinBox, QCheckBox, QHBoxLayout, QVBoxLayout, \
    QGroupBox, QRadioButton, QGridLayout, QSizePolicy, QSpacerItem, QSlider, QPushButton
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize


class Options(QFrame):

    def __init__(self,
                 id_label_color_list=None,
                 vertical_range_min_value_handler=None,
                 vertical_range_max_value_handler=None,
                 initial_vertical_range=(0, 5),
                 slider_enable_handler=None,
                 time_range_sz_handler=None,
                 slider_scroll_handler=None,
                 ts_enable_handler=None,
                 ts_target_handler=None,
                 ts_labels_handler=None,
                 parent=None):
        super().__init__(parent=parent)


        self.setFixedSize(QSize(900, 150))

        self.slider_enable_handler = slider_enable_handler
        self.slider_scroll_handler = slider_scroll_handler
        self.time_range_sz_handler = time_range_sz_handler
        config_bar, self.slider = self.build_config_bar()

        self.min_value_handler = vertical_range_min_value_handler
        self.max_value_handler = vertical_range_max_value_handler
        self.ts_labels_handler = ts_labels_handler
        ret = self.build_vertical_range_controllers(initial_vertical_range=initial_vertical_range)
        vertical_range_frame, self.vertical_min_value, self.vertical_max_value = ret
        ts_labels_enable_frame = self.build_ts_labels_enable()
        left_frame = self.build_left_frame(vertical_range_frame, ts_labels_enable_frame)

        self.ts_enable_handler = ts_enable_handler
        self.ts_target_handler = ts_target_handler
        ts_selector, self.rd_dict = self.build_ts_selector(id_label_color_list)
        ret = self.build_hidden_conf_frame(left_frame, ts_selector)
        self.hidden_config_frame, self.config_expand_ani, self.config_collapse_ani = ret

        layout = QVBoxLayout(self)
        layout.addWidget(config_bar)
        layout.addWidget(self.hidden_config_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

    def build_config_bar(self, time_range_sz_limits=(1e-6, 3.4e38)):
        # Create and setup time range size field
        time_range_sz_field = QDoubleSpinBox()
        time_range_sz_field.setRange(*time_range_sz_limits)
        time_range_sz_field.setValue(5)
        time_range_sz_field.setMaximumWidth(90)
        time_range_sz_field.valueChanged.connect(self._time_range_sz_handler)

        # Create and setup slider enable
        slider_enable = QCheckBox()
        slider_enable.stateChanged.connect(self._slider_enable_handler)

        # Create and setup slider
        slider = QSlider(orientation=Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(slider.maximum())
        slider.setEnabled(False)
        slider.valueChanged.connect(self._slider_scroll_handler)

        # Creates slider group and pack its widgets
        slider_group = QGroupBox()
        slider_group.setContentsMargins(5, 2, 5, 2)
        # slider_group.
        slider_group_layout = QHBoxLayout(slider_group)
        slider_group_layout.setContentsMargins(0, 0, 0, 0)
        slider_group_layout.addWidget(slider_enable)
        slider_group_layout.addWidget(slider)

        # Creates config button
        config_btn = QPushButton('Config')
        config_btn.clicked.connect(self.config_click_handler)

        # Creates the config_bar frame and pack widgets to it
        config_bar = QFrame()
        config_bar.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout(config_bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(time_range_sz_field)
        layout.addWidget(slider_group)
        layout.addWidget(config_btn)

        return config_bar, slider

    def build_vertical_range_controllers(self,
                                         initial_vertical_range,
                                         first_column_width=90,
                                         label='Limites verticais:'
                                         ):
        lb = QLabel(label)
        lb.setMaximumWidth(first_column_width)
        lb.setMinimumWidth(first_column_width)
        min_value = QDoubleSpinBox()
        min_value.setRange(-3.4e38, initial_vertical_range[1])
        min_value.setDecimals(4)
        min_value.setValue(initial_vertical_range[0])
        min_value.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        max_value = QDoubleSpinBox()
        max_value.setRange(initial_vertical_range[0], 3.4e38)
        max_value.setDecimals(4)
        max_value.setValue(initial_vertical_range[1])
        max_value.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(lb)
        layout.addWidget(min_value)
        layout.addWidget(max_value)
        min_value.valueChanged.connect(self._min_value_handler)
        max_value.valueChanged.connect(self._max_value_handler)
        return frame, min_value, max_value

    def build_ts_labels_enable(self, first_column_width=90, label='Ativar legendas:'):
        lb = QLabel(label)
        lb.setMaximumWidth(first_column_width)
        lb.setMinimumWidth(first_column_width)
        ck = QCheckBox()
        ck.stateChanged.connect(self._ts_labels_handler)
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.addWidget(lb)
        layout.addWidget(ck)
        layout.setContentsMargins(0, 0, 0, 0)
        return frame

    def build_ts_selector(self, id_label_color_list=None, label='Sinais disponíveis'):
        group = QGroupBox(label)
        group.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        layout = QGridLayout(group)
        i = 0
        rd_dict = {}
        for id_lb_color in id_label_color_list:
            rd = QRadioButton()
            rd.id = id_lb_color['id']
            rd.setMaximumWidth(15)
            rd.setEnabled(False)
            rd.toggled.connect(self._ts_target_handler)

            ck = QCheckBox(id_lb_color['lb'])
            ck.stateChanged.connect(self._ts_enable_handler)
            ck.id = id_lb_color['id']
            ck.setStyleSheet(f'color: {id_lb_color["color"]}')

            rd_dict[id_lb_color['id']] = rd

            layout.addWidget(rd, i, 0)
            layout.addWidget(ck, i, 1)
            i += 1

        return group, rd_dict

    @staticmethod
    def build_left_frame(range_frame, ts_labels_enable_frame, maximum_width=300):
        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        frame = QFrame()
        frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        frame.setMaximumWidth(maximum_width)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 5, 0, 0)
        layout.addWidget(range_frame)
        layout.addWidget(ts_labels_enable_frame)
        layout.addItem(spacer)
        return frame

    @staticmethod
    def build_hidden_conf_frame(left_frame, ts_selector):
        hidden_config_frame = QFrame()
        hidden_config_frame.setContentsMargins(0, 0, 0, 0)
        hidden_conf_frame_layout = QHBoxLayout(hidden_config_frame)
        hidden_conf_frame_layout.addWidget(left_frame)
        hidden_conf_frame_layout.addWidget(ts_selector)
        hidden_conf_frame_layout.setContentsMargins(0, 0, 0, 0)
        hidden_conf_frame_height = ts_selector.height()

        ani_duration = 1000

        config_expand_ani = QPropertyAnimation(hidden_config_frame, b'maximumHeight')
        config_expand_ani.setDuration(ani_duration)
        config_expand_ani.setStartValue(0)
        config_expand_ani.setEndValue(hidden_conf_frame_height)
        config_expand_ani.setEasingCurve(QEasingCurve.InOutCubic)

        config_collapse_ani = QPropertyAnimation(hidden_config_frame, b'maximumHeight')
        config_collapse_ani.setDuration(ani_duration)
        config_collapse_ani.setStartValue(hidden_conf_frame_height)
        config_collapse_ani.setEndValue(0)
        config_collapse_ani.setEasingCurve(QEasingCurve.InOutCubic)

        return hidden_config_frame, config_expand_ani, config_collapse_ani

    def _time_range_sz_handler(self, value):
        self.time_range_sz_handler(value)

    def _slider_scroll_handler(self, value):
        self.slider_scroll_handler(value)

    def config_click_handler(self):
        if self.hidden_config_frame.height() == 0:
            self.config_expand_ani.start()
        else:
            self.config_collapse_ani.start()

    def _min_value_handler(self, value):
        self.vertical_max_value.setMinimum(value*(1+0.01))
        self.min_value_handler(value)

    def _max_value_handler(self, value):
        self.vertical_min_value.setMaximum(value*(1-0.01))
        self.max_value_handler(value)

    def _slider_enable_handler(self, state):
        is_enabled = state == 2
        if is_enabled:
            self.slider.setEnabled(True)
        else:
            self.slider.setValue(self.slider.maximum())
            self.slider.setEnabled(False)
        if self.slider_enable_handler is not None:
            self.slider_enable_handler(is_enabled)

    def _ts_target_handler(self, enable):
        ts_id = self.sender().id
        self.ts_target_handler(ts_id, enable)

    def _ts_enable_handler(self, state):
        is_enabled = state == 2
        ts_id = self.sender().id
        if is_enabled:
            self.rd_dict[ts_id].setEnabled(True)
        else:
            self.rd_dict[ts_id].setEnabled(False)
            self.rd_dict[ts_id].setAutoExclusive(False)
            self.rd_dict[ts_id].setChecked(False)
            self.rd_dict[ts_id].setAutoExclusive(True)
        self.ts_enable_handler(ts_id, is_enabled)

    def _ts_labels_handler(self, state):
        self.ts_labels_handler(state == 2)
