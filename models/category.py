#!/usr/bin/env python3

from . import *
from .item import Item

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
