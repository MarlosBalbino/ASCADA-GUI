# https://www.pythonguis.com/tutorials/pyside-plotting-pyqtgraph/

from numbers import Number

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QDoubleSpinBox, QCheckBox, QSlider
from PySide6.QtCore import Signal, Slot, Qt
import pyqtgraph as pg


class TsChart(QFrame):
    t_sz_changed = Signal(Number)               # Number: new size
    t_max_changed = Signal(Number)              # Number: new max value
    ts_enable_changed = Signal(int, bool)       # int: ts id. bool: True means enabled, False means disabled
    closing = Signal(int)                       # int: id of TSChart object

    def __init__(self, id, ts_info: dict):
        """
        ts_info: ex.:
            {
                1: {'legend': 'TimeSerie1', 'color': (200, 180, 250)},
                2: {'legend': 'TimeSerie2', 'color': (200, 180, 250)},
                ...
            }
        """
        super().__init__()
        self.id = id

        graph = pg.PlotWidget()
        graph.showGrid(x=True, y=True)

        t_range, ts_enable_changed = self._build_controllers(ts_info)

        self.lyt = QVBoxLayout()
        self.lyt.addWidget(graph)
        self.lyt.addWidget(t_range)
        self.lyt.addWidget(ts_enable_changed)
        self.setLayout(self.lyt)

        self.lines = {}
        for id, info in ts_info.items():
            pen = pg.mkPen(color=info['color'], width=2)
            self.lines[id] = graph.plot([], [], pen=pen)

    def _build_controllers(self, ts_info):
        # Create and setup time range size field
        t_sz = QDoubleSpinBox()
        t_sz.setRange(-3.4e38, 3.4e38)
        t_sz.setValue(5)
        t_sz.setMaximumWidth(90)
        t_sz.valueChanged.connect(lambda value: self.t_sz_changed.emit(value))

        # Create and setup slider
        slider = QSlider(orientation=Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(slider.maximum())
        slider.setEnabled(False)
        slider.valueChanged.connect(lambda value: self.t_max_changed.emit(value))

        # Create and setup slider enable
        slider_enable = QCheckBox()
        def handle_slider_en(value):
            if value == 2:
                slider.setEnabled(True)
                self.t_max_changed.emit(slider.value())
            else:
                slider.setValue(slider.maximum())
                slider.setEnabled(False)
                self.t_max_changed.emit(None)            
        slider_enable.stateChanged.connect(handle_slider_en)
        
        # Packs the slider related widget
        range_frm = QFrame()
        slider_lyt = QHBoxLayout(range_frm)
        slider_lyt.setContentsMargins(0, 0, 0, 0)
        slider_lyt.addWidget(t_sz)
        slider_lyt.addWidget(slider)
        slider_lyt.addWidget(slider_enable)

        # Create and setup time series enable selectors
        ts_enable_frm = QFrame()
        ts_enable_frm.setStyleSheet('background-color: black')
        ts_enable_lyt = QHBoxLayout(ts_enable_frm)
        for id, info in ts_info.items():
            ck = QCheckBox(info['legend'])
            ck.stateChanged.connect(lambda value, id=id: self.ts_enable_changed.emit(id, value == 2))
            color = '#'+''.join([info['color'][i].to_bytes(1, 'big').hex() for i in range(3)])
            ck.setStyleSheet(f"color: {color}")
            ts_enable_lyt.addWidget(ck)

        return range_frm, ts_enable_frm
    
    @Slot()
    def close(self):
        self.closing.emit(self.id)

    # @Slot(dict)
    def update_lines(self, ts_data: dict):
        """
        :ts_data: ex.: {1: (t, x), 2: (t, x), ...}
        """
        for id, data in ts_data.items():
            self.lines[id].setData(*data)

    

