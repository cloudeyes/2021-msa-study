"""Flask 로 구현한 RESTful 서비스 앱."""
from __future__ import annotations
from typing import Callable, TypeVar, Optional, Any, Tuple, cast

from flask import Flask

from ..adapters import orm
from ..adapters.orm import SessionMaker
from ..adapters.repository import SqlAlchemyRepository, AbstractRepository

from .. import config

# types
_AnyFunc = Callable[..., Any]
RouteDecorator = Callable[..., Callable[[_AnyFunc], _AnyFunc]]
FlaskResponse = tuple[Any, int]

# globals
app: Flask = cast(Flask, None)  # pylint: disable=invalid-name
get_session: SessionMaker = cast(SessionMaker, None)  # pylint: disable=invalid-name


def init_db(db_url: Optional[str] = None,
            drop_all: bool = False,
            show_log: bool = False) -> SessionMaker:
    from sqlalchemy.orm import sessionmaker
    global get_session  # pylint: disable=global-statement

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


def get_repo() -> AbstractRepository:
    return SqlAlchemyRepository(get_session())


def create_app() -> Flask:
    global app  # pylint: disable=global-statement, invalid-name
    app = Flask(__name__)
    return app


def init_app() -> Flask:
    from ..routes import flask  # pylint: disable=import-outside-toplevel, unused-import
    global get_session  # pylint: disable=global-statement, invalid-name
    get_session = init_db()
    return app


app = create_app()
route: RouteDecorator = cast(RouteDecorator, app.route)
