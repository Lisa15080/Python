def summa(nums, target):
    """
        Основная функция: находит индексы двух чисел в массиве, которые в сумме дают target

        """


    # проверка, пустой ли список
    if len(nums) == 0:
        raise TypeError("Данный список пустой")

    # проверка target
    if isinstance(target, str):  # является ли target строкой
        raise TypeError("Target должно быть числом, а не строкой")
    if int(target) != target: # является ли target нецелым числом
        raise TypeError("Target должно быть целым числом")

    # перебор элементов массива для проверки на соответствие условиям
    for x in nums:
        if isinstance(x, str):  # является ли элемент строкой
            raise TypeError("Все элементы должны быть числами, а не строками")
        if int(x) != x: # является ли элемент нецелым числом
            raise TypeError("Все элементы должны быть целыми числами")

    # поиск пары чисел
    for i in range(len(nums) - 1): #перебор индексов первого элемента
        for j in range(i + 1, len(nums)): #перебор индексрв второго элемента
            if nums[i] + nums[j] == target: #проверка, что два элемента дают в сумме target
                return [i, j]
   # если после перебора не нашлись элементы, дающие в сумме target, то возвращаем None

