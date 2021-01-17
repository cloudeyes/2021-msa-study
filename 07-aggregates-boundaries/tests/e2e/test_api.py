"""API 테스트."""
from __future__ import annotations
from typing import Callable, Optional
from datetime import date
import uuid

import pytest
import requests

from app import config


def random_suffix() -> str:
    return uuid.uuid4().hex[:6]


def random_sku(name: str = '') -> str:
    return f'sku-{name}-{random_suffix()}'


def random_batchref(num: int = 1) -> str:
    return f'batch-{num}-{random_suffix()}'


def random_orderid(name: str = '') -> str:
    return f'order-{name}-{random_suffix()}'


AddStockFunc = Callable[[list[tuple[str, str, int, Optional[str]]]], None]


def post_to_add_batch(ref: str, sku: str, qty: int,
                      eta: Optional[str]) -> None:
    """서비스 엔드포인트 `POST /batches` 를 통해 배치를 추가합니다."""
    url = config.get_api_url()
    r = requests.post(f'{url}/batches',
                      json={
                          'ref': ref,
                          'sku': sku,
                          'qty': qty,
                          'eta': eta
                      })
    assert r.status_code == 201


@pytest.mark.usefixtures('server')
def test_happy_path_returns_201_and_allocated_batch() -> None:
    sku, othersku = random_sku(), random_sku('other')
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    post_to_add_batch(laterbatch, sku, 100, '2021-01-02')
    post_to_add_batch(earlybatch, sku, 100, '2021-01-01')
    post_to_add_batch(otherbatch, othersku, 100, None)
    data = {'orderid': random_orderid(), 'sku': sku, 'qty': 3}
    url = config.get_api_url()
    r = requests.post(f'{url}/batches/allocate', json=data)
    assert r.status_code == 201
    assert r.json()['batchref'] == earlybatch
