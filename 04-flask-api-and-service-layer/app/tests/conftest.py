from typing import Optional, Callable
from datetime import date, datetime, timedelta
import uuid

import pytest
import requests

from ..domain.models import Batch
from ..adapters.orm import SessionMaker
from ..adapters.repository import SqlAlchemyRepository

from . import ServerThread
from ..apps.flask import init_app, init_db


@pytest.fixture
def session():
    from sqlalchemy.pool import StaticPool
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    from ..adapters.orm import metadata, start_mappers, clear_mappers

    engine = create_engine('sqlite://',
                           connect_args={'check_same_thread': False},
                           poolclass=StaticPool)
    metadata = start_mappers(use_exist=True)
    metadata.create_all(engine)
    yield sessionmaker(engine)()
    # clear_mappers()


@pytest.fixture
def get_session():
    return init_db(drop_all=True)


@pytest.fixture
def get_repo(get_session):
    return lambda: SqlAlchemyRepository(get_session())


@pytest.fixture
def server(get_session) -> ServerThread:
    test_app = init_app()
    server = ServerThread(test_app)
    server.start()

    yield server

    server.shutdown()


@pytest.fixture
def add_stock(get_repo):
    batches_added = set[Batch]()
    with get_repo() as repo:
        repo: SqlAlchemyRepository  # type: ignore

        def inner(lines: [tuple[str, str, int, str]]) -> None:
            for ref, sku, qty, eta in lines:
                eta = datetime.strptime(eta,
                                        '%Y-%m-%d').date() if eta else None
                batch = Batch(ref, sku, qty, eta)
                repo.add(batch)
                batches_added.add(batch)

        yield inner

        # Fixture 사용 이후 clean up 코드
        for batch in batches_added:
            lines = list(batch._allocations)
            batch._allocations.clear()
            for line in lines:
                repo.delete(line)
            repo.delete(batch)

        return inner
