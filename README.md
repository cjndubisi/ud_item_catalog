# Item Catalog
A application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

# Assumptions
Catalogs are stored per user that is, `/catalog/1` implies user 1's catalog.
Catagory is a tag on an item, right now an item can have only one tag.

# Requirements 
There are several steps that you should take to make sure that you have everything downloaded in order to run your this application.
- Install Vagrant and VirtualBox
- Clone the [fullstack-nanodegree-vm](http://github.com/udacity/fullstack-nanodegree-vm)
- Launch the Vagrant VM (vagrant up)

# Setup
SSH into the vagrant VM and move the project files into `catalog/` directory of vagrant (/vagrant/catalog)

### Database Setup
Run `python database_setup.py` to populate data.

### Running Server
Run `python python.py` to start the server
Access the application by visiting http://localhost:5000 locally on your browser.
