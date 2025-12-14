import math

def integrate (f, a, b, *, n_iter = 1000):
    acc = 0
    step = (b-a) / n_iter
    for i in range(n_iter):
        acc+=f(a+i*step)*step
    return acc

print(integrate(math.cos, 0, math.pi/2 ))