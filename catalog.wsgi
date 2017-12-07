#!/usr/bin/python3

import sys, os

# add catalog app as module to python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app as application
