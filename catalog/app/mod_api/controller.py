#!/usr/bin/python3

from app import app, db
from app.models import User, Item, Category

from flask import Blueprint, jsonify

mod_api = Blueprint('api', __name__)

# JSON APIs to view Catalogs Information #################################
@mod_api.route('/api/catalog/categories')
def all_categoriesJSON():
    '''Returns all categories'''
    categories = db.session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])

@mod_api.route('/api/catalog/items')
def all_itemsJSON():
    '''Returns all items with relationships included'''
    items = db.session.query(Item).all()
    return jsonify(categories=[i.serialize for i in items])

# Show catalog with recent items
@mod_api.route('/api/')
@mod_api.route('/api/catalog')
def catalogJSON():
    '''Returns undated catalog with categories and latest items'''
    latest_items = db.session.query(Item).all()
    categories = db.session.query(Category).all()

    return jsonify(latest_items=[i.serialize for i in latest_items],
                   categories=[i.serialize for i in categories])
