back_color = "#5D7064"
select_color = "#798b80"

bakerie_font = "Bakerie Rough Bold.otf"
anta_font = "anta-regular.ttf"

tryby = ["Termoobieg", "Góra-dół", "Jakieś coś"]


def funkcja(temp, tryb="Termoobieg"):
    if tryb == "Termoobieg":
        x = 1
    elif tryb == "Góra-dół":
        x = 2
    else:
        x = 3
    wynik = x + temp
    return wynik
