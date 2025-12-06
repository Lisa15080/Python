import sys
import logging
from decorators import logger

demo_logger = logging.getLogger("quadratic_demo")
demo_logger.setLevel(logging.DEBUG)
demo_logger.addHandler(logging.StreamHandler(sys.stdout))

@logger(handle=demo_logger)
def solve_quadratic(a, b, c):
    """
    Функция `solve_quadratic` решает квадратные уравнения вида ax^2 + bx + c = 0.

    Аргументы:
        a (int|float): коэффициент при x^2
        b (int|float): коэффициент при x
        c (int|float): свободный член
    """

    if not all(isinstance(x, (int, float)) for x in (a, b, c)):
        raise ValueError("Коэффициенты должны быть числами")

    if a == 0 and b == 0:
        raise ValueError("Уравнение не имеет смысла")

    if a == 0:
        return -c / b

    d = b ** 2 - 4 * a * c
    if d < 0:
        return f"Нет действительных корней (D={d})"

    if d == 0:
        return -b / (2 * a)

    x1 = (-b + d ** 0.5) / (2 * a)
    x2 = (-b - d ** 0.5) / (2 * a)
    return x1, x2
