import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow


def run_plotter():
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_plotter()
    # run_example()
