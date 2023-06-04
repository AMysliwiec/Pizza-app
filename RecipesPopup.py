from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtGui import QFont, QFontDatabase
from SlidingStackedWidget import SlidingStackedWidget
from MainNeapol import MainNeapol
from MainAmeryka import MainAmeryka
from MainRzym import MainRzym

class RecipesPopup(QMainWindow):
    """
    Create window with pizza recipes.
    """
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #5D7064;")
        font = QFontDatabase.addApplicationFont("Bakerie Rough Bold.otf")
        bakerie = QFontDatabase.applicationFontFamilies(font)
        self.slidingStacked = SlidingStackedWidget()
        label_neapol = QLabel("Neapolitańska", alignment=QtCore.Qt.AlignCenter)
        label_ameryka = QLabel("Amerykańska", alignment=QtCore.Qt.AlignCenter)
        label_rzym = QLabel("Rzymska", alignment=QtCore.Qt.AlignCenter)
        self.slidingStacked.addWidget(label_neapol)
        self.slidingStacked.addWidget(label_ameryka)
        self.slidingStacked.addWidget(label_rzym)

        button_prev = QPushButton("Poprzednia")
        button_prev.clicked.connect(self.slidingStacked.slideInPrev)
        #button_prev.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_prev.setFont(QFont(bakerie[0], 15))
        button_next = QPushButton("Następna")
        button_next.clicked.connect(self.slidingStacked.slideInNext)
        #button_next.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_next.setFont(QFont(bakerie[0], 15))

        hlay = QHBoxLayout()
        hlay.addWidget(button_prev)
        hlay.addWidget(button_next)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        lay = QVBoxLayout(central_widget)
        lay.addLayout(hlay)
        lay.addWidget(self.slidingStacked)

        sec_lay = QHBoxLayout()
        button_main = QPushButton("Główne")
        button_main.setFont(QFont(bakerie[0], 15))
        button_main.clicked.connect(self.close)
        button_main.clicked.connect(self.open_main)
        sec_lay.addWidget(button_main)
        sec_lay.setAlignment(Qt.AlignCenter)
        lay.addLayout(sec_lay)

        sizegrip = QSizeGrip(central_widget)
        sizegrip.setStyleSheet("border: 1px solid black;")
        lay.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)  # to right mowi w ktora str kursor jest skierowany chyba
        central_widget.setLayout(lay)

    def open_main(self):
        if self.slidingStacked.currentIndex() == 0:
            self.w = MainNeapol()
            self.mw = qtmodern.windows.ModernWindow(self.w)
            self.mw.show()
        elif self.slidingStacked.currentIndex() == 1:
            self.w = MainAmeryka()
            self.mw = qtmodern.windows.ModernWindow(self.w)
            self.mw.show()
        else:
            self.w = MainRzym()
            self.mw = qtmodern.windows.ModernWindow(self.w)
            self.mw.show()