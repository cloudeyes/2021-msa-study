from __future__ import annotations
from typing import Optional, cast
from datetime import date

import pytest

from app.services.uow import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from app.domain.models import Batch, OrderLine
from app.adapters.orm import (start_mappers, init_engine, sessionmaker,
                              Session)
from app import config


def insert_batch(session: Session, ref: str, sku: str, qty: int,
                 eta: Optional[date]) -> None:
    session.execute(
        'INSERT INTO batch (reference, sku, _purchased_quantity, eta)'
        ' VALUES (:ref, :sku, :qty, :eta)',
        dict(ref=ref, sku=sku, qty=qty, eta=eta))


def get_allocated_batch_ref(session: Session, orderid: str, sku: str) -> str:
    [[orderlineid]] = session.execute(
        'SELECT id FROM order_line WHERE orderid=:orderid AND sku=:sku',
        dict(orderid=orderid, sku=sku))
    [[batchref]] = session.execute(
        'SELECT b.reference FROM allocation JOIN batch AS b ON batch_id = b.id'
        ' WHERE orderline_id=:orderlineid', dict(orderlineid=orderlineid))
    return batchref


def delete_batch_and_allocation(session: Session, ref: str) -> None:
    session.execute("""
    DELETE FROM allocation WHERE batch_id in (
            SELECT id FROM batch WHERE reference='batch1'
    )""")
    session.execute("DELETE FROM batch WHERE reference='batch1'")
    session.commit()


def test_uow_with_statement():
    class DummyUoW(AbstractUnitOfWork):
        def commit(self):
            print('call commit()!')

        def rollback(self):
            print('call rollback()!')

    with DummyUoW() as uow:
        pass


def test_uow_with_real_session(get_session):

    with SqlAlchemyUnitOfWork(get_session) as uow:
        uow.batches.clear()
        uow.batches.add(Batch('b1', 'TEST', 10))
        uow.commit()

    with SqlAlchemyUnitOfWork(get_session) as uow:
        [batch, *_] = uow.batches.list()
        assert 'b1' == batch.reference
        uow.batches.delete(batch)
        uow.commit()


def test_uow_can_retrieve_a_batch_and_allocate_to_it(get_session):
    session = get_session()
    insert_batch(session, 'batch1', 'HIPSTER-WORKBENCH', 100, None)
    session.commit()
    uow = SqlAlchemyUnitOfWork(get_session)
    with uow:
        batch = cast(Batch, uow.batches.get(reference='batch1'))
        line = OrderLine('o1', 'HIPSTER-WORKBENCH', 10)
        batch.allocate(line)
        uow.commit()

    batchref = get_allocated_batch_ref(session, 'o1', 'HIPSTER-WORKBENCH')
    assert batchref == 'batch1'

    delete_batch_and_allocation(session, 'batch1')


def test_rolls_back_uncommitted_work_by_default(get_session):
    uow = SqlAlchemyUnitOfWork(get_session)
    with uow:
        insert_batch(uow.session, 'batch1', 'MEDIUM-PLINTH', 100, None)

    # Commit 을 안한 경우 실제 DB에 데이터가 반영되지 않습니다.
    new_session = get_session()
    rows = list(new_session.execute("SELECT * FROM batch"))
    assert [] == rows, f'{rows}'

    delete_batch_and_allocation(new_session, 'batch1')


def test_rolls_back_committed(get_session):
    uow = SqlAlchemyUnitOfWork(get_session)
    with uow:
        insert_batch(uow.session, 'batch1', 'MEDIUM-PLINTH', 100, None)
        uow.session.commit()

    # commit 을 하면 DB 상태가 변경되어야 합니다.
    new_session = get_session()
    [[ref]] = list(new_session.execute('SELECT reference FROM batch'))
    assert 'batch1' == ref, f'{ref}'
    new_session.execute('DELETE FROM batch')
    new_session.commit()


def test_rolls_back_on_error(get_session):
    class MyException(Exception):
        pass

    uow = SqlAlchemyUnitOfWork(get_session)
    with pytest.raises(MyException):
        with uow:
            insert_batch(uow.session, 'batch1', 'LARGE-FORK', 100, None)
            raise MyException()
            uow.commit()

    new_session = get_session()
    rows = list(new_session.execute('SELECT * FROM "batch"'))
    assert rows == []

    delete_batch_and_allocation(new_session, 'batch1')