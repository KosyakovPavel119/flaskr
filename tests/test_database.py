from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flask import Flask

from flask import g, session
from flaskr.model import User, Post


def test_init(client, app: Flask):
    with app.app_context():
        user = g.db.db_session.query(User).first()
        assert user is not None