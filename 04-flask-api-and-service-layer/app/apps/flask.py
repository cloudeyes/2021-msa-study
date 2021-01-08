from typing import Callable, Any, Tuple, cast

from flask import Flask
import flask

from ..adapters import orm
from .. import config

app: Flask = None

def create_app() -> Flask:
    global app
    app = Flask(__name__)
    return app

def init_app() -> Flask:
    from ..routes import flask
    from ..config import init_db
    init_db()
    return app

# types
AnyFuncType = Callable[..., Any]
DecoratorType = Callable[..., Callable[[AnyFuncType], AnyFuncType]]
FlaskResponse = tuple[Any, int]

app = create_app()
route: DecoratorType = cast(DecoratorType, app.route)

