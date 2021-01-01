from typing import Callable, TypeVar, NewType, Any, Tuple, cast
from contextlib import AbstractContextManager

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models, orm, repository
from app.repository import SqlAlchemyRepository

flask_app = Flask(__name__)

FlaskResponse = Tuple[Any, int]
DecoratorType = Callable[..., Callable[[Callable[..., Any]], Callable[...,
                                                                      Any]]]
route: DecoratorType = cast(DecoratorType, flask_app.route)

metadata = orm.start_mappers()
engine = orm.init_engine(metadata, "sqlite://", show_log=True)
get_session = orm.sessionfactory(engine)


def get_repo() -> SqlAlchemyRepository:
    return SqlAlchemyRepository(get_session())


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