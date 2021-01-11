"""ORM 구현."""

from __future__ import annotations

from typing import Callable, Generator, Optional, Sequence, Union, cast
from contextlib import contextmanager, AbstractContextManager
import abc, io, sys, re, logging

from sqlalchemy import (MetaData, Table, Column, ForeignKey, Integer, String,
                        Date, engine, create_engine)
from sqlalchemy.orm import mapper, relationship, sessionmaker, clear_mappers
from sqlalchemy.orm.session import Session

from ..adapters.repository import AbstractRepository
from ..domain.models import Batch, OrderLine

ScopedSession = AbstractContextManager[Session]

metadata: MetaData = None


class AbstractSession(abc.ABC):
    """세션의 일반적인 작업(`commit`, `)."""
    @abc.abstractmethod
    def commit() -> None:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, db: Session):
        self.db = db

    def close(self) -> None:
        self.db.close()

    def add(self, batch: Batch) -> None:
        self.db.add(batch)
        self.db.commit()

    def get(self, reference: str) -> Optional[Batch]:
        return cast(
            Optional[Batch],
            self.db.query(Batch).filter_by(reference=reference).first())

    def delete(self, item: Union[Batch, OrderLine]) -> None:
        self.db.delete(item)
        self.db.commit()

    def list(self) -> list[Batch]:
        return cast(list[Batch], self.db.query(Batch).all())

    def clear(self) -> None:
        self.db.execute('DELETE FROM allocation')
        self.db.execute('DELETE FROM batch')
        self.db.execute('DELETE FROM order_line')
        self.db.commit()


def start_mappers(use_exist=True) -> MetaData:
    global metadata
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


def init_engine(metadata: MetaData,
                url: str,
                connect_args: dict[str, Any] = None,
                poolclass=None,
                show_log: Union[bool, dict] = False,
                drop_all=False) -> engine.Engine:

    logger = logging.getLogger("sqlalchemy.engine.base.Engine")
    out = io.StringIO()
    logger.addHandler(logging.StreamHandler(out))
    engine = create_engine(url,
                           connect_args=connect_args or {},
                           poolclass=poolclass,
                           echo=True)

    drop_all and metadata.drop_all(engine)
    metadata.create_all(engine)

    if show_log:
        log_txt = out.getvalue()
        if show_log is True:
            print(''.join(
                re.findall('CREATE.*?\n\n', log_txt, re.DOTALL | re.I)))
        elif isinstance(show_log, dict):
            if show_log.get('all'):
                print(log_txt)

    return engine


def get_scoped_session(engine) -> ScopedSession:
    get_session = sessionmaker(engine)

    @contextmanager
    def scoped_session():
        session = None
        try:
            yield (session := get_session())
        finally:
            session and session.close()

    return scoped_session


def get_scoped_repo(engine):
    get_session = sessionmaker(engine)

    def get_repo() -> SqlAlchemyRepository:
        return lambda: SqlAlchemyRepository(get_session())

    return get_repo