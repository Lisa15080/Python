class Currency:
    """
    Класс для представления валюты.
    """

    def __init__(self, id: str, num_code: int, char_code: str, name: str, value: float, nominal: int):
        """
        Инициализация объекта Currency.
        """
        self.id = id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self):
        """Возвращает id валюты."""
        return self.__id

    @id.setter
    def id(self, id: str):
        if id is None or isinstance(id, str):
            self.__id = id
        else:
            raise ValueError("id валюты должен быть строкой или None")

    @property
    def num_code(self):
        """Возвращает числовой код валюты."""
        return self.__num_code

    @num_code.setter
    def num_code(self, code: int):
        if code is None or isinstance(code, int):
            self.__num_code = code
        else:
            raise ValueError("num_code должен быть числом или None")

    @property
    def char_code(self):
        """Возвращает символьный код валюты."""
        return self.__char_code

    @char_code.setter
    def char_code(self, code: str):
        if code is None or (isinstance(code, str) and len(code) >= 2):
            self.__char_code = code
        else:
            raise ValueError("char_code должен быть строкой длиной >= 2 или None")

    @property
    def name(self):
        """Возвращает название валюты."""
        return self.__name

    @name.setter
    def name(self, name: str):
        if name is None or (isinstance(name, str) and len(name) >= 2):
            self.__name = name
        else:
            raise ValueError("Название валюты должно быть строкой длиной >= 2 или None")

    @property
    def value(self):
        """Возвращает курс валюты."""
        return self.__value

    @value.setter
    def value(self, value: float):
        if isinstance(value, (int, float)) and value >= 0:
            self.__value = value
        else:
            raise ValueError("Курс валюты должен быть числом >= 0")

    @property
    def nominal(self):
        """Возвращает номинал валюты."""
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: int):
        if isinstance(nominal, int) and nominal > 0:
            self.__nominal = nominal
        else:
            raise ValueError("Номинал должен быть положительным целым числом")
