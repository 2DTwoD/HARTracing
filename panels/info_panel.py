from PyQt6.QtWidgets import QWidget, QGridLayout

from com.communication import CommStatus
from misc.updater import Updater
from widgets.monitor_line import MonitorLine
from misc import di

statusColorList = ["green", "red"]
statusTextList = ["Норм.", "Ошибка"]


class InfoPanel(QWidget, Updater):
    def __init__(self):
        super().__init__()
        self.com = di.Container.com()
        self.comDict = di.Container.comDict()
        grid = QGridLayout()

        self.sensorStatusMonitor = MonitorLine("Статус датчика:", color="white",
                                               background=statusColorList[0])
        self.hartStatusMonitor = MonitorLine("Статус связи по HART:", color="white",
                                             background=statusColorList[0])
        self.measureMonitor = MonitorLine("Измеренное значение:")
        self.currentMonitor = MonitorLine("Выход датчика (мА):")
        self.percentMonitor = MonitorLine("Выход датчика (%):")
        self.calcMonitor = MonitorLine("Выход расчетный:")

        row = 0
        grid.addWidget(self.sensorStatusMonitor.getLabelWidget(), row, 0)
        grid.addWidget(self.sensorStatusMonitor.getValueWidget(), row, 1)
        grid.addWidget(self.hartStatusMonitor.getLabelWidget(), row, 2)
        grid.addWidget(self.hartStatusMonitor.getValueWidget(), row, 3)

        row += 1
        grid.addWidget(self.measureMonitor.getLabelWidget(), row, 0)
        grid.addWidget(self.measureMonitor.getValueWidget(), row, 1)
        grid.addWidget(self.currentMonitor.getLabelWidget(), row, 2)
        grid.addWidget(self.currentMonitor.getValueWidget(), row, 3)
        grid.addWidget(self.percentMonitor.getLabelWidget(), row, 4)
        grid.addWidget(self.percentMonitor.getValueWidget(), row, 5)
        grid.addWidget(self.calcMonitor.getLabelWidget(), row, 6)
        grid.addWidget(self.calcMonitor.getValueWidget(), row, 7)

        self.setLayout(grid)
        self.startUpdate()

    def updateAction(self):
        comError = self.com.status != CommStatus.CONNECT
        self.sensorStatusMonitor.setValue(statusTextList[int(self.comDict.get("sensorStatus"))], errorStatus=comError)
        self.sensorStatusMonitor.setValueBackground(statusColorList[int(self.comDict.get("sensorStatus"))])
        self.hartStatusMonitor.setValue(statusTextList[int(self.comDict.get("hartStatus"))], errorStatus=comError)
        self.hartStatusMonitor.setValueBackground(statusColorList[int(self.comDict.get("hartStatus"))])
        self.measureMonitor.setValue(self.comDict.get("measure"), errorStatus=comError)
        self.currentMonitor.setValue(self.comDict.get("current"), errorStatus=comError)
        self.percentMonitor.setValue(self.comDict.get("percent"), errorStatus=comError)
        lowerLim = self.comDict.get("4mA")
        calcValue = lowerLim + (self.comDict.get("20mA") - lowerLim) * self.comDict.get("percent") / 100.0
        self.calcMonitor.setValue(round(calcValue, 2), errorStatus=comError)
