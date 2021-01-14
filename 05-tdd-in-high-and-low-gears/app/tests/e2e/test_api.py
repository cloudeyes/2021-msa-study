"""API 테스트."""
from __future__ import annotations
from typing import Callable, Optional
import uuid

import pytest
import requests
from ...config import get_api_url


def random_suffix() -> str:
    return uuid.uuid4().hex[:6]


def random_sku(name: str = '') -> str:
    return f'sku-{name}-{random_suffix()}'


def random_batchref(num: int = 1) -> str:
    return f'batch-{num}-{random_suffix()}'


def random_orderid(name: str = '') -> str:
    return f'order-{name}-{random_suffix()}'


AddStockFunc = Callable[[list[tuple[str, str, int, Optional[str]]]], None]


@pytest.mark.usefixtures('server')
def test_api_returns_allocation(add_stock: AddStockFunc) -> None:
    sku, othersku = random_sku(), random_sku('other')
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    add_stock([
        (laterbatch, sku, 100, '2021-01-02'),
        (earlybatch, sku, 100, '2021-01-01'),
        (otherbatch, othersku, 100, None),
    ])
    data = {'orderid': random_orderid(), 'sku': sku, 'qty': 3}

    r = requests.post(f'{get_api_url()}/allocate', json=data)

    assert r.status_code == 201
    assert r.json()['batchref'] == earlybatch
