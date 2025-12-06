import unittest
from lab8.models.author import Author
from lab8.models.app import App
from lab8.models.user import User
from lab8.models.currency import Currency
from lab8.models.user_currency import UserCurrency
from lab8.utils.currencies_api import get_currencies
from jinja2 import Environment, PackageLoader, select_autoescape
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestAuthorModel(unittest.TestCase):
    """Тестирование модели Author."""
    def test_getters_setters(self):
        """Проверка работы геттеров и сеттеров."""
        author = Author("Liza", "P3121")
        self.assertEqual(author.name, "Liza")
        self.assertEqual(author.group, "P3121")
        author.name = "Anna"
        self.assertEqual(author.name, "Anna")
        author.group = "P1234"
        self.assertEqual(author.group, "P1234")

    def test_invalid_values(self):
        """Проверка обработки некорректных значений."""
        with self.assertRaises(ValueError):
            Author("A", "P3121")
        with self.assertRaises(ValueError):
            Author("Liza", "P1")


class TestAppModel(unittest.TestCase):
    """Тестирование модели App."""
    def test_getters_setters(self):
        """Проверка корректной работы геттеров и сеттеров."""
        author = Author("Liza", "P3121")
        app = App("MyApp", "1.0", author)
        self.assertEqual(app.name, "MyApp")
        self.assertEqual(app.version, "1.0")
        self.assertEqual(app.author, author)

    def test_invalid_values(self):
        """Проверка обработки некорректных значений."""
        author = Author("Liza", "P3121")
        with self.assertRaises(ValueError):
            App("A", "1.0", author)
        with self.assertRaises(ValueError):
            App("MyApp", "", author)
        with self.assertRaises(ValueError):
            App("MyApp", "1.0", "not_author")


class TestUserModel(unittest.TestCase):
    """Тестирование модели User."""
    def test_getters_setters(self):
        """Проверка корректной работы геттеров и сеттеров."""
        user = User("1", "Alex")
        self.assertEqual(user.id, "1")
        self.assertEqual(user.name, "Alex")

    def test_invalid_values(self):
        """Проверка обработки некорректных значений."""
        with self.assertRaises(ValueError):
            User("", "Alex")
        with self.assertRaises(ValueError):
            User("1", "A")


class TestCurrencyModel(unittest.TestCase):
    """Тестирование модели Currency."""
    def test_getters_setters(self):
        """Проверка корректной работы геттеров и сеттеров."""
        c = Currency("1", 840, "USD", "Dollar", 100.0, 1)
        self.assertEqual(c.char_code, "USD")
        self.assertEqual(c.value, 100.0)
        c.value = 50
        self.assertEqual(c.value, 50)

    def test_invalid_values(self):
        """Проверка обработки некорректных значений."""
        c = Currency("1", 840, "USD", "Dollar", 100.0, 1)

        with self.assertRaises(ValueError):
            c.char_code = "U"

        with self.assertRaises(ValueError):
            c.name = "D"

        with self.assertRaises(ValueError):
            c.value = -10

        with self.assertRaises(ValueError):
            c.nominal = 0


class TestUserCurrencyModel(unittest.TestCase):
    """Тестирование модели UserCurrency."""

    def test_getters_setters(self):
        """Проверка корректной работы геттеров и сеттеров."""
        uc = UserCurrency("1", "u1", "USD")
        self.assertEqual(uc.id, "1")
        self.assertEqual(uc.user_id, "u1")
        self.assertEqual(uc.currency_id, "USD")



class TestGetCurrenciesFunction(unittest.TestCase):
    """Тестирование функции получения курсов валют."""

    def test_valid_currencies(self):
        """Проверка корректного получения существующих валют."""
        result = get_currencies(['USD', 'EUR'])
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertIsInstance(result['USD'], float)

    def test_nonexistent_currency(self):
        """Проверка обработки несуществующей валюты."""
        with self.assertRaises(KeyError):
            get_currencies(['XYZ'])


class TestTemplates(unittest.TestCase):
    """Тестирование шаблонов Jinja2."""
    @classmethod
    def setUpClass(cls):
        """Настройка окружения Jinja2 для тестов."""
        cls.env = Environment(
            loader=PackageLoader("myapp"),
            autoescape=select_autoescape()
        )

    def test_author_template(self):
        """Проверка рендеринга шаблона автора."""
        html = self.env.get_template("author.html").render(name="Liza", group="P3121")
        self.assertIn("Liza", html)
        self.assertIn("P3121", html)

    def test_currencies_template(self):
        """Проверка рендеринга шаблона валют."""
        currencies = [{'char_code': 'USD', 'name': 'Dollar', 'value': 100, 'nominal': 1}]
        html = self.env.get_template("currencies.html").render(currencies=currencies)
        self.assertIn("USD", html)
        self.assertIn("Dollar", html)
        self.assertIn("100", html)

    def test_users_template(self):
        """Проверка рендеринга шаблона пользователей."""
        users = [{'id': '1', 'name': 'Alex'}]
        html = self.env.get_template("users.html").render(users=users)
        self.assertIn("Alex", html)
        self.assertIn("/users/1", html)


import http.client
import threading
from lab8.myapp import SimpleHTTPRequestHandler, HTTPServer


class TestController(unittest.TestCase):
    """Тестирование HTTP-контроллера."""
    @classmethod
    def setUpClass(cls):
        """Запуск сервера в отдельном потоке для тестов."""
        cls.server = HTTPServer(('localhost', 8081), SimpleHTTPRequestHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    def get_path(self, path):
        """Функция для выполнения GET-запроса."""
        conn = http.client.HTTPConnection('localhost', 8081)
        conn.request("GET", path)
        response = conn.getresponse()
        data = response.read().decode()
        conn.close()
        return response.status, data

    def test_index(self):
        """Проверка главной страницы."""
        status, data = self.get_path("/")
        self.assertEqual(status, 200)
        self.assertIn("Приложение для отслеживания курсов валют", data)

    def test_users(self):
        """Проверка страницы пользователей."""
        status, data = self.get_path("/users")
        self.assertEqual(status, 200)
        self.assertIn("Alexandr", data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
