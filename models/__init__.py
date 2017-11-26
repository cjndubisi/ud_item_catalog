#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from os import getenv

Base = declarative_base()

__all__ = [
    'Base',
    'Column',
    'Integer',
    'String',
    'ForeignKey',
    'DateTime',
    'Boolean',
    'func',
    'relationship']

from .user import User
from .category import Category
from .item import Item

# Setup
db_url = getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///catalog.db')
engine = create_engine(db_url)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base.metadata.create_all(bind=engine)