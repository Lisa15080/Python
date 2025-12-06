from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from lab9.controllers.databasecontroller import DatabaseController
from utils.currencies_api import get_currencies


env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

db = DatabaseController()


initial_users = [
    {'name': 'Alexandr'},
    {'name': 'Vasiliy'}
]
for u in initial_users:
    db.user_create(u['name'])


currency_codes = ['USD', 'EUR', 'GBP']
currency_names = {'USD': 'Доллар США', 'EUR': 'Евро', 'GBP': 'Фунт стерлингов'}
currency_values = get_currencies(currency_codes)

for code in currency_codes:
    db.currency_create(
        num_code='',
        char_code=code,
        name=currency_names[code],
        value=currency_values[code],
        nominal=1
    )


subscriptions_list = [
    {'user_name': 'Alexandr', 'currency_code': 'USD'},
    {'user_name': 'Alexandr', 'currency_code': 'EUR'},
    {'user_name': 'Vasiliy', 'currency_code': 'USD'},
    {'user_name': 'Vasiliy', 'currency_code': 'GBP'}
]

# Привязка подписок к БД
for sub in subscriptions_list:
    user = next(u for u in db.user_read_all() if u['name'] == sub['user_name'])
    currency = next(c for c in db.currency_read_all() if c['char_code'] == sub['currency_code'])
    db.user_currency_add(user['id'], currency['id'])

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        try:
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

        except Exception as e:
            self.wfile.write(f"<h1>Ошибка: {e}</h1>".encode("utf-8"))


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('Server is running on http://localhost:8080')
    httpd.serve_forever()

