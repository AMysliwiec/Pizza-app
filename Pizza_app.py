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
    """
    A class inheriting QMainWindow with added universal methods used in the application
    """

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {back_color};")
        self.setFixedSize(window_width, window_height)
        self.center()
        self.anta = get_font()[0][0]
        self.bakerie = get_font()[1][0]

    def center(self):
        """
        Center window while opening.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def recipes_popup(self):
        self.w = Recipes()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def choice_popup(self):
        self.w = PizzaChoice()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def instructions_popup(self):
        """
        Display popup window with app instructions.
        """
        self.w = Instructions()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def open_main(self):
        self.w = MainWindow()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def open_choice(self):
        """Open main window for certain pizza directly from the recipe."""
        if self.slidingStacked.currentIndex() == 0:
            self.w = Neapolitan()
            self.mw = qtmodern.windows.ModernWindow(self.w)
            self.mw.show()
        elif self.slidingStacked.currentIndex() == 1:
            self.w = American()
            self.mw = qtmodern.windows.ModernWindow(self.w)
            self.mw.show()
        else:
            self.w = Roman()
            self.mw = qtmodern.windows.ModernWindow(self.w)
            self.mw.show()

    def change_toggle(self):
        if self.toggle_button.isChecked():
            self.toggle_button.setText("Góra-dół")
        else:
            self.toggle_button.setText("Termoobieg")

    def updatelabeltemp(self, value):
        """Update label with oven temperature when user change the slider"""
        self.lbl_slider_temp.setText(str(value * 5) + "°C")

    def updatelabelstr(self, value):
        """Upate label with pizza diameter when user change the slider"""
        self.lbl_slider_sr.setText(str(value) + "cm")

    def estimate(self, pizza_type):
        temp = int(self.sld_temp.value() * 5)
        if pizza_type in ["r", "a"]:
            tryb = self.toggle_button.text()
            wynik = pizza(temp, 30, tryb, pizza_type)
        elif pizza_type == "n":
            d = self.sld_diameter.value()
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

    def neapolitan(self):
        """Open window for neapolitan pizza with main functionality."""
        self.w = Neapolitan()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def roman(self):
        """Open window for rome pizza with main functionality."""
        self.w = Roman()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()

    def american(self):
        """Open window for american pizza with main functionality."""
        self.w = American()
        self.mw = qtmodern.windows.ModernWindow(self.w)
        self.mw.show()


class Recipes(HelpWindow):
    """
    Create window with pizza recipes.
    """

    def __init__(self):
        super().__init__()

        self.slidingStacked = SlidingStackedWidget()

        neapolitan_recipe_input = QLabel(neapol_format.format(self.bakerie, self.anta, neapolitan_recipe))
        american_recipe_input = QLabel(ameryka_format.format(self.bakerie, self.anta, american_recipe))
        roman_recipe_input = QLabel(rzym_format.format(self.bakerie, self.anta, roman_recipe))

        neapolitan_recipe_input.setWordWrap(True)
        american_recipe_input.setWordWrap(True)
        roman_recipe_input.setWordWrap(True)
        self.slidingStacked.addWidget(neapolitan_recipe_input)
        self.slidingStacked.addWidget(american_recipe_input)
        self.slidingStacked.addWidget(roman_recipe_input)

        button_prev = make_button("Poprzednia", self.bakerie, 0, 0, 15, False)
        button_prev.clicked.connect(self.slidingStacked.slideInPrev)

        button_next = make_button("Następna", self.bakerie, 0, 0, 15, False)
        button_next.clicked.connect(self.slidingStacked.slideInNext)

        hlay = QHBoxLayout()
        hlay.addWidget(button_prev)
        hlay.addWidget(button_next)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        lay = QVBoxLayout(central_widget)
        lay.addLayout(hlay)
        lay.addWidget(self.slidingStacked)

        sec_lay = QHBoxLayout()
        button_main_func = make_button("Wybierz", self.bakerie, 150, 0, 15, False)
        button_main_func.clicked.connect(self.close)
        button_main_func.clicked.connect(self.open_choice)
        sec_lay.addWidget(button_main_func)
        sec_lay.setAlignment(Qt.AlignCenter)
        lay.addLayout(sec_lay)

        btn_main = make_button("Menu Główne", self.bakerie, 150, 0, 15, False)
        btn_main.clicked.connect(self.close)
        btn_main.clicked.connect(self.open_main)
        sec_lay.addWidget(btn_main)

        central_widget.setLayout(lay)


class PizzaChoice(HelpWindow):
    """
    Create pop up window with main app funcionality where user can first choose certain pizza.
    """

    def __init__(self):
        super().__init__()

        pagelayout = QVBoxLayout()
        label = make_label("Wybierz rodzaj pizzy", self.bakerie, 40)
        pagelayout.addWidget(label)

        btn_n = make_button("Neapolitańska", self.bakerie, 0, 0, font_size=20)
        btn_n.clicked.connect(self.neapolitan)
        btn_n.clicked.connect(self.close)
        pagelayout.addWidget(btn_n)

        btn_a = make_button("Amerykańska", self.bakerie, 0, 0, font_size=20)
        btn_a.clicked.connect(self.american)
        btn_a.clicked.connect(self.close)
        pagelayout.addWidget(btn_a)

        btn_r = make_button("Rzymska", self.bakerie, 0, 0, font_size=20)
        btn_r.clicked.connect(self.roman)
        btn_r.clicked.connect(self.close)
        pagelayout.addWidget(btn_r)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)


class Instructions(HelpWindow):
    """
    Create window with app's instructions.
    """

    def __init__(self):
        super().__init__()
        pagelayout = QVBoxLayout()
        label_naglowek = make_label("Instrukcje", self.bakerie, 40)
        pagelayout.addWidget(label_naglowek, alignment=Qt.AlignCenter)

        empty_label1 = QLabel("")
        empty_label1.setFont(QFont(self.bakerie, 10))
        pagelayout.addWidget(empty_label1)

        label = make_label(instructions, self.anta, 12, False, False)
        pagelayout.addWidget(label)

        label2 = make_label("Smacznego!", self.bakerie, 20, True, False)
        pagelayout.addWidget(label2)

        empty_label2 = QLabel("")
        empty_label2.setFont(QFont(self.bakerie, 10))
        pagelayout.addWidget(empty_label2)

        btn = make_button("Menu główne", self.bakerie, 0, 0, 20, expand=False)
        btn.clicked.connect(self.close)
        btn.clicked.connect(self.open_main)
        pagelayout.addWidget(btn)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)


class Neapolitan(HelpWindow):
    """Create window for neapolitan pizza with main functionality."""

    def __init__(self):
        super().__init__()

        pagelayout = QGridLayout()

        lbl_n = make_label("Pizza Neapolitańśka", self.bakerie, 30)
        pagelayout.addWidget(lbl_n, 0, 0, 1, 3, alignment=Qt.AlignCenter)

        self.empty_label0 = QLabel("")
        pagelayout.addWidget(self.empty_label0, 2, 0)

        lbl_mode = make_label("Tryb pieczenia", self.anta, 15, False, False)
        pagelayout.addWidget(lbl_mode, 3, 0)

        self.cb = QComboBox()
        self.cb.addItems(oven_mode)
        self.cb.setFont(QFont(self.anta, 12))
        self.cb.setStyleSheet(f"selection-background-color: {select_color};")
        pagelayout.addWidget(self.cb, 3, 1, alignment=Qt.AlignCenter)

        lbl_empty = QLabel("")
        pagelayout.addWidget(lbl_empty, 4, 0, 1, 1)

        lbl_diameter = make_label("Średnica", self.anta, 15, False, False)
        pagelayout.addWidget(lbl_diameter, 5, 0)

        self.sld_diameter = QSlider(Qt.Orientation.Horizontal, self)
        self.sld_diameter.setRange(20, 40)
        self.sld_diameter.setPageStep(1)
        self.sld_diameter.setStyleSheet(size_bar)
        self.sld_diameter.setSliderPosition(30)
        self.sld_diameter.valueChanged.connect(self.updatelabelstr)
        pagelayout.addWidget(self.sld_diameter, 5, 1)

        self.lbl_slider_diam = QLabel('30cm', self)
        self.lbl_slider_diam.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                          Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_diam.setMinimumWidth(80)
        self.lbl_slider_diam.setFont(QFont(self.anta, 10))
        pagelayout.addWidget(self.lbl_slider_diam, 5, 2, alignment=Qt.AlignLeft)

        lbl_empty2 = QLabel("")
        pagelayout.addWidget(lbl_empty2, 6, 0, 1, 1)

        lbl_temp = make_label("Temperatura", self.anta, 15, False, False)
        pagelayout.addWidget(lbl_temp, 7, 0)

        self.sld_temp = QSlider(Qt.Orientation.Horizontal, self)
        self.sld_temp.setRange(36, 56)
        self.sld_temp.setSingleStep(1)
        self.sld_temp.setSliderPosition(44)
        self.sld_temp.setStyleSheet(temp_bar)
        self.sld_temp.valueChanged.connect(self.updatelabeltemp)
        pagelayout.addWidget(self.sld_temp, 7, 1)

        self.lbl_slider_temp = QLabel('220°C', self)
        self.lbl_slider_temp.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                          Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_temp.setMinimumWidth(80)
        self.lbl_slider_temp.setFont(QFont(self.anta, 10))
        pagelayout.addWidget(self.lbl_slider_temp, 7, 2, alignment=Qt.AlignLeft)

        empty_label1 = QLabel("")
        pagelayout.addWidget(empty_label1, 8, 0, 1, 3)

        btn_estimate = make_button("Sprawdź", self.bakerie, font_size=20)
        btn_estimate.clicked.connect(lambda: self.estimate("n"))
        pagelayout.addWidget(btn_estimate, 9, 1, alignment=Qt.AlignCenter)

        empty_label3 = QLabel("")
        pagelayout.addWidget(empty_label3, 10, 0, 1, 3)

        btn_recipes = make_button("Przepisy", self.bakerie)
        btn_recipes.clicked.connect(self.close)
        btn_recipes.clicked.connect(self.recipes_popup)
        pagelayout.addWidget(btn_recipes, 11, 0, alignment=Qt.AlignCenter)

        btn_choice = make_button("Wybór Pizzy", self.bakerie)
        btn_choice.clicked.connect(self.choice_popup)
        btn_choice.clicked.connect(self.close)
        pagelayout.addWidget(btn_choice, 11, 1, alignment=Qt.AlignCenter)

        btn_menu = make_button("Menu Główne", self.bakerie)
        btn_menu.clicked.connect(self.close)
        btn_menu.clicked.connect(self.open_main)
        pagelayout.addWidget(btn_menu, 11, 2, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)


class Roman(HelpWindow):
    """Create window for rome pizza with main functionality."""

    def __init__(self):
        super().__init__()

        pagelayout = QGridLayout()

        lbl_r = make_label("Pizza Rzymska", self.bakerie, 30)
        pagelayout.addWidget(lbl_r, 1, 0, 1, 3, alignment=Qt.AlignCenter)

        self.empty_label0 = QLabel("")
        pagelayout.addWidget(self.empty_label0, 2, 0)

        lbl_mode = make_label("Tryb pieczenia", self.anta, 15, False, False)
        pagelayout.addWidget(lbl_mode, 3, 0)

        self.toggle_button = QPushButton("Termoobieg", self)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setFont(QFont(self.anta, 12))
        self.toggle_button.clicked.connect(self.change_toggle)
        pagelayout.addWidget(self.toggle_button, 3, 1, alignment=Qt.AlignCenter)

        lbl_empty = QLabel("")
        pagelayout.addWidget(lbl_empty, 4, 0, 1, 1)

        lbl_temp = make_label("Maksymalna temperatura", self.anta, 15, False, False)
        pagelayout.addWidget(lbl_temp, 5, 0)

        self.sld_temp = QSlider(Qt.Orientation.Horizontal, self)
        self.sld_temp.setRange(36, 56)
        self.sld_temp.setSingleStep(1)
        self.sld_temp.setSliderPosition(44)
        self.sld_temp.setStyleSheet(temp_bar)
        self.sld_temp.valueChanged.connect(self.updatelabeltemp)
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

        btn_estimate = make_button("Sprawdź", self.bakerie, font_size=20)
        btn_estimate.clicked.connect(lambda: self.estimate("r"))
        pagelayout.addWidget(btn_estimate, 7, 1, alignment=Qt.AlignCenter)

        empty_label1 = QLabel("")
        pagelayout.addWidget(empty_label1, 8, 2, 1, 3)

        btn_recipes = make_button("Przepisy", self.bakerie)
        btn_recipes.clicked.connect(self.close)
        btn_recipes.clicked.connect(self.recipes_popup)
        pagelayout.addWidget(btn_recipes, 9, 0, alignment=Qt.AlignCenter)

        btn_choice = make_button("Wybór pizzy", self.bakerie)
        btn_choice.clicked.connect(self.choice_popup)
        btn_choice.clicked.connect(self.close)
        pagelayout.addWidget(btn_choice, 9, 1, alignment=Qt.AlignCenter)

        btn_menu = make_button("Menu Główne", self.bakerie)
        btn_menu.clicked.connect(self.close)
        btn_menu.clicked.connect(self.open_main)
        pagelayout.addWidget(btn_menu, 9, 2, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(pagelayout)


class American(HelpWindow):
    """Create window for american pizza with main functionality."""

    def __init__(self):
        super().__init__()

        pagelayout = QGridLayout()

        lbl_a = make_label("Pizza Amerykańska", self.bakerie, 30)
        pagelayout.addWidget(lbl_a, 1, 0, 1, 4, alignment=Qt.AlignCenter)

        self.empty_label0 = QLabel("")
        pagelayout.addWidget(self.empty_label0, 2, 0)

        lbl_mode = make_label("Tryb pieczenia", self.anta, 15, False, False)
        pagelayout.addWidget(lbl_mode, 3, 0)

        self.toggle_button = QPushButton("Termoobieg", self)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setFont(QFont(self.anta, 12))
        self.toggle_button.clicked.connect(self.change_toggle)
        pagelayout.addWidget(self.toggle_button, 3, 1, alignment=Qt.AlignCenter)

        lbl_empty = QLabel("")
        pagelayout.addWidget(lbl_empty, 4, 0, 1, 1)

        lbl_temp = make_label("Maksymalna temperatura", self.anta, 15, False, False)
        pagelayout.addWidget(lbl_temp, 5, 0)

        self.sld_temp = QSlider(Qt.Orientation.Horizontal, self)
        self.sld_temp.setRange(36, 56)
        self.sld_temp.setSingleStep(1)
        self.sld_temp.setSliderPosition(44)
        self.sld_temp.setStyleSheet(temp_bar)
        self.sld_temp.valueChanged.connect(self.updatelabeltemp)
        pagelayout.addWidget(self.sld_temp, 5, 1)

        self.lbl_slider_temp = QLabel('220°C', self)
        self.lbl_slider_temp.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                          Qt.AlignmentFlag.AlignVCenter)
        self.lbl_slider_temp.setMinimumWidth(80)
        self.lbl_slider_temp.setFont(QFont(self.anta, 10))
        pagelayout.addWidget(self.lbl_slider_temp, 5, 2)

        self.empty_label1 = QLabel("")
        pagelayout.addWidget(self.empty_label1, 6, 2, 1, 3)

        btn_estimate = make_button("Sprawdź", self.bakerie, font_size=20)
        btn_estimate.clicked.connect(lambda: self.estimate("a"))
        pagelayout.addWidget(btn_estimate, 7, 1, alignment=Qt.AlignCenter)

        self.empty_label2 = QLabel("")
        pagelayout.addWidget(self.empty_label2, 8, 2, 1, 3)

        btn_recipes = make_button("Przepisy", self.bakerie)
        btn_recipes.clicked.connect(self.close)
        btn_recipes.clicked.connect(self.recipes_popup)
        pagelayout.addWidget(btn_recipes, 9, 0, alignment=Qt.AlignCenter)

        btn_choice = make_button("Wybór Pizzy", self.bakerie)
        btn_choice.clicked.connect(self.choice_popup)
        btn_choice.clicked.connect(self.close)
        pagelayout.addWidget(btn_choice, 9, 1, alignment=Qt.AlignCenter)

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
        label = make_label("Super Pizzowa Aplikacja", self.bakerie, 40)
        pagelayout.addWidget(label)

        btn_recipe = make_button("Przepisy", self.bakerie, 0, 0, 20)
        btn_recipe.clicked.connect(self.recipes_popup)
        btn_recipe.clicked.connect(self.close)
        pagelayout.addWidget(btn_recipe)

        btn_choice = make_button("Wybór pizzy", self.bakerie, 0, 0, 20)
        btn_choice.clicked.connect(self.choice_popup)
        btn_choice.clicked.connect(self.close)
        pagelayout.addWidget(btn_choice)

        btn_how = make_button("Jak to działa?", self.bakerie, 0, 0, 20)
        btn_how.clicked.connect(self.instructions_popup)
        btn_how.clicked.connect(self.close)
        pagelayout.addWidget(btn_how)

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
