from PyQt5 import QtCore
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QLabel
from sympy import symbols, solve
import math

back_color = "#5D7064"
select_color = "#798b80"
window_width = 600
window_height = 700

neapolitan_recipe_pl = """ <br>
Składniki <br>
● 500g mąki pszennej typu 00 <br>
● 325g letniej wody <br>
● 10g świeżych drożdży <br>
● 5g soli <br> <br>
Rozpuść drożdże w\u00A0wodzie i\u00A0pozostaw je na 10 minut. W\u00A0dużej misce wymieszaj mąkę z\u00A0solą a\u00A0następnie wlej przygotowaną wcześniej wodę 
z\u00A0drożdżami. Połącz składniki drewnianą łyżką i\u00A0rozpocznij wyrabianie ciasta. Jeśli masz taką możliwość możesz użyć robota planetarnego. 
Wyrabiaj ciasto tak długo aż będzie ono elastyczne i\u00A0gładkie. Tak przygotowane ciasto pozostaw pod przykryciem do wyrośnięcia na 
co najmniej pół godziny. Po tym czasie podziel je na 3 części i\u00A0uformuj z\u00A0nich kulki. Pozostaw je do wyrośnięcia pod czystą, zwilżoną ścierką 
materiałową na następne pół godziny. Z\u00A0gotowych kulek ciasta uformuj pizzę o\u00A0bardzo cienkim spodzie. Brzegi pizzy mogą pozostać większe. 
Dodaj ulubione dodatki i\u00A0włóż pizzę do piekarnika."""

american_recipe_pl = """ <br>
Składniki: <br>
● 450 g mąki pszennej typu 00 <br>
● 325 ml ciepłej wody <br>
● 2 łyżki oleju roślinnego <br>
● 2 łyżeczki soli <br>
● 2 łyżeczki cukru <br>
● 7 g suchych drożdży instant <br> <br>
W dużej misce wymieszaj mąkę, sól, cukier i\u00A0drożdże. Do miski dodaj ciepłą wodę i\u00A0olej
roślinny. Mieszaj wszystkie składniki, aż powstanie elastyczne ciasto. Wyłóż je na lekko oprószoną
mąką powierzchnię i\u00A0zagniataj przez około 5-7 minut, aż będzie miękkie i\u00A0elastyczne. Tak
przygotowane ciasto umieść w\u00A0dużej misce posmarowanej oliwą z\u00A0oliwek, przykryj je ściereczką i\u00A0
pozostaw w\u00A0ciepłym miejscu na około 1-2 godziny, aż podwoi swoją objętość. Przygotuj dużą okrągłą
blachę do pizzy i\u00A0posmaruj ją olejem roślinnym.
"""

roman_recipe_pl = """<br>
Składniki: <br>
● 500g mąki pszennej typu 00 <br>
● 325g letniej wody <br>
● 10g świeżych drożdży <br>
● 10g cukru <br>
● 5g soli <br>
● 2 łyżki oliwy z oliwek <br> <br>
W\u00A0dużej misce wymieszaj mąkę, sól i\u00A0cukier. W\u00A0drugiej misce rozpuść drożdże w\u00A0letniej
wodzie i\u00A0pozostaw na kilka minut, aż zaczną się pienić. Dodaj rozpuszczone drożdże do miski z\u00A0mąką i\u00A0
stopniowo mieszaj, aż składniki się połączą. Następnie dodaj oliwę z\u00A0oliwek i\u00A0kontynuuj mieszanie, aż
powstanie elastyczne ciasto. Wyłóż ciasto na oprószoną mąką powierzchnię i\u00A0zagniataj je przez około
10 minut, aż będzie gładkie i\u00A0elastyczne. Umieść ciasto w\u00A0dużej misce posmarowanej oliwą z\u00A0oliwek,
przykryj je ściereczką i\u00A0pozostaw w\u00A0ciepłym miejscu na około 1-2 godziny, aż podwoi swoją objętość.
Następnie na dużą, posmarowaną oliwą blachę wyłóż ciasto i\u00A0rozciągnij je na równomierną grubość,
tworząc klasyczną pizzę rzymską.
"""

neapolitan_recipe_eng = """ <br>
Ingredients <br>
● 500g of "00" type wheat flour <br>
● 325g of lukewarm water  <br>
● 10g of fresh yeast  <br>
● 5g of salt <br> <br>
Dissolve yeast in the water and let it sit for 10 minutes. In a large bowl, mix flour with salt, and then pour the 
previously prepared yeast mixture. Combine the ingredients with a wooden spoon and start kneading the dough. If you have
 the opportunity, you can use a planetary robot. Knead the dough until it’s elastic and smooth. Leave the dough to rise 
 for at least half an hour. After this time, divide it into 3 parts and form into balls. Leave them to rise under a 
 clean, damp cloth for another half hour. From the dough balls, form a pizza with a very thin bottom. The edges of the 
 pizza can be left larger. Add your favourite toppings and put the pizza in the oven."""

