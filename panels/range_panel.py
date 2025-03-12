from PyQt6.QtWidgets import QWidget, QHBoxLayout

from misc import di
from misc.types import MessageType
from widgets.button import Button
from widgets.dialog import Confirm


class RangePanel(QWidget):
    def __init__(self):
        super().__init__()
        self.com = di.Container.com()
        box = QHBoxLayout()

        pvZeroButton = Button("Обнулить датчик (PV Trim zero)")
        zeroButton = Button("Установить 4мА (OUT zero)")
        spanButton = Button("Установить 20мА (OUT span)")

        box.addWidget(pvZeroButton)
        box.addWidget(zeroButton)
        box.addWidget(spanButton)

        pvZeroButton.clicked.connect(self.setPvZero)
        zeroButton.clicked.connect(self.setZero)
        spanButton.clicked.connect(self.setSpan)

        self.setLayout(box)

    def setPvZero(self):
        if Confirm("Обнулить датчик?").cancel():
            return
        self.com.send(MessageType.SET_TRIM_PV_ZERO)

    def setZero(self):
        if Confirm("Установить текущее значение для 4мА?").cancel():
            return
        self.com.send(MessageType.SET_LOWER_RANGE_VALUE)

    def setSpan(self):
        if Confirm("Установить текущее значение для 20мА?").cancel():
            return
        self.com.send(MessageType.SET_UPPER_RANGE_VALUE)
