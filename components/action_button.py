from PyQt5.QtWidgets import *


class ActionButton(QPushButton):
    def __init__(self, text, icon):
        super().__init__()

        self.setText("  " + text)
        self.setMinimumHeight(50)
        self.setMinimumWidth(150)

        self.setCheckable(True)

        self.setIcon(icon)
