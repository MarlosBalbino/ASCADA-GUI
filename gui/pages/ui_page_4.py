""" from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore """

from ctypes import alignment
from copy import deepcopy
import imp

from numpy import spacing
from qt_core import *

from PySide6.QtWidgets import QDoubleSpinBox, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QPushButton, QSpinBox

from gui.widgets.flags.out_flag import OutBoolFlag, OutCharFlag, OutIntFlag, OutFloatFlag
from gui.widgets.flags.in_flag import InFlag

class UI_application_page_4(object):
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

        out_bool_flag = OutBoolFlag(1)
        out_bool_flag.send_value.connect(lambda id, value: print(f"id: {id}\tvalue: {value}"))
        self.verticalLayout_3.addWidget(out_bool_flag)

        out_char_flag = OutCharFlag(2)
        out_char_flag.send_value.connect(lambda id, value: print(f"id: {id}\tvalue: {value}"))
        self.verticalLayout_3.addWidget(out_char_flag)

        out_int_flag = OutIntFlag(3)
        self.verticalLayout_3.addWidget(out_int_flag)
        out_int_flag.send_value.connect(lambda id, value: print(f"id: {id}\tvalue: {value}"))

        out_float_flag = OutFloatFlag(4)
        self.verticalLayout_3.addWidget(out_float_flag)
        out_float_flag.send_value.connect(lambda id, value: print(f"id: {id}\tvalue: {value}"))

        in_flag = InFlag(0, 'All')
        self.verticalLayout_3.addWidget(in_flag)
        out_bool_flag.send_value.connect(lambda id, value: in_flag.update_value(f'Id: {id}\tValue: {value}'))
        out_char_flag.send_value.connect(lambda id, value: in_flag.update_value(f'Id: {id}\tValue: {value}'))
        out_int_flag.send_value.connect(lambda id, value: in_flag.update_value(f'Id: {id}\tValue: {value}'))
        out_float_flag.send_value.connect(lambda id, value: in_flag.update_value(f'Id: {id}\tValue: {value}'))






        
