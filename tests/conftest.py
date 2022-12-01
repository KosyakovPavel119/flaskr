from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flask import Flask

import os

import pytest
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    app = create_app('testing')
    db = SQLAlchemy()

    with app.app_context():
        db.init_app(app)
        for statement in _data_sql.split(';')[:-1]:
            db.session.execute(text(statement))
        db.session.commit()

    yield app


@pytest.fixture
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)

    
