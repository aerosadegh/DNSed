import sys
import os

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QLabel,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon



def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class DNSManagerUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DNSed")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Make the window frameless
        self.setWindowFlags(Qt.Tool)

        self.layout = QVBoxLayout()

        self.interface_selector = QComboBox()
        self.layout.addWidget(self.interface_selector)

        self.profile_selector = QComboBox()
        self.layout.addWidget(self.profile_selector)

        self.set_button = QPushButton("Set DNS")
        self.set_button.setIcon(QIcon(resource_path("assets/set_icon.png")))
        self.layout.addWidget(self.set_button)

        self.clear_button = QPushButton("Clear DNS")
        self.clear_button.setIcon(QIcon(resource_path("assets/clear_icon.png")))
        self.layout.addWidget(self.clear_button)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)  # Center the text
        self.layout.addWidget(self.status_label)

        # self.close_button = QPushButton()
        # self.close_button.setIcon(QIcon(resource_path("assets/close_icon.png")))
        # self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)
