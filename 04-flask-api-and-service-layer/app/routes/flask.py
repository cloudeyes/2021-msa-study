"""Flask 엔드포인트 라우팅 모듈입니다."""
from __future__ import annotations
from flask import request, jsonify

from app.apps.flask import (route, get_repo, FlaskResponse)
from app.domain import models


@route("/allocate", methods=['POST'])
def allocate_endpoint() -> FlaskResponse:
    """``POST /allocate`` 엔트포인트 요청을 처리합니다."""
    with get_repo() as repo:
        batches = repo.list()
        line = models.OrderLine(
            request.json['orderid'],
            request.json['sku'],
            request.json['qty'],
        )
        batchref = models.allocate(line, batches)

    return jsonify({'batchref': batchref}), 201
