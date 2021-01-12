"""도메인 모델."""

from __future__ import annotations
from typing import Optional, NewType
from dataclasses import dataclass
from datetime import date


class OutOfStock(Exception):
    """:class:`Batch` 에 할당할 재고(Stock)가 없을 때 발생하는 예외입니다."""
    pass


@dataclass
class Order:
    """고객이 발주하는 주문(Order) 모델입니다.."""
    id: str


@dataclass(unsafe_hash=True)
class OrderLine:
    """주문(:class:`Order`)에 대한 여러 주문선을 나타냅니다.

    :meth:`Batch.allocate` 를 이용해 재고 :class:`Batch` 소스와 연결합니다.
    """

    orderid: str
    """:attr:`Order.id` 를 가리키는 레퍼런스 id입니다."""

    sku: str
    """|SKU|."""

    qty: int


class Batch:
    """재고 단위(SKU)별로 예정 시간(`eta`)까지 지정 수량(`qta`)으로 한번에 구매될 상품입니다."""
    def __init__(self,
                 ref: str,
                 sku: str,
                 qty: int,
                 eta: Optional[date] = None):
        """`Batch` 의 기본 생성자."""
        self.reference = ref

        self.sku = sku
        """|SKU|."""

        self.eta = eta
        """|ETA|."""

        self._purchased_quantity = qty
        self._allocations = set[OrderLine]()

    def allocate(self, line: OrderLine) -> None:
        """지정된 :class:`OrderLine` 을 현재 :class:`Batch` 에 추가합니다.

        Args:
            line: 배치에 추가할 OrderLine.
        """
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __lt__(self, other: Batch) -> bool:
        if self.eta is None:
            return True
        if other.eta is None:
            return False
        return self.eta < other.eta


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')
