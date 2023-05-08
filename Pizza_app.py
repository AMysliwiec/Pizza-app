from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import QApplication, QCheckBox, QMessageBox, QMainWindow, QWidget, QGridLayout, QLineEdit, QLabel
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as canvas
from functools import partial
import qtmodern.styles
import qtmodern.windows
import numpy as np
import random
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: yellow;")
        self.setWindowTitle("Pizza app")

        pagelayout = QVBoxLayout()
        button_layout = QVBoxLayout()
        self.stacklayout = QStackedLayout()
        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        btn = QPushButton("Przepisy")
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_layout.addWidget(btn)
        btn.setStyleSheet("background-image : url(pizza-3007395__480.jpg);")

        btn = QPushButton('Główne')
        button_layout.addWidget(btn)

        btn = QPushButton('Instrukcja')
        button_layout.addWidget(btn)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)



# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()
window.show()
# start the app
sys.exit(App.exec())
