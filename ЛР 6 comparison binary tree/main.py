import timeit
import matplotlib.pyplot as plt
import random


def build_tree_recursive(height=6, root=2, l_leaf=lambda x: x*3, r_leaf=lambda y: y+4):
    """Генерация бинарного дерева рекурсивно
    Ключевые аргументы:
        height (int): Высота дерева
        root (int): Корень дерева
        l_leaf (callable): Функция для вычисления левого потомка
        r_leaf (callable): Функция для вычисления правого потомка

     Возвращает:
        dict: Бинарное дерево в виде словаря
    """
    if not isinstance(height, int):
        raise TypeError('Высота должна быть целым числом')
    if not isinstance(root, int) and not isinstance(root, float):
        raise TypeError("Корень должен быть числом")
    if height < 0:
        raise TypeError("Высота должна быть неотрицательным числом")
    if height == 1:
        return {str(root): []}
    if height == 0:
        return {}

    return {str(root): [build_tree_recursive(height - 1, l_leaf(root), l_leaf, r_leaf), build_tree_recursive(height - 1, r_leaf(root), l_leaf, r_leaf)]}


def build_tree_iterative(height=6, root=2, l_leaf=lambda x: x*3, r_leaf=lambda y: y+4):
    """Генерация бинарного дерева итеративно через циклы
    Ключевые аргументы:
        height (int): Высота дерева
        root (int): Корень дерева
        l_leaf (callable): Функция для вычисления левого потомка
        r_leaf (callable): Функция для вычисления правого потомка

     Возвращает:
        dict: Бинарное дерево в виде словаря
    """
    if not isinstance(height, int):
        raise TypeError('Высота должна быть целым числом')
    if not isinstance(root, int) and not isinstance(root, float):
        raise TypeError("Корень должен быть числом")
    if height < 0:
        raise TypeError("Высота должна быть неотрицательным числом")
    if height == 1:
        return {str(root): []}
    if height == 0:
        return {}

    tree = {str(root): []}
    cur_level = [(tree[str(root)], root, 1)]
    for level in range(1, height):
        next_level = []
        for cur_list, cur_root, cur_level in cur_level:
            left_leaf = l_leaf(cur_root)
            right_leaf = r_leaf(cur_root)

            left_structure = {str(left_leaf): []}
            right_structure = {str(right_leaf): []}

            cur_list.append(left_structure)
            cur_list.append(right_structure)

            next_level.append((left_structure[str(left_leaf)], left_leaf, level + 1))
            next_level.append((right_structure[str(right_leaf)], right_leaf, level + 1))
        cur_level = next_level
    return tree


def benchmark(func, data, number=5, repeat=2):
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
        построения дерева и визуализирует результаты
        """
    random.seed(42)
    test_data = list(range(1, 18))

    res_recursive = []
    res_iterative = []



    for n in test_data:
        res_recursive.append(benchmark(build_tree_recursive, [n], number=5, repeat=2))
        res_iterative.append(benchmark(build_tree_iterative, [n], number=5, repeat=2))

    plt.figure(figsize=(12, 8))

    plt.plot(test_data, res_recursive, label="Рекурсивное построение дерева",  markersize=2)
    plt.plot(test_data, res_iterative, label="Итеративное построение дерева", markersize=2)
    plt.xlabel("Высота дерева")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение рекурсивного и итеративного построения дерева")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()

