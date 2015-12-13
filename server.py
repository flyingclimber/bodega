#!/usr/bin/env python

'''
server.py - Mini flask API
'''

import json
from fuzzywuzzy import fuzz
from flask import Flask, request

APP = Flask(__name__)
INDEX = 'index.json'
MERCHANTS = {}

with open(INDEX) as f:
    MERCHANTS = json.load(f)


def save_index():
    with open(INDEX, 'w') as g:
        g.write(json.dumps(MERCHANTS))


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

@APP.route("/add", methods=['POST'])
def add_category():

    merchant = request.form['merchant'].lower()
    category = request.form['category']

    if merchant in MERCHANTS:
        return 'Already Present'
    else:
        keys = MERCHANTS.keys()
        for key in keys:
            if fuzz.partial_ratio(merchant, key) > 70:
                return 'FZ Already Present'
        MERCHANTS[merchant] = category
        save_index()
        return 'Added'

if __name__ == "__main__":
    APP.run(port=8080, debug=True)

