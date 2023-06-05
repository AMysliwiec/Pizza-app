from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QCheckBox, QMessageBox, QMainWindow, QWidget, QGridLayout, QLineEdit, QLabel
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as canvas
import qtmodern.styles
import qtmodern.windows
import sys
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QDesktopWidget
import PyQt5.QtGui
from PyQt5.QtCore import QCoreApplication

import constant
from constant import *


# https://stackoverflow.com/questions/52596386/slide-qstackedwidget-page slide pages
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
        self.setStyleSheet(f"background-color: {back_color};")
        self.setMinimumSize(min_width, min_height)
        self.center()
        self.resize(min_width, min_height)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        bakerie = get_font()[1]
        anta = get_font()[0]

        self.slidingStacked = SlidingStackedWidget()

        neapol_przepis = QLabel(f"""<div 
                                style ="font-size:45px; text-align:center;"><span style ="font-family:{bakerie[0]};">Pizza Neapolitańska</span> <br></
                                div><div
                                style="font-size:18px; text-align:left;"><span style="font-family: {anta[0]};"{przepis_neapol}</span
                                </div>""")
        ameryka_przepis = QLabel(f"""<div 
                                style ="font-size:45px; text-align:center;"><span style ="font-family:{bakerie[0]};">Pizza Amerykańska</span> <br></
                                div><div
                                style="font-size:18px; text-align:left;"><span style="font-family: {anta[0]};"{przepis_ameryka}</span
                                </div>""")
        rzym_przepis = QLabel(f"""<div 
                                style ="font-size:45px; text-align:center;"><span style ="font-family:{bakerie[0]};">Pizza Rzymska</span> </
                                div><div
                                style="font-size:18px; text-align:left;"><span style="font-family: {anta[0]};"{przepis_rzym}</span
                                </div>""")
        neapol_przepis.setWordWrap(True)
        ameryka_przepis.setWordWrap(True)
        rzym_przepis.setWordWrap(True)
        self.slidingStacked.addWidget(neapol_przepis)
        self.slidingStacked.addWidget(ameryka_przepis)
        self.slidingStacked.addWidget(rzym_przepis)

        button_prev = QPushButton("Poprzednia")
        button_prev.clicked.connect(self.slidingStacked.slideInPrev)
        button_prev.setFont(QFont(bakerie[0], 15))
        button_next = QPushButton("Następna")
        button_next.clicked.connect(self.slidingStacked.slideInNext)
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
        button_main_func = QPushButton("Główne")
        button_main_func.setMinimumWidth(150)
        button_main_func.setFont(QFont(bakerie[0], 15))
        button_main_func.clicked.connect(self.close)
        button_main_func.clicked.connect(self.open_main)
        sec_lay.addWidget(button_main_func)
        sec_lay.setAlignment(Qt.AlignCenter)
        lay.addLayout(sec_lay)

        btn_main = QPushButton("Menu Główne")
        btn_main.setMinimumWidth(150)
        btn_main.setFont(QFont(bakerie[0], 15))
        btn_main.clicked.connect(self.close)
        btn_main.clicked.connect(self.main_window)
        sec_lay.addWidget(btn_main)

        sizegrip = QSizeGrip(central_widget)
        sizegrip.setStyleSheet("border: 1px solid black;")
        lay.addWidget(sizegrip, 0,
                      QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)  # to right mowi w ktora str kursor jest skierowany chyba
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

    def center(self):
        """
        Center window while opening.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def main_window(self):
        self.w = MainWindow()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()


class MainPopup(QMainWindow):
    """
    Create pop up window with main app funcionality.
    """

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {back_color};")
        self.setMinimumSize(min_width, min_height)
        self.center()
        self.resize(min_width, min_height)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        anta, bakerie = get_font()

        label = QLabel("Wybierz rodzaj pizzy.")
        label.setWordWrap(True)  # zawija tekst
        pagelayout = QVBoxLayout()  # to jeszcze mozna zmienic
        label.setFont(QFont(bakerie[0], 40))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setScaledContents(True)  # no nie dziala gowno, mialo robic ze font zmienia wielkosc przy rozciaganiu okna
        label.setAlignment(QtCore.Qt.AlignCenter)
        pagelayout.addWidget(label)

        btn_neapol = make_button("Neapolitańska", bakerie, 0, 0, font_size=20)
        btn_neapol.clicked.connect(self.neapol)
        btn_neapol.clicked.connect(self.close)
        pagelayout.addWidget(btn_neapol)

        btn_ameryka = make_button("Amerykańska", bakerie, 0, 0,  font_size=20)
        btn_ameryka.clicked.connect(self.ameryka)
        btn_ameryka.clicked.connect(self.close)
        pagelayout.addWidget(btn_ameryka)

        btn_rzym = make_button("Rzymska", bakerie, 0, 0,  font_size=20)
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

    def center(self):
        """
        Center window while opening.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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


