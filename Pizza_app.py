from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget, QGridLayout, QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as canvas
import qtmodern.styles
import qtmodern.windows
import sys
from PyQt5.QtWidgets import QDesktopWidget
from constant import *


# https://stackoverflow.com/questions/52596386/slide-qstackedwidget-page slide pages
class SlidingStackedWidget(QStackedWidget):
    """
    Create sliding stacked widget (sliding pages).
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


class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {back_color};")
        self.setFixedSize(window_width, widow_height)
        self.center()

        self.anta = get_font()[0][0]
        self.bakerie = get_font()[1]

    def recipes_popup(self):
        self.w = RecipesPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def main_popup(self):
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

    def updateLabeltemp(self, value):
        """Update label with oven temperature when user change the slider"""
        self.lbl_slider_temp.setText(str(value*5) + "°C")

    def updateLabelsr(self, value):
        """Upate label with pizza diameter when user change the slider"""
        self.lbl_slider_sr.setText(str(value) + "cm")

    def center(self):
        """
        Center window while opening.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def instructions_popup(self):
        """
        Display popup window with app instructions.
        """
        self.w = InstructionsPopup()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def policz(self, pizza_type):
        temp = int(self.sld_temp.value() * 5)
        if pizza_type in ["r", "a"]:
            tryb = self.toggle_button.text()
            wynik = pizza(temp, 30, tryb, pizza_type)
        elif pizza_type == "n":
            d = self.sld_srednica.value()
            tryb = self.cb.currentText()
            wynik = pizza(temp, d, tryb, "n")
        self.msg = QMessageBox()
        self.msg.setWindowTitle("")
        self.msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.msg.setStyleSheet(f"background-color: {back_color};")
        self.msg.setText(f"Optymalny czas pieczenia pizzy to: \n                  {wynik}")
        self.msg.setFont(QFont(self.anta, 15))
        back_button = QPushButton("Wróć")
        self.msg.addButton(back_button, QMessageBox.YesRole)
        self.msg.setStyleSheet(msg_style)
        self.msg.exec_()


class RecipesPopup(QMainWindow):
    """
    Create window with pizza recipes.
    """

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {back_color};")
        self.setFixedSize(window_width, widow_height)
        self.center()

        bakerie = get_font()[1][0]
        anta = get_font()[0][0]

        self.slidingStacked = SlidingStackedWidget()

        neapol_przepis = QLabel(neapol_format.format(bakerie, anta, przepis_neapol))
        ameryka_przepis = QLabel(ameryka_format.format(bakerie, anta, przepis_ameryka))
        rzym_przepis = QLabel(rzym_format.format(bakerie, anta, przepis_rzym))

        neapol_przepis.setWordWrap(True)
        ameryka_przepis.setWordWrap(True)
        rzym_przepis.setWordWrap(True)
        self.slidingStacked.addWidget(neapol_przepis)
        self.slidingStacked.addWidget(ameryka_przepis)
        self.slidingStacked.addWidget(rzym_przepis)

        button_prev = QPushButton("Poprzednia")
        button_prev.clicked.connect(self.slidingStacked.slideInPrev)
        button_prev.setFont(QFont(bakerie, 15))
        button_next = QPushButton("Następna")
        button_next.clicked.connect(self.slidingStacked.slideInNext)
        button_next.setFont(QFont(bakerie, 15))

        hlay = QHBoxLayout()
        hlay.addWidget(button_prev)
        hlay.addWidget(button_next)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        lay = QVBoxLayout(central_widget)
        lay.addLayout(hlay)
        lay.addWidget(self.slidingStacked)

        sec_lay = QHBoxLayout()
        button_main_func = QPushButton("Wybierz")
        button_main_func.setMinimumWidth(150)
        button_main_func.setFont(QFont(bakerie, 15))
        button_main_func.clicked.connect(self.close)
        button_main_func.clicked.connect(self.open_main)
        sec_lay.addWidget(button_main_func)
        sec_lay.setAlignment(Qt.AlignCenter)
        lay.addLayout(sec_lay)

        btn_main = QPushButton("Menu Główne")
        btn_main.setMinimumWidth(150)
        btn_main.setFont(QFont(bakerie, 15))
        btn_main.clicked.connect(self.close)
        btn_main.clicked.connect(self.main_window)
        sec_lay.addWidget(btn_main)

        central_widget.setLayout(lay)

    def open_main(self):
        """Open main window for certain pizza."""
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
        """Open main app window. """
        self.w = MainWindow()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()


