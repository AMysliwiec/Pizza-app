from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtGui import QFont, QFontDatabase
from MainNeapol import MainNeapol
from MainAmeryka import MainAmeryka
from MainRzym import MainRzym

class MainPopup(QMainWindow):
    """
    Create pop up window with main app funcionality.
    """
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #5D7064;")
        self.setMinimumSize(150, 60)

        font1 = QFontDatabase.addApplicationFont("anta-regular.ttf")
        font2 = QFontDatabase.addApplicationFont("Bakerie Rough Bold.otf")
        anta = QFontDatabase.applicationFontFamilies(font1)
        bakerie = QFontDatabase.applicationFontFamilies(font2)

        label = QLabel("Wybierz rodzaj pizzy.")
        label.setWordWrap(True)  # zawija tekst
        pagelayout = QVBoxLayout()  # to jeszcze mozna zmienic
        label.setFont(QFont(anta[0], 40))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setScaledContents(True)  # no nie dziala gowno, mialo robic ze font zmienia wielkosc przy rozciaganiu okna
        label.setAlignment(QtCore.Qt.AlignCenter)
        pagelayout.addWidget(label)

        btn_neapol = QPushButton("Neapolitańska")
        btn_neapol.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # rozszerza sie przycisk jak rozszerzamy
        btn_neapol.setFont(QFont(bakerie[0], 20))
        btn_neapol.clicked.connect(self.neapol)
        btn_neapol.clicked.connect(self.close)
        pagelayout.addWidget(btn_neapol)

        btn_ameryka = QPushButton("Amerykańska")
        btn_ameryka.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # rozszerza sie przycisk jak rozszerzamy
        btn_ameryka.setFont(QFont(bakerie[0], 20))
        btn_ameryka.clicked.connect(self.ameryka)
        btn_ameryka.clicked.connect(self.close)
        pagelayout.addWidget(btn_ameryka)

        btn_rzym = QPushButton("Rzymska")
        btn_rzym.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # rozszerza sie przycisk jak rozszerzamy
        btn_rzym.setFont(QFont(bakerie[0], 20))
        btn_rzym.clicked.connect(self.rzym)
        btn_rzym.clicked.connect(self.close)
        pagelayout.addWidget(btn_rzym)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)

        sizegrip = QSizeGrip(central_widget)
        sizegrip.setStyleSheet("border: 1px solid black;")
        pagelayout.addWidget(sizegrip, 0,
                      QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)  # to right mowi w ktora str kursor jest skierowany chyba
        central_widget.setLayout(pagelayout)

    def neapol(self):
        self.w = MainNeapol()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def rzym(self):
        self.w = MainRzym()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def ameryka(self):
        self.w = MainAmeryka()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()