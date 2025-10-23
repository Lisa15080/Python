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



def main():
    """Пример работы генератора бинарного дерева с данными из варианта"""
    tree = gen_bin_tree()
    print(tree)


if __name__ == "__main__":
    main()