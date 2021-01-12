from __future__ import annotations

from flask import request, jsonify

from ..apps.flask import (route, get_repo, FlaskResponse)
from ..domain import models


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
