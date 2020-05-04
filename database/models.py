import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    print(database_path)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Movies with attributes title and release date
'''
class Movie(db.Model):
    __tablename__ = 'movie'
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80), unique=True)
    relese_date = db.Column(db.DateTime, nullable=False)
    actors = db.relationship('Actor', backref="movie", lazy=True)

    def __init__(self, title, relese_date):
        self.title = title
        self.relese_date = relese_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
 
'''
Actors with attributes name, age and gender
'''
class Actor(db.Model):
    __tablename__ = 'Actor'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movie.id'), nullable=True)
    name = Column(String(80), unique=True)
    age = Column(Integer().with_variant(Integer, "sqlite"))
    gender = Column(String(80))

    def __init__(self, name, age, gender, movie_id=None):
        self.name = artist_id
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
