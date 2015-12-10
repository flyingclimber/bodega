#!/usr/bin/env python

'''
server.py - Mini flask API
'''

import json
from fuzzywuzzy import fuzz
from flask import Flask

APP = Flask(__name__)
INDEX = 'index.json'
MERCHANTS = {}

with open(INDEX) as f:
    MERCHANTS = json.load(f)


@APP.route("/get/<merchant>")
def get_merchant(merchant):
    merchant = merchant.lower()
    if merchant in MERCHANTS:
        return MERCHANTS[merchant]
    else:
        keys = MERCHANTS.keys()
        res = 'Unknown'
        for key in keys:
            if fuzz.partial_ratio(merchant, key) > 70:
                res = MERCHANTS[key]
        return res

if __name__ == "__main__":
    APP.run(port=8080, debug=True)

