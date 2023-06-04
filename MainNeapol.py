from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtGui import QFont, QFontDatabase
from MainPopup import MainPopup


class MainNeapol(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #5D7064;")
        self.setMinimumSize(150, 60)

        font1 = QFontDatabase.addApplicationFont("anta-regular.ttf")
        font2 = QFontDatabase.addApplicationFont("Bakerie Rough Bold.otf")
        anta = QFontDatabase.applicationFontFamilies(font1)
        bakerie = QFontDatabase.applicationFontFamilies(font2)

        pagelayout = QVBoxLayout()

        hbox_tryb = QHBoxLayout()
        lbl_tryb = QLabel("Tryb pieczenia")
        lbl_tryb.setFont(QFont(anta[0], 15))
        lbl_tryb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lbl_tryb.setScaledContents(
            True)  # no nie dziala gowno, mialo robic ze font zmienia wielkosc przy rozciaganiu okna
        lbl_tryb.setAlignment(QtCore.Qt.AlignLeft)
        hbox_tryb.addWidget(lbl_tryb)
        self.toggle_button = QPushButton("Termoobieg", self)
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.change_toggle)
        hbox_tryb.addWidget(self.toggle_button)
        pagelayout.addLayout(hbox_tryb)

        hbox_temp = QHBoxLayout()
        lbl_temp = QLabel("Maksymalna temperatura")
        lbl_temp.setFont(QFont(anta[0], 15))
        lbl_temp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lbl_temp.setScaledContents(
            True)  # no nie dziala gowno, mialo robic ze font zmienia wielkosc przy rozciaganiu okna
        lbl_temp.setAlignment(QtCore.Qt.AlignLeft)
        hbox_temp.addWidget(lbl_temp)

        hbox_srednica = QHBoxLayout()
        lbl_srednica = QLabel("Średnica")
        lbl_srednica.setFont(QFont(anta[0], 15))
        lbl_srednica.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lbl_srednica.setScaledContents(
            True)  # no nie dziala gowno, mialo robic ze font zmienia wielkosc przy rozciaganiu okna
        lbl_srednica.setAlignment(QtCore.Qt.AlignLeft)
        hbox_srednica.addWidget(lbl_srednica)

        sld_srednica = QSlider(Qt.Orientation.Horizontal, self)
        sld_srednica.setRange(20, 40)
        # nwm jak ustawic zeby to przesuwajace sie niebiezkie bylo innego koloru
        sld_srednica.setPageStep(1)
        sld_srednica.valueChanged.connect(self.updateLabel1)

        sld_temp = QSlider(Qt.Orientation.Horizontal, self)
        sld_temp.setRange(180, 280)
        # nwm jak ustawic zeby to przesuwajace sie niebiezkie bylo innego koloru
        sld_temp.setPageStep(5)
        sld_temp.valueChanged.connect(self.updateLabel2)

        self.lbl_slider_sr = QLabel('20', self)
        self.lbl_slider_sr.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                        Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_sr.setMinimumWidth(80)
        self.lbl_slider_sr.setFont(QFont(anta[0], 10))

        self.lbl_slider_temp = QLabel('180', self)
        self.lbl_slider_temp.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                          Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_temp.setMinimumWidth(80)
        self.lbl_slider_temp.setFont(QFont(anta[0], 10))

        hbox_srednica.addWidget(sld_srednica)
        hbox_srednica.addSpacing(15)
        hbox_srednica.addWidget(self.lbl_slider_sr)
        pagelayout.addLayout(hbox_srednica)

        hbox_temp.addWidget(sld_temp)
        hbox_temp.addSpacing(15)
        hbox_temp.addWidget(self.lbl_slider_temp)
        pagelayout.addLayout(hbox_temp)

        btn = QPushButton("Wróć")
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.setFont(QFont(bakerie[0], 20))
        btn.clicked.connect(self.close)
        # btn.cliked.connect(self.go_back) #nwm czemu to nie dziala
        pagelayout.addWidget(btn)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)

        sizegrip = QSizeGrip(central_widget)
        sizegrip.setStyleSheet("border: 1px solid black;")
        pagelayout.addWidget(sizegrip, 0,
                             QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)  # to right mowi w ktora str kursor jest skierowany chyba
        central_widget.setLayout(pagelayout)

    def updateLabel1(self, value):
        self.lbl_slider_sr.setText(str(value))

    def updateLabel2(self, value):
        self.lbl_slider_temp.setText(str(value))

    def change_toggle(self):
        if self.toggle_button.isChecked():
            self.toggle_button.setText("Góra-dół")
        else:
            self.toggle_button.setText("Termoobieg")
        # mozna jeszcze pomyslec czy chcemy zmieniac jego kolor

    def go_back(self):
        self.w = MainPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()
