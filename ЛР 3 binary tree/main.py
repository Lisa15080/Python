tree = {1:}

def gen_bin_tree(height, root, l_b = left_branch, r_b = right_branch):
    left_branch, right_branch = l_b(root), r_b(root)