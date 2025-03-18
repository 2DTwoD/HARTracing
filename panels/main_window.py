from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from misc.types import Align
from panels.com_panel import ComPanel
from panels.edit_panel import EditPanel
from panels.info_panel import InfoPanel
from panels.range_panel import RangePanel
from widgets.dialog import Confirm
from misc import di
from widgets.label import Label


class MainWindow(QMainWindow):
    def __init__(self, version="v0.0.0", windowWidth=100, windowHeight=100, windowLabel="App"):
        super().__init__()
        self.com = di.Container.com()

        self.mainWidget = QWidget(parent=self)
        self.mainWidget.setFixedSize(windowWidth, windowHeight)

        box = QVBoxLayout()
        versionLabel = Label(version, parent=self)
        comPanel = ComPanel()
        infoPanel = InfoPanel()
        editPanel = EditPanel()
        rangePanel = RangePanel()

        box.addWidget(MainWindow.getHeader("Быстрая настройка датчиков, поддерживающих протокол HART"))
        box.addWidget(self.getSpace())
        box.addWidget(comPanel)
        box.addWidget(self.getSpace())
        box.addWidget(MainWindow.getHeader("Измеренное значение, выход и статусы:"))
        box.addWidget(self.getSpace())
        box.addWidget(infoPanel)
        box.addWidget(self.getSpace())
        box.addWidget(MainWindow.getHeader("Параметры для редактирования (единицы, тег, разгон, калибровка):"))
        box.addWidget(self.getSpace())
        box.addWidget(editPanel)
        box.addWidget(rangePanel)
        box.addWidget(self.getSpace())
        box.addWidget(versionLabel, stretch=1, alignment=Qt.AlignmentFlag.AlignBottom)

        box.addStretch()
        box.setDirection(QVBoxLayout.Direction.TopToBottom)
        self.setWindowTitle(windowLabel)
        self.setFixedSize(windowWidth, windowHeight)
        self.mainWidget.setLayout(box)

    @staticmethod
    def getSpace():
        return Label("", background="lightgray", align=Align.CENTER, transparent=False, height=10)

    @staticmethod
    def getHeader(text: str):
        return Label(text, align=Align.CENTER, color="gray", fontSize=14, bold=True)

    def init(self):
        self.show()

    def closeEvent(self, event):
        if Confirm("Закрыть программу?").cancel():
            event.ignore()
            return
        self.com.disconnect()
        event.accept()