class InstructionsPopup(QMainWindow):
    """
    Create pop up window with app's instructions.
    """

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {back_color};")
        self.setMinimumSize(min_width, min_height)
        self.center()
        self.resize(min_width, min_height)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        anta, bakerie = get_font()

        label = QLabel("Tu bedą instrukcje jak używać apki")
        label.setWordWrap(True)  # zawija tekst
        pagelayout = QVBoxLayout()  # to jeszcze mozna zmienic
        label.setFont(QFont(anta[0], 40))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setScaledContents(True)  # no nie dziala gowno, mialo robic ze font zmienia wielkosc przy rozciaganiu okna
        label.setAlignment(QtCore.Qt.AlignCenter)
        pagelayout.addWidget(label)

        btn = QPushButton("Menu główne")
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # rozszerza sie przycisk jak rozszerzamy
        btn.setFont(QFont(bakerie[0], 20))
        btn.clicked.connect(self.close)
        btn.clicked.connect(self.open_main)
        pagelayout.addWidget(btn)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)

        sizegrip = QSizeGrip(central_widget)
        sizegrip.setStyleSheet("border: 1px solid black;")
        pagelayout.addWidget(sizegrip, 0,
                             QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)  # to right mowi w ktora str kursor jest skierowany chyba
        central_widget.setLayout(pagelayout)

    def center(self):
        """
        Center window while opening.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_main(self):
        self.w = MainWindow()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()


class MainNeapol(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {back_color};")
        self.setMinimumSize(min_width, min_height)
        self.center()
        self.resize(min_width, min_height)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        anta, bakerie = get_font()

        pagelayout = QGridLayout()

        lbl_neapol = QLabel("Pizza Neapolitańska")
        lbl_neapol.setFont(QFont(bakerie[0], 30))
        lbl_neapol.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_neapol, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        lbl_tryb = QLabel("Tryb pieczenia")
        lbl_tryb.setFont(QFont(anta[0], 15))
        lbl_tryb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_tryb, 1, 0)

        self.cb = QComboBox()
        self.cb.addItems(tryby)
        self.cb.setFont(QFont(anta[0], 12))
        self.cb.setStyleSheet(f"selection-background-color: {select_color};")
        pagelayout.addWidget(self.cb, 1, 1, alignment=Qt.AlignCenter)

        lbl_srednica = QLabel("Średnica")
        lbl_srednica.setFont(QFont(anta[0], 15))
        lbl_srednica.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_srednica, 2, 0)

        self.sld_srednica = QSlider(Qt.Orientation.Horizontal, self)
        self.sld_srednica.setRange(20, 40)
        self.sld_srednica.setPageStep(1)
        self.sld_srednica.valueChanged.connect(self.updateLabel1)
        pagelayout.addWidget(self.sld_srednica, 2, 1)

        self.lbl_slider_sr = QLabel('20', self)
        self.lbl_slider_sr.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                        Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_sr.setMinimumWidth(80)
        self.lbl_slider_sr.setFont(QFont(anta[0], 10))
        pagelayout.addWidget(self.lbl_slider_sr, 2, 2, alignment=Qt.AlignLeft)

        lbl_temp = QLabel("Maksymalna temperatura")
        lbl_temp.setWordWrap(True)
        lbl_temp.setFont(QFont(anta[0], 15))
        lbl_temp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_temp, 3, 0)

        self.sld_temp = QSlider(Qt.Orientation.Horizontal, self)
        self.sld_temp.setRange(180, 280)
        self.sld_temp.setPageStep(5)
        self.sld_temp.valueChanged.connect(self.updateLabel2)
        pagelayout.addWidget(self.sld_temp, 3, 1)

        self.lbl_slider_temp = QLabel('180', self)
        self.lbl_slider_temp.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                          Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_temp.setMinimumWidth(80)
        self.lbl_slider_temp.setFont(QFont(anta[0], 10))
        pagelayout.addWidget(self.lbl_slider_temp, 3, 2, alignment=Qt.AlignLeft)

        empty_label1 = QLabel("")
        pagelayout.addWidget(empty_label1, 4, 0, 1, 4)

        btn_licz = make_button("Sprawdź", bakerie, font_size=20)
        btn_licz.clicked.connect(self.policz)
        pagelayout.addWidget(btn_licz, 5, 0, 1, 4, alignment=Qt.AlignCenter)

        """empty_label2 = QLabel("")
        pagelayout.addWidget(empty_label2, 6, 0, 1, 4)

        self.label_result = QLabel("")
        self.label_result.setFont(QFont(anta[0], 15))
        #self.label_result.setWordWrap(True)
        pagelayout.addWidget(self.label_result, 7, 0, 2, 4, alignment=Qt.AlignmentFlag.AlignHCenter)"""

        empty_label3 = QLabel("")
        pagelayout.addWidget(empty_label3, 9, 0, 1, 4)

        btn_przepisy = make_button("Przepisy", bakerie)
        btn_przepisy.clicked.connect(self.close)
        btn_przepisy.clicked.connect(self.recipes_popup)
        pagelayout.addWidget(btn_przepisy, 10, 0, 1, 1, alignment=Qt.AlignCenter)

        btn_wybor = make_button("Wybór Pizzy", bakerie)
        btn_wybor.clicked.connect(self.go_back)
        btn_wybor.clicked.connect(self.close)
        pagelayout.addWidget(btn_wybor, 10, 1, 1, 1 , alignment=Qt.AlignCenter)

        btn_menu = make_button("Menu Główne", bakerie)
        btn_menu.clicked.connect(self.close)
        btn_menu.clicked.connect(self.open_main)
        pagelayout.addWidget(btn_menu, 10, 2, 1, 1, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)

        sizegrip = QSizeGrip(central_widget)
        sizegrip.setStyleSheet("border: 1px solid black;")
        pagelayout.addWidget(sizegrip, 11, 3, 1, 1,
                             alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)  # to right mowi w ktora str kursor jest skierowany chyba
        central_widget.setLayout(pagelayout)

    def updateLabel1(self, value):
        self.lbl_slider_sr.setText(str(value))

    def updateLabel2(self, value):
        self.lbl_slider_temp.setText(str(value))

    def recipes_popup(self):
        self.w = RecipesPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def go_back(self):
        self.w = MainPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def open_main(self):
        self.w = MainWindow()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    """def policz(self):
        temp = self.sld_temp.value()
        d = self.sld_srednica.value()
        tryb = self.cb.currentText()
        wynik = pizza(temp, d, tryb, "n")
        self.label_result.setText(f"Optymalny czas pieczenia to: {wynik}")"""
    def policz(self):
        anta = get_font()[0]
        temp = self.sld_temp.value()
        d = self.sld_srednica.value()
        tryb = self.cb.currentText()
        wynik = pizza(temp, d, tryb, "n")
        self.msg = QMessageBox()
        self.msg.setWindowTitle("")
        self.msg.setStyleSheet(f"background-color: {back_color};")
        self.msg.setText(f"Optymalny czas pieczenia pizzy to: {wynik}")
        self.msg.setFont(QFont(anta[0], 15))
        self.msg.exec_()


    def center(self):
        """
        Center window while opening.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class MainRzym(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {back_color};")
        self.setMinimumSize(min_width, min_height)
        self.center()
        self.resize(min_width, min_height)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        anta, bakerie = get_font()

        pagelayout = QGridLayout()

        lbl_rzymska = QLabel("Pizza Rzymska")
        lbl_rzymska.setFont(QFont(bakerie[0], 30))
        lbl_rzymska.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_rzymska, 1, 0, 1, 4, alignment=Qt.AlignCenter)

        lbl_tryb = QLabel("Tryb pieczenia")
        lbl_tryb.setFont(QFont(anta[0], 15))
        lbl_tryb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_tryb, 2, 0)

        self.toggle_button = QPushButton("Termoobieg", self)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setFont(QFont(anta[0], 10))
        self.toggle_button.clicked.connect(self.change_toggle)
        pagelayout.addWidget(self.toggle_button, 2, 1, alignment=Qt.AlignCenter)

        lbl_temp = QLabel("Maksymalna temperatura")
        lbl_temp.setWordWrap(True)
        lbl_temp.setFont(QFont(anta[0], 15))
        lbl_temp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_temp, 3, 0)

        self.sld_temp = QSlider(Qt.Orientation.Horizontal, self)
        self.sld_temp.setRange(180, 280)
        self.sld_temp.setPageStep(5)
        self.sld_temp.setStyleSheet(temp_bar)
        self.sld_temp.valueChanged.connect(self.updateLabeltemp)
        self.sld_temp.resize(self.sld_temp.sizeHint())
        pagelayout.addWidget(self.sld_temp, 3, 1)

        self.lbl_slider_temp = QLabel('180', self)
        self.lbl_slider_temp.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                          Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_temp.setMinimumWidth(80)
        self.lbl_slider_temp.setFont(QFont(anta[0], 10))
        pagelayout.addWidget(self.lbl_slider_temp, 3, 2)

        self.label_result = QLabel("")
        pagelayout.addWidget(self.label_result, 4, 2)

        btn_licz = make_button("Sprawdź", bakerie)
        btn_licz.clicked.connect(self.policz)
        pagelayout.addWidget(btn_licz, 4, 1)

        btn_przepisy = make_button("Przepisy", bakerie)
        btn_przepisy.clicked.connect(self.close)
        btn_przepisy.clicked.connect(self.recipes_popup)
        pagelayout.addWidget(btn_przepisy, 5, 0)

        btn_wybor = make_button("Wybór pizzy", bakerie)
        btn_wybor.clicked.connect(self.go_back)
        btn_wybor.clicked.connect(self.close)
        pagelayout.addWidget(btn_wybor, 5, 1)

        btn_menu = make_button("Menu Główne", bakerie)
        btn_menu.clicked.connect(self.close)
        btn_menu.clicked.connect(self.open_main)
        pagelayout.addWidget(btn_menu, 5, 2)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)

        sizegrip = QSizeGrip(central_widget)
        sizegrip.setStyleSheet("border: 1px solid black;")
        pagelayout.addWidget(sizegrip, 5, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        central_widget.setLayout(pagelayout)

    def recipes_popup(self):
        self.w = RecipesPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def go_back(self):
        self.w = MainPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def open_main(self):
        self.w = MainWindow()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def policz(self):
        tryb = self.toggle_button.text()
        temp = self.sld_temp.value()
        wynik = pizza(temp, 30, tryb, "r")
        self.label_result.setText(f"Optymalny czas pieczenia to: {wynik}")

    def change_toggle(self):
        if self.toggle_button.isChecked():
            self.toggle_button.setText("Góra-dół")
        else:
            self.toggle_button.setText("Termoobieg")
        # mozna jeszcze pomyslec czy chcemy zmieniac jego kolor

    def updateLabeltemp(self, value):
        self.lbl_slider_temp.setText(str(value))

    def center(self):
        """
        Center window while opening.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class MainAmeryka(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {back_color};")
        self.setMinimumSize(min_width, min_height)
        self.center()
        self.resize(min_width, min_height)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        anta, bakerie = get_font()

        pagelayout = QGridLayout()

        lbl_rzymska = QLabel("Pizza Amerykańska")
        lbl_rzymska.setFont(QFont(bakerie[0], 30))
        lbl_rzymska.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_rzymska, 1, 0, 1, 4, alignment=Qt.AlignCenter)

        lbl_tryb = QLabel("Tryb pieczenia")
        lbl_tryb.setFont(QFont(anta[0], 15))
        lbl_tryb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_tryb, 2, 0)

        self.toggle_button = QPushButton("Termoobieg", self)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setFont(QFont(anta[0], 9))
        self.toggle_button.clicked.connect(self.change_toggle)
        pagelayout.addWidget(self.toggle_button, 2, 1, alignment=Qt.AlignCenter)

        lbl_temp = QLabel("Maksymalna temperatura")
        lbl_temp.setWordWrap(True)
        lbl_temp.setFont(QFont(anta[0], 15))
        lbl_temp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_temp, 3, 0)

        self.sld_temp = QSlider(Qt.Orientation.Horizontal, self)
        self.sld_temp.setRange(180, 280)
        self.sld_temp.setPageStep(5)
        self.sld_temp.valueChanged.connect(self.updateLabeltemp)
        pagelayout.addWidget(self.sld_temp, 3, 1)

        self.lbl_slider_temp = QLabel('180', self)
        self.lbl_slider_temp.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                          Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_temp.setMinimumWidth(80)
        self.lbl_slider_temp.setFont(QFont(anta[0], 10))
        pagelayout.addWidget(self.lbl_slider_temp, 3, 2)

        self.label_result = QLabel("")
        pagelayout.addWidget(self.label_result, 4, 2)

        btn_licz = make_button("Sprawdź", bakerie)
        btn_licz.clicked.connect(self.policz)
        pagelayout.addWidget(btn_licz, 4, 1)

        btn_przepisy = make_button("Przepisy", bakerie)
        btn_przepisy.clicked.connect(self.close)
        btn_przepisy.clicked.connect(self.recipes_popup)
        pagelayout.addWidget(btn_przepisy, 5, 0)

        btn_wybor = make_button("Wybór Pizzy", bakerie)
        btn_wybor.clicked.connect(self.go_back)
        btn_wybor.clicked.connect(self.close)
        pagelayout.addWidget(btn_wybor, 5, 1)

        btn_menu = make_button("Menu Główne", bakerie)
        btn_menu.clicked.connect(self.close)
        btn_menu.clicked.connect(self.open_main)
        pagelayout.addWidget(btn_menu, 5, 2)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)

        sizegrip = QSizeGrip(central_widget)
        sizegrip.setStyleSheet("border: 1px solid black;")
        pagelayout.addWidget(sizegrip, 5, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        central_widget.setLayout(pagelayout)

    def recipes_popup(self):
        self.w = RecipesPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def policz(self):
        tryb = self.toggle_button.text()
        temp = self.sld_temp.value()
        wynik = pizza(temp, 30, tryb, "a")
        self.label_result.setText(f"Optymalny czas pieczenia to: {wynik}")

    def go_back(self):
        self.w = MainPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def open_main(self):
        self.w = MainWindow()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def change_toggle(self):
        if self.toggle_button.isChecked():
            self.toggle_button.setText("Góra-dół")
        else:
            self.toggle_button.setText("Termoobieg")
        # mozna jeszcze pomyslec czy chcemy zmieniac jego kolor

    def updateLabeltemp(self, value):
        self.lbl_slider_temp.setText(str(value))

    def center(self):
        """
        Center window while opening.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class MainWindow(QMainWindow):
    """
    Main window of application. (troche  burdello cyk cyk, wszystko w jednym, mozna rozdzielic wyglad i funkcjonalnosc na fnkcje osobne)
    """

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {back_color};")
        self.setMinimumSize(min_width, min_height)
        self.center()
        self.resize(min_width, min_height)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        bakerie = get_font()[1]

        pagelayout = QVBoxLayout()
        label = QLabel(
            "Super Pizzowa Aplikacja")  # jak to po polsku ladnie napisac to ja nie mam pojecia xd welcome to pizza app
        label.setWordWrap(True)
        label.setFont(QFont(bakerie[0], 40))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setScaledContents(True)  # no nie dziala gowno
        label.setAlignment(QtCore.Qt.AlignCenter)
        pagelayout.addWidget(label)

        btn = QPushButton("Przepisy")
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # rozszerza sie przycisk jak rozszerzamy
        btn.setFont(QFont(bakerie[0], 20))
        btn.clicked.connect(self.recipes_popup)
        btn.clicked.connect(self.close)
        # btn.setStyleSheet("background-image : url(pobrane.jpeg);") #nie wiem czemu to nie dziala, mam wrazenie ze to qtmodern psuje ale nie wiem
        # btn.setStyleSheet("border-image : url(pizza.png);") to powinno od razu dopasowywac wymiary zdjecia ale no narazie nie dziala
        pagelayout.addWidget(btn)

        btn = QPushButton('Główne')
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.setFont(QFont(bakerie[0], 20))
        btn.clicked.connect(self.main_popup)
        btn.clicked.connect(self.close)
        pagelayout.addWidget(btn)

        btn = QPushButton('Jak to działa?')
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.setFont(QFont(bakerie[0], 20))
        btn.clicked.connect(self.instructions_popup)
        btn.clicked.connect(self.close)
        pagelayout.addWidget(btn)

        """
        Dodac opcje ze jak zwiekszamy okno to zwieksza sie tez font labeli i font na buttonach. tu jakis link ale sredni chyba
        https://www.youtube.com/watch?v=3kGKWkQqipc&list=PL3JVwFmb_BnRpvOeIh_To4YSiebiggyXS&index=22
        """

        # dodac moze jakies zdjecia w tle na tych przyciskach
        # nie wiem czy robimy juz te podstronki ale chyba by sie przydalo jakas jedna chociaz, moze ta z przepisami

        widget = QWidget()
        self.setCentralWidget(widget)
        sizegrip = QSizeGrip(widget)
        sizegrip.setStyleSheet("border: 1px solid black;")
        pagelayout.addWidget(sizegrip, 0,
                             QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)  # to right mowi w ktora str kursor jest skierowany chyba
        widget.setLayout(pagelayout)

    def recipes_popup(self):
        """
        Display popup window with pizza recipes.
        """
        self.w = RecipesPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def main_popup(self):
        self.w = MainPopup()
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

    """def closeEvent(self, event):
        QApplication.closeAllWindows()
        event.accept()"""


def main():
    App = QApplication(sys.argv)
    window = MainWindow()
    qtmodern.styles.dark(App)
    mw = qtmodern.windows.ModernWindow(window)
    mw.show()
    # App.aboutToQuit.connect(window.closeEvent)
    sys.exit(App.exec())


if __name__ == '__main__':
    main()
