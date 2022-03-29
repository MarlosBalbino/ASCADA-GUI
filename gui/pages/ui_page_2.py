""" from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore """

from ctypes import alignment
from copy import deepcopy

from numpy import spacing
from qt_core import *

class UI_application_page_2(object):
    def setupUi(self, application_pages):
        if not application_pages.objectName():
            application_pages.setObjectName(u"application_pages")

        self.page = QWidget()
        self.verticalLayout = QVBoxLayout(self.page)
        self.label = QLabel(self.page)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Devices")
        self.verticalLayout.addWidget(self.label)
        application_pages.addWidget(self.page)