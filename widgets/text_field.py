from PyQt6.QtWidgets import QLineEdit

from misc.types import Align
from widgets.style import CommonStyle, ColorStyle, BorderStyle


class TextField(CommonStyle, ColorStyle, BorderStyle, QLineEdit):
    def __init__(self, text, parent=None, align=Align.LEFT, color="black", background="white", transparent=False,
                 width=None, height=None, fontSize=None, bold=False,
                 border=True, borderWidth=1, borderColor="gray", length=None):
        QLineEdit.__init__(self, text, parent=parent)
        CommonStyle.__init__(self, widget=self, width=width, height=height, fontSize=fontSize, bold=bold)
        ColorStyle.__init__(self, widget=self, color=color, background=background, transparent=transparent)
        BorderStyle.__init__(self, widget=self, border=border, borderWidth=borderWidth, borderColor=borderColor)
        if length is not None:
            self.setMaxLength(length)
        # if numeric:
        #     self.setValidator(QIntValidator(minNum, maxNum, self))
        self.setAlignment(align.value)
