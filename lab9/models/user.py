class User:
    """
    Класс для представления пользователя.
    """

    def __init__(self, id: str, name: str):
        """
        Инициализация объекта User.

        Args:
            id (str): Уникальный идентификатор пользователя (не пустая строка).
            name (str): Имя пользователя (минимум 2 символа).
        """
        self.id = id
        self.name = name

    @property
    def name(self):
        """Возвращает имя пользователя."""
        return self.__name

    @name.setter
    def name(self, name: str):
        """
        Устанавливает имя пользователя.

        Args:
            name (str): Имя пользователя.
        """
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError("Ошибка при задании имени пользователя")

    @property
    def id(self):
        """Возвращает уникальный идентификатор пользователя."""
        return self.__id

    @id.setter
    def id(self, id: str):
        """
        Устанавливает уникальный идентификатор пользователя.

        Args:
            id (str): Идентификатор пользователя.
        """
        if isinstance(id, str) and len(id) >= 1:
            self.__id = id
        else:
            raise ValueError("Ошибка при задании уникального идентификатора")
