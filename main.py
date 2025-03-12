import sys

from PyQt6.QtWidgets import QApplication

from panels.main_window import MainWindow

version = "v1.0.0"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(version=version, windowWidth=800, windowHeight=280, windowLabel="HARTracing")
    window.init()
    app.exec()
