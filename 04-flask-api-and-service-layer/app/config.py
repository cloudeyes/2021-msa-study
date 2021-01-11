from __future__ import annotations
from typing import Any, Callable, cast
import os


def get_api_host() -> str:
    return "127.0.0.1"


def get_api_port() -> int:
    return 5000


def get_api_url() -> str:
    return f'http://{get_api_host()}:{get_api_port()}'


def get_db_url() -> str:
    pg_host = '04-flask-api-and-service-layer_postgres_1'
    return f"postgresql+psycopg2://smprc:p%40ssw0rd@{pg_host}/smprc"


def get_db_connect_args() -> str:
    return {}


def get_db_poolclass() -> Any:
    from sqlalchemy.pool import StaticPool
    return StaticPool
