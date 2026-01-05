import logging
from decorators import logger
from get_currency import get_currencies

file_logger = logging.getLogger("currency_file")
file_logger.setLevel(logging.DEBUG)
file_logger.addHandler(logging.FileHandler("currency.log", mode="w", encoding="utf-8"))

@logger(handle=file_logger)
def get_currencies_file_logged(*args, **kwargs):
    return get_currencies(*args, **kwargs)


if __name__ == "__main__":
    try:
        print(get_currencies_file_logged(["USD", "EUR"]))
        print("файл currency.log")
    except Exception as e:
        print("Ошибка:", e)
