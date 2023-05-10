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
import PyQt5.QtGui

#https://stackoverflow.com/questions/52596386/slide-qstackedwidget-page slide pages
class SlidingStackedWidget(QStackedWidget):
    """
    tu oczywiscie nie wiem co sie dzieje, just kopiuj wklej
    """
    def __init__(self, parent=None):
        super(SlidingStackedWidget, self).__init__(parent)

        self.m_direction = QtCore.Qt.Horizontal
        self.m_speed = 500
        self.m_animationtype = QtCore.QEasingCurve.OutCubic
        self.m_now = 0
        self.m_next = 0
        self.m_wrap = False
        self.m_pnow = QtCore.QPoint(0, 0)
        self.m_active = False

    def setDirection(self, direction):
        self.m_direction = direction

    def setSpeed(self, speed):
        self.m_speed = speed

    def setAnimation(self, animationtype):
        self.m_animationtype = animationtype

    def setWrap(self, wrap):
        self.m_wrap = wrap

    @QtCore.pyqtSlot()
    def slideInPrev(self):
        now = self.currentIndex()
        if self.m_wrap or now > 0:
            self.slideInIdx(now - 1)

    @QtCore.pyqtSlot()
    def slideInNext(self):
        now = self.currentIndex()
        if self.m_wrap or now < (self.count() - 1):
            self.slideInIdx(now + 1)

    def slideInIdx(self, idx):
        if idx > (self.count() - 1):
            idx = idx % self.count()
        elif idx < 0:
            idx = (idx + self.count()) % self.count()
        self.slideInWgt(self.widget(idx))

    def slideInWgt(self, newwidget):
        if self.m_active:
            return

        self.m_active = True

        _now = self.currentIndex()
        _next = self.indexOf(newwidget)

        if _now == _next:
            self.m_active = False
            return

        offsetx, offsety = self.frameRect().width(), self.frameRect().height()
        self.widget(_next).setGeometry(self.frameRect())

        if not self.m_direction == QtCore.Qt.Horizontal:
            if _now < _next:
                offsetx, offsety = 0, -offsety
            else:
                offsetx = 0
        else:
            if _now < _next:
                offsetx, offsety = -offsetx, 0
            else:
                offsety = 0

        pnext = self.widget(_next).pos()
        pnow = self.widget(_now).pos()
        self.m_pnow = pnow

        offset = QtCore.QPoint(offsetx, offsety)
        self.widget(_next).move(pnext - offset)
        self.widget(_next).show()
        self.widget(_next).raise_()

        anim_group = QtCore.QParallelAnimationGroup(
            self, finished=self.animationDoneSlot
        )

        for index, start, end in zip(
            (_now, _next), (pnow, pnext - offset), (pnow + offset, pnext)
        ):
            animation = QtCore.QPropertyAnimation(
                self.widget(index),
                b"pos",
                duration=self.m_speed,
                easingCurve=self.m_animationtype,
                startValue=start,
                endValue=end,
            )
            anim_group.addAnimation(animation)

        self.m_next = _next
        self.m_now = _now
        self.m_active = True
        anim_group.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

    @QtCore.Slot()
    def animationDoneSlot(self):
        self.setCurrentIndex(self.m_next)
        self.widget(self.m_now).hide()
        self.widget(self.m_now).move(self.m_pnow)
        self.m_active = False

class RecipesPopup(QMainWindow):
    """
    Create window with pizza recipes.
    """
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #5D7064;")
        slidingStacked = SlidingStackedWidget()
        label_neapol = QLabel("Neapolitanska", alignment=QtCore.Qt.AlignCenter)
        label_ameryka = QLabel("Amerykańska", alignment=QtCore.Qt.AlignCenter)
        label_rzym = QLabel("Rzymska", alignment=QtCore.Qt.AlignCenter)
        slidingStacked.addWidget(label_neapol)
        slidingStacked.addWidget(label_ameryka)
        slidingStacked.addWidget(label_rzym)

        button_prev = QPushButton("Poprzednia", pressed=slidingStacked.slideInPrev)
        button_next = QPushButton("Następna", pressed=slidingStacked.slideInNext)

        hlay = QHBoxLayout()
        hlay.addWidget(button_prev)
        hlay.addWidget(button_next)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        lay = QVBoxLayout(central_widget)
        lay.addLayout(hlay)
        lay.addWidget(slidingStacked)

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

class MainWindow(QMainWindow):
    """
    Main window of application. (troche  burdel, wszystko w jednym, mozna rozdzielic wyglad i funkcjonalnosc na fnkcje osobne)
    """
    def __init__(self):
        super().__init__()

        self.center() #zeby apka wyskakiwala na srodku ekranu po odpaleniu, no mi tak na srodku ale na dole wyskakuje
        self.setStyleSheet("background-color: #5D7064;") #kolor/zdj tła apki

        #nie daje tytulu apki tym windowsettitle bo nie da sie chyba zmienic fontu i jest brzydkie
        self.setMinimumSize(200,700)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        font = QFontDatabase.addApplicationFont("Bakerie Rough Bold.otf")
        bakerie = QFontDatabase.applicationFontFamilies(font)

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
        btn.clicked.connect(self.recipes_popup)
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
        btn.clicked.connect(self.instructions_popup)
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

    def recipes_popup(self):
        """
        Display popup window with pizza recipes.
        """
        self.w = RecipesPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def instructions_popup(self):
        """
        Display popup window with app instructions.
        :return:
        """
        self.w = InstructionsPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def center(self):
        """
        Center window while opening.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    App = QApplication(sys.argv)
    window = MainWindow()
    qtmodern.styles.dark(App)
    mw = qtmodern.windows.ModernWindow(window)
    mw.show()
    sys.exit(App.exec())


if __name__ == '__main__':
    main()


