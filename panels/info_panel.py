from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from widgets.label import Label


class InfoPanel(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()

        self.idLabel = Label("Код производителя датчика: xxx",color="orange", border=True, borderColor="blue", borderWidth=2)
        self.typeLabel = Label("Код модели датчика: xxx")
        self.softLabel = Label("Версия ПО: xxx")
        self.hardLabel = Label("Аппаратная версия: xxx")
        self.measureLabel = Label("Измеренное значние: хх")
        self.currentLabel = Label("Токовый выход: хх")
        self.sensorFaultLabel = Label("Ошибка датчика")
        self.errorLinkLabel = Label("Ошибка связи")

        grid.addWidget(self.idLabel, 0, 0)
        grid.addWidget(self.typeLabel, 0, 1)
        grid.addWidget(self.softLabel, 0, 2)
        grid.addWidget(self.hardLabel, 0, 3)
        grid.addWidget(self.measureLabel, 1, 0)
        grid.addWidget(self.currentLabel, 1, 1)
        grid.addWidget(self.sensorFaultLabel, 1, 2)
        grid.addWidget(self.errorLinkLabel, 1, 3)

        self.setLayout(grid)
