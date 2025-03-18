from misc.types import LineType
from widgets.button import Button
from widgets.combo import ComboBox
from widgets.monitor_line import MonitorLine
from widgets.text_field import TextField

differenceColorList = ["white", "yellow"]


class EditLine(MonitorLine):
    def __init__(self, labelText, lineType: LineType, color="black", background="white", editValue=None, editLen=None,
                 editNumeric=False, unitEn=True):
        super().__init__(labelText, color=color, background=background, unitEn=unitEn)

        if lineType == LineType.UNIT:
            self.editField = ComboBox()
            editValue = [""] if editValue is None else editValue
            self.editField.addItems(editValue)
        else:
            editValue = "" if editValue is None else editValue
            self.editField = TextField(editValue, length=editLen, numeric=editNumeric)
        self.editField.setMaximumWidth(100)
        self.applyButton = Button("Применить")

        self.append(self.editField)
        self.append(self.applyButton)

    def getEditValue(self):
        if type(self.editField) is ComboBox:
            return self.editField.currentText()
        else:
            return self.editField.text()

    def setEditValue(self, value):
        if value is None:
            return
        if type(self.editField) is ComboBox:
            index = self.editField.findText(str(value))
            if index != -1:
                self.editField.setCurrentIndex(index)
        else:
            self.editField.setText(str(value))

    def checkDifference(self, numeric=False):
        editVal = None
        val = None
        if numeric:
            try:
                editVal = float(self.getEditValue())
            except:
                pass
            try:
                val = float(self.getValue())
            except:
                pass
        else:
            editVal = self.getEditValue().strip().lower()
            val = self.getValue().strip().lower()
        if editVal is not None and val is not None and editVal == val:
            self.editField.setBackground(differenceColorList[0])
        else:
            self.editField.setBackground(differenceColorList[1])

    def getEditWidget(self):
        return self[2]

    def getApplyWidget(self):
        return self[3]

    def clicked(self, action):
        return self.applyButton.clicked.connect(action)
