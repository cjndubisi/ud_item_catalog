import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Item, Category

db_url = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///catalog.db')
engine = create_engine(db_url)

DBSession = sessionmaker(bind=engine)
session = DBSession()


# dummy user
user1 = User(name='Chijioke ndubisi', picture='', email='cjndubisi@gmail.com')
session.add(user1)
session.commit()

# dummy categories
categories = [
	Category(name='SkateBoard'),
	Category(name='Soccer'),
	Category(name='Baseball'),
	Category(name='Fisbee'),
	Category(name='Rock Climbing'),
	Category(name='Football'),
	Category(name='Skating'),
	Category(name='Hockey')
]

# add all categores
for s in categories:
	session.add(s)

# dummy items
items = [
	Item(category_id=8, 
		 description='''Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
						Aenean commodo ligula eget dolor. Aenean massa. 
						Cum sociis natoque penatibus et magnis dis parturient montes, 
						nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, 
						pretium quis, sem. Nulla consequat massa quis enim. 
						Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. 
						In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. 
						Nullam dictum felis eu pede mollis pretium. Integer tincidunt. 
						Cras dapibus. Vivamus elementum semper nisi. 
						Aenean vulputate eleifend tellus. Aenean leo ligula''', 
		 name='Stick', 
		 slug='stick', 
		 user_id=1),

	Item(category_id=1, 
		 description='''Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
						Aenean commodo ligula eget dolor. Aenean massa. 
						Cum sociis natoque penatibus et magnis dis parturient montes, 
						nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, 
						pretium quis, sem. Nulla consequat massa quis enim. 
						Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. 
						In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. 
						Nullam dictum felis eu pede mollis pretium. Integer tincidunt. 
						Cras dapibus. Vivamus elementum semper nisi. 
						Aenean vulputate eleifend tellus. Aenean leo ligula''',
	     name='Goggles',
		 slug='goggles',
		 user_id=1),

	Item(category_id=1, 
		 description='''Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
						Aenean commodo ligula eget dolor. Aenean massa. 
					    Cum sociis natoque penatibus et magnis dis parturient montes, 
						nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, 
						pretium quis, sem. Nulla consequat massa quis enim. 
						Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. 
						In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. 
						Nullam dictum felis eu pede mollis pretium. Integer tincidunt. 
						Cras dapibus. Vivamus elementum semper nisi. 
						Aenean vulputate eleifend tellus. Aenean leo ligula''', 
		name='Two Shinguards', 
		slug='two_shinguargs', 
		user_id=1),

	Item(category_id=4, 
		 description='''Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
						Aenean commodo ligula eget dolor. Aenean massa. 
						Cum sociis natoque penatibus et magnis dis parturient montes, 
						nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, 
						pretium quis, sem. Nulla consequat massa quis enim. 
						Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. 
						In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. 
						Nullam dictum felis eu pede mollis pretium. Integer tincidunt. 
						Cras dapibus. Vivamus elementum semper nisi. 
						Aenean vulputate eleifend tellus. Aenean leo ligula''',
		 slug='fisbee', 
		 name='Fisbee', 
		 user_id=1),

	Item(category_id=5, 
		 description='''Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
						Aenean commodo ligula eget dolor. Aenean massa. 
						Cum sociis natoque penatibus et magnis dis parturient montes, 
						nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, 
						pretium quis, sem. Nulla consequat massa quis enim. 
						Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. 
						In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. 
						Nullam dictum felis eu pede mollis pretium. Integer tincidunt. 
						Cras dapibus. Vivamus elementum semper nisi. 
						Aenean vulputate eleifend tellus. Aenean leo ligula''', 
		 name='Bat', 
		 slug='bat', 
		 user_id=1),
	Item(category_id=2, 
		 description='''Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
						Aenean commodo ligula eget dolor. Aenean massa. 
						Cum sociis natoque penatibus et magnis dis parturient montes, 
						nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, 
						pretium quis, sem. Nulla consequat massa quis enim. 
						Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. 
						In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. 
						Nullam dictum felis eu pede mollis pretium. Integer tincidunt. 
						Cras dapibus. Vivamus elementum semper nisi. 
						Aenean vulputate eleifend tellus. Aenean leo ligula''', 
		 name='Jersey', 
		 slug='jersey', 
		 user_id=1),

	Item(category_id=2, 
		 description='''Lorem ipsum dolor sit amet, consectetuer adipiscing elit. 
						Aenean commodo ligula eget dolor. Aenean massa. 
						Cum sociis natoque penatibus et magnis dis parturient montes, 
						nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, 
						pretium quis, sem. Nulla consequat massa quis enim. 
						Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. 
						In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. 
						Nullam dictum felis eu pede mollis pretium. Integer tincidunt. 
						Cras dapibus. Vivamus elementum semper nisi. 
						Aenean vulputate eleifend tellus. Aenean leo ligula''', 
		 name='Soccer Cleat', 
		 slug='soccer_cleat', 
		 user_id=1)
]

# add all items
for x in items:
    session.add(x)

# comit changes
session.commit()
