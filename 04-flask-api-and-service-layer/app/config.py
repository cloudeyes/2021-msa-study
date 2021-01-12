"""App Configurations."""
from __future__ import annotations
from typing import Any, Optional
from sqlalchemy.pool import StaticPool


def get_api_host() -> str:
    """Get API server's host address."""
    return "127.0.0.1"


def get_api_port() -> int:
    """Get API server's host port."""
    return 5000


def get_api_url() -> str:
    """Get API server's full url."""
    return f'http://{get_api_host()}:{get_api_port()}'


def get_db_url() -> str:
    """Get API server's db url.

    The url format should conform the SQLAlchemy's url scheme.
    """
    pg_host = '04-flask-api-and-service-layer_postgres_1'
    return f"postgresql+psycopg2://smprc:p%40ssw0rd@{pg_host}/smprc"


def get_db_connect_args() -> dict[str, Any]:
    """Get db connection arguments for SQLAlchemy's engine creation.

    Example:
        For SQLite dbs, it could be: ::

            {'check_same_thread': False}
    """
    return {}


def get_db_poolclass() -> Optional[sqlalchemy.pool.base.Pool]:
    """Get db poolclass arguemnt for SQLAlchemy's engine creation.

    Returns:
        A pool class

    """
    return StaticPool

