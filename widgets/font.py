from PyQt6.QtGui import QFont


class Font(QFont):
    def __init__(self, size, bold=False):
        super().__init__()
        if size is not None:
            self.setPixelSize(size)
        self.setBold(bold)
