from PyQt6.QtWidgets import QWidget, QGridLayout

from misc.types import Align
from misc.updater import Updater
from widgets.button import Button
from widgets.combo import ComboBox
from widgets.label import Label


class ComPanel(QWidget, Updater):
    def __init__(self):
        Updater.__init__(self)
        QWidget.__init__(self)
        grid = QGridLayout()
        label = Label("Выберите COM-порт HART-модема:", align=Align.VCENTER)
        self.combo = ComboBox()
        self.connect = Button("Подключиться", background="lightgreen")
        self.disconnect = Button("Отключиться", background="pink")
        self.status = Label("X", color="white", transparent=False, background="red", align=Align.CENTER, bold=True)

        grid.addWidget(label, 0, 0)
        grid.addWidget(self.combo, 0, 1)
        grid.addWidget(self.connect, 0, 2)
        grid.addWidget(self.disconnect, 0, 3)
        grid.addWidget(self.status, 0, 4)

        self.setLayout(grid)
        self.startUpdate()

    def updateAction(self):
        print(1)
