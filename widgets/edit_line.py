from misc.types import LineType
from widgets.button import Button
from widgets.combo import ComboBox
from widgets.monitor_line import MonitorLine
from widgets.text_field import TextField


class EditLine(MonitorLine):
    def __init__(self, labelText, lineType: LineType, color="black", background="white", editValue=None, editLen=None,
                 editNumeric=False):
        super().__init__(labelText, color=color, background=background)

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
        if type(self.editField) is ComboBox:
            index = self.editField.findText(str(value))
            if index != -1:
                self.editField.setCurrentIndex(index)
        else:
            self.editField.setText(str(value))

    def getEditWidget(self):
        return self[2]

    def getApplyWidget(self):
        return self[3]

    def clicked(self, action):
        return self.applyButton.clicked.connect(action)
