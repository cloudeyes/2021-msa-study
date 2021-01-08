from typing import Callable, Any, cast

from flask import request, jsonify

from ..apps.flask import (route, FlaskResponse)
from ..domain import models
from ..config import get_repo


@route('/batches', methods=['GET'])
def batches() -> FlaskResponse:
    with get_repo() as repo:
        batches = repo.list()
        return jsonify(batches), 200


@route("/allocate", methods=['POST'])
def allocate_endpoint() -> FlaskResponse:
    with get_repo() as repo:
        batches = repo.list()
        line = models.OrderLine(
            request.json['orderid'],
            request.json['sku'],
            request.json['qty'],
        )
        batchref = models.allocate(line, batches)

    return jsonify({'batchref': batchref}), 201
