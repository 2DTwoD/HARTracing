from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout

from panels.com_panel import ComPanel
from panels.edit_panel import EditPanel
from panels.info_panel import InfoPanel
from panels.range_panel import RangePanel
from widgets.dialog import Confirm
from misc import di


class MainWindow(QMainWindow):
    def __init__(self, version="v0.0.0", windowWidth=100, windowHeight=100, windowLabel="App"):
        super().__init__()
        self.com = di.Container.com()

        self.mainWidget = QWidget(parent=self)
        self.mainWidget.setFixedSize(windowWidth, windowHeight)

        box = QVBoxLayout()
        versionLabel = QLabel(version, parent=self)
        comPanel = ComPanel()
        infoPanel = InfoPanel()
        editPanel = EditPanel()
        rangePanel = RangePanel()

        box.addWidget(comPanel)
        box.addWidget(infoPanel)
        box.addWidget(editPanel)
        box.addWidget(rangePanel)
        box.addWidget(versionLabel, stretch=1, alignment=Qt.AlignmentFlag.AlignBottom)

        box.addStretch()
        box.setDirection(QVBoxLayout.Direction.TopToBottom)
        self.setWindowTitle(windowLabel)
        self.setFixedSize(windowWidth, windowHeight)
        self.mainWidget.setLayout(box)

    def init(self):
        self.show()

    def closeEvent(self, event):
        if Confirm("Закрыть программу?").cancel():
            event.ignore()
            return
        self.com.disconnect()
        event.accept()
