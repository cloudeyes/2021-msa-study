from __future__ import annotations
from typing import Any, Callable

from .adapters import orm
from sqlalchemy.orm import Session, sessionmaker

def get_api_host() -> str:
    return "127.0.0.1"

def get_api_port() -> int:
    return 5000

def get_api_url() -> str:
    return f'http://{get_api_host()}:{get_api_port()}'


def get_db_url() -> str:
    return "sqlite://"


def get_db_connect_args() -> str:
    return {'check_same_thread': False}


def get_db_poolclass() -> Any:
    from sqlalchemy.pool import StaticPool
    return StaticPool


get_session: Callable[[], Session] = None


def init_db():
    global get_session

    if get_session:
        return get_session

    print('initialize db:', get_db_url())
    metadata = orm.start_mappers()
    engine = orm.init_engine(metadata,
                             get_db_url(),
                             connect_args=get_db_connect_args(),
                             poolclass=get_db_poolclass())
    get_session = sessionmaker(engine)
    return get_session


def get_repo():
    from .adapters.orm import SqlAlchemyRepository
    get_session = init_db()
    return SqlAlchemyRepository(get_session())
