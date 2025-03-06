from misc.types import Align
from widgets.label import Label

valueUpdateColorList = ["lightgray", "blue"]

class MonitorLine(list):
    def __init__(self, labelText, color="black", background="white"):
        super().__init__()
        self.append(Label(labelText, align=Align.RIGHT_VCENTER))
        self.value = Label("XXX", transparent=False, color=color, background=background, border=True,
                           borderColor=valueUpdateColorList[0], align=Align.VCENTER)
        self.append(self.value)

    def getLabelWidget(self):
        return self[0]

    def getValueWidget(self):
        return self[1]

    def setValue(self, value):
        newVal = str(value)
        condition = newVal != self.value.text()
        if condition:
            self.value.setText(newVal)
        self.value.setBorderColor(valueUpdateColorList[int(condition)])

    def setValueColor(self, color: str):
        self.value.setColor(color)

    def setValueBackground(self, color: str):
        self.value.setBackground(color)
