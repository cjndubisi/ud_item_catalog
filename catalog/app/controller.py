from catalog.app import app, db, auth_module
from catalog.app.models import Category, Item, User

from flask import render_template, request, redirect, jsonify, url_for
from flask_login import login_required
from flask import session as login_session, make_response, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, asc, exc
from werkzeug.routing import RequestRedirect

# Define the blueprint: 'catalog'
mod_catalog = Blueprint('catalog', __name__)

# Create #################################
@app.route('/catalog/items/new', methods=['GET', 'POST'])
@login_required
def newItem():

    user_id = login_session['user_id']

    if request.method == 'POST':
        item_name = request.form['name']
        item_desc = request.form['description']
        category = db.session.query(Category).filter_by(name=request.form['category']).first()

        item = Item(name=item_name,
                    description=item_desc,
                    slug='_'.join(item_name.split(' ')).lower(),
                    user_id=user_id,
                    category_id=category.id)

        db.session.add(item)
        db.session.commit()
        return redirect(url_for('showItemsInCategory', category_name=category.name))

    categories = db.session.query(Category).all()
    return render_template('newItem.html', categories=categories)

@app.route('/catalog/category/new', methods=['POST'])
@login_required
def newCategory():
    category_name = request.form['name']
    category = Category(name=category_name)
    try:
        db.session.add(category)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return 'Category already exists'
    categories = db.session.query(Category).all()
    return make_response(jsonify([i.serialize for i in categories ]), 200)

# Read #################################
@app.route('/')
@app.route('/catalog')
def showCatalog():
    latest_items = db.session.query(Item).limit(10).all()
    categories = db.session.query(Category).limit(10).all()

    return render_template('catalog.html', categories=categories, items=latest_items)

# Items in category
@app.route('/catalog/<string:category_name>/items', methods=['GET'])
def showItemsInCategory(category_name):
    category = db.session.query(Category).filter_by(name=category_name).first()
    return render_template("showItemsInCategory.html", category=category)

# View Item by User
@app.route('/catalog/<int:user_id>/<string:item_slug>/', methods=['GET'])
def showItem(user_id, item_slug):
    item = db.session.query(Item).filter_by(user_id=user_id, slug=item_slug).first()

    if item is None:
        return "Not Found", 404

    return render_template("item.html", item=item)

@app.route('/catalog/my_items')
@login_required
def currentUserItems():
    return showUserItems(login_session["user_id"])

@app.route('/catalog/<int:user_id>/')
def showUserItems(user_id):
    items = db.session.query(Item).filter_by(user_id=user_id).all()

    return render_template('privateItems.html', items=items)

# Update #################################
@app.route('/catalog/<int:user_id>/<string:item_slug>/update/', methods=['GET','POST'])
@login_required
def updateItem(user_id, item_slug):
    # Find item
    item = db.session.query(Item).filter_by(slug=item_slug,
                                         user_id=user_id).first()
    if item is None:
        return "Not Found"

    # check if current user is owner
    user_email = login_session['email']
    user = db.session.query(User).filter_by(email=user_email).first()

    if user is None or not isUserAuthorized(user.id):
        return showAlert()

    categories = db.session.query(Category).all()
    if request.method == 'POST':
        # find new category
        new_category_name = request.form["category"]
        category = db.session.query(Category).filter_by(name=new_category_name).one()
        # update category
        item.name = request.form["name"]
        item.slug = '_'.join(item.name.split(' ')).lower()
        item.category_id = category.id
        item.description = request.form["description"]
        item.user_id = user_id
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
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

    user = db.session.query(User).filter_by(email=user_email).first()
    if user is None or not isUserAuthorized(user.id):
        return showAlert()

    item = db.session.query(Item).filter_by(slug=item_slug, user_id=user.id).first()
    if item is None:
        return "Not Found"
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('showUserItems', user_id=user_id))
    return render_template('deleteItem.html', item=item)

def showAlert():
    '''Shows Alert when unauthorized'''
    return "<script>function myFunction() {\
            alert('You are not authorized to delete this item. \
            Please create your own item in order to delete.');\
            }</script><body onload='myFunction()''>"

def isUserAuthorized(user_id):
    # check if current user is owner
    user_email = login_session['email']
    user = db.session.query(User).filter_by(email=user_email).first()

    return  user_id == user.id