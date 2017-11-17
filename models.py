#!/usr/bin/env python3

import os
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
db_url = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///catalog.db')

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    picture = Column(String)
    email = Column(String(250), nullable=False)
    authenticated = Column(Boolean, default=False)
    date_created  = Column(DateTime,  default=func.current_timestamp())
    date_modified = Column(DateTime,  default=func.current_timestamp(),
                                       onupdate=func.current_timestamp())
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    @property
    def serialize(self):
        '''Return object data in easily serializeable format'''
        return {
            'id': self.id,
            'username': self.username,
            'picture': self.picture,
            'email': self.email
        }

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    description = Column(String(80), nullable=False)
    name = Column(String(32), index=True, nullable=False, unique=True)
    slug = Column(String(32), index=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    date_created  = Column(DateTime,  default=func.current_timestamp())
    date_modified = Column(DateTime,  default=func.current_timestamp(),
                                       onupdate=func.current_timestamp())
    @property
    def serialize(self):
        '''Return object data in easily serializeable format'''
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'category_name': self.category.name,
            'category_id': self.category_id
        }

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)
    items = relationship(Item, backref='category', lazy='dynamic')
    date_created  = Column(DateTime,  default=func.current_timestamp())
    date_modified = Column(DateTime,  default=func.current_timestamp(),
                                       onupdate=func.current_timestamp())
    @property
    def serialize(self):
        '''Return object data in easily serializeable format'''
        return {
            'id': self.id,
            'name': self.name,
            'items': [i.serialize for i in self.items]
        }

engine = create_engine(db_url)

Base.metadata.create_all(engine)
