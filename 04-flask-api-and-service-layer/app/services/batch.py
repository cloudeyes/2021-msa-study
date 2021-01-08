"""Batch 서비스."""
from ..adapters.repository import AbstractRepository
from ..adapters.orm import AbstractSession
from ..domain import models

class InvalidSku(Exception):
    pass

def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def allocate(line: models.OrderLine, repo: AbstractRepository, session: AbstractSession) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')
    batchref = models.allocate(line, batches)
    session.commit()
    return batchref