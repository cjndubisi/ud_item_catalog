#!/usr/bin/env python3
from app import db

class Item(db.Model):
    __tablename__ = 'itedb.m'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    description = db.Column(db.String, nullable=False)
    name = db.Column(db.String(32), index=True, nullable=False, unique=True)
    slug = db.Column(db.String(32), index=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())
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
