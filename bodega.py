#!/usr/bin/env python

'''
bodega.py - Mini flask API
'''

import os.path
import json
from fuzzywuzzy import fuzz
from flask import Flask, request, jsonify

APP = Flask(__name__)
APP.config.from_pyfile('config.py')


class Bodega:
    """
        Represents a local market with different types of vendors
    """
    def __init__(self):
        self.json_index = APP.config['INDEX']
        self.api_keys = dict([APP.config['KEYS']])
        self.index = ''
        self.load_index()

    def load_index(self):
        """
            Create an index if it doesn't exists or load it from a file
        """
        if not os.path.isfile(self.json_index):
            self.save_index()

        with open(self.json_index) as f:
            self.index = MerchantIndex(json.load(f))

    def save_index(self):
        """
            Write out the current index to file
        """
        with open(self.json_index, 'w') as g:
            g.write(json.dumps(self.index.get_merchants()))

    def valid_api_key(self, key):
        """
            Check if an API key is valid
        """
        try:
            res = self.api_keys[key]
        except KeyError:
            res = False
        return res


class Merchant:
    """
        Individual seller and their details
    """
    def __init__(self, name, category=None):
        self.name = name
        self.category = category


class MerchantIndex:
    """
        The roster of merchants
    """
    def __init__(self, items=None):
        self.merchants = items or []

    def get_merchant_category(self, merchant):
        """
            Given a merchant return its category
        """
        try:
            res = self.merchants[merchant.name]
        except KeyError:
            res = False
        return res

    def get_merchants(self):
        """
            Return all the merchants
        """
        return self.merchants

    def add_merchant(self, merchant, category=None):
        """
            Add a new merchant
        """
        self.merchants[merchant.name] = category

    def search(self, term):
        """
            Given a merchant, see if it's in the index
        """
        keys = self.merchants.keys()
        res = ''

        for key in keys:
            if fuzz.partial_ratio(term, key) > 70:
                res = self.merchants[key]
        return res


@APP.route("/get/<name>")
def get_merchant(name):
    """
        Given a merchant name return if we know about it
    """
    merchant = Merchant(name.lower())
    category = bodega.index.get_merchant_category(merchant)

    if category:
        res = category
    else:
        res = bodega.index.search(name)

    return format_output(res)


@APP.route("/add", methods=['POST'])
def add_category():
    """
        Add a new merchant
    """
    merchant_name = request.form['merchant'].lower()
    category = request.form['category']
    api_key = request.form['api_key']

    merchant = Merchant(merchant_name, category)

    if not api_key:
        res = 'NO API KEY'
    elif not bodega.valid_api_key(api_key):
        res = 'INVALID API KEY'
    else:
        if bodega.index.get_merchant_category(merchant) or\
                        bodega.index.search(merchant) != '':
            res = 'Already Present'
        else:
            bodega.index.add_merchant(merchant, category)
            bodega.save_index()
            res = 'Added'

    return format_output(res)


def format_output(res):
    """
        Given a string return JSON formatted output
    """
    return jsonify(results=res)

if __name__ == "__main__":
    bodega = Bodega()

    APP.run()

