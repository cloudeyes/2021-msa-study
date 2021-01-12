"""ORM 구현."""

from __future__ import annotations

from typing import Callable, Generator, Optional, Union, Any
from contextlib import contextmanager, AbstractContextManager
import abc
import io
import re
import logging

from sqlalchemy import (MetaData, Table, Column, ForeignKey, Integer, String,
                        Date, create_engine)
from sqlalchemy.pool.base import Pool
from sqlalchemy.engine import Engine
from sqlalchemy.orm import (
    mapper,
    relationship,
    sessionmaker,
    clear_mappers as _clear_mappers,
)
from sqlalchemy.orm.session import Session

from ..domain.models import Batch, OrderLine

SessionMaker = Callable[[], Session]
ScopedSession = AbstractContextManager[Session]

metadata: MetaData = None


class AbstractSession(abc.ABC):
    """세션의 일반적인 작업(`commit`, `)."""
    @abc.abstractmethod
    def commit(self) -> None:
        """트랜잭션을 커밋합니다."""
        # TODO: 설명을 좀더 자세하게 적어주세요.
        raise NotImplementedError


def start_mappers(use_exist: bool = True) -> MetaData:
    """도메인 객체들을 SqlAlchemy ORM 매퍼에 등록합니다."""
    global metadata  # pylint: disable=global-statement,invalid-name
    if use_exist and metadata:
        return metadata

    metadata = MetaData()

    order_line = Table('order_line',
                       metadata,
                       Column('id',
                              Integer,
                              primary_key=True,
                              autoincrement=True),
                       Column('sku', String(255)),
                       Column('qty', Integer, nullable=False),
                       Column('orderid', String(255)),
                       extend_existing=True)

    allocation = Table('allocation',
                       metadata,
                       Column('orderline_id',
                              Integer,
                              ForeignKey('order_line.id'),
                              primary_key=True),
                       Column('batch_id',
                              Integer,
                              ForeignKey('batch.id'),
                              primary_key=True),
                       extend_existing=True)

    batch = Table('batch',
                  metadata,
                  Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('reference', String(255), unique=True),
                  Column('_purchased_quantity', Integer),
                  Column('sku', String(255)),
                  Column('eta', Date, nullable=True),
                  extend_existing=True)

    _batch_mapper = mapper(
        Batch,
        batch,
        properties={
            '_allocations':
            relationship(OrderLine,
                         secondary=allocation,
                         collection_class=set,
                         lazy='joined'),
        },
    )

    _order_line_mapper = mapper(OrderLine, order_line)

    return metadata


def clear_mappers() -> None:
    """ORM 매핑을 초기화 합니다."""
    _clear_mappers()


def init_engine(meta: MetaData,
                url: str,
                connect_args: Optional[dict[str, Any]] = None,
                poolclass: Optional[Pool] = None,
                show_log: Union[bool, dict[str, Any]] = False,
                drop_all: bool = False) -> Engine:
    """ORM Engine을 초기화 합니다.

    TODO: 상세 설명 추가.
    """
    logger = logging.getLogger("sqlalchemy.engine.base.Engine")
    out = io.StringIO()
    logger.addHandler(logging.StreamHandler(out))
    engine = create_engine(url,
                           connect_args=connect_args or {},
                           poolclass=poolclass,
                           echo=show_log)

    if drop_all:
        meta.drop_all(engine)

    meta.create_all(engine)

    if show_log:
        log_txt = out.getvalue()
        if show_log is True:
            print(''.join(
                re.findall('CREATE.*?\n\n', log_txt, re.DOTALL | re.I)))
        elif isinstance(show_log, dict):
            if show_log.get('all'):
                print(log_txt)

    return engine


def get_scoped_session(engine: Engine) -> Callable[[], ScopedSession]:
    """``with...`` 문으로 자동 리소스가 반환되는 세션을 리턴합니다.

    Example: ::

        with get_scoped_session() as db:
            batches = db.query(Batch).all()
            ...

    Args:
        engine: Engine.

    """
    get_session = sessionmaker(engine)

    @contextmanager
    def scoped_session() -> Generator[Session, None, None]:
        sess: Session = None
        try:
            yield (sess := get_session())  # pylint: disable=superfluous-parens
        finally:
            if sess:
                sess.close()

    return scoped_session
