#!/usr/bin/python3

from flask import request, redirect
from flask import render_template, session as login_session, make_response, url_for, Blueprint
from flask_login import LoginManager, login_required, login_user, logout_user
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

from app.models import User
from app import app, db

import random, string, json, requests
import os, httplib2

CLIENT_ID = json.loads(
    open(os.path.join(os.getcwd(), 'client_secrets.json'), 'r').read())['web']['client_id']

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "showLogin"

# Define the blueprint: 'auth'
mod_auth = Blueprint('auth', __name__)

@mod_auth.route('/login')
def showLogin():

    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@mod_auth.route('/logout')
def logout():
    try:
        user = getUserInfo(login_session['user_id'])
        login_session.clear()
        user.authenticated = False
        db.session.add(user)
        db.session.commit()
        logout_user()
    except: 
        return redirect(url_for('showCatalog'))

    return redirect(url_for('showCatalog'))

@mod_auth.route('/gconnect', methods=['POST'])
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
        print ("Token's client ID does not match app's.")
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
    db.session.add(user)
    db.session.commit()

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

# flask_login: callback to reload the user object       
@login_manager.user_loader
def load_user(userid):
    try: 
        return getUserInfo(userid)
    except:
        return None

# Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=login_session['email']).one()
    return user

def getUserInfo(user_id):
    user = db.session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
