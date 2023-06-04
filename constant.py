from sympy import symbols, solve
import math

back_color = "#5D7064"
select_color = "#798b80"

bakerie_font = "Bakerie Rough Bold.otf"
anta_font = "anta-regular.ttf"

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
    border: 1px solid #111;
    background-color: #333;
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

# FUNKCJA

def neapolitanska(T_1, d, tryb):
    """
    T_1 - Temperatura
    d - średnica pizzy
    tryb
    """

    T_1 += 273
    t = symbols("t")
    sigma = 5.67 * 10 ** (-8)
    T_b = 100 + 273
    kappa = 0.5
    c = 2 * 10 ** 3
    rho = 0.7 * 10 ** 3
    chi = 3 * 10 ** (-7)
    alpha = 0.16
    T_2 = 20 + 273
    L = 2264.76
    T_0 = (T_1 + 0.1 * T_2) / 1.1
    q_w = 10 ** 3

    tau = solve(sigma * (T_1 ** 4 - T_b ** 4) * t + 2 * kappa * (T_1 - T_0) * (t / (chi)) ** (1 / 2) - c * rho * 0.5 * (
                T_b - T_2) - alpha * L * 0.5 * q_w)[0] / 1939 * ((20 + d) / 50)

    if tryb == "Termoobieg":
        tau = tau
    elif tryb == "Combo":
        tau *= 0.9
    else:
        tau *= 1.4264

    frac, whole = math.modf(tau)
    sekundy = round(frac * 60)
    result = f"{int(whole)}min {sekundy}sek"
    return result


def rzymska(T_1, d, tryb):
    """
    T_1 - Temperatura
    d - średnica pizzy
    tryb
    """

    T_1 += 273
    t = symbols("t")
    sigma = 5.67 * 10 ** (-8)
    T_b = 100 + 273
    kappa = 0.5
    c = 2 * 10 ** 3
    rho = 0.7 * 10 ** 3
    chi = 3 * 10 ** (-7)
    alpha = 0.16
    T_2 = 20 + 273
    L = 2264.76
    T_0 = (T_1 + 0.1 * T_2) / 1.1
    q_w = 10 ** 3

    tau = solve(sigma * (T_1 ** 4 - T_b ** 4) * t + 2 * kappa * (T_1 - T_0) * (t / (chi)) ** (1 / 2) - c * rho * 0.5 * (
                T_b - T_2) - alpha * L * 0.5 * q_w)[0] / 1666 * ((20 + d) / 50)

    if tryb == "Termoobieg":
        tau = tau
    else:
        tau *= 1.27

    frac, whole = math.modf(tau)
    sekundy = round(frac * 60)
    result = f"{int(whole)}min {sekundy}sek"
    return result


def amerykanska(T_1, d, tryb):
    """
    T_1 - Temperatura
    d - średnica pizzy
    tryb
    """

    T_1 += 273
    t = symbols("t")
    sigma = 5.67 * 10 ** (-8)
    T_b = 100 + 273
    kappa = 0.5
    c = 2 * 10 ** 3
    rho = 0.7 * 10 ** 3
    chi = 3 * 10 ** (-7)
    alpha = 0.16
    T_2 = 20 + 273
    L = 2264.76
    T_0 = (T_1 + 0.1 * T_2) / 1.1
    q_w = 10 ** 3

    tau = solve(sigma * (T_1 ** 4 - T_b ** 4) * t + 2 * kappa * (T_1 - T_0) * (t / (chi)) ** (1 / 2) - c * rho * 0.5 * (
                T_b - T_2) - alpha * L * 0.5 * q_w)[0] / 1333 * ((20 + d) / 50)

    if tryb == "Termoobieg":
        tau = tau
    else:
        tau *= 1.27

    frac, whole = math.modf(tau)
    sekundy = round(frac * 60)
    result = f"{int(whole)}min {sekundy}sek"
    return result
