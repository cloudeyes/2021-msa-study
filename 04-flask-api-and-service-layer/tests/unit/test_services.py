"""서비스 레이어 단위 테스트.

Low Gear(고속 기어) 테스트입니다.
"""
from typing import Sequence, Optional, Union, cast

import pytest

from app.adapters import repository
from app.adapters.orm import AbstractSession

from app.domain.models import Batch, OrderLine
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


def test_returns_allocation() -> None:
    line = OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch = Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
    repo = FakeRepository([batch])

    result = services.batch.allocate(line, repo, FakeSession())
    assert result == "b1"


def test_error_for_invalid_sku() -> None:
    line = OrderLine("o1", "NONEXISTENTSKU", 10)
    batch = Batch("b1", "AREALSKU", 100, eta=None)
    repo = FakeRepository([batch])

    with pytest.raises(services.batch.InvalidSku,
                       match="Invalid sku NONEXISTENTSKU"):
        services.batch.allocate(line, repo, FakeSession())


def test_commits() -> None:
    line = OrderLine('o1', 'OMINOUS-MIRROR', 10)
    batch = Batch('b1', 'OMINOUS-MIRROR', 100, eta=None)
    repo = FakeRepository([batch])
    session = FakeSession()

    services.batch.allocate(line, repo, session)
    assert session.committed is True