american_recipe_eng = """ <br>
Ingredients: <br>
● 450g of "00" type wheat flour <br>
● 325ml of warm water  <br>
● 2 tablespoons of vegetable oil  <br>
● 2 teaspoons of salt  <br>
● 2 teaspoons of sugar  <br>
● 7g instant dry yeast <br> <br>
In a large bowl, combine the flour, salt, sugar and yeast. Add warm water and vegetable oil to the bowl. Mix all 
ingredients until an elastic dough forms. Put them on a lightly floured surface and knead for about 5-7 minutes until 
soft and elastic. Put the dough in a large bowl greased with olive oil, cover it with a cloth and leave it in a warm 
place for about 1-2 hours, until it doubles in size. Prepare a large round pizza sheet and grease it with vegetable oil.
 Put the dough on the baking sheet and spread it with your hands or a rolling pin so that the dough is approx 1 cm thick. 
"""

roman_recipe_eng = """<br>
Ingredients: <br>
● 500g of "00" type wheat flour <br>
● 325g of lukewarm water  <br>
● 10g of fresh yeast  <br>
● 10g of sugar <br>
● 5g of salt <br>
● 2 tablespoons of olive oil <br> <br>
In a large bowl, mix flour, salt and sugar. In another bowl, dissolve yeast in lukewarm water and let it sit for a few 
minutes until it starts to foam. Add the dissolved yeast to the bowl of flour and gradually mix until the ingredients 
are combined. Then add the olive oil and continue mixing until an elastic dough forms. Put the dough on a floured 
surface and knead it for about 10 minutes until it is smooth and elastic. Place the dough in a large bowl greased with 
olive oil, cover with a cloth and leave in a warm place for about 1-2 hours until it doubles in size. Then, put the 
dough on a large, oiled baking sheet and spread it to an even thickness, creating a classic Roman pizza.
"""

instructions_pl = """   Aplikacja ma na celu podanie użytkownikowi najbardziej optymalnego czasu pieczenia pizzy w\u00A0zależności od wprowadzonych parametrów.  \n
    Do wyboru dostępne są pizza amerykańska, rzymska oraz neapolitańska. W\u00A0sekcji 'Przepisy' na każdą z\u00A0tych pizz podany jest sposób jej przyrządzania. \n
    Do głównej funkcjonalności można przejść poprzez przycisk 'Wybór pizzy' z\u00A0menu głównego, a\u00A0także wybierając pożądany przepis. \n
    Po wybraniu rodzaju pizzy należy ustawić również tryb i\u00A0temperaturę piekarnika, w\u00A0którym pizza będzie pieczona, a\u00A0w\u00A0przypadku pizzy neapolitańskiej również średnicę surowego ciasta. Następnie po kliknięciu przycisku 'Sprawdź' wyświetli się okno z\u00A0rekomendowanym czasem pieczenia.
"""

instructions_en = """   The app's main goal is to return the most optimal baking time depending on various pizza parameters entered by the user. \n
    Types of pizza that are available to choose from are Neapolitan, Roman and American. In section 'Recipes' there is a\u00A0tutorial on how to prepare each one of them. \n
    Main functionality can be entered after pressing 'Choice of pizza' button from the main menu, but also after clicking on desired recipe. \n
After selecting the desired type of pizza, the mode of the used oven and its temperature must also be set. In case of neapolitan pizza, there also has to be set the desired 
diameter of the pizza. Then, after clicking the 'Check' button, a window with recommended baking time will appear.
"""

neapol_format_pl = """<div style ="font-size:45px; text-align:center;"><span style ="font-family:{};">Pizza Neapolitańska
                </span><br></div><div style="font-size:18px; text-align:left;"><span style="font-family: {};"{}</span
                </div>"""
american_format_pl = """<div style ="font-size:45px; text-align:center;"><span style ="font-family:{};">Pizza Amerykańska
                </span><br></div><div style="font-size:18px; text-align:left;"><span style="font-family: {};"{}</span
                </div>"""
roman_format_pl = """<div style ="font-size:45px; text-align:center;"><span style ="font-family:{};">Pizza Rzymska </span> 
                </div><div style="font-size:18px; text-align:left;"><span style="font-family: {};"{}</span</div>"""

neapol_format_eng = """<div style ="font-size:45px; text-align:center;"><span style ="font-family:{};">Neapolitan Pizza
                </span><br></div><div style="font-size:18px; text-align:left;"><span style="font-family: {};"{}</span
                </div>"""
american_format_eng = """<div style ="font-size:45px; text-align:center;"><span style ="font-family:{};">American Pizza
                </span><br></div><div style="font-size:18px; text-align:left;"><span style="font-family: {};"{}</span
                </div>"""
