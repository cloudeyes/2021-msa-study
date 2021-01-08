from flask import Flask
import pytest

from ..apps.flask import create_app


@pytest.fixture(scope="session")
def flask_app() -> Flask:
    app = create_app()
    app.run()

    from ...adapters import orm, repository
    orm.start_mappers()

    return app
