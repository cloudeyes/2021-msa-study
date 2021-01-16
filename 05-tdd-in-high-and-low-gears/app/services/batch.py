"""Batch 서비스."""
from typing import Sequence

from app.adapters.repository import AbstractRepository
from app.adapters.orm import AbstractSession
from app.domain.models import OrderLine, Batch
from app.domain import models


class InvalidSku(Exception):
    """배치의 SKU와 다른 SKU를 할당하려 할 때 발생하는 예외입니다."""
    ...


def is_valid_sku(sku: str, batches: Sequence[Batch]) -> bool:
    """`batches` 에서 `sku` 와 일치하는 품목이 하나라도 있으며 참을 리턴합니다."""
    return sku in {it.sku for it in batches}


def allocate(line: OrderLine, repo: AbstractRepository,
             session: AbstractSession) -> str:
    """Find an earliest batch and allocate an :class:`.OrderLine` to it."""
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')
    batchref = models.allocate(line, batches)
    session.commit()
    return batchref
