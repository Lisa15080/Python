def get_currencies(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    """
    Получает курсы валют с API Центробанка России.
    """
    import requests

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException("API недоступен") from e

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError("Некорректный JSON") from e

    if "Valute" not in data:
        raise KeyError("Ключ 'Valute' отсутствует в данных")

    currencies = {}
    for code in currency_codes:
        if code not in data["Valute"]:
            raise KeyError(f"Код валюты '{code}' не найден")
        value = data["Valute"][code]["Value"]
        if not isinstance(value, (int, float)):
            raise TypeError(f"Курс валюты '{code}' имеет неверный тип")
        currencies[code] = value

    return currencies
