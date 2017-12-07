#!/usr/bin/python3

import sys

# add catalog app as module to python
sys.path.append('/var/www/catalog')
from catalog.app import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
else:
    app.run(debug=True)