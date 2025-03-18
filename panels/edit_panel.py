import struct

from PyQt6.QtWidgets import QWidget, QGridLayout

from com.communication import CommStatus
from com.hart import unitDict, HARTconnector, MessageType, getUnitKeyFromValue
from misc.types import LineType
from misc.updater import Updater
from widgets.dialog import Confirm
from widgets.edit_line import EditLine
from misc import di


class EditPanel(QWidget, Updater):
    def __init__(self):
        super().__init__()
        self.com = di.Container.com()
        self.comDict = di.Container.comDict()
        self.grid = QGridLayout()
        self.row = 0
        self.column = 0
        self.unitLine = EditLine("Единица измерения: ", LineType.UNIT, editValue=unitDict.keys(), unitEn=False)
        self.tagLine = EditLine("Метка (тег): ", LineType.TAG, editLen=8, unitEn=False)
        self.mA4Line = EditLine("Нижн. предел (4мА): ", LineType.mA4, editNumeric=True)
        self.mA20Line = EditLine("Верхн. предел (20мА)", LineType.mA20, editNumeric=True)

        self.addWidgets(self.unitLine)
        self.addWidgets(self.mA4Line)
        self.row += 1
        self.column = 0
        self.addWidgets(self.tagLine)
        self.addWidgets(self.mA20Line)

        self.setLayout(self.grid)
        self.startUpdate()

        self.unitLine.clicked(self.unitApply)
        self.tagLine.clicked(self.tagApply)
        self.mA4Line.clicked(lambda: self.currentRangeApply(lowerEn=True))
        self.mA20Line.clicked(lambda: self.currentRangeApply(upperEn=True))

    def unitApply(self):
        if Confirm(f"Применить единицы '{self.unitLine.getEditValue()}'?").cancel():
            return
        try:
            unitStr = unitDict[self.unitLine.getEditValue()]
        except:
            unitStr = "unknown"
        self.com.send(MessageType.WRITE_PV_UNITS, [unitStr])

    def tagApply(self):
        if Confirm(f"Применить тег '{self.tagLine.getEditValue()}'?").cancel():
            return
        if self.comDict.getValue("descriptorDate") is None:
            return
        try:
            tagStr = self.tagLine.getEditValue().upper()
        except:
            tagStr = "-" * 8
        if len(tagStr) < 8:
            tagStr += " " * (8 - len(tagStr))
        data = bytearray()
        data.extend(HARTconnector.getTreeBytesFromFourSymbols(tagStr[0:4]))
        data.extend(HARTconnector.getTreeBytesFromFourSymbols(tagStr[4:]))
        data.extend(self.comDict.getValue("descriptorDate"))
        self.com.send(MessageType.WRITE_TAG_DESCRIPTOR_DATE, data)

    def currentRangeApply(self, upperEn=False, lowerEn=False):
        confirmText = "???"
        mA4EditVal = self.mA4Line.getEditValue()
        mA20EditVal = self.mA20Line.getEditValue()
        if upperEn:
            confirmText = f"Применить значение '{mA20EditVal}' для 20мА?"
        elif lowerEn:
            confirmText = f"Применить значение '{mA4EditVal}' для 4мА?"

        if Confirm(confirmText).cancel():
            return
        if (self.comDict.getValue("rangeUnit") is None) or (self.comDict.getValue("4mA") is None) or (self.comDict.getValue("20mA") is None):
            return

        try:
            lowerValue = float(mA4EditVal) if lowerEn else self.comDict.getValue("4mA")
            upperValue = float(mA20EditVal) if upperEn else self.comDict.getValue("20mA")
        except:
            return

        data = bytearray()
        data.append(self.comDict.getValue("rangeUnit"))
        data.extend(bytearray(struct.pack(">f", upperValue)))
        data.extend(bytearray(struct.pack(">f", lowerValue)))
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
        comError = self.com.status != CommStatus.CONNECT
        unitStr = getUnitKeyFromValue(self.comDict.getValue("unit"))
        rangeUnitStr = getUnitKeyFromValue(self.comDict.getValue("rangeUnit"))
        self.unitLine.setValue(unitStr, errorStatus=comError)
        self.tagLine.setValue(self.comDict.getValue("tag"), errorStatus=comError)
        self.mA4Line.setValue(self.comDict.getValue("4mA"), errorStatus=comError)
        self.mA4Line.setUnit(rangeUnitStr)
        self.mA20Line.setValue(self.comDict.getValue("20mA"), errorStatus=comError)
        self.mA20Line.setUnit(rangeUnitStr)
        self.unitLine.checkDifference()
        self.tagLine.checkDifference()
        self.mA4Line.checkDifference(numeric=True)
        self.mA20Line.checkDifference(numeric=True)
        if self.com.firstTimeDataReady():
            self.unitLine.setEditValue(unitStr)
            self.tagLine.setEditValue(self.comDict.getValue("tag"))
            self.mA4Line.setEditValue(self.comDict.getValue("4mA"))
            self.mA20Line.setEditValue(self.comDict.getValue("20mA"))
