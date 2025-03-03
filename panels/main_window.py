from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton

from misc.types import LineType
from panels.com_panel import ComPanel
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
        self.unitLine = EditLine("Единица измерения: ", LineType.UNIT)
        self.tagLine = EditLine("Метка (тег): ", LineType.TAG)
        self._4mALine = EditLine("4мА: ", LineType._4mA)
        self._20mALine = EditLine("20мА", LineType._20mA)
        self.zeroButton = Button("Обнулить датчик")

        box.addWidget(self.comPanel)
        box.addWidget(self.infoPanel)
        box.addWidget(self.unitLine)
        box.addWidget(self.tagLine)
        box.addWidget(self._4mALine)
        box.addWidget(self._20mALine)
        box.addWidget(self.zeroButton)
        box.addWidget(versionLabel)

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

