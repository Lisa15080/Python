from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from utils.currencies_api import get_currencies

# Настройка шаблонизатора Jinja2
env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

# Список пользователей
users = [
    {'id': 1, 'name': 'Alexandr'},
    {'id': 2, 'name': 'Vasiliy'}
]

# Подписки пользователей на валюты
subscriptions_list = [
    {'user_id': 1, 'currency_code': 'USD'},
    {'user_id': 1, 'currency_code': 'EUR'},
    {'user_id': 2, 'currency_code': 'USD'},
    {'user_id': 2, 'currency_code': 'GBP'}
]

# Коды валют
currency_codes = ['USD', 'EUR', 'GBP']
currency_values = get_currencies(currency_codes)
currencies = {
    code: {
        'char_code': code,
        'name': {
            'USD': 'Доллар США',
            'EUR': 'Евро',
            'GBP': 'Фунт стерлингов'
        }[code],
        'value': currency_values[code]
    }
    for code in currency_codes
}

# HTML страницы
author_html = env.get_template("author.html").render(
    name='Liza',
    group='P3121',
    description="Информация об авторе проекта"
)

index_html = env.get_template("index.html").render(
    myapp="Приложение для отслеживания курсов валют",
    author_name='Liza',
    group='P3121',
    navigation=[
        {'caption': 'Главная', 'href': "/"},
        {'caption': 'Пользователи', 'href': "/users"},
        {'caption': 'Курсы валют', 'href': "/currencies"},
        {'caption': 'Об авторе проекта', 'href': "/author"}
    ]
)

users_html = env.get_template("users.html").render(users=users)

currencies_html = env.get_template("currencies.html").render(
    currencies=[
        {
            'char_code': code,
            'name': currencies[code]['name'],
            'value': currencies[code]['value'],
            'nominal': 1
        }
        for code in currency_codes
    ]
)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Простая обработка HTTP-запросов.
    Поддерживаются маршруты:
        /            - Главная страница
        /users       - Список пользователей
        /users/<id>  - Подписки конкретного пользователя
        /currencies  - Список валют и курсов
        /author      - Информация об авторе
    """

    def do_GET(self):
        """
        Обработка GET-запросов.
        Отправляет соответствующую HTML-страницу в зависимости от пути.
        """
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        if self.path == "/":
            self.wfile.write(index_html.encode("utf-8"))
        elif self.path == "/users":
            self.wfile.write(users_html.encode("utf-8"))
        elif self.path.startswith("/users/"):
            user_id = int(self.path.split("/")[2])
            user = next(u for u in users if u['id'] == user_id)
            user_subs = [
                currencies[s['currency_code']]
                for s in subscriptions_list
                if s['user_id'] == user_id
            ]

            html = env.get_template("user_subscriptions.html").render(
                user=user, subscriptions=user_subs
            )
            self.wfile.write(html.encode("utf-8"))
        elif self.path == "/currencies":
            self.wfile.write(currencies_html.encode("utf-8"))
        elif self.path == "/author":
            self.wfile.write(author_html.encode("utf-8"))
        else:
            self.wfile.write(b"<h1>404 Not Found</h1>")


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('Server is running on http://localhost:8080')
    httpd.serve_forever()