class MainPopup(QMainWindow):
    """
    Create pop up window with main app funcionality where user can first choose certain pizza.
    """

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {back_color};")
        self.setFixedSize(window_width, widow_height)
        self.center()

        anta, bakerie = get_font()

        label = QLabel("Wybierz rodzaj pizzy.")
        label.setWordWrap(True)  # zawija tekst
        pagelayout = QVBoxLayout()
        label.setFont(QFont(bakerie[0], 40))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setAlignment(QtCore.Qt.AlignCenter)
        pagelayout.addWidget(label)

        btn_neapol = make_button("Neapolitańska", bakerie, 0, 0, font_size=20)
        btn_neapol.clicked.connect(self.neapol)
        btn_neapol.clicked.connect(self.close)
        pagelayout.addWidget(btn_neapol)

        btn_ameryka = make_button("Amerykańska", bakerie, 0, 0, font_size=20)
        btn_ameryka.clicked.connect(self.ameryka)
        btn_ameryka.clicked.connect(self.close)
        pagelayout.addWidget(btn_ameryka)

        btn_rzym = make_button("Rzymska", bakerie, 0, 0, font_size=20)
        btn_rzym.clicked.connect(self.rzym)
        btn_rzym.clicked.connect(self.close)
        pagelayout.addWidget(btn_rzym)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
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
        """Open window for neapolitan pizza with main functionality."""
        self.w = MainNeapol()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def rzym(self):
        """Open window for rome pizza with main functionality."""
        self.w = MainRzym()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def ameryka(self):
        """Open window for american pizza with main functionality."""
        self.w = MainAmeryka()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()


class InstructionsPopup(HelpWindow):
    """
    Create window with app's instructions.
    """

    def __init__(self):
        super().__init__()
        pagelayout = QVBoxLayout()
        label_naglowek = QLabel("Instrukcje")
        label_naglowek.setFont(QFont(self.bakerie[0], 40))
        pagelayout.addWidget(label_naglowek, alignment=Qt.AlignCenter)

        label = QLabel(instructions)
        label.setWordWrap(True)
        label.setFont(QFont(self.anta, 15))
        pagelayout.addWidget(label)

        empty_label = QLabel("")
        empty_label.setFont(QFont(self.bakerie[0], 10))
        pagelayout.addWidget(empty_label)

        btn = QPushButton("Menu główne")
        btn.setFont(QFont(self.bakerie[0], 20))
        btn.clicked.connect(self.close)
        btn.clicked.connect(self.open_main)
        pagelayout.addWidget(btn)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)


