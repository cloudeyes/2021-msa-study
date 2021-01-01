from __future__ import annotations
from typing import Callable, Generator
from contextlib import contextmanager
import io, sys, re, logging

from sqlalchemy import (MetaData, Table, Column, ForeignKey, Integer, String,
                        Date, create_engine)
from sqlalchemy.orm import mapper, relationship, sessionmaker
from sqlalchemy.engine import Engine

from app.models import Batch, OrderLine
from app import ScopedSession
metadata: MetaData = None


def start_mappers() -> MetaData:
    global metadata
    if metadata:
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
                show_log: bool = False) -> Engine:
    logger = logging.getLogger("sqlalchemy.engine.base.Engine")
    out = io.StringIO()
    logger.addHandler(logging.StreamHandler(out))

    engine = create_engine(url, echo=True)  # temporary memory db
    metadata.create_all(engine)

    if show_log:
        print(''.join(
            re.findall('CREATE TABLE.*?\n\n', out.getvalue(), re.DOTALL)))

    return engine


def sessionfactory(engine: Engine) -> Callable[..., ScopedSession]:
    SqliteSessionMaker = sessionmaker(engine, expire_on_commit=False)
    '''
    Argument 1 to "contextmanager" has incompatible type "Callable[..., ContextManager[Any]]";
    expected "Callable[..., Iterator[<nothing>]]"
    '''
    @contextmanager
    def get_session() -> Generator[ScopedSession, None, None]:
        '''`with session` 블록을 이용한 자동 리소스 반환을 구현합니다.'''
        session = SqliteSessionMaker()
        try:
            yield session
        finally:
            session.close()

    return get_session
