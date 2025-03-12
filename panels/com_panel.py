from PyQt6.QtWidgets import QWidget, QGridLayout

from misc.types import Align
from misc.updater import Updater
from widgets.button import Button
from widgets.combo import ComboBox
from widgets.dialog import Confirm
from widgets.label import Label
from misc import di

connectStatusColors = ["red", "green"]
connectButtonColors = ["gray", "#F0F0F0"]


class ComPanel(QWidget, Updater):
    def __init__(self):
        Updater.__init__(self)
        QWidget.__init__(self)
        self.com = di.Container.com()
        self.comDict = di.Container.comDict()
        grid = QGridLayout()
        label = Label("Выберите COM-порт HART-модема:", align=Align.VCENTER)
        self.combo = ComboBox()
        self.combo.addItems(self.com.getAvailablePorts())
        self.connect = Button("Подключиться", background="lightgreen")
        self.disconnect = Button("Отключиться", background="pink")
        self.status = Label("X", color="white", transparent=False, background="red", align=Align.CENTER, bold=True)

        grid.addWidget(label, 0, 0)
        grid.addWidget(self.combo, 0, 1)
        grid.addWidget(self.connect, 0, 2)
        grid.addWidget(self.disconnect, 0, 3)
        grid.addWidget(self.status, 0, 4)

        self.connect.clicked.connect(self.connectClick)
        self.disconnect.clicked.connect(self.disconnectClick)

        self.setLayout(grid)
        self.startUpdate()

    def updateAction(self):
        self.status.setText(self.com.getStatus())
        self.status.setBackground(connectStatusColors[self.com.connected()])
        self.connect.setBackground(connectButtonColors[self.com.disconnected()])
        self.disconnect.setBackground(connectButtonColors[self.com.connected()])

    def connectClick(self):
        self.com.connect(self.combo.currentText())

    def disconnectClick(self):
        if self.com.connected():
            if Confirm("Отключиться от HART-модема?").cancel():
                return
        self.com.disconnect()
