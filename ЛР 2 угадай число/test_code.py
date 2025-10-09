"""Находит число в списке указанным методом и возвращает результат с количеством попыток.

        Аргументы:
            target: Искомое число
            lst: Список для поиска
            type: Тип поиска - 'seq' (последовательный), 'bin' (бинарный),
            'bin_with_making_list' (бинарный с составлением списка из двух чисел)

        Возвращает:
            list: [найденное число или None, количество попыток]
    """
    lst.sort()
    attempts = 0
    if type == "bin_with_making_list":
        if len(lst) == 2:
            lst = list(range(lst[0], lst[1] + 1))
            left, right = 0, len(lst) - 1
            while left <= right:
                attempts += 1
                mid = (left + right) // 2
                if lst[mid] == target:
                    return [target, attempts]  # [индекс, попытки]
                elif lst[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return [None, attempts]  # число не найдено

    elif type == "bin":  # Бинарный поиск
        lst.sort()
        left, right = 0, len(lst) - 1
        while left <= right:
            attempts += 1
            mid = (left + right) // 2
            if lst[mid] == target:
                return [target, attempts]  # [индекс, попытки]
            elif lst[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return [None, attempts]  # число не найдено

    elif type == "seq":  # Последовательный поиск
        for i in range(len(lst)):
            attempts += 1
            if lst[i] == target:
                return [target, attempts]  # [индекс, попытки]

        return [None, attempts]  # число не найдено


def main():
    target = int(input("Введите таргет"))
    type = input("Введите тип поиска - 'seq' (последовательный), 'bin' (бинарный) или 'bin_with_making_list' \
    (бинарный поиск с созданием массива из двух чисел ")
    list_your_numb = (input("Введите массив данных через пробел"))
    list_your_numb = [int(i) for i in list_your_numb.split()]
    res = guess_number(target, list_your_numb, type)
    print(res)


if __name__ == "__main__":
    main()