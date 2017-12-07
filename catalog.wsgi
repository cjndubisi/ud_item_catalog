#!/usr/bin/python3

import sys, os

# add catalog app as module to python
sys.path.append(os.path.join(__file__, 'catalog'))
from app import app as application
