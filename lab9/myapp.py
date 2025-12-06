from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from lab9.controllers.databasecontroller import DatabaseController
from utils.currencies_api import get_currencies

# --- Настройка шаблонизатора Jinja2 ---
env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

# --- Пользователи ---
users = [
    {'id': 1, 'name': 'Alexandr'},
    {'id': 2, 'name': 'Vasiliy'}
]

# --- Инициализация базы данных ---
db = DatabaseController()
for u in users:
    db.user_create(u['name'])

# --- Валюты ---
currency_codes = ['USD', 'EUR', 'GBP']
currency_names = {
    'USD': 'Доллар США',
    'EUR': 'Евро',
    'GBP': 'Фунт стерлингов'
}
currency_values = get_currencies(currency_codes)

for code in currency_codes:
    db.currency_create(
        num_code='',
        char_code=code,
        name=currency_names[code],
        value=currency_values[code],
        nominal=1
    )

# --- Подписки пользователей на валюты ---
subscriptions_list = [
    {'user_id': 1, 'currency_code': 'USD'},
    {'user_id': 1, 'currency_code': 'EUR'},
    {'user_id': 2, 'currency_code': 'USD'},
    {'user_id': 2, 'currency_code': 'GBP'}
]

for sub in subscriptions_list:
    currency = next(c for c in db.currency_read_all() if c['char_code'] == sub['currency_code'])
    db.user_currency_add(sub['user_id'], currency['id'])


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Обработка HTTP-запросов.
    Поддерживаемые маршруты:
        /            - Главная страница
        /users       - Список пользователей
        /user?id=   - Подписки конкретного пользователя
        /currencies  - Список валют и их курсов
        /author      - Информация об авторе проекта
    """

    def do_GET(self):
        """
        Обработка GET-запросов и генерация HTML-страниц.
        """
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        if path == "/":
            html = env.get_template("index.html").render(
                myapp="Приложение для отслеживания курсов валют",
                author_name='Liza',
                group='P3121',
                navigation=[
                    {'caption': 'Главная', 'href': "/"},
                    {'caption': 'Пользователи', 'href': "/users"},
                    {'caption': 'Курсы валют', 'href': "/currencies"},
                    {'caption': 'Об авторе проекта', 'href': "/author"}
                ],
                currencies=db.currency_read_all()
            )
            self.wfile.write(html.encode("utf-8"))

        elif path == "/author":
            html = env.get_template("author.html").render(
                name='Liza',
                group='P3121'
            )
            self.wfile.write(html.encode("utf-8"))

        elif path == "/users":
            html = env.get_template("users.html").render(
                users=db.user_read_all()
            )
            self.wfile.write(html.encode("utf-8"))

        elif path == "/user":
            user_id = int(query.get('id', [0])[0])
            user = db.user_read_one(user_id)
            if not user:
                self.wfile.write("<h1>Пользователь не найден</h1>".encode("utf-8"))
                return

            subscriptions = db.user_currencies(user_id)
            html = env.get_template("user_subscriptions.html").render(
                user=user,
                subscriptions=subscriptions
            )
            self.wfile.write(html.encode("utf-8"))

        elif path == "/currencies":
            html = env.get_template("currencies.html").render(
                currencies=db.currency_read_all()
            )
            self.wfile.write(html.encode("utf-8"))

        else:
            self.wfile.write("<h1>404 Not Found</h1>".encode("utf-8"))

    def do_POST(self):
        """
        Обработка POST-запросов.
        Поддержка создания, обновления и удаления валют.
        """
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(post_data)

        if path == "/currencies":
            action = form.get("action", [""])[0]

            if action == "create":
                char_code = form.get("char_code", [""])[0]
                name = form.get("name", [""])[0]
                value_raw = form.get("value", [""])[0]
                nominal = int(form.get("nominal", ["1"])[0])
                value = float(value_raw) if value_raw else None

                db.currency_create(
                    num_code="",
                    char_code=char_code,
                    name=name,
                    value=value,
                    nominal=nominal
                )

            elif action == "update":
                char_code = form.get("char_code", [""])[0]
                value_raw = form.get("value", [""])[0]
                value = float(value_raw) if value_raw else None
                db.currency_update(char_code, value)

            elif action == "delete":
                currency_id = int(form.get("id", ["0"])[0])
                db.currency_delete(currency_id)

            self.send_response(303)
            self.send_header("Location", "/currencies")
            self.end_headers()
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"POST not supported")


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('Server is running on http://localhost:8080')
    httpd.serve_forever()
