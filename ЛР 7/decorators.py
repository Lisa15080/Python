import sys
import functools
import logging
import requests.exceptions

def logger(func=None, *, handle=sys.stdout):
    """
    Декоратор `logger` для логирования вызовов функций.

    Аргументы:
        func (callable, optional): Функция для декорирования. Если не передан, возвращается декоратор с настройками.
        handle (sys.stdout или logging.Logger, опционально): Поток или логгер для вывода сообщений. По умолчанию sys.stdout.
    """

    if func is None:
        return lambda real_func: logger(real_func, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        kwargs.pop('handle', None)

        is_logger = isinstance(handle, logging.Logger)

        try:
            msg_start = f"INFO: Start {func.__name__} with args={args}, kwargs={kwargs}\n"
            if is_logger:
                handle.info(msg_start)
            else:
                handle.write(msg_start)

            result = func(*args, **kwargs)

            msg_end = f"INFO: Finished {func.__name__} with result={result}\n"
            if is_logger:
                handle.info(msg_end)
            else:
                handle.write(msg_end)

            return result
        except requests.exceptions.RequestException as e:
            msg_err = f"ERROR: Ошибка при запросе к API: {e}\n"
            if is_logger:
                handle.error(msg_err)
            else:
                handle.write(msg_err)
            raise requests.exceptions.RequestException("Упали с исключением") from e

    return inner


