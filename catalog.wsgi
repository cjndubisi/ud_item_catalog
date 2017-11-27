#!/usr/bin/python3

import sys

# add catalog app as module to python
sys.path.insert(0,"/var/www/catalog")

from catalog import app as application
application.secret_key = 'super_secret_key'
