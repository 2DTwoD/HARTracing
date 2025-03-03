from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton, QComboBox

from misc.types import LineType


class EditLine(QWidget):
    def __init__(self, labelText, lineType: LineType):
        super().__init__()
        self.lineType = lineType
        box = QHBoxLayout()
        label = QLabel(labelText)
        self.curValLabel = QLabel("xxx")
        if lineType == LineType.UNIT:
            self.editField = QComboBox()
        else:
            self.editField = QLineEdit()

        self.editField.setMaximumWidth(100)
        self.applyButton = QPushButton("Применить")

        box.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
        box.addWidget(self.curValLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        box.addWidget(self.editField, alignment=Qt.AlignmentFlag.AlignLeft)
        box.addWidget(self.applyButton, alignment=Qt.AlignmentFlag.AlignLeft)

        box.addStretch()
        box.setDirection(QHBoxLayout.Direction.LeftToRight)

        self.setLayout(box)
