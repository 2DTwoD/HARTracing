from misc.types import Align
from widgets.label import Label


class MonitorLine(list):
    def __init__(self, labelText):
        super().__init__()
        self.append(Label(labelText, align=Align.RIGHT_VCENTER))
        self.value = Label("XXX", transparent=False, background="white", border=True, borderColor="lightgray",
                           align=Align.VCENTER)
        self.append(self.value)

    def getLabelWidget(self):
        return self[0]

    def getValueWidget(self):
        return self[1]
