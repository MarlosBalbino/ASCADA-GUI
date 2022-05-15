import sys
import os
import time
import threading
from qt_core import *

from app import DataGateway

# IMPORT MAIN WINDOW
from gui.windows.main_window.ui_main_window import *


# MAIN WINDOW
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASCADA")

        # SETUP MAIN WINDOW
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # Toggle button 
        self.ui.toggle_btn.clicked.connect(self.toggle_button)

        # Show pages
        self.ui.btn_1.clicked.connect(self.show_page_1)
        self.ui.btn_2.clicked.connect(self.show_page_2)
        self.ui.btn_3.clicked.connect(self.show_page_3)
        self.ui.btn_4.clicked.connect(self.show_page_4)

        # Open file
        self.ui.btn_5.clicked.connect(self.open_file)

        # Show settings
        self.ui.settings_btn.clicked.connect(self.show_settings)

        # RESTORES THE LAST SESSION GEOMETRIC STATE
        self._readAndApplyWindowAttributeSettings()

        # EXIBE A APLICAÇÂO
        self.show()

        # STARTS THE DataGateway THREADS AND ITS TASKS
        DataGateway.setup()

    def reset_selection(self):
        for btn in self.ui.left_menu.findChildren(QPushButton):
            try:
                btn.set_active(False)
            except:
                pass
    
    def show_page_1(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_page_1.page)
        self.ui.btn_1.set_active(True)
        self.ui.top_right_label.setText("Home")

    def show_page_2(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_page_2.page)
        self.ui.btn_2.set_active(True)
        self.ui.top_right_label.setText("Devices")

    def show_page_3(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_page_3.page)
        self.ui.btn_3.set_active(True)
        self.ui.top_right_label.setText("Charts")

    def show_page_4(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_page_4.page)
        self.ui.btn_4.set_active(True)
        self.ui.top_right_label.setText("SCADA")

    def show_settings(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_sttgs.page)
        self.ui.settings_btn.set_active(True)
        self.ui.top_right_label.setText("Settings")

    def toggle_button(self):
        # Get left menu width
        menu_width = self.ui.left_menu.width()

        # Check width
        width = 0
        if menu_width == 0:
            width = 50

        # Start animation
        self.animation = QPropertyAnimation(self.ui.left_menu, b"minimumWidth")
        self.animation.setStartValue(menu_width)
        self.animation.setEndValue(width)
        self.animation.setDuration(150)
        self.animation.start()

    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open_file")
        print(file_name)

    def get_text(self):
        text = self.mw.text_edit.toPlainText()
        print(text)

    def _readAndApplyWindowAttributeSettings(self):
        '''
        https://gist.github.com/bootchk/5330231
        Read window attributes from settings,
        using current attributes as defaults (if settings not exist.)
        Called at QMainWindow initialization, before show().
        '''
        qsettings = QSettings()
        qsettings.beginGroup("mainWindow")
        # No need for toPoint, etc. : PySide converts types
        self.restoreGeometry(qsettings.value("geometry", self.saveGeometry()))
        self.restoreState(qsettings.value("saveState", self.saveState()))
        qsettings.endGroup()

    def _writeWindowAttributeSettings(self):
        '''
        https://gist.github.com/bootchk/5330231
        Save window attributes as settings.
        Called when window moved, resized, or closed.
        '''
        qsettings = QSettings()
        qsettings.beginGroup("mainWindow")
        qsettings.setValue("geometry", self.saveGeometry())
        qsettings.endGroup()

    def closeEvent(self, event) -> None:
        DataGateway.stop()
        self._writeWindowAttributeSettings()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
