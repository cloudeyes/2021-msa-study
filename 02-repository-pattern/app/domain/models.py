from __future__ import annotations
from typing import Optional, NewType
from dataclasses import dataclass
from datetime import date

class OutOfStock(Exception):
    pass

@dataclass
class Order:
    orderid: str


@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

        
class Batch:
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date]=None
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set[OrderLine]()
    
    def allocate(self, line: OrderLine) -> None:
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
