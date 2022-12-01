from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.app import db
from flaskr.auth import login_required
from flaskr.model import Post

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc()).all()
    
    return render_template('blog/index.html.j2', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(g.user.id, title, body)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html.j2')


def get_post(id, check_author=True) -> Post:
    post = Post.query.filter(Post.id == id).first()

    if post is None:
        abort(404, f"Post id {id} does not exist.")

    if check_author and post.user == g.user:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET','POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/update.html.j2', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    post.delete()
    db.session.commit()
    return redirect(url_for('blog.index'))
