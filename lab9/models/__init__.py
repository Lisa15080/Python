from jinja2 import Environment, PackageLoader, select_autoescape
from .author import Author
from .app import App
from .user import User
from .currency import Currency
from .user_currency import UserCurrency

env = Environment(
    loader=PackageLoader("lab8"),
    autoescape=select_autoescape()
)
