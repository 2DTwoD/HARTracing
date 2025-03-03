from enum import Enum

from PyQt6.QtCore import Qt


class LineType(Enum):
    UNIT = 0
    TAG = 1
    _4mA = 2
    _20mA = 3


class Align(Enum):
    LEFT = Qt.AlignmentFlag.AlignLeft
    RIGHT = Qt.AlignmentFlag.AlignRight
    TOP = Qt.AlignmentFlag.AlignTop
    BOTTOM = Qt.AlignmentFlag.AlignBottom
