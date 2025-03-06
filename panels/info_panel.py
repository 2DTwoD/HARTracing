from PyQt6.QtWidgets import QWidget, QGridLayout

from misc.updater import Updater
from widgets.monitor_line import MonitorLine
from misc import di

statusColorList = ["green", "red"]
statusTextList = ["Норм.", "Ошибка"]


class InfoPanel(QWidget, Updater):
    def __init__(self):
        super().__init__()
        self.comDict = di.Container.comDict()
        grid = QGridLayout()

        self.sensorStatusMonitor = MonitorLine("Статус датчика:", color="white",
                                               background=statusColorList[0])
        self.hartStatusMonitor = MonitorLine("Статус связи по HART:", color="white",
                                             background=statusColorList[0])
        self.manufMonitor = MonitorLine("Код производителя датчика:")
        self.modelMonitor = MonitorLine("Код модели датчика:")
        self.softMonitor = MonitorLine("Версия ПО:")
        self.hardMonitor = MonitorLine("Аппаратная версия:")
        self.measureMonitor = MonitorLine("Измеренное значние:")
        self.currentMonitor = MonitorLine("Токовый выход (мА):")

        row = 0
        grid.addWidget(self.manufMonitor.getLabelWidget(), row, 0)
        grid.addWidget(self.manufMonitor.getValueWidget(), row, 1)
        grid.addWidget(self.modelMonitor.getLabelWidget(), row, 2)
        grid.addWidget(self.modelMonitor.getValueWidget(), row, 3)
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
        self.startUpdate()

    def updateAction(self):
        self.sensorStatusMonitor.setValue(statusTextList[int(self.comDict.get("sensorStatus"))])
        self.sensorStatusMonitor.setValueBackground(statusColorList[int(self.comDict.get("sensorStatus"))])
        self.hartStatusMonitor.setValue(statusTextList[int(self.comDict.get("hartStatus"))])
        self.hartStatusMonitor.setValueBackground(statusColorList[int(self.comDict.get("hartStatus"))])
        self.manufMonitor.setValue(self.comDict.get("manuf"))
        self.modelMonitor.setValue(self.comDict.get("model"))
        self.softMonitor.setValue(self.comDict.get("soft"))
        self.hardMonitor.setValue(self.comDict.get("hard"))
        self.measureMonitor.setValue(self.comDict.get("measure"))
        self.currentMonitor.setValue(self.comDict.get("current"))