roman_format_eng = """<div style ="font-size:45px; text-align:center;"><span style ="font-family:{};">Roman Pizza </span> 
                </div><div style="font-size:18px; text-align:left;"><span style="font-family: {};"{}</span</div>"""
def get_font():
    bakerie_font = "Bakerie Rough Bold.otf"
    anta_font = "anta-regular.ttf"
    font1 = QFontDatabase.addApplicationFont(anta_font)
    font2 = QFontDatabase.addApplicationFont(bakerie_font)
    anta = QFontDatabase.applicationFontFamilies(font1)
    bakerie = QFontDatabase.applicationFontFamilies(font2)

    return anta, bakerie


def make_button(name, font, min_width=160, max_height=60, font_size=15, expand=True):
    btn = QPushButton(name)
    if min_width != 0:
        btn.setMinimumWidth(min_width)
    if max_height != 0:
        btn.setMaximumHeight(max_height)
    if expand:
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    btn.setFont(QFont(font, font_size))

    return btn


def make_label(name, font, font_size, center=True, policy=True):
    lbl = QLabel(name)
    lbl.setWordWrap(True)
    lbl.setFont(QFont(font, font_size))
    if policy:
        lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    if center:
        lbl.setAlignment(QtCore.Qt.AlignCenter)

    return lbl


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

pol_lang = {
            "up_down_mode": "Góra-dół",
            "convection": "Termoobieg",
            "returned_time": "Optymalny czas pieczenia pizzy to:",
            "go_back": "Wróć",
            "previous": "Poprzedni",
            "next": "Następny",
            "choose": "Wybierz",
            "main_menu": "Menu Główne",
            "choose_pizza_type": "Wybierz rodzaj pizzy",
            "neapolitan": "Neapolitańska",
            "american": "Amerykańska",
            "roman": "Rzymska",
            "instructions": "Insrukcje",
            "baking_mode": "Tryb pieczenia",
            "diameter": "Średnica",
            "temp": "Temperatura",
            "check": "Sprawdź",
            "recipes": "Przepisy",
            "pizza_choice": "Wybór pizzy",
            "roman_pizza": "Pizza Rzymska",
            "neapolitan_pizza": "Pizza Neapolitańska",
            "title":  "Super Pizzowa Aplikacja",
            "american_pizza":  "Pizza Amerykańska",
            "how_it_works": "Jak to działa?",
            "oven_mode": ["Termoobieg", "Góra-dół", "Combo"],
            "neapolitan_recipe": neapolitan_recipe_pl,
            "american_recipe": american_recipe_pl,
            "roman_recipe": roman_recipe_pl,
            "neapol_format": neapol_format_pl,
            "american_format": american_format_pl,
            "roman_format": roman_format_pl,
            "choose_language": "Język",
            "instructions_content": instructions_pl,
            "enjoy_your_meal": "Smacznego!"
}

eng_lang = {
            "up_down_mode": "Up-down",
            "convection": "Convection",
            "returned_time": "Optimal baking pizza time is:",
            "go_back": "Back",
            "previous": "Previous",
            "next": "Next",
            "choose":  "Choose",
            "main_menu": "Main Menu",
            "choose_pizza_type":  "Choose pizza type",
            "neapolitan": "Neapolitan",
            "american": "American",
            "roman": "Roman",
            "instructions": "Instructions",
            "baking_mode":  "Baking mode",
            "diameter":  "Diameter",
            "temp": "Temeprature",
            "check": "Check",
            "recipes": "Recipes",
            "pizza_choice": "Choose pizza type",
            "roman_pizza": "Roman Pizza",
            "neapolitan_pizza": "Neapolitan Pizza",
            "title":  "Super Pizza App",
            "american_pizza": "American Pizza",
            "how_it_works": "How it works?",
            "oven_mode": ["Convection", "Up-down", "Combo"],
            "neapolitan_recipe": neapolitan_recipe_eng,
            "american_recipe": american_recipe_eng,
            "roman_recipe": roman_recipe_eng,
            "neapol_format": neapol_format_eng,
            "american_format": american_format_eng,
            "roman_format": roman_format_eng,
            "choose_language": "Language",
            "instructions_content": instructions_en,
            "enjoy_your_meal": "Enjoy your meal!"
        }

# ------------------------------------------- FUNKCJA -----------------------------------------------

def pizza(T_1, d, mode, pizza):
    """
    T_1 - Temperaturre
    d - diameter
    mode
    pizza type
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
        if mode == "Termoobieg" or mode == "Convection":
            tau = tau
        elif mode == "Combo":
            tau *= 0.9
        else:
            tau *= 1.4264

    else:
        if pizza == "a":
            tau = tauu / 1333
        else:
            tau = tauu / 1666

        if mode == "Termoobieg" or mode == "Convection":
            tau = tau
        else:
            tau *= 1.27

    frac, whole = math.modf(tau)
    seconds = round(frac * 60)
    result = f"{int(whole)}min {seconds}sec"
    return result
