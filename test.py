# def my_zip(*iter):
#     return list(map(lambda *args: args, *iter))

print(list(map(lambda *args: args, [1, 2])))
print(list(map(lambda *args: args, [1, 2], [3, 4])))
print(list(map(lambda *args: args, [1, 2], [3, 4], [5, 6])))