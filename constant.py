from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QPushButton, QSizePolicy
from sympy import symbols, solve
import math

back_color = "#5D7064"
select_color = "#798b80"
window_width = 600
widow_height = 700

przepis_neapol = """ <br>
Składniki <br>
● 500g mąki pszennej typu 00 <br>
● 325g letniej wody <br>
● 10g świeżych drożdży <br>
● 5g soli <br> <br>
Rozpuść drożdże w wodzie i pozostaw je na 10 minut. W dużej misce wymieszaj mąkę z solą a następnie wlej przygotowaną wcześniej wodę 
z drożdżami. Połącz składniki drewnianą łyżką i rozpocznij wyrabianie ciasta. Jeśli masz taką możliwość możesz użyć robota planetarnego. 
Wyrabiaj ciasto tak długo aż będzie ono elastyczne i gładkie. Tak  przygotowane ciasto pozostaw pod przykryciem do wyrośnięcia na 
co najmniej pół godziny. Po tym czasie podziel je na 3 części i uformuj z nich kulki. Pozostaw je do wyrośnięcia pod czystą, zwilżoną ścierką 
materiałową na następne pół godziny. Z gotowych kulek ciasta uformuj pizzę o bardzo cienkim spodzie. Brzegi pizzy mogą pozostać większe. 
Dodaj ulubione dodatki i włóż pizzę do piekarnika."""

przepis_ameryka = """ <br>
Składniki: <br>
● 450 g mąki pszennej typu 00 <br>
● 325 ml ciepłej wody <br>
● 2 łyżki oleju roślinnego <br>
● 2 łyżeczki soli <br>
● 2 łyżeczki cukru <br>
● 7 g suchych drożdży instant <br> <br>
W dużej misce wymieszaj mąkę, sól, cukier i drożdże. Do miski dodaj ciepłą wodę i olej
roślinny. Mieszaj wszystkie składniki, aż powstanie elastyczne ciasto. Wyłóż je na lekko oprószoną
mąką powierzchnię i zagniataj przez około 5-7 minut, aż będzie miękkie i elastyczne. Tak
przygotowane ciasto umieść w dużej misce posmarowanej oliwą z oliwek, przykryj je ściereczką i
pozostaw w ciepłym miejscu na około 1-2 godziny, aż podwoi swoją objętość. Przygotuj dużą okrągłą
blachę do pizzy i posmaruj ją olejem roślinnym.
"""

przepis_rzym = """<br>
Składniki: <br>
● 500g mąki pszennej typu 00 <br>
● 325g letniej wody <br>
● 10g świeżych drożdży <br>
● 10g cukru <br>
● 5g soli <br>
● 2 łyżki oliwy z oliwek <br> <br>
W dużej misce wymieszaj mąkę, sól i cukier. W drugiej misce rozpuść drożdże w letniej
wodzie i pozostaw na kilka minut, aż zaczną się pienić. Dodaj rozpuszczone drożdże do miski z mąką i
stopniowo mieszaj, aż składniki się połączą. Następnie dodaj oliwę z oliwek i kontynuuj mieszanie, aż
powstanie elastyczne ciasto. Wyłóż ciasto na oprószoną mąką powierzchnię i zagniataj je przez około
10 minut, aż będzie gładkie i elastyczne. Umieść ciasto w dużej misce posmarowanej oliwą z oliwek,
przykryj je ściereczką i pozostaw w ciepłym miejscu na około 1-2 godziny, aż podwoi swoją objętość.
Następnie na dużą, posmarowaną oliwą blachę wyłóż ciasto i rozciągnij je na równomierną grubość,
tworząc klasyczną pizzę rzymską.
"""

instructions = """nkjfaaaaa aaaaaaaaaaaaaaaaa  aaaaaaaaaaaa aaaaaaaa aaaaaaaaaa aaaaaaaaaaaaa aaaaaaaaaaaaaaa aaaaaaaaaaaa
aaaaaaaaaaa  aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaa aaaaaaaaaaaaa aaaaaaaaaaaaaaaaa aaaaaaaaaaaa aaaaaaa aaaaaaaaaaaaa aaaaaaaaaaaaaaaa
aaaaaaaa aaaaaaaaaaa aaaaaaaaa aaaaaaaaaaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaa aaaaaaaaaaaaaaa aaaaaaaaaaaaaa aaaaaaajfbdsf
adaf s gnj jd jd gdjd gjs gdsg jbfjbsjfbsf fjkfghgb kjgnjdkb kjdnfjkn jkdngkjn ksdnjs nkjn jsgn sjgs jgsndjgkns jgsngkjsd 
ngds n njn jdngnnjngjnfjgnj njnng fsdgjkb jhdfdbghb bjdbgjbhjbgjb kbdgjbvdk bkjbjfkjbd gkjsbdghsjb sbg sijg 
b hjdbgv jbikfsnkjsfn s nsjfnsjkgnjvn sjkj bsjbdsf s  fjksdf  skjf s fsfskf sfsf sdfsf dskf sf"""

