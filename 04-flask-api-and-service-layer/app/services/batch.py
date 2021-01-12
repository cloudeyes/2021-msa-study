"""Batch 서비스."""
from typing import Sequence, Protocol, Any

from ..adapters.repository import AbstractRepository
from ..adapters.orm import AbstractSession
from ..domain.models import Batch, OrderLine
from ..domain import models


class InvalidSku(Exception):
    ...


def is_valid_sku(sku: str, items: Sequence[Any]) -> bool:
    return sku in {it.sku for it in items}


def allocate(line: OrderLine, repo: AbstractRepository,
             session: AbstractSession) -> str:
    """Find an earliest batch and allocate an :class:`.OrderLine` to it."""
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')
    batchref = models.allocate(line, batches)
    session.commit()
    return batchref