class MainNeapol(HelpWindow):
    """Create window for neapolitan pizza with main functionality."""

    def __init__(self):
        super().__init__()

        pagelayout = QGridLayout()

        lbl_neapol = QLabel("Pizza Neapolitańska")
        lbl_neapol.setFont(QFont(self.bakerie[0], 30))
        lbl_neapol.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_neapol, 0, 0, 1, 3, alignment=Qt.AlignCenter)

        self.empty_label0 = QLabel("")
        pagelayout.addWidget(self.empty_label0, 2, 0)

        lbl_tryb = QLabel("Tryb pieczenia")
        lbl_tryb.setFont(QFont(self.anta, 15))
        pagelayout.addWidget(lbl_tryb, 3, 0)

        self.cb = QComboBox()
        self.cb.addItems(tryby)
        self.cb.setFont(QFont(self.anta, 12))
        self.cb.setStyleSheet(f"selection-background-color: {select_color};")
        pagelayout.addWidget(self.cb, 3, 1, alignment=Qt.AlignCenter)

        lbl_empty = QLabel("")
        pagelayout.addWidget(lbl_empty, 4, 0, 1, 1)

        lbl_srednica = QLabel("Średnica")
        lbl_srednica.setFont(QFont(self.anta, 15))
        pagelayout.addWidget(lbl_srednica, 5, 0)

        self.sld_srednica = QSlider(Qt.Orientation.Horizontal, self)
        self.sld_srednica.setRange(20, 40)
        self.sld_srednica.setPageStep(1)
        self.sld_srednica.setStyleSheet(size_bar)
        self.sld_srednica.setSliderPosition(30)
        self.sld_srednica.valueChanged.connect(self.updateLabelsr)
        pagelayout.addWidget(self.sld_srednica, 5, 1)

        self.lbl_slider_sr = QLabel('30cm', self)
        self.lbl_slider_sr.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                        Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_sr.setMinimumWidth(80)
        self.lbl_slider_sr.setFont(QFont(self.anta, 10))
        pagelayout.addWidget(self.lbl_slider_sr, 5, 2, alignment=Qt.AlignLeft)

        lbl_empty2 = QLabel("")
        pagelayout.addWidget(lbl_empty2, 6, 0, 1, 1)

        lbl_temp = QLabel("Maksymalna temperatura")
        lbl_temp.setWordWrap(True)
        lbl_temp.setFont(QFont(self.anta, 15))
        pagelayout.addWidget(lbl_temp, 7, 0)

        self.sld_temp = QSlider(Qt.Orientation.Horizontal, self)
        self.sld_temp.setRange(36, 56)
        self.sld_temp.setSingleStep(1)
        self.sld_temp.setSliderPosition(44)
        self.sld_temp.setStyleSheet(temp_bar)
        self.sld_temp.valueChanged.connect(self.updateLabeltemp)
        pagelayout.addWidget(self.sld_temp, 7, 1)

        self.lbl_slider_temp = QLabel('220°C', self)
        self.lbl_slider_temp.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                          Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_temp.setMinimumWidth(80)
        self.lbl_slider_temp.setFont(QFont(self.anta, 10))
        pagelayout.addWidget(self.lbl_slider_temp, 7, 2, alignment=Qt.AlignLeft)

        empty_label1 = QLabel("")
        pagelayout.addWidget(empty_label1, 8, 0, 1, 3)

        btn_licz = make_button("Sprawdź", self.bakerie, font_size=20)
        btn_licz.clicked.connect(lambda: self.policz("n"))
        pagelayout.addWidget(btn_licz, 9, 1, alignment=Qt.AlignCenter)

        empty_label3 = QLabel("")
        pagelayout.addWidget(empty_label3, 10, 0, 1, 3)

        btn_przepisy = make_button("Przepisy", self.bakerie)
        btn_przepisy.clicked.connect(self.close)
        btn_przepisy.clicked.connect(self.recipes_popup)
        pagelayout.addWidget(btn_przepisy, 11, 0, alignment=Qt.AlignCenter)

        btn_wybor = make_button("Wybór Pizzy", self.bakerie)
        btn_wybor.clicked.connect(self.main_popup)
        btn_wybor.clicked.connect(self.close)
        pagelayout.addWidget(btn_wybor, 11, 1, alignment=Qt.AlignCenter)

        btn_menu = make_button("Menu Główne", self.bakerie)
        btn_menu.clicked.connect(self.close)
        btn_menu.clicked.connect(self.open_main)
        pagelayout.addWidget(btn_menu, 11, 2, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)


