import atexit
import datetime
import os

import sqlalchemy as db
from sqlalchemy import DateTime, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "12345")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "adv_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")


PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class User(Base):
    """Пользователи"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(50), unique=True)


    def __str__(self):
        return f'<Users {self.name}>'

    @property
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Advertisement(Base):
    """Объявление."""
    __tablename__ = 'Advertisements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(24))
    description = db.Column(db.String(64))
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    user = relationship(User, backref='Advertisements')

    @property
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'creator': self.creator,
            'date': self.created_at.isoformat()
        }


Base.metadata.create_all(bind=engine)
