import random

def main(target, search_type, start, end) -> list[int|None, int]:
    """
       Поиск числа в заданном диапазоне
       Создает список чисел от start
       Ключевые аргументы:
           target (int): Число, которое необходимо найти
           start (int): Начало диапазона поиска
           end (int): Конец диапазона поиска
           search_type (str): Тип поиска ('seq'-  последовательный, 'bin' - бинарный)
           """
    if isinstance(target, str):  # является ли target строкой
        raise TypeError("Target должно быть числом, а не строкой")
    if start>end:
        raise ValueError('Введите диапазон, в котором начальное значение <= конечного')
    lst=[i for i in range(start, end+1)]
    return guess_number(target, lst, search_type)

def input_of_numbers(target, search_type) -> list[int|None, int]:
    """
        Поиск числа в списке, введенном с клавиатуры
       Ключевые аргументы:
           target (int): Число, которое необходимо найти
           n (int): Количество чисел в массиве
           search_type (str): Тип поиска ('seq'-  последовательный, 'bin' - бинарный)
           """
    if isinstance(target, str):  # является ли target строкой
        raise TypeError("Target должно быть числом, а не строкой")
    lst=[]
    n=int(input('Введите количество чисел'))
    print('Введите числа')
    for i in range(n):
        lst.append(int(input()))
    return guess_number(target, lst, search_type)

def random_numbers(target, search_type, start, end, n) -> list[int|None, int]:
    """
        Поиск числа в случайно сгенерированном списке
       Ключевые аргументы:
           target (int): Число, которое необходимо найти
           start (int): Минимальное значение для генерации случайных чисел
           n (int): Количество чисел в массиве
           end (int): Максимальное значение для генерации случайных чисел
           search_type (str): Тип поиска ('seq'-  последовательный, 'bin' - бинарный)
           """
    if not isinstance(n, int) or n<=0:
        raise TypeError('Введите положительное целое n')
    if (not isinstance(start, int) and not isinstance(start, float)) or (not isinstance(end, int) and not isinstance(end, float)):
        raise TypeError('Start и end должны быть числами')
    lst = [random.randint(start, end) for i in range(n)]
    return guess_number(target, lst, search_type)

def guess_number(target, lst, type_search) -> list[int|None, int]:
    """
       Поиск числа в списке указанным методом
       Ключевые аргументы:
           target (int): Число, которое необходимо найти
           lst (list): Список чисел для поиска
           search_type (str): Тип поиска ('seq'-  последовательный, 'bin' - бинарный)
           """
    c=0
    if type_search == 'seq':
        for i in range(len(lst)):
            c+=1
            if target==lst[i]:
                return [target, c]

    elif type_search == 'bin':
        lst.sort()
        left=0
        right=len(lst)-1
        while left<=right:
            c+=1
            mid = (left+right)//2
            if lst[mid] == target:
                return [target, c]
            elif target < lst[mid]:
                right = mid-1
            else:
                left = mid +1
    else:
        raise TypeError('Введите корректный тип поиска')
    return [None, c]
