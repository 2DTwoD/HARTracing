from PyQt6.QtWidgets import QLineEdit

from misc.types import Align
from widgets.style import CommonStyle, ColorStyle, BorderStyle


class TextField(CommonStyle, ColorStyle, BorderStyle, QLineEdit):
    def __init__(self, parent=None, align=Align.LEFT, color="black", background="white", transparent=False,
                 width=None, height=None, fontSize=None, bold=False,
                 border=True, borderWidth=1, borderColor="gray"):
        QLineEdit.__init__(self, parent=parent)
        CommonStyle.__init__(self, widget=self, width=width, height=height, fontSize=fontSize, bold=bold)
        ColorStyle.__init__(self, widget=self, color=color, background=background, transparent=transparent)
        BorderStyle.__init__(self, widget=self, border=border, borderWidth=borderWidth, borderColor=borderColor)
        self.setAlignment(align.value)
