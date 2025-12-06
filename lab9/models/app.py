class App:
    """
    Класс для представления приложения.
    """

    def __init__(self, name: str, version: str, author):
        """
        Инициализация объекта App.

        Args:
            name (str): Название приложения (минимум 2 символа).
            version (str): Версия приложения (не пустая строка).
            author (Author): Автор приложения, объект класса Author.
        """
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self):
        """Возвращает название приложения."""
        return self.__name

    @name.setter
    def name(self, name: str):
        """
        Устанавливает название приложения.

        Args:
            name (str): Название приложения.
        """
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError("Ошибка при задании названия приложения")

    @property
    def version(self):
        """Возвращает версию приложения."""
        return self.__version

    @version.setter
    def version(self, version: str):
        """
        Устанавливает версию приложения.

        Args:
            version (str): Версия приложения.
        """
        if isinstance(version, str) and len(version) >= 1:
            self.__version = version
        else:
            raise ValueError("Ошибка при задании версии приложения")

    @property
    def author(self):
        """Возвращает автора приложения."""
        return self.__author

    @author.setter
    def author(self, author):
        """
        Устанавливает автора приложения.

        Args:
            author (Author): Объект класса Author.
        """
        from .author import Author
        if isinstance(author, Author):
            self.__author = author
        else:
            raise ValueError("Автор должен быть объектом класса Author")
