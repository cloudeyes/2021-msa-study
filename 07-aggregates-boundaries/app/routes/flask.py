"""Flask 엔드포인트 라우팅 모듈입니다."""
from __future__ import annotations
from datetime import datetime

from flask import request, jsonify

from app.apps.flask import route, FlaskResponse
from app.domain import models
from app.services.uow import SqlAlchemyUnitOfWork
from app import services


@route("/batches", methods=['POST'])
def add_batch() -> FlaskResponse:
    """``POST /batches`` 요청을 처리하여 새로운 배치를 저장소에 추가합니다."""
    with SqlAlchemyUnitOfWork() as uow:
        eta = request.json['eta']
        if eta:
            eta = datetime.fromisoformat(eta).date()
        services.batch.add(request.json['ref'], request.json['sku'],
                           request.json['qty'], eta, uow)
    return 'OK', 201


@route("/batches/allocate", methods=['POST'])
def allocate_batch() -> FlaskResponse:
    """``POST /allocate`` 엔트포인트 요청을 처리합니다."""
    with SqlAlchemyUnitOfWork() as uow:
        batches = uow.batches.list()
        line = models.OrderLine(
            request.json['orderid'],
            request.json['sku'],
            request.json['qty'],
        )
        batchref = models.allocate(line, batches)
        uow.commit()

    return jsonify({'batchref': batchref}), 201
