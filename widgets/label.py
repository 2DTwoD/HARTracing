from PyQt6.QtWidgets import QLabel

from misc.types import Align
from widgets.style import CommonStyle, ColorStyle, BorderStyle


class Label(CommonStyle, ColorStyle, BorderStyle, QLabel):
    def __init__(self, text, parent=None, align=Align.LEFT, color="black", background="#F0F0F0", transparent=True,
                 width=None, height=None, fontSize=None, bold=False,
                 border=False, borderWidth=1, borderColor="black"):
        QLabel.__init__(self, text, parent=parent)
        CommonStyle.__init__(self, widget=self, width=width, height=height, fontSize=fontSize, bold=bold)
        ColorStyle.__init__(self, widget=self, color=color, background=background, transparent=transparent)
        BorderStyle.__init__(self, widget=self, border=border, borderWidth=borderWidth, borderColor=borderColor)
        self.setAlignment(align.value)
