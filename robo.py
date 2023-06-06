
language = ''
print(language)

def set_language(lang):
    global language
    if lang == "english":
        language = 'english'
    elif lang == 'polish':
        language = 'polish'

up_down_mode = ""
convection = ""
returned_time = ""
go_back = ""
previous = ""
next = ""
choose = ""
main_menu = ""
choose_pizza_type = ""
neapolitan = ""
american = ""
roman = ""
instruction = ""
baking_mode = ""
diameter = ""
temp = ""
check = ""
recipes = ""
pizza_choice = ""
roman_pizza = ""
american_pizza = ""
title = ""
how_it_works = ""

if language == 'polish':
    up_down_mode = "Góra_dół"
    convection = "Termoobieg"
    returned_time = "Optymalny czas pieczenia pizzy to:"
    go_back = "Wróć"
    previous = "Poprzednia"
    next = "Następna"
    choose = "Wybierz"
    main_menu = "Menu główne"
    choose_pizza_type = "Wybierz rodzaj pizzy"
    neapolitan = "Neapolitańska"
    american = "Amerykańska"
    roman = "Rzymska"
    instruction = "Instructions"
    baking_mode = "Tryb pieczenia"
    diameter = "Średnica"
    temp = "Temperatura"
    check = "Sprawdź"
    recipes = "Przepisy"
    pizza_choice = "Wybór pizzy"
    roman_pizza = "Pizza rzymska"
    american_pizza = "Pizza amerykańska"
    title = "Super Pizzowa Aplikacja"
    how_it_works = "Jak to działa?"
elif language == 'english':
    up_down_mode = "Up-down"
    convection = "Convection"
    returned_time = "Optimal baking pizza time is:"
    go_back = "Back"
    previous = "Previous"
    next = "Next"
    choose = "Choose"
    main_menu = "Main menu"
    choose_pizza_type = "Choose pizza type"
    neapolitan = "Neapolitan"
    american = "American"
    roman = 'Roman'
    instructions = "Instructions"
    baking_mode = "Baking mode"
    diameter = "Diameter"
    temp = "Temperature"
    check = "Check"
    recipes = "Recipes"
    pizza_choice = "Pizza choice"
    roman_pizza = "Roman pizza"
    american_pizza = "American pizza"
    title = "Super Pizza App"
    how_it_works = "How it works?"



print(language)
set_language('polish')
print(main_menu)
print(language)
set_language('english')
print(main_menu)
print(language)