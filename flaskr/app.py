from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flaskr.config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    import flaskr.model
    with app.app_context():
        db.reflect()
        db.create_all()
        g.db = db

    @app.route('/hello')
    def hello() -> None:
        return "Hello, World!"

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app