class MainRzym(HelpWindow):
    """Create window for rome pizza with main functionality."""

    def __init__(self):
        super().__init__()

        pagelayout = QGridLayout()

        lbl_rzymska = QLabel("Pizza Rzymska")
        lbl_rzymska.setFont(QFont(self.bakerie[0], 30))
        lbl_rzymska.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_rzymska, 1, 0, 1, 3, alignment=Qt.AlignCenter)

        self.empty_label0 = QLabel("")
        pagelayout.addWidget(self.empty_label0, 2, 0)

        lbl_tryb = QLabel("Tryb pieczenia")
        lbl_tryb.setFont(QFont(self.anta, 15))
        pagelayout.addWidget(lbl_tryb, 3, 0)

        self.toggle_button = QPushButton("Termoobieg", self)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setFont(QFont(self.anta, 12))
        self.toggle_button.clicked.connect(self.change_toggle)
        pagelayout.addWidget(self.toggle_button, 3, 1, alignment=Qt.AlignCenter)

        lbl_empty = QLabel("")
        pagelayout.addWidget(lbl_empty, 4, 0, 1, 1)

        lbl_temp = QLabel("Maksymalna temperatura")
        lbl_temp.setWordWrap(True)
        lbl_temp.setFont(QFont(self.anta, 15))
        pagelayout.addWidget(lbl_temp, 5, 0)

        self.sld_temp = QSlider(Qt.Orientation.Horizontal, self)
        self.sld_temp.setRange(36, 56)
        self.sld_temp.setSingleStep(1)
        self.sld_temp.setSliderPosition(44)
        self.sld_temp.setStyleSheet(temp_bar)
        self.sld_temp.valueChanged.connect(self.updateLabeltemp)
        self.sld_temp.resize(self.sld_temp.sizeHint())
        pagelayout.addWidget(self.sld_temp, 5, 1)

        self.lbl_slider_temp = QLabel('220°C', self)
        self.lbl_slider_temp.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                          Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_temp.setMinimumWidth(80)
        self.lbl_slider_temp.setFont(QFont(self.anta, 10))
        pagelayout.addWidget(self.lbl_slider_temp, 5, 2, alignment=Qt.AlignLeft)

        self.empty_label1 = QLabel("")
        pagelayout.addWidget(self.empty_label1, 6, 0, 1, 3)

        btn_licz = make_button("Sprawdź", self.bakerie, font_size=20)
        btn_licz.clicked.connect(lambda: self.policz("r"))
        pagelayout.addWidget(btn_licz, 7, 1, alignment=Qt.AlignCenter)

        empty_label1 = QLabel("")
        pagelayout.addWidget(empty_label1, 8, 2, 1, 3)

        btn_przepisy = make_button("Przepisy", self.bakerie)
        btn_przepisy.clicked.connect(self.close)
        btn_przepisy.clicked.connect(self.recipes_popup)
        pagelayout.addWidget(btn_przepisy, 9, 0, alignment=Qt.AlignCenter)

        btn_wybor = make_button("Wybór pizzy", self.bakerie)
        btn_wybor.clicked.connect(self.main_popup)
        btn_wybor.clicked.connect(self.close)
        pagelayout.addWidget(btn_wybor, 9, 1, alignment=Qt.AlignCenter)

        btn_menu = make_button("Menu Główne", self.bakerie)
        btn_menu.clicked.connect(self.close)
        btn_menu.clicked.connect(self.open_main)
        pagelayout.addWidget(btn_menu, 9, 2, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)


