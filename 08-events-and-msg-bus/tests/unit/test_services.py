"""서비스 레이어 단위 테스트.

Low Gear(고속 기어) 테스트입니다.
"""
from typing import Sequence, Optional, Union, cast

import pytest

from app.adapters import repository
from app.adapters.orm import AbstractSession

from app.domain.models import Batch, OrderLine
from app.services.uow import AbstractUnitOfWork
from app import services


class FakeRepository(repository.AbstractRepository):
    def __init__(self, batches: Sequence[Batch]):
        self._batches = set(batches)

    def add(self, batch: Batch) -> None:
        self._batches.add(batch)

    def delete(self, batch: Union[Batch, OrderLine]) -> None:
        self._batches.remove(cast(Batch, batch))

    def get(self, reference: str) -> Optional[Batch]:
        return next(b for b in self._batches if b.reference == reference)

    def list(self) -> list[Batch]:
        return list(self._batches)

    def close(self) -> None:
        pass

    def clear(self) -> None:
        self._bacthes = set[Batch]()


class FakeSession(AbstractSession):
    committed = False

    def commit(self) -> None:
        self.committed = True


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self, batches: Optional[list[Batch]] = None) -> None:
        if not batches:
            self.batches = FakeRepository([])
        else:
            self.batches = FakeRepository(batches)
        self.committed = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        pass


def test_add_batch():
    uow = FakeUnitOfWork()
    services.batch.add("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)
    assert uow.batches.get("b1") is not None
    assert uow.committed


def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    services.batch.add("batch1", "COMPLICATED-LAMP", 100, None, uow)
    result = services.batch.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert "batch1", result


def test_returns_allocation() -> None:
    batch = Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
    uow = FakeUnitOfWork([batch])
    result = services.batch.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "b1"


def test_error_for_invalid_sku() -> None:
    batch = Batch("b1", "AREALSKU", 100, eta=None)
    uow = FakeUnitOfWork([batch])
    with pytest.raises(services.batch.InvalidSku,
                       match="Invalid sku NONEXISTENTSKU"):
        services.batch.allocate("o1", "NONEXISTENTSKU", 10, uow)


def test_commits() -> None:
    batch = Batch('b1', 'OMINOUS-MIRROR', 100, eta=None)
    uow = FakeUnitOfWork([batch])
    services.batch.allocate('o1', 'OMINOUS-MIRROR', 10, uow)
    assert uow.committed is True


def test_allocate_returns_allocation() -> None:
    uow = FakeUnitOfWork()
    services.batch.add("batch1", "COMPLICATED-LAMP", 100, None, uow)
    result = services.batch.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert "batch1" == result


def test_allocate_errors_for_invalid_sku() -> None:
    uow = FakeUnitOfWork()
    services.batch.add("b1", "AREALSKU", 100, None, uow)
    with pytest.raises(services.batch.InvalidSku,
                       match="Invalid sku NONEXISTENTSKU"):
        services.batch.allocate("o1", "NONEXISTENTSKU", 10, uow)
