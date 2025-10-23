def gen_bin_tree(height: int = 0, root: int = 3, l_p = lambda x: x, r_p=lambda y:y):
    if height <= 1:
        return {str(root): []}
    return {str(root): [gen_bin_tree(height - 1, l_p(root), l_p, r_p),
                        gen_bin_tree(height - 1, r_p(root), l_p, r_p)]}

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

    return {str(root): [gen_bin_tree(height - 1, l_p(root), l_p, r_p), gen_bin_tree(height - 1, r_p(root), l_p, r_p)]}


def main():
    print(gen_bin_tree(4, 1, lambda x: x + 1, lambda x: x + 2))