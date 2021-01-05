from __future__ import annotations
"""API 테스트."""
import uuid

import pytest


@pytest.fixture
def add_stock() -> None:
    def inner(stocks: list[tuple[str, str, int, str]]):
        pass

    return inner


def random_sku(name: Optional[str] = None) -> str:
    """`uuid.uuid4` 로 생성된 Unique ID로 임의의 SKU 문자열을 리턴합니다."""
    if name:
        return name
    return str(uuid.uuid4())


def random_batchref(id: int):
    pass


def test_api_returns_allocation(add_stock) -> None:
    sku, othersku = random_sku(), random_sku('other')
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    add_stock([
        (laterbatch, sku, 100, '2011-01-02'),
        (earlybatch, sku, 100, '2011-01-01'),
        (otherbatch, othersku, 100, None),
    ])
    data = {'orderid': random_orderid(), 'sku': sku, 'qty': 3}
    url = config.get_api_url()
    r = requests.post(f'{url}/allocate', json=data)
    assert r.status_code == 201
    assert r.json()['batchref'] == earlybatch