#!/usr/bin/env python3
import os, sys
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user

APPLICATION_NAME = "Item Catalog"

app = Flask(__name__)
app.config.from_object('app.config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "showLogin"

db = SQLAlchemy(app)

# Register blueprint(s)
from app.auth.controller import auth, getUserInfo
from app.api.controller import api
from app.controller import mod_catalog as catalog

app.register_blueprint(auth)
app.register_blueprint(api)
app.register_blueprint(catalog)

# Connect to Database and create database session
db.create_all()

# flask_login: callback to reload the user object       
@login_manager.user_loader
def load_user(userid):
    try: 
        return getUserInfo(userid)
    except:
        return None

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)