import random

def main(target, type_search, start, end) -> list[int, int|None]:
    lst=[i for i in range(start, end+1)]
    return guess_number(target, lst, type_search)

def input_of_numbers(target, type_search) -> list[int, int|None]:
    lst=[]
    n=int(input('Введите количество чисел'))
    print('Введите числа')
    for i in range(n):
        lst.append(int(input()))
    lst.sort()
    return guess_number(target, lst, type_search)

def random_numbers(target, type_search, start, end, n) -> list[int, int|None]:
    lst = [random.randint(start, end) for i in range(n)]
    lst.sort()
    return guess_number(target, lst, type_search)

def guess_number(target, lst, type_search):
    c=0
    if type_search == 'seq':
        for i in range(len(lst)):
            c+=1
            if target==lst[i]:
                return [target, c]

    elif type_search == 'bin':
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
    return [None, c]



# вторая функция - введение чисел с клавиатуры и сортировка
# тип способа угадывания
# пустой список, не найден элемент, не подходит диапазон
# комментарии