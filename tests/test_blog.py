import pytest
from flask import g

from flaskr.app import db
from flaskr.model import User, Post


def test_index(client, auth):
    response = client.get('/')
    assert b"Log in" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b"Log out" in response.data
    assert b"test title" in response.data
    # assert b"by test on 2018-01-01" in response.data
    assert b"test\nbody" in response.data
    # assert b"href=\"/1/update\"" in response.data


@pytest.mark.parametrize(
    'path',
    ('/create', '/1/update', '/1/delete')
)
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == '/auth/login'


def test_user_required(app, client, auth):
    with app.app_context():
        post = Post.query.filter(Post.id == 1).first()
        post.user_id = 2
        db.session.add(post)
        db.session.commit()

    auth.login()
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    assert b"href=\"/1/update\"" not in client.get('/').data


@pytest.mark.parametrize(
    'path',
    ('/2/update','/2/delete')
)
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title':'created', 'body': ''})

    with app.app_context():
        count = Post.query.count()
        assert count == 2

    
def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated','body': ''})
    
    with app.app_context():
        post = Post.query.filter(Post.id == 1).first()
        assert post.title == 'updated'


@pytest.mark.parametrize(
    'path',
    ('/create', '/1/update')
)
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b"Title is required." in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == '/'

    with app.app_context():
        post = Post.query.filter(Post.id == 1).first()
        assert post is None