"""Batch 서비스."""
from typing import Sequence, Optional
from datetime import date

from app.adapters.repository import AbstractRepository
from app.adapters.orm import AbstractSession
from app.domain.models import Batch
from app.domain import models


class InvalidSku(Exception):
    """배치의 SKU와 다른 SKU를 할당하려 할 때 발생하는 예외입니다."""
    ...


def is_valid_sku(sku: str, batches: Sequence[Batch]) -> bool:
    """`batches` 에서 `sku` 와 일치하는 품목이 하나라도 있으며 참을 리턴합니다."""
    return sku in {it.sku for it in batches}


def add(
    ref: str,
    sku: str,
    qty: int,
    eta: Optional[date],
    repo: AbstractRepository,
    session: AbstractSession,
) -> None:
    """배치를 추가합니다."""
    repo.add(models.Batch(ref, sku, qty, eta))
    session.commit()


def allocate(orderid: str, sku: str, qty: int, repo: AbstractRepository,
             session: AbstractSession) -> str:
    """ETA가 가장 빠른 배치를 찾아 :class:`.OrderLine` 을 할당합니다.

    Raises:
        InvalidSku: ``SKU`` 가 잘못 지정되어 할당하는한 배치가 없을 경우 발생하는 예외
    """
    line = models.OrderLine(orderid, sku, qty)
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')
    batchref = models.allocate(line, batches)
    session.commit()
    return batchref
