import unittest
from unittest.mock import MagicMock
from lab9.controllers.currencycontroller import CurrencyController

class TestCurrencyControllerCRUD(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.controller = CurrencyController(self.mock_db)

    def test_create_currency(self):
        """Проверка добавления новой валюты через update с value."""
        self.controller.update_currency("USD", 100.0)
        self.mock_db._update.assert_called_once_with({"USD": 100.0})

    def test_read_currencies(self):
        """Проверка получения списка валют."""
        self.mock_db._read.return_value = [
            {"id": 1, "char_code": "USD", "name": "Dollar", "value": 100, "nominal": 1}
        ]
        result = self.controller.list_currencies()
        self.assertEqual(result[0]['char_code'], "USD")
        self.mock_db._read.assert_called_once()

    def test_update_currency(self):
        """Проверка обновления курса валюты."""
        self.controller.update_currency("EUR", 95.0)
        self.mock_db._update.assert_called_once_with({"EUR": 95.0})

    def test_delete_currency(self):
        """Проверка удаления валюты по id."""
        self.controller.delete_currency(1)
        self.mock_db._delete.assert_called_once_with(1)

    def test_read_empty(self):
        """Проверка чтения из пустой базы."""
        self.mock_db._read.return_value = []
        result = self.controller.list_currencies()
        self.assertEqual(result, [])
        self.mock_db._read.assert_called_once()

    def test_delete_nonexistent(self):
        """Удаление несуществующего id."""
        self.controller.delete_currency(999)
        self.mock_db._delete.assert_called_once_with(999)

    def test_update_invalid_value(self):
        """Обновление с отрицательным значением (контроллер просто передаёт в БД)."""
        self.controller.update_currency("GBP", -10.0)
        self.mock_db._update.assert_called_once_with({"GBP": -10.0})


if __name__ == "__main__":
    unittest.main(verbosity=2)
