import cython
from libc.math cimport sin as c_sin, cos as c_cos, tan as c_tan

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def integrate_cython_generic(object f, double a, double b, int n_iter=100000):
    if not callable(f):
        raise TypeError("f должен быть вызываемой функцией")
    if a > b:
        raise ValueError("a не может быть больше b")
    if n_iter <= 0:
        raise ValueError("n_iter должно быть положительным")
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step
    return acc

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def integrate_cython_sin(double a, double b, int n_iter):
    if a > b:
        raise ValueError("a не может быть больше b")
    if n_iter <= 0:
        raise ValueError("n_iter должно быть положительным")
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    for i in range(n_iter):
        acc += c_sin(a + i * step) * step
    return acc

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def integrate_cython_cos(double a, double b, int n_iter):
    if a > b:
        raise ValueError("a не может быть больше b")
    if n_iter <= 0:
        raise ValueError("n_iter должно быть положительным")
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    for i in range(n_iter):
        acc += c_cos(a + i * step) * step
    return acc

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def integrate_cython_tan(double a, double b, int n_iter):
    if a > b:
        raise ValueError("a не может быть больше b")
    if n_iter <= 0:
        raise ValueError("n_iter должно быть положительным")
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    for i in range(n_iter):
        acc += c_tan(a + i * step) * step
    return acc

# --- Итерация 5: версия с отпусканием GIL ---
from libc.math cimport sin as c_sin

cdef double _integrate_sin_nogil(double a, double b, int n_iter) nogil:
    """Вычисление интеграла sin(x) без GIL."""
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += c_sin(x) * step  # ← C-функция, разрешена в nogil
    return acc

def integrate_cython_sin_nogil_wrapper(double a, double b, int n_iter):
    """Python-обёртка с отпусканием GIL."""
    if a > b:
        raise ValueError("a не может быть больше b")
    if n_iter <= 0:
        raise ValueError("n_iter должно быть положительным")
    cdef double result
    with nogil:
        result = _integrate_sin_nogil(a, b, n_iter)
    return result