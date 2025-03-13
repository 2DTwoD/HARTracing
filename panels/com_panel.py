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
baudDict = {"600": 600, "1200 (+)": 1200, "2400": 2400, "4800": 4800, "9600": 9600,
            "19200": 19200, "57600": 57600, "115200": 115200}
parityDict = {"Нет": 'N', "Чет.": 'E', "Нечет.(+)": 'O'}
bitDict = {"1": 1, "1.5": 1.5, "2 (+)": 2}

class ComPanel(QWidget, Updater):
    def __init__(self):
        Updater.__init__(self)
        QWidget.__init__(self)
        self.com = di.Container.com()
        self.comDict = di.Container.comDict()
        self.grid = QGridLayout()
        label = Label("HART-модем:", align=Align.VCENTER)
        self.portCombo = ComboBox()
        self.baudCombo = ComboBox()
        self.parityCombo = ComboBox()
        self.bitCombo = ComboBox()

        self.portCombo.addItems(self.com.getAvailablePorts())
        self.baudCombo.addItems(baudDict.keys())
        self.parityCombo.addItems(parityDict.keys())
        self.bitCombo.addItems(bitDict.keys())

        self.connect = Button("Подключиться", background="lightgreen")
        self.disconnect = Button("Отключиться", background="pink")
        self.status = Label("X", color="white", transparent=False, background="red", align=Align.CENTER, bold=True)

        self.row = 0
        self.column = 1
        self.addItemToLayout(Label("COM-порт:"))
        self.addItemToLayout(Label("Скорость:"))
        self.addItemToLayout(Label("Четность:"))
        self.addItemToLayout(Label("Стоп-биты:"))
        self.row = 1
        self.column = 0
        self.addItemToLayout(label)
        self.addItemToLayout(self.portCombo)
        self.addItemToLayout(self.baudCombo)
        self.addItemToLayout(self.parityCombo)
        self.addItemToLayout(self.bitCombo)
        self.addItemToLayout(self.connect)
        self.addItemToLayout(self.disconnect)
        self.addItemToLayout(self.status)

        self.baudCombo.setCurrentIndex(1)
        self.parityCombo.setCurrentIndex(2)
        self.bitCombo.setCurrentIndex(2)

        self.connect.clicked.connect(self.connectClick)
        self.disconnect.clicked.connect(self.disconnectClick)

        self.setLayout(self.grid)
        self.startUpdate()

    def addItemToLayout(self, item: QWidget):
        self.grid.addWidget(item, self.row, self.column)
        self.column += 1

    def updateAction(self):
        self.status.setText(self.com.getStatus())
        self.status.setBackground(connectStatusColors[self.com.connected()])
        self.connect.setBackground(connectButtonColors[self.com.disconnected()])
        self.disconnect.setBackground(connectButtonColors[self.com.connected()])
        self.portCombo.setEnabled(self.com.disconnected())
        self.baudCombo.setEnabled(self.com.disconnected())
        self.parityCombo.setEnabled(self.com.disconnected())
        self.bitCombo.setEnabled(self.com.disconnected())
        self.updateAvailablePorts()

    def updateAvailablePorts(self):
        if self.com.connected():
            return
        ports = self.com.getAvailablePorts()
        ports.sort()
        allItems = [self.portCombo.itemText(i) for i in range(self.portCombo.count())]
        if ports == allItems:
            return
        self.portCombo.clear()
        self.portCombo.addItems(ports)

    def connectClick(self):
        self.com.connect(self.portCombo.currentText(),
                         baudrate=baudDict[self.baudCombo.currentText()],
                         parity=parityDict[self.parityCombo.currentText()],
                         stopBits=bitDict[self.bitCombo.currentText()])

    def disconnectClick(self):
        if self.com.connected():
            if Confirm("Отключиться от HART-модема?").cancel():
                return
        self.com.disconnect()
