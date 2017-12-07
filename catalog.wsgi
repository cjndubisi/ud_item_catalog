#!/usr/bin/python3

import sys

# add catalog app as module to python
sys.path.append('/var/www/catalog')
from catalog.app import app as application
