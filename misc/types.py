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
    CENTER = Qt.AlignmentFlag.AlignCenter
    VCENTER = Qt.AlignmentFlag.AlignVCenter
    RIGHT_VCENTER = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight


class CommStatus(Enum):
    CONNECT = "V"
    DISCONNECT = "X"
    LINK_ERROR = "Ошибка связи"
    RECEIVE_ERROR = "Ошибка передачи"


class MessageType(Enum):
    READ_UNIQUE_IDENTIFIER = {"id": 0, "commandNumber": 0, "dataLen": 12}
    READ_PRIMARY_VARIABLE = {"id": 1, "commandNumber": 1, "dataLen": 5}
    READ_CURRENT_AND_PERCENT_OF_RANGE = {"id": 2, "commandNumber": 2, "dataLen": 8}
    READ_TAG_DESCRIPTOR_DATE = {"id": 3, "commandNumber": 13, "dataLen": 21}
    READ_OUTPUT_INFORMATION = {"id": 4, "commandNumber": 15, "dataLen": 17}
