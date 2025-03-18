from misc.types import Align
from widgets.label import Label
from misc import di

statusColorList = ["lightgray", "red"]


class Status(list):
    def __init__(self, headerText: str, statusTextList, shiftMask: int):
        super().__init__()
        self.comDict = di.Container.comDict()
        self.shiftMask = shiftMask
        self.append(Label(headerText, align=Align.CENTER))
        for statusText in statusTextList:
            self.append(Label(statusText, background=statusColorList[0], color="white", border=True,
                              align=Align.VCENTER, borderColor=statusColorList[0], transparent=False))

    def update(self, status, errorStatus=False):
        if status is None:
            status = 0
        for index, widget in enumerate(self[1:]):
            statusBit = status & (1 << (index + self.shiftMask))
            widget.setBackground(statusColorList[statusBit > 0])
            widget.setBorderColor(statusColorList[errorStatus])
