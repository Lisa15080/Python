class Author:
    """
    Класс для представления автора.
    """

    def __init__(self, name: str, group: str):
        """
        Инициализация объекта Author.
        Args:
            name (str): Имя автора (минимум 2 символа).
            group (str): Группа автора (минимум 5 символов).
        """
        self.name = name
        self.group = group

    @property
    def name(self):
        """Возвращает имя автора."""
        return self.__name

    @name.setter
    def name(self, name: str):
        """
        Устанавливает имя автора.

        Args:
            name (str): Имя автора.
        """
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени автора')

    @property
    def group(self):
        """Возвращает группу автора."""
        return self.__group

    @group.setter
    def group(self, group: str):
        """
        Устанавливает группу автора.

        Args:
            group (str): Группа автора.
        """
        if isinstance(group, str) and len(group) >= 5:
            self.__group = group
        else:
            raise ValueError('Ошибка при задании группы автора')