class MainAmeryka(HelpWindow):
    """Create window for american pizza with main functionality."""

    def __init__(self):
        super().__init__()

        pagelayout = QGridLayout()

        lbl_rzymska = QLabel("Pizza Amerykańska")
        lbl_rzymska.setFont(QFont(self.bakerie[0], 30))
        lbl_rzymska.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pagelayout.addWidget(lbl_rzymska, 1, 0, 1, 4, alignment=Qt.AlignCenter)

        self.empty_label0 = QLabel("")
        pagelayout.addWidget(self.empty_label0, 2, 0)

        lbl_tryb = QLabel("Tryb pieczenia")
        lbl_tryb.setFont(QFont(self.anta, 15))
        pagelayout.addWidget(lbl_tryb, 3, 0)

        self.toggle_button = QPushButton("Termoobieg", self)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setFont(QFont(self.anta, 12))
        self.toggle_button.clicked.connect(self.change_toggle)
        pagelayout.addWidget(self.toggle_button, 3, 1, alignment=Qt.AlignCenter)

        lbl_empty = QLabel("")
        pagelayout.addWidget(lbl_empty, 4, 0, 1, 1)

        lbl_temp = QLabel("Maksymalna temperatura")
        lbl_temp.setWordWrap(True)
        lbl_temp.setFont(QFont(self.anta, 15))
        pagelayout.addWidget(lbl_temp, 5, 0)

        self.sld_temp = QSlider(Qt.Orientation.Horizontal, self)
        self.sld_temp.setRange(36, 56)
        self.sld_temp.setSingleStep(1)
        self.sld_temp.setSliderPosition(44)
        self.sld_temp.setStyleSheet(temp_bar)
        self.sld_temp.valueChanged.connect(self.updateLabeltemp)
        pagelayout.addWidget(self.sld_temp, 5, 1)

        self.lbl_slider_temp = QLabel('220°C', self)
        self.lbl_slider_temp.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                          Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_temp.setMinimumWidth(80)
        self.lbl_slider_temp.setFont(QFont(self.anta, 10))
        pagelayout.addWidget(self.lbl_slider_temp, 5, 2)

        self.empty_label1 = QLabel("")
        pagelayout.addWidget(self.empty_label1, 6, 2, 1, 3)

        btn_licz = make_button("Sprawdź", self.bakerie, font_size=20)
        btn_licz.clicked.connect(lambda: self.policz("a"))
        pagelayout.addWidget(btn_licz, 7, 1, alignment=Qt.AlignCenter)

        self.empty_label2 = QLabel("")
        pagelayout.addWidget(self.empty_label2, 8, 2, 1, 3)

        btn_przepisy = make_button("Przepisy", self.bakerie)
        btn_przepisy.clicked.connect(self.close)
        btn_przepisy.clicked.connect(self.recipes_popup)
        pagelayout.addWidget(btn_przepisy, 9, 0, alignment=Qt.AlignCenter)

        btn_wybor = make_button("Wybór Pizzy", self.bakerie)
        btn_wybor.clicked.connect(self.main_popup)
        btn_wybor.clicked.connect(self.close)
        pagelayout.addWidget(btn_wybor, 9, 1, alignment=Qt.AlignCenter)

        btn_menu = make_button("Menu Główne", self.bakerie)
        btn_menu.clicked.connect(self.close)
        btn_menu.clicked.connect(self.open_main)
        pagelayout.addWidget(btn_menu, 9, 2, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)


class MainWindow(HelpWindow):
    """
    Main window of application.
    """

    def __init__(self):
        super().__init__()

        pagelayout = QVBoxLayout()
        label = QLabel(
            "Super Pizzowa Aplikacja")
        label.setWordWrap(True)
        label.setFont(QFont(self.bakerie[0], 40))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setAlignment(QtCore.Qt.AlignCenter)
        pagelayout.addWidget(label)

        btn = QPushButton("Przepisy")
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.setFont(QFont(self.bakerie[0], 20))
        btn.clicked.connect(self.recipes_popup)
        btn.clicked.connect(self.close)
        pagelayout.addWidget(btn)

        btn = QPushButton('Wybór pizzy')
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.setFont(QFont(self.bakerie[0], 20))
        btn.clicked.connect(self.main_popup)
        btn.clicked.connect(self.close)
        pagelayout.addWidget(btn)

        btn = QPushButton('Jak to działa?')
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.setFont(QFont(self.bakerie[0], 20))
        btn.clicked.connect(self.instructions_popup)
        btn.clicked.connect(self.close)
        pagelayout.addWidget(btn)

        widget = QWidget()
        self.setCentralWidget(widget)
        widget.setLayout(pagelayout)


def main():
    App = QApplication(sys.argv)
    window = MainWindow()
    qtmodern.styles.dark(App)
    mw = qtmodern.windows.ModernWindow(window)
    mw.show()
    sys.exit(App.exec())


if __name__ == '__main__':
    main()
