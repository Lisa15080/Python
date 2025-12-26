import unittest
import io
import requests

from get_currency import get_currencies
from decorators import logger
from solve_quadratic import solve_quadratic

class TestGetCurrencies(unittest.TestCase):
    """
    Проверяет функцию `get_currencies`.
    """

    def setUp(self):
        self.clean_get = get_currencies.__wrapped__

    def test_valid_currency(self):
        """Проверка корректного возврата существующих валют."""
        result = self.clean_get(['USD', 'EUR'])
        self.assertIn("USD", result)
        self.assertIn("EUR", result)

    def test_nonexistent_currency(self):
        """Проверка исключения KeyError для несуществующей валюты."""
        with self.assertRaises(KeyError):
            self.clean_get(['XYZ'])

    def test_connection_error(self):
        """Проверка RequestException при ошибке подключения."""
        with self.assertRaises(requests.exceptions.RequestException):
            self.clean_get(['USD'], url="https://invalid-url")

    def test_invalid_json(self):
        """Проверка ValueError при некорректном JSON."""
        with self.assertRaises(ValueError):
            self.clean_get(['USD'], url="https://example.com")


class TestDecoratorLogging(unittest.TestCase):
    """
    Проверяет декоратор logger.
    """

    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped_get(codes, url=None):
            return get_currencies.__wrapped__(codes, url=url)

        self.wrapped = wrapped_get

    def test_logging_connection_error(self):
        """Проверка логирования при ошибке подключения."""
        with self.assertRaises(requests.exceptions.RequestException):
            self.wrapped(['USD'], url="https://invalid-url")

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("Ошибка при запросе к API", logs)

    def test_logging_nonexistent_currency(self):
        """Проверка логирования при запросе несуществующей валюты."""
        with self.assertRaises(requests.exceptions.RequestException):
            self.wrapped(['XYZ'])


class TestSolveQuadratic(unittest.TestCase):
    """
    Проверяет функцию solve_quadratic.
    """

    def test_two_roots(self):
        """Проверка функции при двух корнях."""
        res = solve_quadratic(1, -3, 2)
        self.assertCountEqual(res, [1.0, 2.0])

    def test_one_root(self):
        """Проверка функции при одном корне."""
        res = solve_quadratic(1, 2, 1)
        self.assertEqual(res, -1.0)

    def test_no_real(self):
        """Проверка функции при отсутствии действительных корней."""
        res = solve_quadratic(1, 0, 5)
        self.assertIn("Нет действительных корней", res)

    def test_invalid(self):
        """Проверка исключения при некорректных аргументах."""
        with self.assertRaises(ValueError):
            solve_quadratic("abc", 2, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
