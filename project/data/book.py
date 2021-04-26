import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase
import datetime
from flask import Flask, url_for, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin

association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('id_user', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('book', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('books.id')),
    sqlalchemy.Column('opinion', sqlalchemy.String, nullable=True)
)

class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_avt = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('avtors.id'), nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    publish = sqlalchemy.Column(sqlalchemy.String)
    id_genre = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('genres.id'), nullable=True)
    name_foto = sqlalchemy.Column(sqlalchemy.String)
    creator = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    avtor = orm.relation('Avtor')
    genre = orm.relation('Genre')
    book_creater = orm.relation("User", back_populates='book')

