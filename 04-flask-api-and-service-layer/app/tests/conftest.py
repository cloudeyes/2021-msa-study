# pylint: disable=redefined-outer-name, protected-access
"""pytest 에서 사용될 전역 Fixture들을 정의합니다."""
from typing import Optional, Callable, Generator
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import pytest

from ..adapters.orm import start_mappers, SessionMaker
from ..adapters.repository import SqlAlchemyRepository, AbstractRepository
from ..domain.models import Batch

from ..apps.flask import init_app, init_db
from . import ServerThread

# types

_AbstractRepoMaker = Callable[[], AbstractRepository]
_AddStockLines = list[tuple[str, str, int, Optional[str]]]
_AddStockFunc = Callable[[_AddStockLines], None]


@pytest.fixture
def session() -> Generator[SessionMaker, None, None]:
    engine = create_engine('sqlite://',
                           connect_args={'check_same_thread': False},
                           poolclass=StaticPool)
    metadata = start_mappers(use_exist=True)
    metadata.create_all(engine)
    yield sessionmaker(engine)()


@pytest.fixture
def get_session() -> SessionMaker:
    return init_db(drop_all=True)


@pytest.fixture
def get_repo(get_session: SessionMaker) -> _AbstractRepoMaker:
    return lambda: SqlAlchemyRepository(get_session())


@pytest.fixture
# pylint: disable=unused-argument
def server(get_session: SessionMaker) -> Generator[ServerThread, None, None]:
    test_app = init_app()
    server = ServerThread(test_app)
    server.start()

    yield server

    server.shutdown()


@pytest.fixture
def add_stock(
    get_repo: _AbstractRepoMaker
) -> Generator[_AddStockFunc, None, _AddStockFunc]:
    batches_added = set[Batch]()
    with get_repo() as repo:
        repo: SqlAlchemyRepository  # type: ignore

        def inner(lines: _AddStockLines) -> None:
            for ref, sku, qty, eta in lines:
                eta_date = datetime.strptime(
                    eta, '%Y-%m-%d').date() if eta else None
                batch = Batch(ref, sku, qty, eta_date)
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
