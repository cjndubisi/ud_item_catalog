#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from flask import session as login_session, make_response
from sqlalchemy import create_engine, asc, exc
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item
from datetime import datetime
from werkzeug.routing import RequestRedirect

import json, random, string
import requests
import functools
import httplib2
import redis

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"



# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "showLogin"

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/logout')
def logout():
    try:
        user = getUserInfo(login_session['user_id'])
        login_session.clear()
        user.authenticated = False
        session.add(user)
        session.commit()
        logout_user()
    except: 
        return redirect(url_for('showCatalog'))

    return redirect(url_for('showCatalog'))

@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists  create on
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session).id

    login_session['user_id'] = user_id

    user = getUserInfo(user_id)
    user.authenticated = True
    # add new user to db
    session.add(user)
    session.commit()

    # login user with flask_login
    login_user(user)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    return output

# Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# flask_login: callback to reload the user object       
@login_manager.user_loader
def load_user(userid):
    try: 
        return getUserInfo(userid)
    except:
        return None

# Create #################################
@app.route('/catalog/items/new', methods=['GET', 'POST'])
@login_required
def newItem():

    user_id = login_session['user_id']

    if request.method == 'POST':
        item_name = request.form['name']
        item_desc = request.form['description']
        category = session.query(Category).filter_by(name=request.form['category']).first()

        item = Item(name=item_name,
                    description=item_desc,
                    slug='_'.join(item_name.split(' ')).lower(),
                    user_id=user_id,
                    category_id=category.id)

        session.add(item)
        session.commit()
        return redirect(url_for('showItemsInCategory', category_name=category.name))

    categories = session.query(Category).all()
    return render_template('newItem.html', categories=categories)

@app.route('/catalog/category/new', methods=['POST'])
@login_required
def newCategory():
    category_name = request.form['name']
    category = Category(name=category_name)
    try:
        session.add(category)
        session.commit()
    except exc.IntegrityError:
        session.rollback()
        return 'Category already exists'
    categories = session.query(Category).all()
    return make_response(jsonify([i.serialize for i in categories ]), 200)

# Read #################################
@app.route('/')
@app.route('/catalog')
def showCatalog():
    latest_items = session.query(Item).limit(10).all()
    categories = session.query(Category).limit(10).all()

    return render_template('catalog.html', categories=categories, items=latest_items)

# Items in category
@app.route('/catalog/<string:category_name>/items', methods=['GET'])
def showItemsInCategory(category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    return render_template("showItemsInCategory.html", category=category)

# View Item by User
@app.route('/catalog/<int:user_id>/<string:item_slug>/', methods=['GET'])
def showItem(user_id, item_slug):
    item = session.query(Item).filter_by(user_id=user_id, slug=item_slug).first()

    if item is None:
        return "Not Found", 404

    return render_template("item.html", item=item)

@app.route('/catalog/my_items')
@login_required
def currentUserItems():
    return showUserItems(login_session["user_id"])

@app.route('/catalog/<int:user_id>/')
def showUserItems(user_id):
    items = session.query(Item).filter_by(user_id=user_id).all()

    return render_template('privateItems.html', items=items)

# Update #################################
@app.route('/catalog/<int:user_id>/<string:item_slug>/update/', methods=['GET','POST'])
@login_required
def updateItem(user_id, item_slug):
    # Find item
    item = session.query(Item).filter_by(slug=item_slug,
                                         user_id=user_id).first()
    if item is None:
        return "Not Found"

    # check if current user is owner
    user_email = login_session['email']
    user = session.query(User).filter_by(email=user_email).first()

    if user is None or not isUserAuthorized(user.id):
        return showAlert()

    categories = session.query(Category).all()
    if request.method == 'POST':
        # find new category
        new_category_name = request.form["category"]
        category = session.query(Category).filter_by(name=new_category_name).one()
        # update category
        item.name = request.form["name"]
        item.slug = '_'.join(item.name.split(' ')).lower()
        item.category_id = category.id
        item.description = request.form["description"]
        item.user_id = user_id
        try:
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            return item.name + ' already exists'

        return redirect(url_for('showUserItems', user_id=user_id))
    else:
        return render_template('editItem.html', item=item, categories=categories)

# Delete #################################
@app.route('/catalog/<int:user_id>/<string:item_slug>/delete/', methods=['GET', 'POST'])
@login_required
def deleteItem(user_id, item_slug):
    # check if current user is owner
    user_email = login_session['email']

    user = session.query(User).filter_by(email=user_email).first()
    if user is None or not isUserAuthorized(user.id):
        return showAlert()

    item = session.query(Item).filter_by(slug=item_slug, user_id=user.id).first()
    if item is None:
        return "Not Found"
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showUserItems', user_id=user_id))
    return render_template('deleteItem.html', item=item)

def isUserAuthorized(user_id):
    # check if current user is owner
    user_email = login_session['email']
    user = session.query(User).filter_by(email=user_email).first()

    return  user_id == user.id

def showAlert():
    '''Shows Alert when unauthorized'''
    return "<script>function myFunction() {\
            alert('You are not authorized to delete this item. \
            Please create your own item in order to delete.');\
            }</script><body onload='myFunction()''>"

# JSON APIs to view Catalogs Information #################################
@app.route('/api/catalog/categories')
def all_categoriesJSON():
    '''Returns all categories'''
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])

@app.route('/api/catalog/items')
def all_itemsJSON():
    '''Returns all items with relationships included'''
    items = session.query(Item).all()
    return jsonify(categories=[i.serialize for i in items])

# Show catalog with recent items
@app.route('/api/')
@app.route('/api/catalog')
def catalogJSON():
    '''Returns undated catalog with categories and latest items'''
    latest_items = session.query(Item).all()
    categories = session.query(Category).all()

    return jsonify(latest_items=[i.serialize for i in latest_items],
                   categories=[i.serialize for i in categories])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(host="0.0.0.0", port=5000, debug=True)
