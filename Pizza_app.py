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
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QDesktopWidget



class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.center() #zeby apka wyskakiwala na srodku ekranu po odpaleniu, no mi tak na srodku ale na dole wyskakuje
        self.setStyleSheet("background-color: #5D7064;") #kolor/zdj tła apki

        #nie daje tytulu apki tym windowsettitle bo nie da sie chyba zmienic fontu i jest brzydkie
        self.setMinimumSize(200,700)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        font1 = QFontDatabase.addApplicationFont("anta-regular.ttf")
        anta = QFontDatabase.applicationFontFamilies(font1)
        font2 = QFontDatabase.addApplicationFont("Bakerie Rough Bold.otf")
        bakerie = QFontDatabase.applicationFontFamilies(font2)

        pagelayout = QVBoxLayout()

        label = QLabel("Super Pizzowa Aplikacja") #jak to po polsku ladnie napisac to ja nie mam pojecia xd welcome to pizza app
        label.setFont(QFont(bakerie[0], 40))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setScaledContents(True) #no nie dziala gowno
        label.setAlignment(QtCore.Qt.AlignCenter)
        pagelayout.addWidget(label)

        btn = QPushButton("Przepisy")
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) #rozszerza sie przycisk jak rozszerzamy
        btn.setFont(QFont(bakerie[0], 20))
        #btn.setStyleSheet("background-image : url(pobrane.jpeg);") #nie wiem czemu to nie dziala, mam wrazenie ze to qtmodern psuje ale nie wiem
        #btn.setStyleSheet("border-image : url(pizza.png);") to powinno od razu dopasowywac wymiary zdjecia ale no narazie nie dziala
        pagelayout.addWidget(btn)

        btn = QPushButton('Główne')
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.setFont(QFont(bakerie[0], 20))
        pagelayout.addWidget(btn)

        btn = QPushButton('Jak to działa?')
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.setFont(QFont(bakerie[0], 20))
        pagelayout.addWidget(btn)

        """
        Dodac opcje ze jak zwiekszamy okno to zwieksza sie tez font labeli i font na buttonach. tu jakis link ale sredni chyba
        https://www.youtube.com/watch?v=3kGKWkQqipc&list=PL3JVwFmb_BnRpvOeIh_To4YSiebiggyXS&index=22
        """

        #dodac moze jakies zdjecia w tle na tych przyciskach
        #nie wiem czy robimy juz te podstronki ale chyba by sie przydalo jakas jedna chociaz, moze ta z przepisami

        widget = QWidget()
        self.setCentralWidget(widget)
        sizegrip = QSizeGrip(widget)
        sizegrip.setStyleSheet("border: 1px solid black;")
        pagelayout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight) #to right mowi w ktora str kursor jest skierowany chyba
        widget.setLayout(pagelayout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    App = QApplication(sys.argv)
    window = Window()
    qtmodern.styles.dark(App)
    mw = qtmodern.windows.ModernWindow(window)
    mw.show()
    sys.exit(App.exec())


if __name__ == '__main__':
    main()


