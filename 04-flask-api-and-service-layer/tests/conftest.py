# pylint: disable=redefined-outer-name, protected-access
"""pytest 에서 사용될 전역 Fixture들을 정의합니다."""
from __future__ import annotations
from typing import Optional, Callable, Generator, List, Tuple
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
import pytest

from app.adapters.orm import start_mappers, SessionMaker
from app.adapters.repository import SqlAlchemyRepository, AbstractRepository
from app.domain.models import Batch

from app.apps.flask import init_app, init_db
from . import ServerThread

# types

AbstractRepoMaker = Callable[[], AbstractRepository]
AddStockLines = List[Tuple[str, str, int, Optional[str]]]
""":meth:`add_stock` 함수의 인자 타입."""
AddStockFunc = Callable[[AddStockLines], None]
""":meth:`add_stock` 함수 타입."""


@pytest.fixture
def session() -> Session:
    """테스트에 사용될 새로운 :class:`.Session` 픽스처를 리턴합니다.

    :rtype: :class:`~sqlalchemy.orm.Session`
    """
    engine = create_engine('sqlite://',
                           connect_args={'check_same_thread': False},
                           poolclass=StaticPool)
    metadata = start_mappers(use_exist=True)
    metadata.create_all(engine)
    return sessionmaker(engine)()


@pytest.fixture
def get_session() -> SessionMaker:
    """:class:`.Session` 팩토리 메소드(:class:`~app.adapters.orm.SessionMaker`)
    를 리턴하는 픽스쳐 입니다.

    호출시마다 :meth:`~app.apps.flask.init_db` 을 호출(`drop_all=True`)하여
    모든 DB 엔티티를 매번 재생성합니다.

    :rtype: :class:`~app.adapters.orm.SessionMaker`
    """
    return init_db(drop_all=True)


@pytest.fixture
def get_repo(get_session: SessionMaker) -> AbstractRepoMaker:
    """:class:`SqlAlchemyRepository` 팩토리 함수를 리턴하는 픽스쳐입니다."""
    return lambda: SqlAlchemyRepository(get_session())


@pytest.fixture
# pylint: disable=unused-argument
def server(get_session: SessionMaker) -> Generator[ServerThread, None, None]:
    # noqa
    """:class:`ServerThread` 로 구현된 재시작 가능한 멀티스레드 Flask 서버를
    리턴하는 픽스쳐입니다.

    픽스쳐 사용후에는 `shutdown`을 통해 서버를 종료합니다.
    """
    test_app = init_app()
    server = ServerThread(test_app)
    server.start()

    yield server

    server.shutdown()


@pytest.fixture
def add_stock(
    get_repo: AbstractRepoMaker
) -> Generator[AddStockFunc, None, AddStockFunc]:
    """:meth:`get_repo` 픽스쳐를 이용해 레포지터리에 배치를 추가하는 `add_stock`
    함수를 리턴하는 픽스쳐입니다.

    제너레이터를 이용해 리턴하며 픽스쳐 사용 이후에는 레포지터리에서 입력된 배치를
    Clean up 합니다.

    :rtype: :class:`AddStockFunc`
    """

    batches_added = set[Batch]()
    with get_repo() as repo:
        repo: SqlAlchemyRepository  # type: ignore

        def inner(lines: AddStockLines) -> None:
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
