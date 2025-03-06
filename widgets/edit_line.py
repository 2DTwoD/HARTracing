from misc.types import LineType
from misc.updater import Updater
from widgets.button import Button
from widgets.combo import ComboBox
from widgets.monitor_line import MonitorLine
from widgets.text_field import TextField


class EditLine(MonitorLine):
    def __init__(self, labelText, lineType: LineType, color="black", background="white"):
        super().__init__(labelText, color=color, background=background)
        self.lineType = lineType

        if lineType == LineType.UNIT:
            self.editField = ComboBox()
        else:
            self.editField = TextField()
        self.editField.setMaximumWidth(100)
        self.applyButton = Button("Применить")

        self.append(self.editField)
        self.append(self.applyButton)

    def getEditWidget(self):
        return self[2]

    def getApplyWidget(self):
        return self[3]
