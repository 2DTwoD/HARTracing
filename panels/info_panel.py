from PyQt6.QtWidgets import QWidget, QGridLayout

from com.communication import CommStatus
from com.hart import getUnitKeyFromValue
from misc.updater import Updater
from widgets.monitor_line import MonitorLine
from widgets.status import Status
from misc import di

statusTextList = ["Норм.", "Ошибка"]


class InfoPanel(QWidget, Updater):
    def __init__(self):
        super().__init__()
        self.com = di.Container.com()
        self.comDict = di.Container.comDict()
        grid = QGridLayout()

        self.sensorStatus = Status("Статус датчика:",
                                   ["Перв. перем. вышла за пределы",
                                    "Втор. перем. вышла за пределы",
                                    "Аналог. вых. превыш.",
                                    "Аналог. вых. зафикс.",
                                    "Больше статусов доступно",
                                    "Холодный старт",
                                    "Конфиг-ия изменена",
                                    "Неисправн. полевого устр-ва"], 0)

        self.hartStatus = Status("Статус связи по HART:",
                                   ["Переполнение буфера",
                                    "Ошибка связи",
                                    "Ошибка четности по длине",
                                    "Ошибка кадра",
                                    "Перезапись данных",
                                    "Ошибка вертикальной четности"], 1)

        self.measureMonitor = MonitorLine("Измер. знач.:")
        self.currentMonitor = MonitorLine("Выход датчика (мА):")
        self.percentMonitor = MonitorLine("Выход датчика (%):")
        self.calcMonitor = MonitorLine("Выход расчетный:")

        row = 0
        grid.addWidget(self.sensorStatus[0], row, 0, 1, 4)
        grid.addWidget(self.hartStatus[0], row, 4, 1, 4)
        row += 1
        grid.addWidget(self.sensorStatus[1], row, 0, 1, 2)
        grid.addWidget(self.sensorStatus[2], row, 2, 1, 2)
        grid.addWidget(self.hartStatus[1], row, 4, 1, 2)
        grid.addWidget(self.hartStatus[2], row, 6, 1, 2)
        row += 1
        grid.addWidget(self.sensorStatus[3], row, 0, 1, 2)
        grid.addWidget(self.sensorStatus[4], row, 2, 1, 2)
        grid.addWidget(self.hartStatus[3], row, 4, 1, 2)
        grid.addWidget(self.hartStatus[4], row, 6, 1, 2)
        row += 1
        grid.addWidget(self.sensorStatus[5], row, 0, 1, 2)
        grid.addWidget(self.sensorStatus[6], row, 2, 1, 2)
        grid.addWidget(self.hartStatus[5], row, 4, 1, 2)
        grid.addWidget(self.hartStatus[6], row, 6, 1, 2)
        row += 1
        grid.addWidget(self.sensorStatus[7], row, 0, 1, 2)
        grid.addWidget(self.sensorStatus[8], row, 2, 1, 2)
        row += 1
        grid.addWidget(self.measureMonitor.getLabelWidget(), row, 0)
        grid.addWidget(self.measureMonitor.getValueWidget(), row, 1)
        grid.addWidget(self.currentMonitor.getLabelWidget(), row, 2)
        grid.addWidget(self.currentMonitor.getValueWidget(), row, 3)
        grid.addWidget(self.percentMonitor.getLabelWidget(), row, 4)
        grid.addWidget(self.percentMonitor.getValueWidget(), row, 5)
        grid.addWidget(self.calcMonitor.getLabelWidget(), row, 6)
        grid.addWidget(self.calcMonitor.getValueWidget(), row, 7)

        self.currentMonitor.setUnit("мА")
        self.percentMonitor.setUnit("%")

        self.setLayout(grid)
        self.startUpdate()

    def updateAction(self):
        comError = self.com.status != CommStatus.CONNECT
        unitStr = getUnitKeyFromValue(self.comDict.getValue("unit"))
        rangeUnitStr = getUnitKeyFromValue(self.comDict.getValue("rangeUnit"))
        self.sensorStatus.update(self.comDict.get("sensorStatus"), errorStatus=comError)
        self.hartStatus.update(self.comDict.get("hartStatus"), errorStatus=comError)
        self.measureMonitor.setValue(self.comDict.get("measure"), errorStatus=comError)
        self.measureMonitor.setUnit(unitStr)
        self.currentMonitor.setValue(self.comDict.get("current"), errorStatus=comError)
        self.percentMonitor.setValue(self.comDict.get("percent"), errorStatus=comError)

        lowerLim = self.comDict.get("4mA")
        upperLim = self.comDict.get("20mA")
        percent = self.comDict.get("percent")
        if lowerLim is None or upperLim is None or percent is None:
            calcValue = 0
        else:
            calcValue = lowerLim + (upperLim - lowerLim) * percent / 100.0
        self.calcMonitor.setValue(round(calcValue, 2), errorStatus=comError)
        self.calcMonitor.setUnit(rangeUnitStr)
