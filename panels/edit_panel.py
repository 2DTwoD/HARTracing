import struct

from PyQt6.QtWidgets import QWidget, QGridLayout

from com.hart import unitDict, HARTconnector
from misc.types import LineType, MessageType
from misc.updater import Updater
from widgets.button import Button
from widgets.edit_line import EditLine
from misc import di


class EditPanel(QWidget, Updater):
    def __init__(self):
        super().__init__()
        self.comDict = di.Container.comDict()
        self.com = di.Container.com()
        self.grid = QGridLayout()
        self.row = 0
        self.column = 0
        self.unitLine = EditLine("Единица измерения: ", LineType.UNIT, editValue=unitDict.keys())
        self.tagLine = EditLine("Метка (тег): ", LineType.TAG, editLen=8)
        self._4mALine = EditLine("4мА: ", LineType._4mA, editNumeric=True)
        self._20mALine = EditLine("20мА", LineType._20mA, editNumeric=True)
        pvZeroButton = Button("Обнулить датчик")
        zeroButton = Button("Установить 4мА")
        spanButton = Button("Установить 20мА")

        self.addWidgets(self.unitLine)
        self.addWidgets(self._4mALine)
        self.row += 1
        self.column = 0
        self.addWidgets(self.tagLine)
        self.addWidgets(self._20mALine)
        self.row += 1
        self.grid.addWidget(pvZeroButton, self.row, 0)
        self.row += 1
        self.grid.addWidget(zeroButton, self.row, 0)
        self.row += 1
        self.grid.addWidget(spanButton, self.row, 0)

        self.setLayout(self.grid)
        self.startUpdate()

        self.unitLine.clicked(self.unitApply)
        self.tagLine.clicked(self.tagApply)
        self._4mALine.clicked(lambda: self.currentRangeApply(lowerEn=True))
        self._20mALine.clicked(lambda: self.currentRangeApply(upperEn=True))
        pvZeroButton.clicked.connect(self.setPvZero)
        zeroButton.clicked.connect(self.setZero)
        spanButton.clicked.connect(self.setSpan)

    def unitApply(self):
        try:
            unitStr = unitDict[self.unitLine.getEditValue()]
        except:
            unitStr = "unknown"
        self.com.send(MessageType.WRITE_PV_UNITS, [unitStr])

    def tagApply(self):
        if self.comDict.getValue("descriptorDate") is None:
            return
        try:
            tagStr = self.tagLine.getEditValue().upper()
        except:
            tagStr = "-" * 8
        tagStr = self.tagLine.getEditValue().upper()
        if len(tagStr) < 8:
            tagStr += " " * (8 - len(tagStr))
        data = bytearray()
        data.extend(HARTconnector.getTreeBytesFromFourSymbols(tagStr[0:4]))
        data.extend(HARTconnector.getTreeBytesFromFourSymbols(tagStr[4:]))
        data.extend(self.comDict.getValue("descriptorDate"))
        self.com.send(MessageType.WRITE_TAG_DESCRIPTOR_DATE, data)

    def currentRangeApply(self, upperEn=False, lowerEn=False):
        if (self.comDict.getValue("unit") is None) or (self.comDict.getValue("4mA") is None) or (self.comDict.getValue("20mA") is None):
            return
        data = bytearray()
        data.append(self.comDict.getValue("unit"))
        try:
            lowerValue = float(self._4mALine.getEditValue()) if lowerEn else self.comDict.getValue("4mA")
            upperValue = float(self._20mALine.getEditValue()) if upperEn else self.comDict.getValue("20mA")
        except:
            return
        data.extend(bytearray(struct.pack(">f", upperValue)))
        data.extend(bytearray(struct.pack(">f", lowerValue)))
        self.com.send(MessageType.WRITE_RANGE_VALUES, data)

    def setPvZero(self):
        self.com.send(MessageType.SET_TRIM_PV_ZERO)

    def setZero(self):
        self.com.send(MessageType.SET_LOWER_RANGE_VALUE)

    def setSpan(self):
        self.com.send(MessageType.SET_UPPER_RANGE_VALUE)

    def addRow(self, line: EditLine):
        self.grid.addWidget(line.getLabelWidget(), self.row, 0)
        self.grid.addWidget(line.getValueWidget(), self.row, 1)
        self.grid.addWidget(line.getEditWidget(), self.row, 2)
        self.grid.addWidget(line.getApplyWidget(), self.row, 3)
        self.row += 1

    def addWidgets(self, line: EditLine):
        self.grid.addWidget(line.getLabelWidget(), self.row, self.column)
        self.column += 1
        self.grid.addWidget(line.getValueWidget(), self.row, self.column)
        self.column += 1
        self.grid.addWidget(line.getEditWidget(), self.row, self.column)
        self.column += 1
        self.grid.addWidget(line.getApplyWidget(), self.row, self.column)
        self.column += 1

    def updateAction(self):
        unitStr = "Не определен"
        for key, val in unitDict.items():
            if val == self.comDict.getValue("unit"):
                unitStr = key
                break
        self.unitLine.setValue(unitStr)
        self.tagLine.setValue(self.comDict.getValue("tag"))
        self._4mALine.setValue(self.comDict.getValue("4mA"))
        self._20mALine.setValue(self.comDict.getValue("20mA"))
