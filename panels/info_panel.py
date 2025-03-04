from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from misc.types import Align
from widgets.label import Label
from widgets.monitor_line import MonitorLine


class InfoPanel(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()

        self.sensorStatusMonitor = MonitorLine("Статус датчика:")
        self.hartStatusMonitor = MonitorLine("Статус связи по HART:")
        self.idMonitor = MonitorLine("Код производителя датчика:")
        self.typeMonitor = MonitorLine("Код модели датчика:")
        self.softMonitor = MonitorLine("Версия ПО:")
        self.hardMonitor = MonitorLine("Аппаратная версия:")
        self.measureMonitor = MonitorLine("Измеренное значние:")
        self.currentMonitor = MonitorLine("Токовый выход (мА):")

        row = 0
        grid.addWidget(self.idMonitor.getLabelWidget(), row, 0)
        grid.addWidget(self.idMonitor.getValueWidget(), row, 1)
        grid.addWidget(self.typeMonitor.getLabelWidget(), row, 2)
        grid.addWidget(self.typeMonitor.getValueWidget(), row, 3)
        grid.addWidget(self.softMonitor.getLabelWidget(), row, 4)
        grid.addWidget(self.softMonitor.getValueWidget(), row, 5)
        grid.addWidget(self.hardMonitor.getLabelWidget(), row, 6)
        grid.addWidget(self.hardMonitor.getValueWidget(), row, 7)
        row += 1
        grid.addWidget(self.measureMonitor.getLabelWidget(), row, 0)
        grid.addWidget(self.measureMonitor.getValueWidget(), row, 1)
        grid.addWidget(self.currentMonitor.getLabelWidget(), row, 2)
        grid.addWidget(self.currentMonitor.getValueWidget(), row, 3)
        grid.addWidget(self.sensorStatusMonitor.getLabelWidget(), row, 4)
        grid.addWidget(self.sensorStatusMonitor.getValueWidget(), row, 5)
        grid.addWidget(self.hartStatusMonitor.getLabelWidget(), row, 6)
        grid.addWidget(self.hartStatusMonitor.getValueWidget(), row, 7)

        self.setLayout(grid)
