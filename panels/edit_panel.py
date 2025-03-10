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
        self._4mALine = EditLine("4мА: ", LineType._4mA)
        self._20mALine = EditLine("20мА", LineType._20mA)
        zeroButton = Button("Обнулить датчик")

        self.addWidgets(self.unitLine)
        self.addWidgets(self._4mALine)
        self.row += 1
        self.column = 0
        self.addWidgets(self.tagLine)
        self.addWidgets(self._20mALine)
        self.row += 1
        self.grid.addWidget(zeroButton, self.row, 0)

        self.setLayout(self.grid)
        self.startUpdate()

        self.unitLine.clicked(self.unitApply)
        self.tagLine.clicked(self.tagApply)
        self._4mALine.clicked(self.currentRangeApply)

    def unitApply(self):
        self.com.send(MessageType.WRITE_PV_UNITS, [unitDict[self.unitLine.getEditValue()]])

    def tagApply(self):
        if self.comDict.getValue("descriptorDate") is None:
            return
        tagStr = self.tagLine.getEditValue().upper()
        if len(tagStr) < 8:
            tagStr += " " * (8 - len(tagStr))
        data = bytearray()
        data.extend(HARTconnector.getTreeBytesFromFourSymbols(tagStr[0:4]))
        data.extend(HARTconnector.getTreeBytesFromFourSymbols(tagStr[4:]))
        data.extend(self.comDict.getValue("descriptorDate"))
        self.com.send(MessageType.WRITE_TAG_DESCRIPTOR_DATE, data)

    def currentRangeApply(self):
        if (self.comDict.getValue("unit") is None) or (self.comDict.getValue("4mA") is None) or (self.comDict.getValue("20mA") is None):
            return
        data = bytearray()
        data.append(self.comDict.getValue("unit"))
        lower = float(self._4mALine.getEditValue())
        upper = float(self._20mALine.getEditValue())
        data.extend(bytearray(struct.pack("f", upper)))
        data.extend(bytearray(struct.pack("f", lower)))
        self.com.send(MessageType.WRITE_RANGE_VALUES, data)

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
