#!/usr/bin/env python3
from . import *

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    description = Column(String, nullable=False)
    name = Column(String(32), index=True, nullable=False, unique=True)
    slug = Column(String(32), index=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    date_created = Column(DateTime,  default=func.current_timestamp())
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
