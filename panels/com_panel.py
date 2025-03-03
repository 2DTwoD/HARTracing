from PyQt6.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QHBoxLayout

from widgets.button import Button
from widgets.combo import ComboBox


class ComPanel(QWidget):
    def __init__(self):
        super().__init__()
        box = QHBoxLayout()
        comLabel = QLabel("Выберите COM-порт HART-модема:")
        self.comCombo = ComboBox(background="white")
        self.connectButton = Button("Подключиться", background="white")
        self.disconnectButton = Button("Отключиться")
        self.statusLabel = QLabel("V")

        box.addWidget(comLabel)
        box.addWidget(self.comCombo)
        box.addWidget(self.connectButton)
        box.addWidget(self.disconnectButton)
        box.addWidget(self.statusLabel)

        self.setLayout(box)
