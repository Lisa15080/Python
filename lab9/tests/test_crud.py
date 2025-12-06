import unittest
from unittest.mock import MagicMock
from lab9.controllers.currencycontroller import CurrencyController
from lab9.controllers.databasecontroller import DatabaseController

class TestCurrencyController(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock(spec=DatabaseController)
        self.controller = CurrencyController(self.mock_db)

    def test_list_currencies(self):
        """Проверка получения списка валют."""
        self.mock_db.currency_read_all.return_value = [
            {"id": 1, "char_code": "USD", "name": "Dollar", "value": 100, "nominal": 1},
            {"id": 2, "char_code": "EUR", "name": "Euro", "value": 95, "nominal": 1}
        ]
        result = self.controller.list_currencies()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['char_code'], "USD")
        self.mock_db.currency_read_all.assert_called_once()

    def test_list_empty(self):
        """Чтение списка валют, если база пустая."""
        self.mock_db.currency_read_all.return_value = []
        result = self.controller.list_currencies()
        self.assertEqual(result, [])
        self.mock_db.currency_read_all.assert_called_once()

    def test_update_currency(self):
        """Проверка обновления курса валюты."""
        self.controller.update_currency("EUR", 95.0)
        self.mock_db.currency_update.assert_called_once_with("EUR", 95.0)

    def test_update_negative_value(self):
        """Обновление валюты с отрицательным значением (контроллер просто передаёт в БД)."""
        self.controller.update_currency("GBP", -10.0)
        self.mock_db.currency_update.assert_called_once_with("GBP", -10.0)

    def test_delete_currency(self):
        """Проверка удаления валюты по id."""
        self.controller.delete_currency(1)
        self.mock_db.currency_delete.assert_called_once_with(1)

    def test_delete_nonexistent_currency(self):
        """Удаление несуществующей валюты."""
        self.controller.delete_currency(999)
        self.mock_db.currency_delete.assert_called_once_with(999)

    def test_create_currency_via_update(self):
        """Создание новой валюты через контроллер (симуляция через update)."""
        # Предположим, что если валюты нет, контроллер вызывает update
        self.mock_db.currency_update.return_value = None
        self.controller.update_currency("NEW", 123.45)
        self.mock_db.currency_update.assert_called_once_with("NEW", 123.45)

    def test_update_without_value(self):
        """Обновление валюты без передачи значения (контроллер должен вызвать обновление с None)."""
        self.controller.update_currency("USD", None)
        self.mock_db.currency_update.assert_called_once_with("USD", None)

    def test_list_currencies_contains_expected_fields(self):
        """Проверка, что возвращаемые словари содержат все ключи."""
        self.mock_db.currency_read_all.return_value = [
            {"id": 1, "char_code": "USD", "name": "Dollar", "value": 100, "nominal": 1}
        ]
        result = self.controller.list_currencies()
        self.assertIn('id', result[0])
        self.assertIn('char_code', result[0])
        self.assertIn('name', result[0])
        self.assertIn('value', result[0])
        self.assertIn('nominal', result[0])

if __name__ == "__main__":
    unittest.main(verbosity=2)
