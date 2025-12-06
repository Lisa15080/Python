class UserCurrency:
    """
    Класс для связывания пользователя с валютой.
    """

    def __init__(self, id: str, user_id: str, currency_id: str):
        """
        Инициализация объекта UserCurrency.

        Args:
            id (str): Уникальный идентификатор связи (не пустая строка).
            user_id (str): Идентификатор пользователя (не пустая строка).
            currency_id (str): Идентификатор валюты (не пустая строка).
        """
        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self):
        """Возвращает уникальный идентификатор связи."""
        return self.__id

    @id.setter
    def id(self, id: str):
        """
        Устанавливает уникальный идентификатор связи.

        Args:
            id (str): Идентификатор.
        """
        if isinstance(id, str) and len(id) >= 1:
            self.__id = id
        else:
            raise ValueError("id должен быть строкой")

    @property
    def user_id(self):
        """Возвращает идентификатор пользователя."""
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: str):
        """
        Устанавливает идентификатор пользователя.

        Args:
            user_id (str): Идентификатор пользователя.
        """
        if isinstance(user_id, str) and len(user_id) >= 1:
            self.__user_id = user_id
        else:
            raise ValueError("user_id должен быть строкой")

    @property
    def currency_id(self):
        """Возвращает идентификатор валюты."""
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, currency_id: str):
        """
        Устанавливает идентификатор валюты.

        Args:
            currency_id (str): Идентификатор валюты.
        """
        if isinstance(currency_id, str) and len(currency_id) >= 1:
            self.__currency_id = currency_id
        else:
            raise ValueError("currency_id должен быть строкой")
