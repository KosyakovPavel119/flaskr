# from __future__ import annotations
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from flask import Flask

# from flask import current_app
from flaskr.app import db

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    posts = relationship('Post', back_populates='user', order_by='Post.id')


class Post(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    title = Column(String(100), nullable=False)
    body = Column(String(2000))

    user = relationship('User', back_populates='posts')


# with current_app.app_context():
#     db.create_all()

# class SingletonMeta(type):
#     _instances = {}

#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]


# class DatabaseHandler(metaclass=SingletonMeta):
#     @property
#     def engine(self):
#         return self.__engine

#     @property
#     def db_session(self):
#         return self.__db_session

#     def __init__(self, app: Flask):
#         with app.app_context():
#             self.__engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
#             self.__db_session = scoped_session(
#                 sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
#             )
#         Base.query = self.__db_session.query_property()
#         Base.metadata.reflect(bind=self.__engine)
#         Base.metadata.create_all(bind=self.__engine)

#     def truncate_database(self):
#         import contextlib
#         with contextlib.closing(self.__engine.connect()) as transaction:
#             transaction.begin()
#             for table in reversed(Base.metadata.sorted_tables):
#                 transaction.execute(table.delete())
#             transaction.commit()
