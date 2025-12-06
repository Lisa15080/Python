import sqlite3
from lab9.utils.currencies_api import get_currencies


class DatabaseController:
    def __init__(self):
        self.con = sqlite3.connect(":memory:", check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.cursor = self.con.cursor()
        self._create_tables()

    # ---------------------- CREATE TABLES ----------------------
    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value FLOAT,
                nominal INTEGER NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id)
            );
        """)

        self.con.commit()

    # --------------------- CRUD: CURRENCY ----------------------
    def currency_create(self, num_code, char_code, name, value=None, nominal=1):
        """
        Создание валюты. Если value не указан, берём с ЦБ.
        """
        if value is None:
            try:
                api_val = get_currencies([char_code])
                value = api_val.get(char_code, 0)
            except Exception:
                value = 0

        sql = """INSERT INTO currency(num_code, char_code, name, value, nominal)
                 VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(sql, (num_code or "", char_code, name, value, nominal))
        self.con.commit()

    def currency_read_all(self):
        sql = "SELECT * FROM currency"
        return [dict(row) for row in self.cursor.execute(sql).fetchall()]

    def currency_update(self, char_code, new_value=None):
        """
        Обновление курса валюты. Если new_value=None, берём с ЦБ.
        """
        if new_value is None:
            try:
                api_val = get_currencies([char_code])
                new_value = api_val.get(char_code)
            except Exception:
                return  # ничего не делаем
        if new_value is not None:
            sql = "UPDATE currency SET value = ? WHERE char_code = ?"
            self.cursor.execute(sql, (new_value, char_code))
            self.con.commit()

    def currency_delete(self, currency_id):
        sql = "DELETE FROM currency WHERE id = ?"
        self.cursor.execute(sql, (currency_id,))
        self.con.commit()

    # ------------------------ USERS CRUD -----------------------
    def user_create(self, name):
        self.cursor.execute("INSERT INTO user(name) VALUES(?)", (name,))
        self.con.commit()

    def user_read_all(self):
        return [dict(row) for row in self.cursor.execute("SELECT * FROM user")]

    def user_read_one(self, user_id):
        sql = "SELECT * FROM user WHERE id = ?"
        res = self.cursor.execute(sql, (user_id,)).fetchone()
        return dict(res) if res else None

    # -------------------- USER_CURRENCY CRUD --------------------
    def user_currency_add(self, user_id, currency_id):
        sql = "INSERT INTO user_currency(user_id, currency_id) VALUES(?, ?)"
        self.cursor.execute(sql, (user_id, currency_id))
        self.con.commit()

    def user_currencies(self, user_id):
        """
        Возвращает все валюты, на которые подписан пользователь.
        """
        sql = """
            SELECT currency.*
            FROM currency
            JOIN user_currency ON currency.id = user_currency.currency_id
            WHERE user_currency.user_id = ?
        """
        return [dict(row) for row in self.cursor.execute(sql, (user_id,)).fetchall()]

