from PyQt6.QtWidgets import QWidget, QGridLayout

from misc.types import LineType
from widgets.button import Button
from widgets.edit_line import EditLine


class EditPanel(QWidget):
    def __init__(self, width=400):
        super().__init__()
        self.grid = QGridLayout()
        self.row = 0
        self.column = 0
        self.unitLine = EditLine("Единица измерения: ", LineType.UNIT)
        self.tagLine = EditLine("Метка (тег): ", LineType.TAG)
        self._4mALine = EditLine("4мА: ", LineType._4mA)
        self._20mALine = EditLine("20мА", LineType._20mA)
        zeroButton = Button("Обнулить датчик")

        self.addWidgets(self.unitLine)
        self.addWidgets(self._4mALine)
        self.row += 1
        self.column = 0
        self.addWidgets(self.tagLine)
        self.addWidgets(self._20mALine)
        self.row += 1
        self.grid.addWidget(zeroButton, self.row, 0)

        # self.setFixedWidth(width)
        self.setLayout(self.grid)

    def addRow(self, line: EditLine):
        self.grid.addWidget(line.getLabelWidget(), self.row, 0)
        self.grid.addWidget(line.getValueWidget(), self.row, 1)
        self.grid.addWidget(line.getEditWidget(), self.row, 2)
        self.grid.addWidget(line.getApplyWidget(), self.row, 3)
        self.row += 1

    def addWidgets(self, line: EditLine):
        self.grid.addWidget(line.getLabelWidget(), self.row, self.column)
        self.column += 1
        self.grid.addWidget(line.getValueWidget(), self.row, self.column)
        self.column += 1
        self.grid.addWidget(line.getEditWidget(), self.row, self.column)
        self.column += 1
        self.grid.addWidget(line.getApplyWidget(), self.row, self.column)
        self.column += 1
