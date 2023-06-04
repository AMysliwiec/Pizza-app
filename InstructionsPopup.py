from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QFont, QFontDatabase

class InstructionsPopup(QMainWindow):
    """
    Create pop up window with app's instructions.
    """
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #5D7064;")
        self.setMinimumSize(150, 60)

        font1 = QFontDatabase.addApplicationFont("anta-regular.ttf")
        anta = QFontDatabase.applicationFontFamilies(font1)

        label = QLabel("Tu bedą instrukcje jak używać apki")
        label.setWordWrap(True) #zawija tekst
        pagelayout = QVBoxLayout() #to jeszcze mozna zmienic
        label.setFont(QFont(anta[0], 40))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setScaledContents(True)  # no nie dziala gowno, mialo robic ze font zmienia wielkosc przy rozciaganiu okna
        label.setAlignment(QtCore.Qt.AlignCenter)
        pagelayout.addWidget(label)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)

        sizegrip = QSizeGrip(central_widget)
        sizegrip.setStyleSheet("border: 1px solid black;")
        pagelayout.addWidget(sizegrip, 0,
                      QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)  # to right mowi w ktora str kursor jest skierowany chyba
        central_widget.setLayout(pagelayout)
