from enum import Enum

from PyQt6.QtCore import Qt


class LineType(Enum):
    UNIT = 0
    TAG = 1
    mA4 = 2
    mA20 = 3


class Align(Enum):
    LEFT = Qt.AlignmentFlag.AlignLeft
    RIGHT = Qt.AlignmentFlag.AlignRight
    TOP = Qt.AlignmentFlag.AlignTop
    BOTTOM = Qt.AlignmentFlag.AlignBottom
    CENTER = Qt.AlignmentFlag.AlignCenter
    VCENTER = Qt.AlignmentFlag.AlignVCenter
    RIGHT_VCENTER = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight
