#!/usr/bin/env python

'''
server.py - Mini flask API
'''

import json
from fuzzywuzzy import fuzz
from flask import Flask, request
from ConfigParser import ConfigParser

APP = Flask(__name__)
INDEX = 'index.json'
CONFIGFILE = '.config'
MERCHANTS = {}
API_KEYS = []

config = ConfigParser()
config.readfp(open(CONFIGFILE))
API_KEYS.append(config.get('API_KEYS', 'KEYS'))

with open(INDEX) as f:
    MERCHANTS = json.load(f)


def save_index():
    with open(INDEX, 'w') as g:
        g.write(json.dumps(MERCHANTS))


def valid_api_key(key):
    if key in API_KEYS:
        return True
    else:
        return False


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
    api_key = request.form['api_key']

    if not api_key:
        return 'NO API KEY'
    elif not valid_api_key(api_key):
        return 'INVALID API KEY'
    else:
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

