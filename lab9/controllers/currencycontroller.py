# Было:
# from lab9.controllers.databasecontroller import CurrencyRatesCRUD

# Стало:
from lab9.controllers.databasecontroller import DatabaseController


class CurrencyController:
    def __init__(self, db_controller: DatabaseController):  # <- здесь аннотация DatabaseController
        self.db = db_controller

    def list_currencies(self):
        return self.db.currency_read_all()

    def update_currency(self, char_code: str, value: float):
        self.db.currency_update(char_code, value)

    def delete_currency(self, currency_id: int):
        self.db.currency_delete(currency_id)
