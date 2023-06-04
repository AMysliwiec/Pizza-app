from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
import qtmodern.styles
from PyQt5.QtGui import QFont, QFontDatabase
import qtmodern.windows
from MainPopup import *


class MainAmeryka(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #5D7064;")
        self.setMinimumSize(150, 60)

        font1 = QFontDatabase.addApplicationFont("anta-regular.ttf")
        font2 = QFontDatabase.addApplicationFont("Bakerie Rough Bold.otf")
        anta = QFontDatabase.applicationFontFamilies(font1)
        bakerie = QFontDatabase.applicationFontFamilies(font2)
        pagelayout = QGridLayout()

        lbl_rzymska = QLabel("Pizza Amerykańska")
        lbl_rzymska.setFont(QFont(bakerie[0], 30))
        lbl_rzymska.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_rzymska, 1, 0, 1, 4, alignment=Qt.AlignCenter)

        lbl_tryb = QLabel("Tryb pieczenia")
        lbl_tryb.setFont(QFont(anta[0], 15))
        lbl_tryb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_tryb, 2, 0)

        self.cb = QComboBox()
        self.cb.addItems(["Termoobieg", "Góra-dół", "Jakieś coś"])
        self.cb.setFont(QFont(anta[0], 9))
        self.cb.setStyleSheet('selection-background-color: #798b80')
        pagelayout.addWidget(self.cb, 2, 1)

        lbl_temp = QLabel("Maksymalna temperatura")
        lbl_temp.setWordWrap(True)
        lbl_temp.setFont(QFont(anta[0], 15))
        lbl_temp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_temp, 3, 0)

        sld_temp = QSlider(Qt.Orientation.Horizontal, self)
        sld_temp.setRange(180, 280)
        sld_temp.setPageStep(5)
        sld_temp.valueChanged.connect(self.updateLabeltemp)
        pagelayout.addWidget(sld_temp, 3, 1)

        self.lbl_slider_temp = QLabel('180', self)
        self.lbl_slider_temp.setMinimumWidth(80)
        self.lbl_slider_temp.setFont(QFont(anta[0], 10))
        pagelayout.addWidget(self.lbl_slider_temp, 3, 2, alignment=Qt.AlignmentFlag.AlignRight)

        btn = QPushButton("Wróć")
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.setFont(QFont(bakerie[0], 20))
        btn.clicked.connect(self.close)
        # btn.cliked.connect(self.go_back) #nwm czemu to nie dziala
        pagelayout.addWidget(btn, 4, 0, 1, 4, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)

        sizegrip = QSizeGrip(central_widget)
        sizegrip.setStyleSheet("border: 1px solid black;")
        pagelayout.addWidget(sizegrip, 5, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        central_widget.setLayout(pagelayout)

    def go_back(self):
        self.w = MainPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def updateLabeltemp(self, value):
        self.lbl_slider_temp.setText(str(value))