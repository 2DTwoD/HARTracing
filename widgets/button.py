from PyQt6.QtWidgets import QPushButton

from widgets.style import CommonStyle, ColorStyle


class Button(CommonStyle, ColorStyle, QPushButton):
    def __init__(self, text, parent=None, color="black", background="#F0F0F0", transparent=False,
                 width=None, height=None, fontSize=None, bold=False):
        QPushButton.__init__(self, text, parent=parent)
        CommonStyle.__init__(self, widget=self, width=width, height=height, fontSize=fontSize, bold=bold)
        ColorStyle.__init__(self, widget=self, color=color, background=background, transparent=transparent)
