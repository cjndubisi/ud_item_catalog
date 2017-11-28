#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy

APPLICATION_NAME = "Item Catalog"

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# Register blueprint(s)
from app.mod_auth.controller import mod_auth as auth_module
from app.mod_api.controller import mod_api as api_module
from controller import mod_catalog as catalog_module
app.register_blueprint(auth_module)
app.register_blueprint(api_module)
app.register_blueprint(catalog_module)

# Connect to Database and create database session
db.create_all()