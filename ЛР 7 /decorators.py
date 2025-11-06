import sys
import functools
import requests.exceptions

def trace(func=None, *, handle=sys.stdout):
    if func is None:
        return lambda real_func: trace(real_func, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        kwargs.pop('handle', None)
        handle.write("Using handling output\n")
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            handle.write(f"Ошибка при запросе к API: {e}")
            raise     # пробрасываем исходное исключение
    return inner
