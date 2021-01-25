"""Batch 서비스."""
from typing import Sequence, Optional, cast
from datetime import date

from app.domain.models import Batch, OrderLine
from app.domain import models

from app.services.uow import AbstractUnitOfWork


class InvalidSku(Exception):
    """배치의 SKU와 다른 SKU를 할당하려 할 때 발생하는 예외입니다."""
    ...


class ReferenceNotFound(Exception):
    """배치 레퍼런스가 존재하지 않을 때 발생하는 예외입니ㅏ.."""
    ...


def is_valid_sku(sku: str, batches: Sequence[Batch]) -> bool:
    """`batches` 에서 `sku` 와 일치하는 품목이 하나라도 있으며 참을 리턴합니다."""
    return sku in {it.sku for it in batches}


def add(ref: str, sku: str, qty: int, eta: Optional[date],
        uow: AbstractUnitOfWork) -> None:
    """UOW를 이용해 배치를 추가합니다."""
    with uow:
        uow.batches.add(Batch(ref, sku, qty, eta))
        uow.commit()


def allocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork) -> str:
    """ETA가 가장 빠른 배치를 찾아 :class:`.OrderLine` 을 할당합니다.

    Raises:
        InvalidSku: ``SKU`` 가 잘못 지정되어 할당하는한 배치가 없을 경우 발생하는 예외
    """
    line = OrderLine(orderid, sku, qty)
    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = models.allocate(line, batches)
        uow.commit()
        return batchref


def reallocate(line: OrderLine, uow: AbstractUnitOfWork) -> None:
    """기존 Sku의 주문선을 할당 해재 후 새로운 `line`을 할당합니다.

    재할당 서비스 함수의 경우, 작업중 예외가 발생하면 UoW의 동작 방식에 의해 이전 상태로 자동 롤백됩니다.
    모든 유효성 검사와 세부 작업이 다 성공할 경우에만 명시적으로 호출된 commit 함수에 의해 저장소 내용이 변경됩니다.
    """
    with uow:
        batch = uow.batches.get(sku=line.sku)
        if batch is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batch.deallocate(line)
        batch.allocate(line)
        uow.commit()


def change_batch_quantity(batchref: str, new_qty: int,
                          uow: AbstractUnitOfWork) -> None:
    """배치에 할당된 주문선을 수량만큼 해제합니다."""
    with uow:
        batch = cast(Batch, uow.batches.get(reference=batchref))
        if not batch:
            raise ReferenceNotFound()
        batch.change_purchased_quantity(new_qty)
        while batch.available_quantity < 0:
            batch.deallocate_one()
        uow.commit()