neapol_format = """<div style ="font-size:45px; text-align:center;"><span style ="font-family:{};">Pizza Neapolitańska
                </span><br></div><div style="font-size:18px; text-align:left;"><span style="font-family: {};"{}</span
                </div>"""
ameryka_format = """<div style ="font-size:45px; text-align:center;"><span style ="font-family:{};">Pizza Amerykańska
                </span><br></div><div style="font-size:18px; text-align:left;"><span style="font-family: {};"{}</span
                </div>"""
rzym_format = """<div style ="font-size:45px; text-align:center;"><span style ="font-family:{};">Pizza Rzymska </span> 
                </div><div style="font-size:18px; text-align:left;"><span style="font-family: {};"{}</span</div>"""




def get_font():
    bakerie_font = "Bakerie Rough Bold.otf"
    anta_font = "anta-regular.ttf"
    font1 = QFontDatabase.addApplicationFont(anta_font)
    font2 = QFontDatabase.addApplicationFont(bakerie_font)
    anta = QFontDatabase.applicationFontFamilies(font1)
    bakerie = QFontDatabase.applicationFontFamilies(font2)

    return anta, bakerie


def make_button(nazwa, bakerie, min_width=160, max_height=60, font_size=15):
    btn = QPushButton(nazwa)
    if min_width != 0:
        btn.setMinimumWidth(min_width)
    if max_height != 0:
        btn.setMaximumHeight(max_height)
    btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    btn.setFont(QFont(bakerie[0], font_size))

    return btn


tryby = ["Termoobieg", "Góra-dół", "Combo"]

eh = """
/* QSlider --------------------------------------  */
QSlider::groove:horizontal {
    border-radius: 1px;
    height: 3px;
    margin: 0px;
    background-color: rgb(52, 59, 72);
}
QSlider::groove:horizontal:hover {
    background-color: rgb(55, 62, 76);
}
QSlider::handle:horizontal {
    background-color: rgb(85, 170, 255);
    border: none;
    height: 40px;
    width: 40px;
    margin: -20px 0;
    border-radius: 20px;
    padding: -20px 0px;
}
QSlider::handle:horizontal:hover {
    background-color: rgb(155, 180, 255);
}
QSlider::handle:horizontal:pressed {
    background-color: rgb(65, 255, 195);
}
"""
temp_bar = """
QSlider::handle:horizontal {image: url('oven.png');margin: -24px -12px;
    height: -30px;}
}
QSlider::groove:vertical {
    width: 6px;
    margin: 24px 12px;
}
QSlider::sub-page:horizontal {
background: qlineargradient(x1: 0, y1: 0,    x2: 1, y2: 1,
    stop: 0 #FD0, stop: 1 #C00);
border: 1px solid #777;
height: 10px;
border-radius: 4px;
}"""

size_bar = """
QSlider::handle:horizontal {image: url('pzza.png');margin: -24px -12px;
background: transparent;
    height: -30px;}
}
QSlider::groove:vertical {
    width: 6px;
    margin: 24px 12px;
}
QSlider::sub-page:horizontal {
background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
    stop: 0 #FD0, stop: 1 #FD0);
background: qlineargradient(x1: 0, y1: 1, x2: 1, y2: 1,
    stop: 0 #FD0, stop: 1 #C00);
border: 1px solid #777;
height: 10px;
border-radius: 4px;
}"""

msg_style = """
        QMessageBox {
        background-color: #333333;
        color: white;
        border: none;
    }
    QMessageBox QPushButton {
        background-color: #555555;
        color: white;
    }
        """


# ------------------------------------------- FUNKCJA -----------------------------------------------

def pizza(T_1, d, tryb, pizza):
    """
    T_1 - Temperatura
    d - średnica pizzy
    tryb
    pizza- rodzaj
    """

    T_1 += 273
    t = symbols("t")
    sigma = 5.67 * 10 ** (-8)
    T_b, kappa, c, rho, chi, alpha, T_2, L = 373, 0.5, 2 * 10 ** 3, 0.7 * 10 ** 3, 3 * 10 ** (-7), 0.16, 293, 2264.76
    T_0 = (T_1 + 0.1 * T_2) / 1.1
    q_w = 10 ** 3

    tauu = \
        solve(sigma * (T_1 ** 4 - T_b ** 4) * t + 2 * kappa * (T_1 - T_0) * (t / chi) ** (1 / 2) - c * rho * 0.5 * (
                T_b - T_2) - alpha * L * 0.5 * q_w)[0] * ((20 + d) / 50)

    if pizza == "n":
        tau = tauu / 1939
        if tryb == "Termoobieg":
            tau = tau
        elif tryb == "Combo":
            tau *= 0.9
        else:
            tau *= 1.4264

    else:
        if pizza == "a":
            tau = tauu / 1333
        else:
            tau = tauu / 1666

        if tryb == "Termoobieg":
            tau = tau
        else:
            tau *= 1.27

    frac, whole = math.modf(tau)
    sekundy = round(frac * 60)
    result = f"{int(whole)}min {sekundy}sek"
    return result
