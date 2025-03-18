import sys

from PyQt6.QtWidgets import QApplication

from panels.main_window import MainWindow

version = "v2.0.0"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(version=version, windowWidth=1000, windowHeight=600, windowLabel="HARTracing")
    window.init()
    app.exec()
