from PyQt6.QtWidgets import QComboBox

from widgets.style import CommonStyle, ColorStyle


class ComboBox(CommonStyle, ColorStyle, QComboBox):
    def __init__(self, parent=None, color="black", background="white", transparent=False,
                 width=None, height=None, fontSize=None, bold=False):
        QComboBox.__init__(self, parent=parent)
        CommonStyle.__init__(self, widget=self, width=width, height=height, fontSize=fontSize, bold=bold)
        ColorStyle.__init__(self, widget=self, color=color, background=background, transparent=transparent)