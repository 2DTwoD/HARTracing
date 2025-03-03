from PyQt6.QtWidgets import QWidget

from widgets.font import Font


def getDictFromStyleSheet(styleSheet: str):
    data = {}
    for item in styleSheet.split(";")[:-1]:
        key, value = item.split(":")
        data[key] = value
    return data


def getStyleSheetFromDict(dictionary: dict):
    styleSheet = ""
    for key, value in dictionary.items():
        styleSheet += f"{str(key)}:{str(value)};"
    return styleSheet


class CommonStyle:
    def __init__(self, widget: QWidget, width=None, height=None, fontSize=None, bold=False):
        self.widget = widget

        self.widget.setFont(Font(fontSize, bold))
        if width is not None:
            self.widget.setMaximumWidth(width)
        if height is not None:
            self.widget.setMaximumHeight(height)


class ColorStyle:
    def __init__(self, widget: QWidget, color="black", background="#F0F0F0", transparent=False):
        self.widget = widget
        self.color = color
        self.background = background
        if transparent:
            self.background = "transparent"
        self._updateColorSheet()

    def setColor(self, color):
        self.color = color
        self._updateColorSheet()

    def setBackground(self, color):
        self.background = color
        self._updateColorSheet()

    def _updateColorSheet(self):
        styles = getDictFromStyleSheet(self.widget.styleSheet())
        styles["color"] = self.color
        styles["background"] = self.background
        self.widget.setStyleSheet(getStyleSheetFromDict(styles))


class BorderStyle:
    def __init__(self, widget: QWidget, border=False, borderWidth=1, borderColor="black"):
        self.widget = widget
        self.border = border
        self.borderWidth = borderWidth
        self.borderColor = borderColor

        self._updateBorderSheet()

    def setBorder(self, value):
        self.border = value
        self._updateBorderSheet()

    def setBorderColor(self, color):
        self.borderColor = color
        self._updateBorderSheet()

    def setBorderWidth(self, width):
        self.borderWidth = width
        self._updateBorderSheet()

    def _updateBorderSheet(self):
        styles = getDictFromStyleSheet(self.widget.styleSheet())
        styles["border-style"] = "solid" if self.border else "none"
        styles["border-width"] = f"{self.borderWidth}px"
        styles["border-color"] = self.borderColor
        self.widget.setStyleSheet(getStyleSheetFromDict(styles))

