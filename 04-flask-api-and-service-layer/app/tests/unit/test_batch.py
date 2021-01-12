# noqa
"""Batch 도메인 모델 테스트."""
from datetime import date
from ...domain.models import Batch, OrderLine

today = date.today()


def test_batch_equality() -> None:
    batch1 = Batch('batch-001', 'SIMPLE-TABLE', 10, eta=today)
    batch2 = Batch('batch-001', 'SIMPLE-CHAIR', 5, eta=today)

    assert batch1 == batch2


def test_allocating_to_a_batch_reduces_the_available_quantity() -> None:
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=today)
    line = OrderLine('order-ref', "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def make_batch_and_line(sku: str, batch_qty: int,
                        line_qty: int) -> tuple[Batch, OrderLine]:
    return (Batch("batch-001", sku, batch_qty,
                  eta=today), OrderLine("order-123", sku, line_qty))


def test_can_allocate_if_available_greater_than_required() -> None:
    large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_smaller_than_required() -> None:
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_available_equal_to_required() -> None:
    batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match() -> None:
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
    assert batch.can_allocate(different_sku_line) is False


def test_allocation_is_idempotent() -> None:
    batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18


def test_deallocate() -> None:
    batch, line = make_batch_and_line("EXPENSIVE-FOOTSTOOL", 20, 2)
    batch.allocate(line)
    batch.deallocate(line)
    assert batch.available_quantity == 20


def test_can_only_deallocate_allocated_lines() -> None:
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20