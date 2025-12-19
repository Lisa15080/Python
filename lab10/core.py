# core.py
import math
from typing import Callable
import concurrent.futures as ftres


def integrate(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 100_000) -> float:
    """
    Вычисляет приближённое значение определённого интеграла функции на заданном интервале
    методом левых прямоугольников (rectangle rule): разбивает отрезок [a, b] на подотрезки,
    вычисляет значение функции в левой точке каждого подотрезка
    и суммирует площади получившихся прямоугольников.

    Аргументы:
        f (Callable[[float], float]): Интегрируемая функция одной вещественной переменной.
        a (float): Нижний предел интегрирования.
        b (float): Верхний предел интегрирования. Должен быть больше или равен `a`.
        n_iter (int): Количество подынтервалов для разбиения. Должно быть положительным целым числом.
                      По умолчанию: 100 000.

    Возвращает:
        float: Приближённое значение определённого интеграла ∫ₐᵇ f(x) dx.

    Возбуждает:
        TypeError: Если `f` не является вызываемым объектом (callable).
        ValueError: Если `a > b` или если `n_iter` не является положительным целым числом.

    Примеры:
        >>> # Пример 1: Интеграл sin(x) от 0 до π равен 2.0
        >>> result = integrate(math.sin, 0, math.pi, n_iter=100000)
        >>> abs(result - 2.0) < 0.01
        True

        >>> # Пример 2: Интеграл x² от 0 до 1 равен 1/3 ≈ 0.33333
        >>> result = integrate(lambda x: x ** 2, 0, 1, n_iter=100000)
        >>> abs(result - 1/3) < 0.001
        True
    """
    if not callable(f):
        raise TypeError("f должен быть вызываемой функцией")
    if a > b:
        raise ValueError("a не может быть больше b")
    if n_iter <= 0 or not isinstance(n_iter, int):
        raise ValueError("n_iter должно быть положительным целым числом")

    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


# Вспомогательная функция для ProcessPoolExecutor
def _integrate_worker(args):
    f, a, b, n_iter = args
    return integrate(f, a, b, n_iter=n_iter)


def integrate_async(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 1000, n_jobs: int = 2) -> float:
    """
    Вычисляет интеграл с использованием потоков (ThreadPoolExecutor).

    Аргументы:
        f: Интегрируемая функция.
        a: Нижний предел.
        b: Верхний предел.
        n_iter: Число итераций.
        n_jobs: Число потоков.

    Возвращает:
        Приближённое значение интеграла.
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs должно быть положительным")
    n_jobs = min(n_jobs, n_iter)

    step = (b - a) / n_jobs
    base = n_iter // n_jobs
    remainder = n_iter % n_jobs

    def worker(i):
        a_i = a + i * step
        b_i = a + (i + 1) * step
        n_i = base + (1 if i < remainder else 0)
        return integrate(f, a_i, b_i, n_iter=n_i)

    with ftres.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        return sum(executor.map(worker, range(n_jobs)))


def integrate_mp(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 1000, n_jobs: int = 2) -> float:
    """
    Вычисляет интеграл с использованием процессов (ProcessPoolExecutor).

    Аргументы:
        f: Интегрируемая функция.
        a: Нижний предел.
        b: Верхний предел.
        n_iter: Число итераций.
        n_jobs: Число процессов.

    Возвращает:
        Приближённое значение интеграла.
    """
    if n_jobs <= 0:
        raise ValueError("n_jobs должно быть положительным")
    n_jobs = min(n_jobs, n_iter)

    step = (b - a) / n_jobs
    base = n_iter // n_jobs
    remainder = n_iter % n_jobs

    tasks = []
    for i in range(n_jobs):
        a_i = a + i * step
        b_i = a + (i + 1) * step
        n_i = base + (1 if i < remainder else 0)
        tasks.append((f, a_i, b_i, n_i))

    with ftres.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        return sum(executor.map(_integrate_worker, tasks))