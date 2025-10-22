def gen_bin_tree(height=6, root=2, l_leaf=lambda x: x*3, r_leaf=lambda y: y+4):
    """Генерация бинарного дерева
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

    return {str(root): [gen_bin_tree(height - 1, l_leaf(root), l_leaf, r_leaf), gen_bin_tree(height - 1, r_leaf(root), l_leaf, r_leaf)]}

def main():
    """Пример работы генератора бинарного дерева с данными из варианта"""
    tree = gen_bin_tree()
    print(tree)


if __name__ == "__main__":
    main()

