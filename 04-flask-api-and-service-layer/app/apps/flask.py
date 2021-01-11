from typing import Callable, Any, Tuple, cast

from flask import Flask
import flask

from ..adapters import orm
from ..adapters.orm import SessionMaker
from ..adapters.repository import SqlAlchemyRepository

from .. import config

app: Flask = cast(Flask, None)
get_session: SessionMaker = cast(SessionMaker, None)


def init_db(db_url=None, drop_all=False, show_log=False) -> SessionMaker:
    from sqlalchemy.orm import sessionmaker

    global get_session

    if get_session:
        return get_session

    metadata = orm.start_mappers()
    engine = orm.init_engine(metadata,
                             db_url or config.get_db_url(),
                             connect_args=config.get_db_connect_args(),
                             poolclass=config.get_db_poolclass(),
                             drop_all=drop_all,
                             show_log=show_log)
    get_session = cast(SessionMaker, sessionmaker(engine))
    return get_session


def get_repo():
    return SqlAlchemyRepository(get_session())


def create_app() -> Flask:
    global app
    app = Flask(__name__)
    return app


def init_app() -> Flask:
    from ..routes import flask
    global get_session
    get_session = init_db()
    return app


# types
_AnyFunc = Callable[..., Any]
_Decorator = Callable[..., Callable[[_AnyFunc], _AnyFunc]]
FlaskResponse = tuple[Any, int]

app = create_app()
route: _Decorator = cast(_Decorator, app.route)
