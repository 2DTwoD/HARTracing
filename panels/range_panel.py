from PyQt6.QtWidgets import QWidget, QHBoxLayout

from com.hart import MessageType
from misc import di
from widgets.button import Button
from widgets.dialog import Confirm


class RangePanel(QWidget):
    def __init__(self):
        super().__init__()
        self.com = di.Container.com()
        box = QHBoxLayout()

        pvZeroButton = Button("Обнулить датчик (PV trim zero)")
        zeroButton = Button("Установить 4мА (кнопка ZERO)")
        spanButton = Button("Установить 20мА (кнопка SPAN)")
        resetChangedFlagButton = Button("Сбросить флаг 'Конфиг-ия изменена'")

        box.addWidget(pvZeroButton)
        box.addWidget(zeroButton)
        box.addWidget(spanButton)
        box.addWidget(resetChangedFlagButton)

        pvZeroButton.clicked.connect(lambda: self.sendCommand(MessageType.SET_TRIM_PV_ZERO,
                                                              "Обнулить датчик?"))
        zeroButton.clicked.connect(lambda: self.sendCommand(MessageType.SET_LOWER_RANGE_VALUE,
                                                            "Установить текущее значение для 4мА?"))
        spanButton.clicked.connect(lambda: self.sendCommand(MessageType.SET_UPPER_RANGE_VALUE,
                                                            "Установить текущее значение для 20мА?"))
        resetChangedFlagButton.clicked.connect(lambda: self.sendCommand(MessageType.RESET_CONFIG_CHANGE_FLAG,
                                                            "Сбросить флаг 'Конфигурация изменена'?"))
        self.setLayout(box)

    def sendCommand(self, messageType: MessageType, text: str):
        if Confirm(text).cancel():
            return
        self.com.send(messageType)
