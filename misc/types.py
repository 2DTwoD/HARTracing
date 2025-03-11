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
    READ_UNIQUE_IDENTIFIER = {"id": 0, "commandNumber": 0, "dataLen": 12, "deleteFlag": True}
    READ_PRIMARY_VARIABLE = {"id": 1, "commandNumber": 1, "dataLen": 5, "deleteFlag": False}
    READ_CURRENT_AND_PERCENT_OF_RANGE = {"id": 2, "commandNumber": 2, "dataLen": 8, "deleteFlag": False}
    READ_TAG_DESCRIPTOR_DATE = {"id": 3, "commandNumber": 13, "dataLen": 21, "deleteFlag": True}
    READ_OUTPUT_INFORMATION = {"id": 4, "commandNumber": 15, "dataLen": 17, "deleteFlag": True}
    WRITE_TAG_DESCRIPTOR_DATE = {"id": 5, "commandNumber": 18, "dataLen": 21, "deleteFlag": True}
    WRITE_RANGE_VALUES = {"id": 6, "commandNumber": 35, "dataLen": 9, "deleteFlag": True}
    SET_UPPER_RANGE_VALUE = {"id": 7, "commandNumber": 36, "dataLen": 0, "deleteFlag": True}
    SET_LOWER_RANGE_VALUE = {"id": 8, "commandNumber": 37, "dataLen": 0, "deleteFlag": True}
    SET_TRIM_PV_ZERO = {"id": 9, "commandNumber": 43, "dataLen": 0, "deleteFlag": True}
    WRITE_PV_UNITS = {"id": 10, "commandNumber": 44, "dataLen": 1, "deleteFlag": True}
