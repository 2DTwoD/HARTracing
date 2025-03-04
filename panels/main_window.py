from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout

from misc.types import LineType
from panels.com_panel import ComPanel
from panels.edit_panel import EditPanel
from panels.info_panel import InfoPanel
from widgets.button import Button
from widgets.edit_line import EditLine


class MainWindow(QMainWindow):
    def __init__(self, version="v0.0.0", windowWidth=100, windowHeight=100, windowLabel="App"):
        super().__init__()

        self.mainWidget = QWidget(parent=self)
        self.mainWidget.setFixedSize(windowWidth, windowHeight)
        box = QVBoxLayout()
        versionLabel = QLabel(version, parent=self)
        self.comPanel = ComPanel()
        self.infoPanel = InfoPanel()
        self.editPanel = EditPanel(width=int(windowWidth / 2))

        box.addWidget(self.comPanel)
        box.addWidget(self.infoPanel)
        box.addWidget(self.editPanel)
        box.addWidget(versionLabel, stretch=1, alignment=Qt.AlignmentFlag.AlignBottom)

        box.addStretch()
        box.setDirection(QVBoxLayout.Direction.TopToBottom)
        self.setWindowTitle(windowLabel)
        self.setFixedSize(windowWidth, windowHeight)
        self.mainWidget.setLayout(box)


    def init(self):
        self.show()

    def closeEvent(self, event):
        # if Confirm("Закрыть программу?").cancel():
        #     event.ignore()
        #     return
        event.accept()

