from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QGridLayout, QPushButton, QLabel


class Confirm(QDialog):
    def __init__(self, text):
        super().__init__()

        self.setWindowTitle("Подтвердите действие")

        yesBut = QPushButton("Да")
        cancelBut = QPushButton("Отмена")
        message = QLabel(text)
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        yesBut.clicked.connect(self.accept)
        cancelBut.clicked.connect(self.reject)

        grid = QGridLayout()
        grid.addWidget(message, 0, 0, 1, 2)
        grid.addWidget(yesBut, 1, 0, 1, 1)
        grid.addWidget(cancelBut, 1, 1, 1, 1)
        self.setLayout(grid)
        self.setFixedSize(250, 100)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowCloseButtonHint)

    def yes(self):
        return self.exec()

    def cancel(self):
        return not self.exec()
