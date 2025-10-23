import timeit
import matplotlib.pyplot as plt
import random
from functools import lru_cache


def fact_recursive(n: int) -> int:
    """
        Вычисляет факториал числа с использованием рекурсии без кэширования.
        Args:
            n (int): Число, для которого вычисляется факториал. Должно быть неотрицательным.
        Returns:
            int: Значение факториала числа n)
        """
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


@lru_cache(maxsize=None)
def fact_recursive_cache(n: int) -> int:
    """
    Вычисляет факториал числа с использованием рекурсии с кэшированием.
    Использует @lru_cache для мемоизации результатов вычислений,
    Args:
        n (int): Число, для которого вычисляется факториал. Должно быть неотрицательным.
    Returns:
        int: Значение факториала числа n)
    """
    if n == 0:
        return 1
    return n * fact_recursive_cache(n - 1)

def fact_iterative(n: int) -> int:
    """
    Вычисляет факториал числа с использованием итеративного подхода
    Args:
        n (int): Число, для которого вычисляется факториал. Должно быть неотрицательным.
    Returns:
        int: Значение факториала числа n)
    """
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


def benchmark(func, data, number=100, repeat=5):
    """
     Проводит бенчмаркинг функции на наборе данных.
     Args:
         func (callable): Функция для тестирования
         data (list): Входные данные для функции
         number (int): Количество выполнений функции за одно измерение
         repeat (int): Количество повторений измерений

     Returns:
         float: Среднее минимальное время выполнения функции на одном элементе данных
     """
    total = 0
    for n in data:
        times = timeit.repeat(lambda: func(n), number=number, repeat=repeat)
        total += min(times)
    return total / len(data)


def main():
    """
        Основная функция программы
        Проводит сравнительный анализ производительности алгоритмов
        вычисления факториала и визуализирует результаты
        """
    random.seed(42)
    test_data = list(range(1, 100, 3))

    res_recursive = []
    res_iterative = []
    res_recursive_cache = []


    for n in test_data:
        res_recursive.append(benchmark(fact_recursive, [n], number=100, repeat=3))
        res_iterative.append(benchmark(fact_iterative, [n], number=100, repeat=3))
        res_recursive_cache.append(benchmark(fact_recursive_cache, [n], number=100, repeat=3))

    plt.figure(figsize=(12, 8))

    # Первый график: без кэширования
    plt.subplot(2, 1, 1)
    plt.plot(test_data, res_recursive, label="Рекурсивный",  markersize=2)
    plt.plot(test_data, res_iterative, label="Итеративный", markersize=2)
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного факториала (без кэширования)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Второй график: с кэшированием
    plt.subplot(2, 1, 2)
    plt.plot(test_data, res_recursive_cache, label="Рекурсивный с кэшированием", markersize=2)
    plt.plot(test_data, res_iterative, label="Итеративный", markersize=2)
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного (с кэшированием) и итеративного факториала")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()