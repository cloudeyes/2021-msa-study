from __future__ import annotations
from typing import Optional, NewType
from dataclasses import dataclass
from datetime import date

Quantity = NewType("Quantity", int)
Sku = NewType("Sku", str)
Reference = NewType("Reference", str)
OrderReference = NewType("OrderReference", str)
ProductReference = NewType("ProductReference", str)

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
        self, ref: Reference, sku: Sku, qty: int, eta: Optional[date]
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
    

def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
        batch.allocate(line)
        return batch.reference            
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')