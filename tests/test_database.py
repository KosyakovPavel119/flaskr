from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flask import Flask

from flaskr.app import db
from flaskr.model import User, Post


def test_init(client, app: Flask):
    with app.app_context():
        user = User.query.first()
        assert user is not None
        post = Post.query.first()
        assert post is not None