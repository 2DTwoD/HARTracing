from PyQt6.QtWidgets import QWidget, QHBoxLayout

from misc.types import Align
from widgets.label import Label

valueUpdateColorList = ["lightgray", "blue", "red"]


class MonitorLine(list):
    def __init__(self, labelText, color="black", background="white", unitEn=True):
        super().__init__()
        self.append(Label(labelText, align=Align.RIGHT_VCENTER))
        valueUnit = QWidget()
        box = QHBoxLayout()

        self.value = Label("значение", transparent=False, color=color, background=background, border=True,
                           borderColor=valueUpdateColorList[0], align=Align.VCENTER)
        self.unit = Label("единица", color="gray")

        box.addWidget(self.value, stretch=1)
        if unitEn:
            box.addWidget(self.unit)
        valueUnit.setLayout(box)
        self.append(valueUnit)

    def getLabelWidget(self):
        return self[0]

    def getValueWidget(self):
        return self[1]

    def setValue(self, value, errorStatus=False):
        newVal = str(value)
        condition = newVal != self.value.text()
        if condition:
            self.value.setText(newVal)
        if errorStatus:
            self.value.setBorderColor(valueUpdateColorList[-1])
        else:
            self.value.setBorderColor(valueUpdateColorList[int(condition)])

    def setUnit(self, unit):
        if unit is None:
            return
        self.unit.setText(unit)

    def getValue(self):
        return self.value.text()

    def setValueColor(self, color: str):
        self.value.setColor(color)

    def setValueBackground(self, color: str):
        self.value.setBackground(color)
