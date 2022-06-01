""" from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore """

from sys import float_info
from qt_core import *

from app import DataTypes, DataGateway


class UI_application_page_4:
    def setupUi(self, application_pages):
        if not application_pages.objectName():
            application_pages.setObjectName(u"application_pages")

        self.page = QWidget()
        self.verticalLayout_3 = QVBoxLayout(self.page)
        self.label = QLabel(self.page)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("SCADA")
        self.verticalLayout_3.addWidget(self.label)
        application_pages.addWidget(self.page)

        self._flag_view_widgets = {}
        for i in range(1, 6):
            self._flag_view_widgets[i] = self.build_flag_view_widget(i)
            DataGateway.in_flag[i] = None
            self.verticalLayout_3.addWidget(self._flag_view_widgets[i])
        self._update_flag_view_widgets = QTimer(self.page)
        self._update_flag_view_widgets.setInterval(round(1/2*1000))
        self._update_flag_view_widgets.timeout.connect(self.update_flag_view)
        self._update_flag_view_widgets.start()

        for i in range(3):
            self.verticalLayout_3.addWidget(self.build_send_flag_widget())

    def update_flag_view(self):
        for id, widget in self._flag_view_widgets.items():
            widget.set_value(DataGateway.in_flag[id])

    @staticmethod
    def build_flag_view_widget(id):
        id_lb = QLabel()
        id_lb.setText("id: " + str(id))
        value_lb = QLabel()
        value_lb.setText("\tValue:")
        value_field = QLabel("None")
        lyt = QHBoxLayout()
        lyt.addWidget(id_lb)
        lyt.addWidget(value_lb)
        lyt.addWidget(value_field)
        frm = QFrame()
        frm.setLayout(lyt)
        frm.set_value = lambda value: value_field.setText(str(value))
        return frm

    @staticmethod
    def build_send_flag_widget():
        id_lb = QLabel()
        id_lb.setText("id:")
        id_entry = QDoubleSpinBox()
        id_entry.setRange(1, 14)
        id_entry.setDecimals(0)
        value_lb = QLabel()
        value_lb.setText("\tValue:")
        value_entry = QDoubleSpinBox()
        value_entry.setRange(-float_info.max, float_info.max)
        value_entry.setDecimals(6)
        type_lb = QLabel()
        type_lb.setText("\tType:")
        type_entry = QComboBox()
        type_entry.addItems(DataTypes.types.values())
        send_btn = QPushButton(text="Send")

        lyt = QHBoxLayout()
        lyt.addWidget(id_lb)
        lyt.addWidget(id_entry)
        lyt.addWidget(value_lb)
        lyt.addWidget(value_entry)
        lyt.addWidget(type_lb)
        lyt.addWidget(type_entry)
        lyt.addWidget(send_btn)

        send_btn.clicked.connect(
            lambda: DataGateway.send_flag(id_entry.value(), type_entry.currentText(),
                                          value_entry.value())
        )

        frm = QFrame()
        frm.setLayout(lyt)
        return frm
